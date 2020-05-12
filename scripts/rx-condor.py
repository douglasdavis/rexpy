#!/usr/bin/env python

from __future__ import print_function

# stdlib
import os
import re
import shutil
import sys

# third party
import click
from pathlib2 import PosixPath

# rexuple
from rexuple.batch import job_params
import rexuple.pycondor as pycondor
from rexuple.parse import (
    get_regions,
    get_systematics,
    gen_fit_argument,
    gen_rank_arguments,
    gen_ntuple_arguments,
)

TREX_EXE = os.popen("which trex-fitter").read().strip()
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


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command("ntup")
@click.argument("config")
@click.option(
    "--quick", is_flag=True, help="generate a 'quick' submission (Lumi sys only)"
)
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
    systematics = get_systematics(config)
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
@click.option("--dont-submit", is_flag=True, help="do not submit to condor")
@click.option("--dont-fit", is_flag=True, help="only do n and d steps")
@click.option(
    "-s", "--systematic", type=str, multiple=True, help="only these systematics"
)
@click.option("-w", "--ws-suffix", type=str, help="extra workspace suffix")
def complete(config, dont_submit, dont_fit, systematic, ws_suffix):
    """Run a complete set of trex-fitter stages ('n', then 'wf', then 'dp', then 'r')"""
    config_path = PosixPath(config)
    config_name = config_path.name
    workspace = "rxcws-{}".format(config_path.stem)
    if ws_suffix:
        workspace = "{}_{}".format(workspace, ws_suffix)
    os.mkdir(workspace)
    shutil.copyfile(str(config_path), os.path.join(workspace, "fit.conf"))
    workspace = os.path.abspath(workspace)

    systematics = get_systematics(config, specific_sys=systematic)
    regions = get_regions(config)

    dagman = pycondor.Dagman(
        name="rx-condor_complete", submit=os.path.join(workspace, "sub")
    )
    standard_params = job_params(workspace, TREX_EXE)

    ntuple = pycondor.Job(name="ntuple", dag=dagman, **standard_params)

    if systematic:
        ntuple.add_args(gen_ntuple_arguments(config, specific_sys=systematics))
    else:
        ntuple.add_args(gen_ntuple_arguments(config))

    if dont_fit:
        draw = pycondor.Job(name="draw", dag=dagman, **standard_params)
        draw.add_args(["d {} Regions={}".format(config, r) for r in regions])
        # now define the dependencies
        draw.add_parent(ntuple)
    else:
        # the fit step
        fit = pycondor.Job(name="fit", dag=dagman, **standard_params)
        fit.add_arg(
            gen_fit_argument(config, specific_sys=systematics if systematic else None)
        )
        # the draw step
        draw = pycondor.Job(name="draw", dag=dagman, **standard_params)
        draw.add_args(["dp {} Regions={}".format(config, r) for r in regions])
        # the rank (fit) step
        rank = pycondor.Job(name="rank", dag=dagman, **standard_params)
        rank.add_args(gen_rank_arguments(config, specific_sys=systematics))
        # the rank (plot) step
        rank_draw = pycondor.Job(name="rank_draw", dag=dagman, **standard_params)
        rank_draw.add_arg("r {} Ranking=plot".format(config))
        # now define the dependencies starting with the last step and working upstream
        rank_draw.add_parent(rank)
        rank.add_parent(draw)
        draw.add_parent(fit)
        fit.add_parent(ntuple)

    orig_path = os.getcwd()
    os.chdir(workspace)
    if dont_submit:
        dagman.build()
    else:
        dagman.build_submit()
    os.chdir(orig_path)

    return 0


if __name__ == "__main__":
    cli()
