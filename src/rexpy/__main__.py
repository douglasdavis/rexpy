#!/usr/bin/env python

# stdlib
from pathlib import PosixPath
import logging
import os
import warnings

# third party
import click

# rexpy
import rexpy.batch as rpbatch
import rexpy.blocks as rpb
import rexpy.confparse as rpc
import rexpy.helpers as rph
import rexpy.valplot as rpv
import rexpy.simpconf as rpsc


log = logging.getLogger("rex.py")


context_settings = {
    "max_content_width": 110,
    "help_option_names": ['-h', '--help'],
}


@click.group(name="rexpy", context_settings=context_settings)
def cli():
    """Command line interface for rexpy."""
    pass


@cli.command("augment")
@click.argument("rootfiledir", type=click.Path(resolve_path=True, exists=True))
@click.argument("npyfiledir", type=click.Path(resolve_path=True, exists=True))
@click.option("--dry", is_flag=True, help="Dry run (print would-be commands.")
@click.option("--condor-sub", type=str, help="Use condor, arg is workspace dir.")
@click.option("--submit/--no-submit", default=False, help="If using condor, submit.")
def augment(rootfiledir, npyfiledir, dry, condor_sub, submit):
    """Augment ROOT files with NumPy array files."""
    import rexpy.augnpy
    rexpy.augnpy.augment(rootfiledir, npyfiledir, dry, condor_sub, submit)


@cli.group("config")
def config():
    """Generate and handle TRExFitter configuration files."""
    pass


