#!/usr/bin/env python

# future
from __future__ import print_function

# stdlib
from textwrap import dedent

# third party
import click
from pathlib2 import PosixPath

# rexuple
from rexuple.constants import (
    SAMPLE_BLOCKS,
    NORMFACTOR_BLOCKS,
    MODELING_BLOCKS,
    SYS_WEIGHT_BLOCKS,
    SYS_PDF_WEIGHT_BLOCKS,
    SYS_TWOSIDED_TREE_BLOCKS,
    SYS_ONESIDED_TREE_BLOCKS,
)
from rexuple.vrp import load_meta_table, all_three_regions

DEF_1j1b_sels = "reg1j1b == 1 && OS == 1"
DEF_1j1b_swmc = "reg1j1b == 1 && OS == 1 && mass_lep1jet1 < 155 && mass_lep2jet1 < 155"
DEF_1j1b_vari = "bdtres00"
DEF_1j1b_nbin = 12
DEF_1j1b_xmin = 0.17
DEF_1j1b_xmax = 0.76
DEF_1j1b_bins = "{},{},{}".format(DEF_1j1b_nbin, DEF_1j1b_xmin, DEF_1j1b_xmax)

DEF_2j1b_sels = "reg2j1b == 1 && OS == 1"
DEF_2j1b_swmc = "reg2j1b == 1 && OS == 1 && mass_lep1jetb < 155 && mass_lep2jetb < 155"
DEF_2j1b_vari = "bdtres00"
DEF_2j1b_nbin = 12
DEF_2j1b_xmin = 0.22
DEF_2j1b_xmax = 0.85
DEF_2j1b_bins = "{},{},{}".format(DEF_2j1b_nbin, DEF_2j1b_xmin, DEF_2j1b_xmax)

DEF_2j2b_sels = "reg2j2b == 1 && OS == 1"
DEF_2j2b_swmc = "reg2j2b == 1 && OS == 1 && minimaxmbl < 155"
DEF_2j2b_vari = "bdtres00"
DEF_2j2b_nbin = 12
DEF_2j2b_xmin = 0.20
DEF_2j2b_xmax = 0.90
DEF_2j2b_bins = "{},{},{}".format(DEF_2j2b_nbin, DEF_2j2b_xmin, DEF_2j2b_xmax)


def top(**kwargs):
    params = dict(
        job="tW",
        fit="tW",
        label="tW Dilepton",
        ntuplepaths="/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
        dotables="TRUE",
        systplots="TRUE",
        fitblind="TRUE",
        reg1j1b_selection=DEF_1j1b_sels,
        reg1j1b_variable=DEF_1j1b_vari,
        reg1j1b_binning=DEF_1j1b_bins,
        reg2j1b_selection=DEF_2j1b_sels,
        reg2j1b_variable=DEF_2j1b_vari,
        reg2j1b_binning=DEF_2j1b_bins,
        reg2j2b_selection=DEF_2j2b_sels,
        reg2j2b_variable=DEF_2j2b_vari,
        reg2j2b_binning=DEF_2j2b_bins,
    )
    for k in kwargs:
        params[k] = kwargs[k]

    return dedent(
        """\
    Job: "{job}"
      Label: "{label}"
      ReadFrom: NTUP
      DebugLevel: 1
      POI: "SigXsecOverSM"
      PlotOptions: NOXERR,CHI2
      MCstatThreshold: 0.001
      SystPruningNorm: 0.0005
      SystPruningShape: 0.001
      NtuplePaths: "{ntuplepaths}"
      NtupleName: "WtLoop_nominal"
      HistoChecks: NOCRASH
      DoPieChartPlot: FALSE
      CmeLabel: "13 TeV"
      DoSummaryPlot: FALSE
      SummaryPlotRegions: reg1j1b,reg2j1b,reg2j2b
      DoTables: {dotables}
      SystCategoryTables: FALSE
      SystControlPlots: {systplots}
      SystDataPlots: {systplots}
      LegendNColumns: 1
      ImageFormat: "pdf"
      Lumi: 138.965
      LumiLabel: "139.0 fb^{{-1}}"
      GetChi2: TRUE
      UseATLASRoundingTxt: TRUE
      UseATLASRoundingTex: TRUE
      TableOptions: STANDALONE
      RankingPlot: Systs
      RankingMaxNP: 20
      RatioYmin: 0.80
      RatioYmax: 1.20
      RatioYminPostFit: 0.90
      RatioYmaxPostFit: 1.10
      SplitHistoFiles: TRUE
      CorrelationThreshold: 0.35

    Fit: "{fit}"
      NumCPU: 1
      POIAsimov: 1
      FitType: SPLUSB
      FitRegion: CRSR
      FitBlind: {fitblind}
      UseMinos: all
      GetGoodnessOfFit: TRUE
      SaturatedModel: TRUE

    Region: "reg1j1b"
      VariableTitle: "BDT Classifier Response"
      ShortLabel: 1j1b
      Label: 1j1b
      Selection: "{reg1j1b_selection}"
      Type: SIGNAL
      Variable: "{reg1j1b_variable}",{reg1j1b_binning}

    Region: "reg2j1b"
      VariableTitle: "BDT Classifier Response"
      ShortLabel: 2j1b
      Label: 2j1b
      Selection: "{reg2j1b_selection}"
      Type: SIGNAL
      Variable: "{reg2j1b_variable}",{reg2j1b_binning}

    Region: "reg2j2b"
      VariableTitle: "BDT Classifier Response"
      ShortLabel: 2j2b
      Label: 2j2b
      Selection: "{reg2j2b_selection}"
      Type: SIGNAL
      Variable: "{reg2j2b_variable}",{reg2j2b_binning}
    """.format(
            **params
        )
    )


