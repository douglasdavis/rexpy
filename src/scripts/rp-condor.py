#!/usr/bin/env python

# stdlib
import logging
import os
import re
import shutil
import sys
from pathlib import PosixPath

# third party
import click

# rexpy
from rexpy.batch import job_params
import rexpy.pycondor as pycondor
from rexpy.confparse import (
    regions_from,
    systematics_from,
    draw_argument,
    fit_argument,
    rank_arguments,
    ntuple_arguments,
    ntuple_arguments_granular,
    grouped_impact_arguments,
)

TREX_EXE = shutil.which("trex-fitter")
HUPDATE_EXE = shutil.which("hupdate.exe")
CONTEXT_SETTINGS = {"max_content_width": 92}
BNL_CONDOR_HEADER = """
Universe        = vanilla
notification    = Error
notify_user     = ddavis@phy.duke.edu
GetEnv          = True
Executable      = {0}
Output          = logs/job.out.{1}.$(cluster).$(process)
Error           = logs/job.err.{1}.$(cluster).$(process)
Log             = logs/job.log.{1}.$(cluster).$(process)
request_memory  = 2.0G
"""

log = logging.getLogger("rp-condor.py")


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command("ntup")
@click.argument("config")
@click.option("--quick", is_flag=True, help="generate a 'quick' submission (Lumi sys only)")
@click.option("--this-sys", type=str, help="do a single user defined systematic")
def ntup(config, quick, this_sys):
    """Generate a condor submission script for the ntuple creation step of TRExFitter"""
    config_name = PosixPath(config).name
    if quick:
        if this_sys is not None:
            print("--quick and --this-sys cannot be used together")
            exit(1)
        outfile = "condor.ntup.quick.{}.sub".format(config_name)
    elif this_sys is not None:
        outfile = "condor.ntup.{}.{}.sub".format(this_sys, config_name)
    else:
        outfile = "condor.ntup.{}.sub".format(config_name)
    full_config = str(PosixPath(config).resolve())
    commands = []
    with open(full_config, "r") as f:
        for line in f.readlines():
            if line.startswith(r"%"):
                continue
            elif line.startswith("Region:"):
                reg = line.strip().split("Region: ")[-1].replace('"', "")
                if quick:
                    commands.append(
                        "n {} Systematics=Lumi:Regions={}".format(full_config, reg)
                    )
                elif this_sys is not None:
                    commands.append(
                        "n {} Systematics={}:Regions={}".format(
                            full_config, this_sys, reg
                        )
                    )
                else:
                    commands.append("n {} Regions={}".format(full_config, reg))

    with open(outfile, "w") as f:
        print(BNL_CONDOR_HEADER.format(TREX_EXE, "ntup"), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)


@cli.command("fit")
@click.option("--config", "-c", multiple=True, type=str, help="config file(s) to fit")
def fit(config):
    """Generate a condor submission script to run the fit step on some config files"""
    configs = [str(PosixPath(c).resolve()) for c in config]
    outfile = "condor.fit.sub"
    with open(outfile, "w") as f:
        print(BNL_CONDOR_HEADER.format(TREX_EXE, "fit"), file=f)
        for conf in configs:
            print("Arguments = wf {}".format(conf), file=f)
            print("Queue\n", file=f)


@cli.command("draw")
@click.option("--config", "-c", multiple=True, type=str, help="config file(s) to draw")
@click.option("--postfit", "-p", is_flag=True, help="also run the postfit draw step")
def draw(config, postfit):
    """Generate a condor submission script to run the drawing steps on some config files"""
    region_re = re.compile(r"^Region: \"\w+\"")

    def get_arguments(config_file, do_postfit):
        regions = []
        with open(config_file, "r") as f:
            for line in f.readlines():
                if region_re.match(line):
                    region = line.strip().split("Region: ")[-1].replace('"', "")
                    regions.append(region)
        arguments = []
        prefix = "dp" if do_postfit else "d"
        for region in regions:
            arguments.append("{} {} Regions={}".format(prefix, config_file, region))
        return arguments

    configs = [str(PosixPath(c).resolve()) for c in config]
    outfile = "condor.draw.sub"
    with open(outfile, "w") as f:
        print(BNL_CONDOR_HEADER.format(TREX_EXE, "draw"), file=f)
        for conf in configs:
            args = get_arguments(conf, postfit)
            for arg in args:
                print("Arguments = {}".format(arg), file=f)
                print("Queue\n", file=f)


@cli.command("rank")
@click.argument("config", type=str)
def rank(config):
    """Generate a condor submission script to do the ranking plot steps"""
    config_file = PosixPath(config)
    config_name = config_file.name
    full_config = str(config_file.resolve())
    commands = []
    systematics = systematics_from(config)
    for s in systematics:
        commands.append("r {} Ranking={}".format(full_config, s))

    outfile = "condor.rank.{}.sub".format(config_name)
    with open(outfile, "w") as f:
        print(BNL_CONDOR_HEADER.format(TREX_EXE, "rank"), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)


