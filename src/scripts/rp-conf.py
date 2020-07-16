#!/usr/bin/env python

# stdlib
from textwrap import dedent

# third party
import click
from pathlib import PosixPath

# rexpy
import rexpy.blocks as rpb
from rexpy.blocks import (
    top_blocks,
    modeling_blocks,
    SAMPLE_BLOCKS,
    NORMFACTOR_BLOCKS,
    SYS_MINOR_BLOCKS,
    SYS_WEIGHT_BLOCKS,
    SYS_PDF_WEIGHT_BLOCKS,
    SYS_TWOSIDED_TREE_BLOCKS,
    SYS_ONESIDED_TREE_BLOCKS,
)
from rexpy.confparse import all_blocks, regions_from, drop_systematics
from rexpy.helpers import selection_with_period

@click.group(context_settings=dict(max_content_width=92))
def cli():
    pass


@cli.command("simple-setup0")
@click.argument("outname", type=click.Path(resolve_path=True))
def simple_setup0(outname):
    """Generate a config from default settings, save to OUTNAME."""
    with open(outname, "w") as f:
        print(top_blocks(), file=f)
        print(SAMPLE_BLOCKS, file=f)
        print(NORMFACTOR_BLOCKS, file=f)
        print(modeling_blocks(rpb.NTUP_DIR, rpb.DEF_1j1b_sels, rpb.DEF_2j1b_sels, rpb.DEF_2j2b_sels), file=f)
        rpb.const_sys_blocks(f)
    return 0


@cli.command("simple-setup1")
@click.argument("outname", type=click.Path(resolve_path=True))
def simple_setup1(outname):
    """Generate a config from default settings using mass cuts, save to OUTNAME."""
    preamble = top_blocks(
        reg1j1b_selection=rpb.DEF_1j1b_swmc,
        reg2j1b_selection=rpb.DEF_2j1b_swmc,
        reg2j2b_selection=rpb.DEF_2j2b_swmc,
        reg1j1b_variable="bdtres01",
        reg2j1b_variable="bdtres01",
        reg2j2b_variable="bdtres01",
        reg1j1b_binning="12,0.17,0.745",
    )
    with open(outname, "w") as f:
        print(preamble, file=f)
        print(SAMPLE_BLOCKS, file=f)
        print(NORMFACTOR_BLOCKS, file=f)
        print(modeling_blocks(rpb.NTUP_DIR, rpb.DEF_1j1b_swmc, rpb.DEF_2j1b_swmc, rpb.DEF_2j2b_swmc), file=f)
        rpb.const_sys_blocks(f)
    return 0