def all_but_preamble(f):
    print(SAMPLE_BLOCKS, file=f)
    print(NORMFACTOR_BLOCKS, file=f)
    print(MODELING_BLOCKS, file=f)
    print(SYS_PDF_WEIGHT_BLOCKS, file=f)
    print(SYS_WEIGHT_BLOCKS, file=f)
    print(SYS_TWOSIDED_TREE_BLOCKS, file=f)
    print(SYS_ONESIDED_TREE_BLOCKS, file=f)


@click.group(context_settings=dict(max_content_width=92))
def cli():
    pass


@cli.command("simple-setup0")
@click.argument("outname", type=click.Path(resolve_path=True))
def simple_setup0(outname):
    """Generate a config from default settings, save to OUTNAME."""
    with open(outname, "w") as f:
        print(top(), file=f)
        all_but_preamble(f)
    return 0


@cli.command("simple-setup1")
@click.argument("outname", type=click.Path(resolve_path=True))
def simple_setup1(outname):
    """Generate a config from default settings using mass cuts, save to OUTNAME."""
    preamble = top(
        reg1j1b_selection=DEF_1j1b_swmc,
        reg2j1b_selection=DEF_2j1b_swmc,
        reg2j2b_selection=DEF_2j2b_swmc,
        reg1j1b_variable="bdtres01",
        reg2j1b_variable="bdtres01",
        reg2j2b_variable="bdtres01",
        reg1j1b_binning="12,0.17,0.745",
    )
    with open(outname, "w") as f:
        print(preamble, file=f)
        all_but_preamble(f)
    return 0


@cli.command("tunable")
@click.argument("outname", type=click.Path(resolve_path=True))
@click.option(
    "--bin-1j1b", type=str, default=DEF_1j1b_bins, help="1j1b region binning settings"
)
@click.option(
    "--bin-2j1b", type=str, default=DEF_2j1b_bins, help="2j1b region binning settings"
)
@click.option(
    "--bin-2j2b", type=str, default=DEF_2j2b_bins, help="2j2b region binning settings"
)
@click.option(
    "--var-1j1b", type=str, default=DEF_1j1b_vari, help="1j1b region variable setting"
)
@click.option(
    "--var-2j1b", type=str, default=DEF_2j1b_vari, help="2j1b region variable setting"
)
@click.option(
    "--var-2j2b", type=str, default=DEF_2j2b_vari, help="2j2b region variable setting"
)
@click.option(
    "--sel-1j1b", type=str, default=DEF_1j1b_sels, help="1j1b region selection setting"
)
@click.option(
    "--sel-2j1b", type=str, default=DEF_2j1b_sels, help="2j1b region selection setting"
)
@click.option(
    "--sel-2j2b", type=str, default=DEF_2j2b_sels, help="2j2b region selection setting"
)
@click.option("--skip-tables", is_flag=True, help="Don't produce tables")
@click.option("--skip-syst-plots", is_flag=True, help="Don't produce red/blue plots")
@click.option(
    "--vrp",
    type=click.Path(resolve_path=True, exists=True),
    help="validation region plots",
)
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
    skip_tables,
    skip_syst_plots,
    vrp,
):
    """Generate a config with user defined binning, save to OUTNAME."""
    preamble = top(
        reg1j1b_binning=bin_1j1b,
        reg2j1b_binning=bin_2j1b,
        reg2j2b_binning=bin_2j2b,
        reg1j1b_variable=var_1j1b,
        reg2j1b_variable=var_2j1b,
        reg2j2b_variable=var_2j2b,
        reg1j1b_selection=sel_1j1b,
        reg2j1b_selection=sel_2j1b,
        reg2j2b_selection=sel_2j2b,
        dotables="FALSE" if skip_tables else "TRUE",
        systplots="FALSE" if skip_syst_plots else "TRUE",
    )
    with open(outname, "w") as f:
        print(preamble, file=f)
        if vrp is not None:
            meta = load_meta_table(vrp)
            print(all_three_regions(meta, sel_1j1b, sel_2j1b, sel_2j2b), file=f)
            print("", file=f)
        all_but_preamble(f)

    return 0


if __name__ == "__main__":
    cli()