@config.command("gen")
@click.argument("outname", type=click.Path(resolve_path=True))
@click.option("--pre-exec", type=click.Path(resolve_path=True), help="File to execute (for config modifications)")
@click.option("--ntup-dir", type=click.Path(resolve_path=True), help="Path to ntuples.")
@click.option("--bin-1j1b", type=str, default=rpsc.r1j1b_bins(), help="1j1b region binning settings.", show_default=True)
@click.option("--bin-2j1b", type=str, default=rpsc.r2j1b_bins(), help="2j1b region binning settings.", show_default=True)
@click.option("--bin-2j2b", type=str, default=rpsc.r2j2b_bins(), help="2j2b region binning settings.", show_default=True)
@click.option("--var-all", type=str, default=None, help="Override all region variables", show_default=True)
@click.option("--var-1j1b", type=str, default=rpsc.r1j1b_var(), help="1j1b region variable setting.", show_default=True)
@click.option("--var-2j1b", type=str, default=rpsc.r2j1b_var(), help="2j1b region variable setting.", show_default=True)
@click.option("--var-2j2b", type=str, default=rpsc.r2j2b_var(), help="2j2b region variable setting.", show_default=True)
@click.option("--sel-1j1b", type=str, default=rpsc.r1j1b_selection(), help="1j1b region selection setting.", show_default=True)
@click.option("--sel-2j1b", type=str, default=rpsc.r2j1b_selection(), help="2j1b region selection setting.", show_default=True)
@click.option("--sel-2j2b", type=str, default=rpsc.r2j2b_selection(), help="2j2b region selection setting.", show_default=True)
@click.option("--herwig", type=click.Choice(["704", "713"]), default="704", help="ttbar Herwig version.", show_default=True)
@click.option("--drop-sys", type=str, help="Drop a systematic.")
@click.option("--do-tables", is_flag=True, help="Produce tables.")
@click.option("--do-sys-plots", is_flag=True, help="Produce red/blue plots.")
@click.option("--do-val-plots", is_flag=True, help="Produce validation region plots.")
@click.option("--is-preselection", is_flag=True, help="use preselection plotting definitions")
@click.option("--only-1516", is_flag=True, help="Fit only 15/16.")
@click.option("--only-17", is_flag=True, help="Fit only 17.")
@click.option("--only-18", is_flag=True, help="Fit only 18.")
@click.option("--drop-1j1b", is_flag=True, help="Drop the 1j1b region.")
@click.option("--drop-2j1b", is_flag=True, help="Drop the 2j1b region.")
@click.option("--drop-2j2b", is_flag=True, help="Drop the 2j2b region.")
@click.option("--fit-data", is_flag=True, help="Fit to data")
@click.option("--asimov-fit", is_flag=True, help="deprecated option (Asimov is default, use --fit-data for fit to data)")
def gen(
    outname,
    pre_exec,
    ntup_dir,
    bin_1j1b,
    bin_2j1b,
    bin_2j2b,
    var_all,
    var_1j1b,
    var_2j1b,
    var_2j2b,
    sel_1j1b,
    sel_2j1b,
    sel_2j2b,
    herwig,
    drop_sys,
    do_tables,
    do_sys_plots,
    do_val_plots,
    is_preselection,
    only_1516,
    only_17,
    only_18,
    drop_1j1b,
    drop_2j1b,
    drop_2j2b,
    fit_data,
    asimov_fit,
):
    """Generate a config with user defined binning, save to OUTNAME."""

    if pre_exec is not None:
        exec(PosixPath(pre_exec).read_text())

    if asimov_fit:
        warnings.warn(
            "--asimov-fit is deprecated (it's the default, use --fit-data to fit to data",
            DeprecationWarning
        )

    bin_1j1b = bin_1j1b if bin_1j1b is not None else rpsc.r1j1b_bins()
    bin_2j1b = bin_2j1b if bin_2j1b is not None else rpsc.r2j1b_bins()
    bin_2j2b = bin_2j2b if bin_2j2b is not None else rpsc.r2j2b_bins()
    var_1j1b = var_1j1b if var_1j1b is not None else rpsc.DEF_1j1b_var
    var_2j1b = var_2j1b if var_2j1b is not None else rpsc.DEF_2j1b_var
    var_2j2b = var_2j2b if var_2j2b is not None else rpsc.DEF_2j2b_var
    sel_1j1b = sel_1j1b if sel_1j1b is not None else rpsc.r1j1b_selection()
    sel_2j1b = sel_2j1b if sel_2j1b is not None else rpsc.r2j1b_selection()
    sel_2j2b = sel_2j2b if sel_2j2b is not None else rpsc.r2j2b_selection()

    if var_all is not None:
        var_1j1b = var_all
        var_2j1b = var_all
        var_2j2b = var_all

    log.info("Generating config file: %s" % outname)
    if ntup_dir is None:
        ntup_dir = rpsc.ntuple_directory()
    log.info("Using ntuple directory: %s" % ntup_dir)
    from rexpy.valplot import fix_systematics
    if drop_1j1b:
        sel_1j1b = None
        log.info("Excluding 1j1b")
    else:
        sel_1j1b = rph.selection_with_period(sel_1j1b, only_1516, only_17, only_18)
    if drop_2j1b:
        sel_2j1b = None
        log.info("Excluding 2j1b")
    else:
        sel_2j1b = rph.selection_with_period(sel_2j1b, only_1516, only_17, only_18)
    if drop_2j2b:
        sel_2j2b = None
        log.info("Excluding 2j2b")
    else:
        sel_2j2b = rph.selection_with_period(sel_2j2b, only_1516, only_17, only_18)

    preamble = rpb.top_blocks(
        ntuplepaths=ntup_dir,
        reg1j1b_binning=bin_1j1b,
        reg2j1b_binning=bin_2j1b,
        reg2j2b_binning=bin_2j2b,
        reg1j1b_variable=var_1j1b,
        reg2j1b_variable=var_2j1b,
        reg2j2b_variable=var_2j2b,
        reg1j1b_selection=sel_1j1b,
        reg2j1b_selection=sel_2j1b,
        reg2j2b_selection=sel_2j2b,
        dotables="TRUE" if do_tables else "FALSE",
        systplots="TRUE" if do_sys_plots else "FALSE",
        fitblind="FALSE" if fit_data else "TRUE",
    )
    with open(outname, "w") as f:
        print(preamble, file=f)
        if do_val_plots:
            print(rpv.default_vrp_blocks(sel_1j1b, sel_2j1b, sel_2j2b, is_preselection=is_preselection), file=f)
        print(rpb.sample_blocks(), file=f)
        print(rpb.norm_factor_blocks(), file=f)
        print(rpb.sys_modeling_blocks(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b, herwig), file=f)
        print(rpb.sys_minor_blocks(), file=f)
        print(rpb.sys_sf_weight_blocks(), file=f)
        print(rpb.sys_pdf_weight_blocks(), file=f)
        print(rpb.sys_twosided_tree_blocks(), file=f)
        print(rpb.sys_onesided_tree_blocks(), file=f)

    if do_val_plots:
        fix_systematics(outname)

    blocks = rpc.all_blocks(outname)
    if drop_1j1b:
        blocks = rpc.drop_region(blocks, "1j1b")
    if drop_2j1b:
        blocks = rpc.drop_region(blocks, "2j1b")
    if drop_2j2b:
        blocks = rpc.drop_region(blocks, "2j2b")
    if drop_sys is not None:
        blocks = rpc.drop_systematics(blocks, [drop_sys])

    final_conf = "\n\n".join(blocks)
    with open(outname, "w") as outf:
        print(final_conf, file=outf)

    return 0


@config.command("rm-region")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-r", "--region", type=str, multiple=True)
@click.option("-n", "--new-file", type=str)
def rm_region(config, region, new_file):
    """Remove regions from a config file."""
    blocks = rpc.all_blocks(config)
    for r in region:
        blocks = rpc.drop_region(blocks, r)

    outf = config if new_file is None else new_file
    with open(outf, "w") as f:
        print("\n\n".join(blocks), file=f)


@config.command("rm-sys")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-s", "--sys", type=str, multiple=True)
@click.option("-n", "--new-file", type=str)
def rm_sys(config, sys, new_file):
    """Remove systematics from a config file."""
    new_conf = "\n\n".join(rpc.drop_systematics(rpc.all_blocks(config), sys))
    outf = config if new_file is None else new_file
    with open(outf, "w") as f:
        print(new_conf, file=f)


@cli.group("run")
def run():
    """Run TRExFitter steps in an automated way."""
    pass


