#!/usr/bin/env python

# stdlib
import logging
from textwrap import dedent

# third party
import click
from pathlib import PosixPath

# rexpy
import rexpy.blocks as rpb
import rexpy.confparse as rpc
import rexpy.helpers as rph
import rexpy.valplot as rpv
import rexpy.simpconf as rpsc


log = logging.getLogger("rp-conf.py")


@click.group(context_settings=dict(max_content_width=92))
def cli():
    pass


@cli.command("generate")
@click.argument("outname", type=click.Path(resolve_path=True))
@click.option("--bin-1j1b", type=str, default=rpsc.DEF_1j1b_bins, help="1j1b region binning settings.")
@click.option("--bin-2j1b", type=str, default=rpsc.DEF_2j1b_bins, help="2j1b region binning settings.")
@click.option("--bin-2j2b", type=str, default=rpsc.DEF_2j2b_bins, help="2j2b region binning settings.")
@click.option("--var-1j1b", type=str, default=rpsc.DEF_1j1b_vari, help="1j1b region variable setting.")
@click.option("--var-2j1b", type=str, default=rpsc.DEF_2j1b_vari, help="2j1b region variable setting.")
@click.option("--var-2j2b", type=str, default=rpsc.DEF_2j2b_vari, help="2j2b region variable setting.")
@click.option("--sel-1j1b", type=str, default=rpsc.DEF_1j1b_sels, help="1j1b region selection setting.")
@click.option("--sel-2j1b", type=str, default=rpsc.DEF_2j1b_sels, help="2j1b region selection setting.")
@click.option("--sel-2j2b", type=str, default=rpsc.DEF_2j2b_sels, help="2j2b region selection setting.")
@click.option("--ttbar-aux-weight", type=click.Choice(["1.0", "tptrw", "trrw"]), default="1.0", help="Extra ttbar weight.")
@click.option("--herwig-version", type=click.Choice(["704", "713"]), default="704", help="ttbar Herwig version.")
@click.option("--drop-sys", type=str, help="Drop a systematic.")
@click.option("--do-tables", is_flag=True, help="Produce tables.")
@click.option("--do-sys-plots", is_flag=True, help="Produce red/blue plots.")
@click.option("--do-valplots", is_flag=True, help="Produce validation region plots.")
@click.option("--is-preselection", is_flag=True, help="use preselection plotting definitions")
@click.option("--only-1516", is_flag=True, help="Fit only 15/16.")
@click.option("--only-17", is_flag=True, help="Fit only 17.")
@click.option("--only-18", is_flag=True, help="Fit only 18.")
@click.option("--drop-1j1b", is_flag=True, help="Drop the 1j1b region.")
@click.option("--drop-2j1b", is_flag=True, help="Drop the 2j1b region.")
@click.option("--drop-2j2b", is_flag=True, help="Drop the 2j2b region.")
def generate(
    outname,
    bin_1j1b,
    bin_2j1b,
    bin_2j2b,
    var_1j1b,
    var_2j1b,
    var_2j2b,
    sel_1j1b,
    sel_2j1b,
    sel_2j2b,
    ttbar_aux_weight,
    herwig_version,
    drop_sys,
    do_tables,
    do_sys_plots,
    do_valplots,
    is_preselection,
    only_1516,
    only_17,
    only_18,
    drop_1j1b,
    drop_2j1b,
    drop_2j2b,
):
    """Generate a config with user defined binning, save to OUTNAME."""
    log.info("Generating config file: %s" % outname)
    import yaml
    from rexpy.valplot import blocks_for_all_regions, fix_systematics
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

    if ttbar_aux_weight == "tptrw":
        rpsc.TTBAR_AUX_WEIGHT = "weight_tptrw_tool"
    elif ttbar_aux_weight == "trrw":
        rpsc.TTBAR_AUX_WEIGHT = "weight_trrw_tool"

    preamble = rpb.top_blocks(
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
    )
    with open(outname, "w") as f:
        print(preamble, file=f)
        if do_valplots:
            print(rpv.default_vrp_blocks(sel_1j1b, sel_2j1b, sel_2j2b, is_preselection=is_preselection), file=f)
        print(rpb.sample_blocks(), file=f)
        print(rpb.norm_factor_blocks(), file=f)
        print(rpb.sys_modeling_blocks(rpsc.NTUP_DIR, sel_1j1b, sel_2j1b, sel_2j2b, herwig_version), file=f)
        print(rpb.sys_minor_blocks(), file=f)
        print(rpb.sys_sf_weight_blocks(), file=f)
        print(rpb.sys_pdf_weight_blocks(), file=f)
        print(rpb.sys_twosided_tree_blocks(), file=f)
        print(rpb.sys_onesided_tree_blocks(), file=f)

    if do_valplots:
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


@cli.command("rm-region")
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


@cli.command("rm-sys")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-s", "--sys", type=str, multiple=True)
@click.option("-n", "--new-file", type=str)
def rm_sys(config, sys, new_file):
    """Remove systematics from a config file."""
    new_conf = "\n\n".join(rpc.drop_systematics(rpc.all_blocks(config), sys))
    outf = config if new_file is None else new_file
    with open(outf, "w") as f:
        print(new_conf, file=f)


if __name__ == "__main__":
    cli()
