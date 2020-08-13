"""Module for generating TRExFitter config blocks.

A complete configuration will be composed of calling these functions:

- top_blocks
- sample_blocks
- norm_factor_blocks
- sys_modeling_blocks
- sys_minor_blocks
- sys_sf_weight_blocks
- sys_pdf_weight_blocks
- sys_twosided_tree_blocks
- sys_onesided_tree_blocks

"""


# stdlib
from textwrap import dedent

# rexpy
from rexpy.shower import norm_uncertainties_tW, norm_uncertainties_ttbar
from rexpy.systematic_tables import (
    SYS_WEIGHTS,
    PDF_WEIGHTS,
    SYS_TREES_TWOSIDED,
    SYS_TREES_ONESIDED,
)
import rexpy.simpconf as c


def top_blocks(**kwargs):
    params = dict(
        job="tW",
        fit="tW",
        label="tW Dilepton",
        ntuplepaths=c.NTUP_DIR,
        dotables="FALSE",
        systplots="FALSE",
        reg1j1b_selection=c.DEF_1j1b_sels,
        reg1j1b_variable=c.DEF_1j1b_vari,
        reg1j1b_binning=c.DEF_1j1b_bins,
        reg2j1b_selection=c.DEF_2j1b_sels,
        reg2j1b_variable=c.DEF_2j1b_vari,
        reg2j1b_binning=c.DEF_2j1b_bins,
        reg2j2b_selection=c.DEF_2j2b_sels,
        reg2j2b_variable=c.DEF_2j2b_vari,
        reg2j2b_binning=c.DEF_2j2b_bins,
        spr="reg1j1b,reg2j1b,reg2j2b",
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
      SummaryPlotRegions: {spr}
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
      HEPDataFormat: TRUE

    Fit: "{fit}"
      NumCPU: 1
      POIAsimov: 1
      FitType: SPLUSB
      FitRegion: CRSR
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


def sample_blocks(**kwargs):
    params = dict()
    for k in kwargs:
        params[k] = kwargs[k]
    return dedent(
        """\
    Sample: "tW_AFII"
      Title: "tW_AFII"
      Type: GHOST
      NtupleFiles: tW_DR_410648_AFII_MC16a_nominal,tW_DR_410648_AFII_MC16d_nominal,tW_DR_410649_AFII_MC16d_nominal,tW_DR_410648_AFII_MC16e_nominal,tW_DR_410649_AFII_MC16e_nominal,tW_DR_410649_AFII_MC16a_nominal
      MCweight: "weight_nominal"

    Sample: "tW_PDF"
      Title: "tW_PDF"
      Type: GHOST
      NtupleFiles: tW_DR_410648_FS_MC16a_nominal,tW_DR_410648_FS_MC16d_nominal,tW_DR_410649_FS_MC16d_nominal,tW_DR_410648_FS_MC16e_nominal,tW_DR_410649_FS_MC16e_nominal,tW_DR_410649_FS_MC16a_nominal
      MCweight: "weight_sys_PDFset_90900"

    Sample: "ttbar_AFII"
      Title: "ttbar_AFII"
      Type: GHOST
      NtupleFiles: ttbar_410472_AFII_MC16a_nominal,ttbar_410472_AFII_MC16e_nominal,ttbar_410472_AFII_MC16d_nominal
      MCweight: "weight_nominal * {ttbar_aux_weight}"

    Sample: "ttbar_PDF"
      Title: "ttbar_PDF"
      Type: GHOST
      NtupleFiles: ttbar_410472_FS_MC16a_nominal,ttbar_410472_FS_MC16e_nominal,ttbar_410472_FS_MC16d_nominal
      MCweight: "weight_sys_PDFset_90900 * {ttbar_aux_weight}"

    Sample: "Data"
      HistoNameSuff: "_Data"
      Type: DATA
      Title: "Data"
      NtupleFiles: Data16_data16_Data_Data_nominal,Data18_data18_Data_Data_nominal,Data17_data17_Data_Data_nominal,Data15_data15_Data_Data_nominal
      MCweight: "weight_nominal"

    Sample: "tW"
      NtupleFiles: tW_DR_410648_FS_MC16a_nominal,tW_DR_410648_FS_MC16d_nominal,tW_DR_410649_FS_MC16d_nominal,tW_DR_410648_FS_MC16e_nominal,tW_DR_410649_FS_MC16e_nominal,tW_DR_410649_FS_MC16a_nominal
      Title: "tW"
      TexTitle: "$tW$"
      FillColor: 862
      LineColor: 1
      Type: SIGNAL
      MCweight: "weight_nominal"

    Sample: "ttbar"
      NtupleFiles: ttbar_410472_FS_MC16a_nominal,ttbar_410472_FS_MC16e_nominal,ttbar_410472_FS_MC16d_nominal
      Title: "Top pair"
      TexTitle: "$t\bar{{t}}$"
      FillColor: 634
      LineColor: 1
      Type: BACKGROUND
      MCweight: "weight_nominal * {ttbar_aux_weight}"

    Sample: "Zjets"
      Title: "Z+jets"
      TexTitle: "$Z+$jets"
      FillColor: 802
      LineColor: 1
      Type: BACKGROUND
      MCweight: "weight_nominal"
      NtupleFiles: Zjets_999999_FS_MC16a_nominal,Zjets_999999_FS_MC16d_nominal,Zjets_999999_FS_MC16e_nominal

    Sample: "Diboson"
      Title: "Diboson"
      TexTitle: "Diboson"
      FillColor: 419
      LineColor: 1
      Type: BACKGROUND
      MCweight: "weight_nominal"
      NtupleFiles: Diboson_999999_FS_MC16a_nominal,Diboson_999999_FS_MC16d_nominal,Diboson_999999_FS_MC16e_nominal

    Sample: "MCNP"
      Title: "Non-prompt"
      TexTitle: "Non-prompt"
      FillColor: 875
      LineColor: 1
      Type: BACKGROUND
      MCweight: "weight_nominal"
      NtupleFiles: MCNP_999999_FS_MC16a_nominal,MCNP_999999_FS_MC16d_nominal,MCNP_999999_FS_MC16e_nominal
    """
    ).format(ttbar_aux_weight=c.TTBAR_AUX_WEIGHT, **params)


def norm_factor_blocks():
    return dedent(
        """\
    NormFactor: "SigXsecOverSM"
      Max: 2
      Nominal: 1
      Min: 0
      Samples: tW
      Title: "mu_tW"

    NormFactor: "mu_ttbar"
      Max: 1.5
      Nominal: 1
      Min: 0.5
      Samples: ttbar
      Title: "mu_ttbar"
    """
    )


def _tW_shower_norms(ntup_dir, sel_1j1b=None, sel_2j1b=None, sel_2j2b=None):
    overall, m1j1b, m2j1b, m2j2b = norm_uncertainties_tW(
        ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b
    )
    return """\
Systematic: "tW_PS_norm"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Norm"
  Type: OVERALL
  OverallUp: {0}
  OverallDown: -{0}
  Samples: tW

Systematic: "tW_PS_migration"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Migration"
  NuisanceParameter: "tW_PS_migration"
  Type: OVERALL
  OverallUp: {1}
  OverallDown: -{1}
  Samples: tW
  Regions: reg1j1b

Systematic: "tW_PS_migration"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Migration"
  NuisanceParameter: "tW_PS_migration"
  Type: OVERALL
  OverallUp: {2}
  OverallDown: -{2}
  Samples: tW
  Regions: reg2j1b

Systematic: "tW_PS_migration"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Migration"
  NuisanceParameter: "tW_PS_migration"
  Type: OVERALL
  OverallUp: {3}
  OverallDown: -{3}
  Samples: tW
  Regions: reg2j2b""".format(
        overall, m1j1b, m2j1b, m2j2b
    )


def _ttbar_shower_norms(
    ntup_dir,
    sel_1j1b=None,
    sel_2j1b=None,
    sel_2j2b=None,
    herwig_dsid="410558",
):
    overall, m1j1b, m2j1b, m2j2b = norm_uncertainties_ttbar(
        ntup_dir,
        sel_1j1b,
        sel_2j1b,
        sel_2j2b,
        herwig_dsid,
        f"weight_nominal * {c.TTBAR_AUX_WEIGHT}",
    )
    return """\
Systematic: "ttbar_PS_norm"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Norm"
  Type: OVERALL
  OverallUp: {0}
  OverallDown: -{0}
  Samples: ttbar

Systematic: "ttbar_PS_migration"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Migration"
  NuisanceParameter: "ttbar_PS_migration"
  Type: OVERALL
  OverallUp: {1}
  OverallDown: -{1}
  Samples: ttbar
  Regions: reg1j1b

Systematic: "ttbar_PS_migration"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Migration"
  NuisanceParameter: "ttbar_PS_migration"
  Type: OVERALL
  OverallUp: {2}
  OverallDown: -{2}
  Samples: ttbar
  Regions: reg2j1b

Systematic: "ttbar_PS_migration"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Migration"
  NuisanceParameter: "ttbar_PS_migration"
  Type: OVERALL
  OverallUp: {3}
  OverallDown: -{3}
  Samples: ttbar
  Regions: reg2j2b""".format(
        overall, m1j1b, m2j1b, m2j2b
    )


def _herwig_version_to_dsid(herwig_version):
    if herwig_version == "704":
        return "410558"
    elif herwig_version == "713":
        return "411234"
    else:
        raise ValueError("Bad Herwig version")


def sys_modeling_blocks(
    ntup_dir,
    sel_1j1b=None,
    sel_2j1b=None,
    sel_2j2b=None,
    herwig_version="704",
):
    herwig_dsid = _herwig_version_to_dsid(herwig_version)
    tW_norms = _tW_shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b)
    ttbar_norms = _ttbar_shower_norms(
        ntup_dir,
        sel_1j1b,
        sel_2j1b,
        sel_2j2b,
        herwig_dsid,
    )
    shower_norm_blocks = "{}\n\n{}".format(tW_norms, ttbar_norms)
    return """\
Systematic: "tW_DRDS"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Symmetrisation: ONESIDED
  Samples: tW
  Title: "tW DR vs DS"
  Type: HISTO
  NtupleFilesUp: tW_DS_410657_FS_MC16d_nominal,tW_DS_410657_FS_MC16e_nominal,tW_DS_410657_FS_MC16a_nominal,tW_DS_410656_FS_MC16e_nominal,tW_DS_410656_FS_MC16a_nominal,tW_DS_410656_FS_MC16d_nominal

{shower_norm_blocks}

Systematic: "tW_PS_1j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Shape 1j1b"
  ReferenceSample: tW_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: tW
  Type: HISTO
  Regions: reg1j1b
  NtupleFilesUp: tW_DR_411038_AFII_MC16a_nominal,tW_DR_411038_AFII_MC16d_nominal,tW_DR_411039_AFII_MC16a_nominal,tW_DR_411039_AFII_MC16d_nominal,tW_DR_411038_AFII_MC16e_nominal,tW_DR_411039_AFII_MC16e_nominal

Systematic: "tW_PS_2j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Shape 2j1b"
  ReferenceSample: tW_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: tW
  Type: HISTO
  Regions: reg2j1b
  NtupleFilesUp: tW_DR_411038_AFII_MC16a_nominal,tW_DR_411038_AFII_MC16d_nominal,tW_DR_411039_AFII_MC16a_nominal,tW_DR_411039_AFII_MC16d_nominal,tW_DR_411038_AFII_MC16e_nominal,tW_DR_411039_AFII_MC16e_nominal

Systematic: "tW_PS_2j2b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW Parton Shower Shape 2j2b"
  ReferenceSample: tW_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: tW
  Type: HISTO
  Regions: reg2j2b
  NtupleFilesUp: tW_DR_411038_AFII_MC16a_nominal,tW_DR_411038_AFII_MC16d_nominal,tW_DR_411039_AFII_MC16a_nominal,tW_DR_411039_AFII_MC16d_nominal,tW_DR_411038_AFII_MC16e_nominal,tW_DR_411039_AFII_MC16e_nominal

Systematic: "ttbar_PS_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Shape 1j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b
  NtupleFilesUp: ttbar_{herwig_dsid}_AFII_MC16a_nominal,ttbar_{herwig_dsid}_AFII_MC16d_nominal,ttbar_{herwig_dsid}_AFII_MC16e_nominal

Systematic: "ttbar_PS_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Shape 2j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b
  NtupleFilesUp: ttbar_{herwig_dsid}_AFII_MC16a_nominal,ttbar_{herwig_dsid}_AFII_MC16d_nominal,ttbar_{herwig_dsid}_AFII_MC16e_nominal

Systematic: "ttbar_PS_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar Parton Shower Shape 2j2b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b
  NtupleFilesUp: ttbar_{herwig_dsid}_AFII_MC16a_nominal,ttbar_{herwig_dsid}_AFII_MC16d_nominal,ttbar_{herwig_dsid}_AFII_MC16e_nominal

Systematic: "tW_AR_ISR_scale_muR_1j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR Scale muR Variation 1j1b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_ISR_scale_muR_2j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR Scale muR Variation 2j1b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_ISR_scale_muR_2j2b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR Scale muR Variation 2j2b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "tW_AR_ISR_scale_muF_1j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR Scale muF Variation 1j1b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_ISR_scale_muF_2j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR Scale muF Variation 2j1b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_ISR_scale_muF_2j2b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR Scale muF Variation 2j2b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "tW_AR_ISR_A14_1j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR A14 1j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_ISR_A14_2j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR A14 2j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_ISR_A14_2j2b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW ISR A14 2j2b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "tW_AR_FSR_1j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW FSR 1j1b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_FSR_2j1b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW FSR 2j1b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_FSR_2j2b"
  Category: "Signal_Model"
  SubCategory: "Signal_Model"
  Title: "tW FSR 2j2b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_ISR_scale_muR_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR Scale muR Variation 1j1b"
  WeightUp: "weight_sys_scale_muR_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_scale_muR_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_ISR_scale_muR_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR Scale muR Variation 2j1b"
  WeightUp: "weight_sys_scale_muR_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_scale_muR_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_ISR_scale_muR_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR Scale muR Variation 2j2b"
  WeightUp: "weight_sys_scale_muR_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_scale_muR_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_ISR_scale_muF_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR Scale muF Variation 1j1b"
  WeightUp: "weight_sys_scale_muF_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_scale_muF_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_ISR_scale_muF_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR Scale muF Variation 2j1b"
  WeightUp: "weight_sys_scale_muF_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_scale_muF_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_ISR_scale_muF_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR Scale muF Variation 2j2b"
  WeightUp: "weight_sys_scale_muF_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_scale_muF_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_ISR_A14_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR A14 1j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp * {ttbar_aux_weight}"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_ISR_A14_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR A14 2j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp * {ttbar_aux_weight}"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_ISR_A14_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar ISR A14 2j2b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp * {ttbar_aux_weight}"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_FSR_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar FSR 1j1b"
  WeightUp: "weight_sys_fsr_muR_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_fsr_muR_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_FSR_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar FSR 2j1b"
  WeightUp: "weight_sys_fsr_muR_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_fsr_muR_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_FSR_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar FSR 2j2b"
  WeightUp: "weight_sys_fsr_muR_20 * {ttbar_aux_weight}"
  WeightDown: "weight_sys_fsr_muR_05 * {ttbar_aux_weight}"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_hdamp_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar hdamp 1j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b
  NtupleFilesUp: ttbar_410482_AFII_MC16a_nominal,ttbar_410482_AFII_MC16d_nominal,ttbar_410482_AFII_MC16e_nominal

Systematic: "ttbar_hdamp_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar hdamp 2j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b
  NtupleFilesUp: ttbar_410482_AFII_MC16a_nominal,ttbar_410482_AFII_MC16d_nominal,ttbar_410482_AFII_MC16e_nominal

Systematic: "ttbar_hdamp_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar hdamp 2j2b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b
  NtupleFilesUp: ttbar_410482_AFII_MC16a_nominal,ttbar_410482_AFII_MC16d_nominal,ttbar_410482_AFII_MC16e_nominal

Systematic: "ttbar_ptreweight_1j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar pt reweight 1j1b"
  WeightUp: "weight_sys_noreweight"
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_ptreweight_2j1b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar pt reweight 2j1b"
  WeightUp: "weight_sys_noreweight"
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_ptreweight_2j2b"
  Category: "Background_Model"
  SubCategory: "Background_Model"
  Title: "ttbar pt reweight 2j2b"
  WeightUp: "weight_sys_noreweight"
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b\n""".format(
      shower_norm_blocks=shower_norm_blocks,
      herwig_dsid=herwig_dsid,
      ttbar_aux_weight=c.TTBAR_AUX_WEIGHT,
  )