@cli.command("tunable")
@click.argument("outname", type=click.Path(resolve_path=True))
@click.option("--bin-1j1b", type=str, default=rpb.DEF_1j1b_bins, help="1j1b region binning settings")
@click.option("--bin-2j1b", type=str, default=rpb.DEF_2j1b_bins, help="2j1b region binning settings")
@click.option("--bin-2j2b", type=str, default=rpb.DEF_2j2b_bins, help="2j2b region binning settings")
@click.option("--var-1j1b", type=str, default=rpb.DEF_1j1b_vari, help="1j1b region variable setting")
@click.option("--var-2j1b", type=str, default=rpb.DEF_2j1b_vari, help="2j1b region variable setting")
@click.option("--var-2j2b", type=str, default=rpb.DEF_2j2b_vari, help="2j2b region variable setting")
@click.option("--sel-1j1b", type=str, default=rpb.DEF_1j1b_sels, help="1j1b region selection setting")
@click.option("--sel-2j1b", type=str, default=rpb.DEF_2j1b_sels, help="2j1b region selection setting")
@click.option("--sel-2j2b", type=str, default=rpb.DEF_2j2b_sels, help="2j2b region selection setting")
@click.option("--herwig-version", type=click.Choice(["704", "713"]), default="713", help="ttbar Herwig version")
@click.option("--drop-sys", type=str, help="Drop a systematic")
@click.option("--do-tables", is_flag=True, help="Don't produce tables")
@click.option("--do-sys-plots", is_flag=True, help="Don't produce red/blue plots")
@click.option("--do-valplots", is_flag=True, help="validation region plots")
@click.option("--is-preselection", is_flag=True, help="use preselection plotting definitions")
@click.option("--fit-data", is_flag=True, help="Fit to data")
@click.option("--only-1516", is_flag=True, help="Fit only 15/16")
@click.option("--only-17", is_flag=True, help="Fit only 17")
@click.option("--only-18", is_flag=True, help="Fit only 18")
def tunable(
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
    herwig_version,
    drop_sys,
    do_tables,
    do_sys_plots,
    do_valplots,
    is_preselection,
    fit_data,
    only_1516,
    only_17,
    only_18,
):
    """Generate a config with user defined binning, save to OUTNAME."""
    import yaml
    from rexpy.valplot import blocks_for_all_regions, fix_systematics
    sel_1j1b = selection_with_period(sel_1j1b, only_1516, only_17, only_18)
    sel_2j1b = selection_with_period(sel_2j1b, only_1516, only_17, only_18)
    sel_2j2b = selection_with_period(sel_2j2b, only_1516, only_17, only_18)
    preamble = top_blocks(
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
        if do_valplots:
            import requests
            meta_req = requests.get("https://cern.ch/ddavis/tdub_data/meta.yml")
            # meta = load_meta_table(meta_req.content)
            meta = yaml.full_load(meta_req.content)
            print(
                blocks_for_all_regions(
                    meta, sel_1j1b, sel_2j1b, sel_2j2b, is_preselection=is_preselection
                ),
                file=f
            )
            print("", file=f)
        print(SAMPLE_BLOCKS, file=f)
        print(NORMFACTOR_BLOCKS, file=f)
        print(modeling_blocks(rpb.NTUP_DIR, sel_1j1b, sel_2j1b, sel_2j2b, herwig_version), file=f)
        rpb.const_sys_blocks(f)
    if do_valplots:
        fix_systematics(outname)

    if drop_sys is not None:
        new_conf = "\n\n".join(drop_systematics(all_blocks(outname), [drop_sys]))
        with open(outname, "w") as outf:
            print(new_conf, outf)

    return 0


@cli.command("rm-region")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-r", "--region", type=str, multiple=True)
@click.option("-n", "--new-file", type=str)
def rm_region(config, region, new_file):
    """Remove regions from a config file."""
    ##
    def remove_region(config_blocks, region):
        new_blocks = []
        for block in config_blocks:
            if block.startswith("Region:"):
                if region in block:
                    continue
            if block.startswith("Systematic:"):
                if region in block:
                    continue
            new_blocks.append(block)

        summary_plot_regions_o = new_blocks[0].split("SummaryPlotRegions: ")[-1].split()[0]
        summary_plot_regions_n = summary_plot_regions_o.split(",")
        if region in summary_plot_regions_n:
            summary_plot_regions_n.remove(region)
        new_blocks[0] = new_blocks[0].replace(
            summary_plot_regions_o, ",".join(summary_plot_regions_n)
        )
        return new_blocks
    ##
    blocks = all_blocks(config)
    for r in region:
        blocks = remove_region(blocks, r)

    outf = config if new_file is None else new_file
    with open(outf, "w") as f:
        print("\n\n".join(blocks), file=f)


@cli.command("rm-sys")
@click.argument("config", type=click.Path(resolve_path=True))
@click.option("-s", "--sys", type=str, multiple=True)
@click.option("-n", "--new-file", type=str)
def rm_sys(config, sys, new_file):
    """Remove systematics from a config file."""
    new_conf = "\n\n".join(drop_systematics(all_blocks(config), sys))
    outf = config if new_file is None else new_file
    with open(outf, "w") as f:
        print(new_conf, file=f)


if __name__ == "__main__":
    cli()
