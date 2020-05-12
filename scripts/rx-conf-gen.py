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

def top(**kwargs):
    params = dict(
        job="tW",
        fit="tW",
        label="tW Dilepton",
        ntuplepaths="/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
        dotables="TRUE",
        systplots="TRUE",
        fitblind="TRUE",
        reg1j1b_selection="reg1j1b == 1 && OS == 1",
        reg1j1b_variable="bdtres00",
        reg1j1b_binning="12,0.17,0.76",
        reg2j1b_selection="reg2j1b == 1 && OS == 1",
        reg2j1b_variable="bdtres00",
        reg2j1b_binning="12,0.22,0.85",
        reg2j2b_selection="reg2j2b == 1 && OS == 1",
        reg2j2b_variable="bdtres00",
        reg2j2b_binning="12,0.2,0.90",
    )
    for k in kwargs:
        params[k] = kwargs[k]

    return dedent('''\
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
    '''.format(**params))


def all_put_preamble(f):
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


@cli.command("simple")
@click.argument("outname", type=click.Path(resolve_path=True))
def simple(outname):
    """Generate a config from default settings, save to OUTNAME."""
    with open(outname, "w") as f:
        print(top(), file=f)
        all_put_preamble(f)
    return 0


@cli.command("tunable")
@click.argument("outname", type=click.Path(resolve_path=True))
@click.option("--bin-1j1b", type=str, default="12,0.17,0.76", help="1j1b region binning settings")
@click.option("--bin-2j1b", type=str, default="12,0.22,0.85", help="2j1b region binning settings")
@click.option("--bin-2j2b", type=str, default="12,0.2,0.90", help="2j2b region binning settings")
@click.option("--var-1j1b", type=str, default="bdtres00", help="1j1b region variable setting")
@click.option("--var-2j1b", type=str, default="bdtres00", help="2j1b region variable setting")
@click.option("--var-2j2b", type=str, default="bdtres00", help="2j2b region variable setting")
@click.option("--sel-1j1b", type=str, default="reg1j1b == 1 && OS == 1", help="1j1b region selection setting")
@click.option("--sel-2j1b", type=str, default="reg2j1b == 1 && OS == 1", help="2j1b region selection setting")
@click.option("--sel-2j2b", type=str, default="reg2j2b == 1 && OS == 1", help="2j2b region selection setting")
@click.option("--skip-tables", is_flag=True, help="Don't produce tables")
@click.option("--skip-syst-plots", is_flag=True, help="Don't produce red/blue plots")
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
    skip_syst_plots
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
        all_put_preamble(f)
    return 0


if __name__ == "__main__":
    cli()