def sys_minor_blocks():
    return dedent(
        """\
    Systematic: "Norm_Diboson_1j1b"
      Type: OVERALL
      Title: "Norm Diboson 1j1b"
      Regions: reg1j1b
      Samples: Diboson
      OverallUp: 0.22
      OverallDown: -0.22
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_Diboson_2j1b"
      Type: OVERALL
      Title: "Norm Diboson 2j1b"
      Regions: reg2j1b
      Samples: Diboson
      OverallUp: 0.22
      OverallDown: -0.22
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_Diboson_2j2b"
      Type: OVERALL
      Title: "Norm Diboson 2j2b"
      Regions: reg2j2b
      Samples: Diboson
      OverallUp: 0.13
      OverallDown: -0.13
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_Zjets_1j1b"
      Type: OVERALL
      Title: "Norm Zjets 1j1b"
      Regions: reg1j1b
      Samples: Zjets
      OverallUp: 0.11
      OverallDown: -0.11
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_Zjets_2j1b"
      Type: OVERALL
      Title: "Norm Zjets 2j1b"
      Regions: reg2j1b
      Samples: Zjets
      OverallUp: 0.11
      OverallDown: -0.11
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_Zjets_2j2b"
      Type: OVERALL
      Title: "Norm Zjets 2j2b"
      Regions: reg2j2b
      Samples: Zjets
      OverallUp: 0.17
      OverallDown: -0.17
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_MCNP_1j1b"
      Type: OVERALL
      Title: "Norm MCNP 1j1b"
      Regions: reg1j1b
      Samples: MCNP
      OverallUp: 0.5
      OverallDown: -0.5
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_MCNP_2j1b"
      Type: OVERALL
      Title: "Norm MCNP 2j1b"
      Regions: reg2j1b
      Samples: MCNP
      OverallUp: 0.5
      OverallDown: -0.5
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Norm_MCNP_2j2b"
      Type: OVERALL
      Title: "Norm MCNP 2j2b"
      Regions: reg2j2b
      Samples: MCNP
      OverallUp: 0.5
      OverallDown: -0.5
      Category: "Minor_Background_Model"
      SubCategory: "Minor_Background_Model"

    Systematic: "Lumi"
      OverallDown: -0.017
      Category: "Luminosity"
      SubCategory: "Luminosity"
      OverallUp: 0.017
      Title: "Lumi"
      Samples: tW,ttbar
      Type: OVERALL
    """
    )