@run.command("local")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-x", "--suffix", type=str, help="Add suffix to workspace.")
@click.option("-c", "--copy-hists", type=click.Path(resolve_path=True, exists=True), help="Copy existing histograms")
@click.option("-n", "--n-parallel", type=int, default=None, help="Max parallel jobs (default is CPU count)")
@click.option("-d", "--force-data", is_flag=True, help="Force config to fit to data.")
@click.option("-s", "--steps", type=str, default="nwfdpri", help="TRExFitter steps to run", show_default=True)
def local(config, suffix, copy_hists, n_parallel, force_data, steps):
    """Run TRExFitter steps locally."""
    import rexpy.batch as rpb

    if force_data and suffix is not None:
        suffix = f"{suffix}.force-data"
    elif force_data:
        suffix = "force-data"

    curdir = PosixPath.cwd()
    workspace, f = rpb.create_workspace(config, suffix)

    # copy histograms if requested
    if copy_hists is not None:
        rph.copy_histograms(copy_hists, workspace)

    if force_data:
        f = rpc.unblind(f)
    os.chdir(workspace)
    if "n" in steps and copy_hists is None:
        rpb.parallel_n_step(f, processes=n_parallel)
    if "wf" in steps:
        rpb.wf_step(f)
    if "dp" in steps:
        rpb.dp_step(f)
    if "r" in steps:
        rpb.parallel_r_step(f, processes=n_parallel)
        rpb.r_draw_step(f)
    if "i" in steps:
        rpb.parallel_i_step(f, processes=n_parallel)
        rpb.i_combine_step(f)
    os.chdir(curdir)


@run.command("condor")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-s", "--sys", type=str, help="Comma separated specific systematics to use.")
@click.option("-x", "--suffix", type=str, help="Add suffix to workspace.")
@click.option("-c", "--copy-hists", type=click.Path(resolve_path=True), help="Copy existing histograms.")
@click.option("-n", "--ntup-only", is_flag=True, help="Only fun the ntuple step.")
@click.option("-d", "--force-data", is_flag=True, help="Force config to fit to data.")
@click.option("--submit/--no-submit", default=False, help="Submit the jobs")
def condor(config, sys, suffix, copy_hists, ntup_only, force_data, submit):
    """Run TRExFitter steps with HTCondor."""
    import rexpy.batch as rpb
    import rexpy.pycondor as pycondor

    if force_data and suffix is not None:
        suffix = f"{suffix}.force-data"
    elif force_data:
        suffix = "force-data"

    # create workspace and the condo dagman
    workspace, f = rpb.create_workspace(config, suffix)
    dagman = pycondor.Dagman("rexpy-dag", submit=str(workspace / "sub"))

    if force_data:
        f = rpc.unblind(f)

    cwd = PosixPath.cwd()
    os.chdir(workspace)

    # check for specific systematics
    sys = sys.split(",") if sys is not None else None

    # copy histograms if requested
    if copy_hists is not None:
        rph.copy_histograms(copy_hists, workspace)

    # generate all condor jobs.
    n = None
    if copy_hists is None:
        n = rpb.condor_n_step(workspace, dag=dagman, sys=sys)

    if not ntup_only:
        wf = rpb.condor_wf_step(workspace, dag=dagman, sys=sys)
        dp = rpb.condor_dp_step(workspace, dag=dagman, sys=sys)
        r = rpb.condor_r_step(workspace, dag=dagman, sys=sys)
        rplot = rpb.condor_rplot_step(workspace, dag=dagman)

    # setup job dependencies
    if n is not None and not ntup_only:
        wf.add_parent(n)
    else:
        pass
    if not ntup_only:
        dp.add_parent(wf)
        r.add_parent(wf)
        rplot.add_parent(r)
        if sys is None:
            i = rpb.condor_i_step(workspace, dag=dagman)
            icombine = rpb.condor_icombine_step(workspace, dag=dagman)
            i.add_parent(wf)
            icombine.add_parent(i)
        else:
            pass
    else:
        pass

    if submit:
        dagman.build_submit()
    else:
        dagman.build()

    os.chdir(cwd)


@cli.command("sysholdout")
@click.argument("workspace", type=click.Path(resolve_path=True, exists=True))
@click.argument("systematics", type=str)
@click.option("-n", "--n-parallel", type=int, default=None, help="Max parallel jobs (default is CPU count)")
def sysholdout(workspace, systematics, n_parallel):
    """Refit a configuration holding out a set of systematics."""
    wsp = PosixPath(workspace)
    syslistfile = PosixPath(systematics)
    if systematics == "_default":
        systematics = rpsc.regular_stability_test_list()
    elif syslistfile.exists():
        systematics = syslistfile.read_text().strip().split()
    else:
        systematics = systematics.split(",")

    curdir = PosixPath.cwd()
    os.chdir(wsp)
    rpbatch.parallel_run(
        [f"{rpbatch.TREX_EXE} wf fit.conf Exclude={s}:Suffix=_exclude-{s}" for s in systematics],
        processes=n_parallel,
    )
    os.chdir(curdir)


if __name__ == "__main__":
    cli(prog_name="rexpy")
