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

def top(params=None):
    if params is None:
        params=dict(
            job="tW",
            fit="tW",
            label="tW Dilepton",
            ntuplepaths="/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
            reg1j1b_selection="reg1j1b == 1 && OS == 1",
            reg1j1b_variable="bdtres00",
            reg1j1b_nbins=12,
            reg1j1b_xmin=0.17,
            reg1j1b_xmax=0.76,
            reg2j1b_selection="reg2j1b == 1 && OS == 1",
            reg2j1b_variable="bdtres00",
            reg2j1b_nbins=12,
            reg2j1b_xmin=0.22,
            reg2j1b_xmax=0.85,
            reg2j2b_selection="reg2j2b == 1 && OS == 1",
            reg2j2b_variable="bdtres00",
            reg2j2b_nbins=12,
            reg2j2b_xmin=0.18,
            reg2j2b_xmax=0.90,
        )

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
      DoTables: TRUE
      SystCategoryTables: FALSE
      SystControlPlots: TRUE
      SystDataPlots: TRUE
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
      FitBlind: TRUE
      UseMinos: all
      GetGoodnessOfFit: TRUE
      SaturatedModel: TRUE

    Region: "reg1j1b"
      VariableTitle: "BDT Classifier Response"
      ShortLabel: 1j1b
      Label: 1j1b
      Selection: "{reg1j1b_selection}"
      Type: SIGNAL
      Variable: "{reg1j1b_variable}",{reg1j1b_nbins},{reg1j1b_xmin},{reg1j1b_xmax}

    Region: "reg2j1b"
      VariableTitle: "BDT Classifier Response"
      ShortLabel: 2j1b
      Label: 2j1b
      Selection: "{reg2j1b_selection}"
      Type: SIGNAL
      Variable: "{reg2j1b_variable}",{reg2j1b_nbins},{reg2j1b_xmin},{reg2j1b_xmax}

    Region: "reg2j2b"
      VariableTitle: "BDT Classifier Response"
      ShortLabel: 2j2b
      Label: 2j2b
      Selection: "{reg2j2b_selection}"
      Type: SIGNAL
      Variable: "{reg2j2b_variable}",{reg2j2b_nbins},{reg2j2b_xmin},{reg2j2b_xmax}
    '''.format(**params))


@click.group(context_settings=dict(max_content_width=92))
def cli():
    pass


@cli.command("simple")
@click.argument("outname", type=click.Path(resolve_path=True))
def simple(outname):
    """Generate a config from default settings, save to OUTNAME."""
    with open(outname, "w") as f:
        print(top(), file=f)
        print(SAMPLE_BLOCKS, file=f)
        print(NORMFACTOR_BLOCKS, file=f)
        print(MODELING_BLOCKS, file=f)
        print(SYS_PDF_WEIGHT_BLOCKS, file=f)
        print(SYS_WEIGHT_BLOCKS, file=f)
        print(SYS_TWOSIDED_TREE_BLOCKS, file=f)
        print(SYS_ONESIDED_TREE_BLOCKS, file=f)


if __name__ == "__main__":
    cli()