def sys_sf_weight_blocks():
    blocks = []
    for name, properties in SYS_WEIGHTS.items():
        block = """\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          WeightUp: "{branch_up}"
          WeightDown: "{branch_down}"
          Type: HISTO
          Symmetrisation: TWOSIDED
          Samples: tW

        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          WeightUp: "{branch_up} * {ttbar_aux_weight}"
          WeightDown: "{branch_down} * {ttbar_aux_weight}"
          Type: HISTO
          Symmetrisation: TWOSIDED
          Samples: ttbar\n""".format(
            name=name,
            category=properties.category,
            title=properties.title,
            branch_up=properties.branch_up,
            branch_down=properties.branch_down,
            ttbar_aux_weight=c.TTBAR_AUX_WEIGHT,
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


def sys_pdf_weight_blocks():
    blocks = []
    for name, properties in PDF_WEIGHTS.items():
        block = """\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          WeightUp: "{branch} * {ttbar_aux_weight}"
          ReferenceSample: ttbar_PDF
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: ttbar
          ReferenceSample: ttbar_PDF

        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          WeightUp: "{branch}"
          ReferenceSample: tW_PDF
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: tW
          ReferenceSample: tW_PDF\n""".format(
            name=name,
            category=properties.category,
            title=properties.title,
            branch=properties.branch,
            ttbar_aux_weight=c.TTBAR_AUX_WEIGHT,
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


def sys_twosided_tree_blocks():
    blocks = []
    for name, properties in SYS_TREES_TWOSIDED.items():
        block = """\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          NtupleFilesUp: ttbar_410472_FS_MC16a_{tree_up},ttbar_410472_FS_MC16d_{tree_up},ttbar_410472_FS_MC16e_{tree_up}
          NtupleFilesDown: ttbar_410472_FS_MC16a_{tree_down},ttbar_410472_FS_MC16d_{tree_down},ttbar_410472_FS_MC16e_{tree_down}
          NtupleNameUp: "WtLoop_{tree_up}"
          NtupleNameDown: "WtLoop_{tree_down}"
          Samples: ttbar
          Type: HISTO
          Symmetrisation: TWOSIDED

        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          NtupleFilesUp: tW_DR_410648_FS_MC16a_{tree_up},tW_DR_410648_FS_MC16d_{tree_up},tW_DR_410648_FS_MC16e_{tree_up},tW_DR_410649_FS_MC16a_{tree_up},tW_DR_410649_FS_MC16d_{tree_up},tW_DR_410649_FS_MC16e_{tree_up}
          NtupleFilesDown: tW_DR_410648_FS_MC16a_{tree_down},tW_DR_410648_FS_MC16d_{tree_down},tW_DR_410648_FS_MC16e_{tree_down},tW_DR_410649_FS_MC16a_{tree_down},tW_DR_410649_FS_MC16d_{tree_down},tW_DR_410649_FS_MC16e_{tree_down}
          NtupleNameUp: "WtLoop_{tree_up}"
          NtupleNameDown: "WtLoop_{tree_down}"
          Samples: tW
          Type: HISTO
          Symmetrisation: TWOSIDED\n""".format(
            name=name,
            category=properties.category,
            title=properties.title,
            tree_up=properties.branch_up,
            tree_down=properties.branch_down,
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


def sys_onesided_tree_blocks():
    blocks = []
    for name, properties in SYS_TREES_ONESIDED.items():
        block = """\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          NtupleFilesUp: ttbar_410472_FS_MC16a_{tree_up},ttbar_410472_FS_MC16d_{tree_up},ttbar_410472_FS_MC16e_{tree_up}
          NtupleNameUp: "WtLoop_{tree_up}"
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: ttbar

        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          SubCategory: "{category}"
          Title: "{title}"
          NtupleFilesUp: tW_DR_410648_FS_MC16a_{tree_up},tW_DR_410648_FS_MC16d_{tree_up},tW_DR_410648_FS_MC16e_{tree_up},tW_DR_410649_FS_MC16a_{tree_up},tW_DR_410649_FS_MC16d_{tree_up},tW_DR_410649_FS_MC16e_{tree_up}
          NtupleNameUp: "WtLoop_{tree_up}"
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: tW\n""".format(
            name=name,
            title=properties.title,
            category=properties.category,
            tree_up=properties.branch,
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)