@cli.command("complete")
@click.argument("config", type=click.Path(exists=True, resolve_path=True))
@click.option("-s", "--systematics", type=str, help="only these systematics (comma separated)")
@click.option("-w", "--ws-suffix", type=str, help="extra workspace suffix")
@click.option("--copy-histograms-from", type=click.Path(exists=True, resolve_path=True), help="Use existing histograms")
@click.option("--dont-fit", is_flag=True, help="only do n and d steps")
@click.option("--dont-rank", is_flag=True, help="Skip the ranking step")
@click.option("--dont-draw", is_flag=True, help="Skip the plotting steps")
@click.option("--dont-submit", is_flag=True, help="do not submit to condor")
@click.option("--granular-ntup", is_flag=True, help="do granular ntuple step")
@click.option("--actually-local", is_flag=True, help="do steps locally")
def complete(
    config,
    systematics,
    ws_suffix,
    copy_histograms_from,
    dont_fit,
    dont_rank,
    dont_draw,
    dont_submit,
    granular_ntup,
    actually_local,
):
    """Run a complete set of trex-fitter stages ('n'; 'wf'; 'dp'; 'r'; 'i')"""
    config_path = PosixPath(config).resolve()
    config_name = config_path.name
    workspace = (config_path.parent / "rpcc_{}".format(config_path.stem)).resolve()
    if ws_suffix:
        workspace = "{}__{}".format(workspace, ws_suffix)
    os.mkdir(workspace)
    shutil.copyfile(str(config_path), os.path.join(workspace, "fit.conf"))
    workspace = os.path.abspath(workspace)

    if systematics is not None:
        systematics = systematics.split(",")
    syslist = systematics_from(config, specific_sys=systematics)
    regions = regions_from(config)

    dagman = pycondor.Dagman(name="rp-complete", submit=os.path.join(workspace, "sub"))
    standard_params = job_params(workspace, TREX_EXE)
    hupdate_params = job_params(workspace, HUPDATE_EXE)

    # never submit if we do local.
    if actually_local:
        dont_submit = True

    if copy_histograms_from is None:
        log.info("Will run ntuple step")
        if systematics:
            ntuple = pycondor.Job(name="ntuple", dag=dagman, **standard_params)
            ntuple.add_args(ntuple_arguments(config, specific_sys=syslist))
        else:
            if granular_ntup:
                a0, a1 = ntuple_arguments_granular(config)
                ntuple0 = pycondor.Job(name="ntuple0", dag=dagman, **standard_params)
                ntuple0.add_args(a0)
                ntuple = pycondor.Job(name="ntuple", dag=dagman, **hupdate_params)
                ntuple.add_args(a1)
                ntuple.add_parent(ntuple0)
            else:
                ntuple = pycondor.Job(name="ntuple", dag=dagman, **standard_params)
                ntuple.add_args(ntuple_arguments(config))
    else:
        os.makedirs(PosixPath(workspace) / "tW" / "Histograms")
        for entry in PosixPath(copy_histograms_from).glob("*histos.root"):
            shutil.copyfile(entry, str(PosixPath(workspace) / "tW" / "Histograms" / PosixPath(entry).name))

    # fmt: off
    if dont_fit:
        log.info("Will run drawing steps")
        draw = pycondor.Job(name="draw", dag=dagman, **standard_params)
        draw.add_arg(draw_argument(config, specific_sys=syslist if systematics else None))
        if copy_histograms_from is not None:
            draw.add_parent(ntuple)
    else:
        # the fit step
        log.info("Will run fit step")
        fit = pycondor.Job(name="fit", dag=dagman, **standard_params)
        fit.add_arg(fit_argument(config, specific_sys=syslist if systematics else None))
        if copy_histograms_from is None:
            fit.add_parent(ntuple)
        # the draw step
        if not dont_draw:
            log.info("Will run drawing steps")
            draw = pycondor.Job(name="draw", dag=dagman, **standard_params)
            draw.add_arg(draw_argument(config, specific_sys=syslist if systematics else None))
            draw.add_parent(fit)
        # the rank step
        if not dont_rank:
            log.info("Will run ranking step")
            rank = pycondor.Job(name="rank", dag=dagman, **standard_params)
            rank.add_args(rank_arguments(config, specific_sys=syslist))
            rank.add_parent(fit)
            rank_draw = pycondor.Job(name="rank_draw", dag=dagman, **standard_params)
            rank_draw.add_arg("r {} Ranking=plot".format(config))
            rank_draw.add_parent(rank)
            if systematics is None:
                log.info("Will run impact step")
                group = pycondor.Job(name="group", dag=dagman, **standard_params)
                group.add_args(grouped_impact_arguments(config))
                group.add_parent(fit)
                group_combine = pycondor.Job(name="group_combine", dag=dagman, **standard_params)
                group_combine.add_arg("i {} GroupedImpact=combine".format(config))
                group_combine.add_parent(group)
    # fmt: on

    orig_path = os.getcwd()
    os.chdir(workspace)
    if dont_submit:
        dagman.build()
    else:
        dagman.build_submit()
    os.chdir(orig_path)

    if actually_local:
        import rexpy.batch as rpb
        f = str(PosixPath(workspace) / "fit.conf")
        rpb.parallel_n_step(f)
        rpb.wfdp_step(f)
        rpb.parallel_r_step(f)
        rpb.r_draw_step(f)
        rpb.parallel_i_step(f)
        rpb.i_combine_step(f)

    return 0


if __name__ == "__main__":
    cli()
