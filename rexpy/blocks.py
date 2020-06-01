# stdlib
from textwrap import dedent
from collections import OrderedDict, namedtuple

from rexpy.shower import norm_uncertainties_tW, norm_uncertainties_ttbar


NTUP_DIR = "/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506"

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


def top_blocks(**kwargs):
    params = dict(
        job="tW",
        fit="tW",
        label="tW Dilepton",
        ntuplepaths=NTUP_DIR,
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


def const_sys_blocks(f):
    print(SYS_MINOR_BLOCKS, file=f)
    print(SYS_PDF_WEIGHT_BLOCKS, file=f)
    print(SYS_WEIGHT_BLOCKS, file=f)
    print(SYS_TWOSIDED_TREE_BLOCKS, file=f)
    print(SYS_ONESIDED_TREE_BLOCKS, file=f)


# fmt: off
NTSysWeight = namedtuple("SysWeight" , "branch_up branch_down category smoothing title tiny")
NTSysPDF    = namedtuple("SysPDF"    , "branch category smoothing title tiny")
NTSysTree2s = namedtuple("SysTree2s" , "branch_up branch_down category smoothing title tiny")
NTSysTree1s = namedtuple("SysTree1s" , "branch category smoothing title tiny")

SYS_WEIGHTS = OrderedDict()
SYS_WEIGHTS["JVT"]          = NTSysWeight("weight_sys_jvt_UP"                          , "weight_sys_jvt_DOWN"                          , "Instrumental" , "40", "JVT"                 , False)
SYS_WEIGHTS["Pileup"]       = NTSysWeight("weight_sys_pileup_UP"                       , "weight_sys_pileup_DOWN"                       , "Instrumental" , "40", "Pileup"              , False)
SYS_WEIGHTS["EL_Trig"]      = NTSysWeight("weight_sys_leptonSF_EL_SF_Trigger_UP"       , "weight_sys_leptonSF_EL_SF_Trigger_DOWN"       , "WeightLepSFs" , "40", "Electron Trig"       , False)
SYS_WEIGHTS["EL_Reco"]      = NTSysWeight("weight_sys_leptonSF_EL_SF_Reco_UP"          , "weight_sys_leptonSF_EL_SF_Reco_DOWN"          , "WeightLepSFs" , "40", "Electron Reco"       , False)
SYS_WEIGHTS["EL_ID"]        = NTSysWeight("weight_sys_leptonSF_EL_SF_ID_UP"            , "weight_sys_leptonSF_EL_SF_ID_DOWN"            , "WeightLepSFs" , "40", "Electron ID"         , False)
SYS_WEIGHTS["EL_Isol"]      = NTSysWeight("weight_sys_leptonSF_EL_SF_Isol_UP"          , "weight_sys_leptonSF_EL_SF_Isol_DOWN"          , "WeightLepSFs" , "40", "Electron Isol"       , False)
SYS_WEIGHTS["MU_TrigStat"]  = NTSysWeight("weight_sys_leptonSF_MU_SF_Trigger_STAT_UP"  , "weight_sys_leptonSF_MU_SF_Trigger_STAT_DOWN"  , "WeightLepSFs" , "40", "Muon Trig Stat"      , False)
SYS_WEIGHTS["MU_TrigSyst"]  = NTSysWeight("weight_sys_leptonSF_MU_SF_Trigger_SYST_UP"  , "weight_sys_leptonSF_MU_SF_Trigger_SYST_DOWN"  , "WeightLepSFs" , "40", "Muon Trig Syst"      , False)
SYS_WEIGHTS["MU_IDStat"]    = NTSysWeight("weight_sys_leptonSF_MU_SF_ID_STAT_UP"       , "weight_sys_leptonSF_MU_SF_ID_STAT_DOWN"       , "WeightLepSFs" , "40", "Muon ID Stat"        , False)
SYS_WEIGHTS["MU_IDSyst"]    = NTSysWeight("weight_sys_leptonSF_MU_SF_ID_SYST_UP"       , "weight_sys_leptonSF_MU_SF_ID_SYST_DOWN"       , "WeightLepSFs" , "40", "Muon ID Syst"        , False)
SYS_WEIGHTS["MU_IDStatLPT"] = NTSysWeight("weight_sys_leptonSF_MU_SF_ID_STAT_LOWPT_UP" , "weight_sys_leptonSF_MU_SF_ID_STAT_LOWPT_DOWN" , "WeightLepSFs" , "40", "Muon ID Stat Low PT" , False)
SYS_WEIGHTS["MU_IDSystLPT"] = NTSysWeight("weight_sys_leptonSF_MU_SF_ID_SYST_LOWPT_UP" , "weight_sys_leptonSF_MU_SF_ID_SYST_LOWPT_DOWN" , "WeightLepSFs" , "40", "Muon ID Syst Low PT" , False)
SYS_WEIGHTS["MU_IsolStat"]  = NTSysWeight("weight_sys_leptonSF_MU_SF_Isol_STAT_UP"     , "weight_sys_leptonSF_MU_SF_Isol_STAT_DOWN"     , "WeightLepSFs" , "40", "Muon Isol Stat"      , False)
SYS_WEIGHTS["MU_IsolSyst"]  = NTSysWeight("weight_sys_leptonSF_MU_SF_Isol_SYST_UP"     , "weight_sys_leptonSF_MU_SF_Isol_SYST_DOWN"     , "WeightLepSFs" , "40", "Muon Isol Syst"      , False)
SYS_WEIGHTS["MU_TTVAStat"]  = NTSysWeight("weight_sys_leptonSF_MU_SF_TTVA_STAT_UP"     , "weight_sys_leptonSF_MU_SF_TTVA_STAT_DOWN"     , "WeightLepSFs" , "40", "Muon TTVA Stat"      , False)
SYS_WEIGHTS["MU_TTVASyst"]  = NTSysWeight("weight_sys_leptonSF_MU_SF_TTVA_SYST_UP"     , "weight_sys_leptonSF_MU_SF_TTVA_SYST_DOWN"     , "WeightLepSFs" , "40", "Muon TTVA Syst"      , False)


SYS_WEIGHTS["B_ev_B_0"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_0_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_0_down", "WeightFT_B", "40", "b-tag ev B0", False)
SYS_WEIGHTS["B_ev_B_1"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_1_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_1_down", "WeightFT_B", "40", "b-tag ev B1", False)
SYS_WEIGHTS["B_ev_B_2"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_2_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_2_down", "WeightFT_B", "40", "b-tag ev B2", False)
SYS_WEIGHTS["B_ev_B_3"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_3_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_3_down", "WeightFT_B", "40", "b-tag ev B3", False)
SYS_WEIGHTS["B_ev_B_4"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_4_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_4_down", "WeightFT_B", "40", "b-tag ev B4", False)
SYS_WEIGHTS["B_ev_B_5"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_5_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_5_down", "WeightFT_B", "40", "b-tag ev B5", False)
SYS_WEIGHTS["B_ev_B_6"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_6_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_6_down", "WeightFT_B", "40", "b-tag ev B6", False)
SYS_WEIGHTS["B_ev_B_7"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_7_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_7_down", "WeightFT_B", "40", "b-tag ev B7", False)
SYS_WEIGHTS["B_ev_B_8"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_B_8_up", "weight_sys_bTagSF_DL1r_77_eigenvars_B_8_down", "WeightFT_B", "40", "b-tag ev B8", False)
SYS_WEIGHTS["B_ev_C_0"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_C_0_up", "weight_sys_bTagSF_DL1r_77_eigenvars_C_0_down", "WeightFT_C", "40", "b-tag ev C0", False)
SYS_WEIGHTS["B_ev_C_1"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_C_1_up", "weight_sys_bTagSF_DL1r_77_eigenvars_C_1_down", "WeightFT_C", "40", "b-tag ev C1", False)
SYS_WEIGHTS["B_ev_C_2"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_C_2_up", "weight_sys_bTagSF_DL1r_77_eigenvars_C_2_down", "WeightFT_C", "40", "b-tag ev C2", False)
SYS_WEIGHTS["B_ev_C_3"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_C_3_up", "weight_sys_bTagSF_DL1r_77_eigenvars_C_3_down", "WeightFT_C", "40", "b-tag ev C3", False)
SYS_WEIGHTS["B_ev_C_4"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_C_4_up", "weight_sys_bTagSF_DL1r_77_eigenvars_C_4_down", "WeightFT_C", "40", "b-tag ev C4", False)
SYS_WEIGHTS["B_ev_L_0"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_Light_0_up", "weight_sys_bTagSF_DL1r_77_eigenvars_Light_0_down", "WeightFT_L", "40", "b-tag ev L0", False)
SYS_WEIGHTS["B_ev_L_1"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_Light_1_up", "weight_sys_bTagSF_DL1r_77_eigenvars_Light_1_down", "WeightFT_L", "40", "b-tag ev L1", False)
SYS_WEIGHTS["B_ev_L_2"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_Light_2_up", "weight_sys_bTagSF_DL1r_77_eigenvars_Light_2_down", "WeightFT_L", "40", "b-tag ev L2", False)
SYS_WEIGHTS["B_ev_L_3"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_Light_3_up", "weight_sys_bTagSF_DL1r_77_eigenvars_Light_3_down", "WeightFT_L", "40", "b-tag ev L3", False)
SYS_WEIGHTS["B_ev_L_4"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_eigenvars_Light_4_up", "weight_sys_bTagSF_DL1r_77_eigenvars_Light_4_down", "WeightFT_L", "40", "b-tag ev L4", False)
SYS_WEIGHTS["B_ev_extrap"]   = NTSysWeight("weight_sys_bTagSF_DL1r_77_extrapolation_up", "weight_sys_bTagSF_DL1r_77_extrapolation_down", "WeightFT_Extrap", "40", "b-tag extrap", False)
SYS_WEIGHTS["B_ev_extrapfc"] = NTSysWeight("weight_sys_bTagSF_DL1r_77_extrapolation_from_charm_up", "weight_sys_bTagSF_DL1r_77_extrapolation_from_charm_down", "WeightFT_ExtrapFromCharm", "40", "b-tag extrap from charm", False)


PDF_WEIGHTS = OrderedDict()
PDF_WEIGHTS["PDFset90901"] = NTSysPDF("weight_sys_PDFset_90901", "PDF", "40", "PDF 90901", False)
PDF_WEIGHTS["PDFset90902"] = NTSysPDF("weight_sys_PDFset_90902", "PDF", "40", "PDF 90902", False)
PDF_WEIGHTS["PDFset90903"] = NTSysPDF("weight_sys_PDFset_90903", "PDF", "40", "PDF 90903", False)
PDF_WEIGHTS["PDFset90904"] = NTSysPDF("weight_sys_PDFset_90904", "PDF", "40", "PDF 90904", False)
PDF_WEIGHTS["PDFset90905"] = NTSysPDF("weight_sys_PDFset_90905", "PDF", "40", "PDF 90905", False)
PDF_WEIGHTS["PDFset90906"] = NTSysPDF("weight_sys_PDFset_90906", "PDF", "40", "PDF 90906", False)
PDF_WEIGHTS["PDFset90907"] = NTSysPDF("weight_sys_PDFset_90907", "PDF", "40", "PDF 90907", False)
PDF_WEIGHTS["PDFset90908"] = NTSysPDF("weight_sys_PDFset_90908", "PDF", "40", "PDF 90908", False)
PDF_WEIGHTS["PDFset90909"] = NTSysPDF("weight_sys_PDFset_90909", "PDF", "40", "PDF 90909", False)
PDF_WEIGHTS["PDFset90910"] = NTSysPDF("weight_sys_PDFset_90910", "PDF", "40", "PDF 90910", False)
PDF_WEIGHTS["PDFset90911"] = NTSysPDF("weight_sys_PDFset_90911", "PDF", "40", "PDF 90911", False)
PDF_WEIGHTS["PDFset90912"] = NTSysPDF("weight_sys_PDFset_90912", "PDF", "40", "PDF 90912", False)
PDF_WEIGHTS["PDFset90913"] = NTSysPDF("weight_sys_PDFset_90913", "PDF", "40", "PDF 90913", False)
PDF_WEIGHTS["PDFset90914"] = NTSysPDF("weight_sys_PDFset_90914", "PDF", "40", "PDF 90914", False)
PDF_WEIGHTS["PDFset90915"] = NTSysPDF("weight_sys_PDFset_90915", "PDF", "40", "PDF 90915", False)
PDF_WEIGHTS["PDFset90916"] = NTSysPDF("weight_sys_PDFset_90916", "PDF", "40", "PDF 90916", False)
PDF_WEIGHTS["PDFset90917"] = NTSysPDF("weight_sys_PDFset_90917", "PDF", "40", "PDF 90917", False)
PDF_WEIGHTS["PDFset90918"] = NTSysPDF("weight_sys_PDFset_90918", "PDF", "40", "PDF 90918", False)
PDF_WEIGHTS["PDFset90919"] = NTSysPDF("weight_sys_PDFset_90919", "PDF", "40", "PDF 90919", False)
PDF_WEIGHTS["PDFset90920"] = NTSysPDF("weight_sys_PDFset_90920", "PDF", "40", "PDF 90920", False)
PDF_WEIGHTS["PDFset90921"] = NTSysPDF("weight_sys_PDFset_90921", "PDF", "40", "PDF 90921", False)
PDF_WEIGHTS["PDFset90922"] = NTSysPDF("weight_sys_PDFset_90922", "PDF", "40", "PDF 90922", False)
PDF_WEIGHTS["PDFset90923"] = NTSysPDF("weight_sys_PDFset_90923", "PDF", "40", "PDF 90923", False)
PDF_WEIGHTS["PDFset90924"] = NTSysPDF("weight_sys_PDFset_90924", "PDF", "40", "PDF 90924", False)
PDF_WEIGHTS["PDFset90925"] = NTSysPDF("weight_sys_PDFset_90925", "PDF", "40", "PDF 90925", False)
PDF_WEIGHTS["PDFset90926"] = NTSysPDF("weight_sys_PDFset_90926", "PDF", "40", "PDF 90926", False)
PDF_WEIGHTS["PDFset90927"] = NTSysPDF("weight_sys_PDFset_90927", "PDF", "40", "PDF 90927", False)
PDF_WEIGHTS["PDFset90928"] = NTSysPDF("weight_sys_PDFset_90928", "PDF", "40", "PDF 90928", False)
PDF_WEIGHTS["PDFset90929"] = NTSysPDF("weight_sys_PDFset_90929", "PDF", "40", "PDF 90929", False)
PDF_WEIGHTS["PDFset90930"] = NTSysPDF("weight_sys_PDFset_90930", "PDF", "40", "PDF 90930", False)


SYS_TREES_TWOSIDED = OrderedDict()
SYS_TREES_TWOSIDED["EG_RES_ALL"                        ] = NTSysTree2s("EG_RESOLUTION_ALL__1up"                                             , "EG_RESOLUTION_ALL__1down"                                             , "LeptonInstrum" , "40", "EGamma Resolution"          , False)
SYS_TREES_TWOSIDED["EG_SCALE_ALL"                      ] = NTSysTree2s("EG_SCALE_ALL__1up"                                                  , "EG_SCALE_ALL__1down"                                                  , "LeptonInstrum" , "40", "EGamma Scale"               , False)
SYS_TREES_TWOSIDED["Jet_BJES_Response"                 ] = NTSysTree2s("CategoryReduction_JET_BJES_Response__1up"                           , "CategoryReduction_JET_BJES_Response__1down"                           , "Jets"   , "40", "Jet BJES Response"                 , False)
SYS_TREES_TWOSIDED["Jet_EffectiveNP_Detector1"         ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Detector1__1up"                   , "CategoryReduction_JET_EffectiveNP_Detector1__1down"                   , "Jets"   , "40", "Jet EffectiveNP Detector1"         , False)
SYS_TREES_TWOSIDED["Jet_EffectiveNP_Detector2"         ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Detector2__1up"                   , "CategoryReduction_JET_EffectiveNP_Detector2__1down"                   , "Jets"   , "40", "Jet EffectiveNP Detector2"         , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Mixed1"                  ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Mixed1__1up"                      , "CategoryReduction_JET_EffectiveNP_Mixed1__1down"                      , "Jets"   , "40", "Jet EffNP Mixed1"                  , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Mixed2"                  ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Mixed2__1up"                      , "CategoryReduction_JET_EffectiveNP_Mixed2__1down"                      , "Jets"   , "40", "Jet EffNP Mixed2"                  , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Mixed3"                  ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Mixed3__1up"                      , "CategoryReduction_JET_EffectiveNP_Mixed3__1down"                      , "Jets"   , "40", "Jet EffNP Mixed3"                  , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling1"              ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Modelling1__1up"                  , "CategoryReduction_JET_EffectiveNP_Modelling1__1down"                  , "Jets"   , "40", "Jet EffNP Modelling1"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling2"              ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Modelling2__1up"                  , "CategoryReduction_JET_EffectiveNP_Modelling2__1down"                  , "Jets"   , "40", "Jet EffNP Modelling2"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling3"              ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Modelling3__1up"                  , "CategoryReduction_JET_EffectiveNP_Modelling3__1down"                  , "Jets"   , "40", "Jet EffNP Modelling3"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling4"              ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Modelling4__1up"                  , "CategoryReduction_JET_EffectiveNP_Modelling4__1down"                  , "Jets"   , "40", "Jet EffNP Modelling4"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical1"            ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Statistical1__1up"                , "CategoryReduction_JET_EffectiveNP_Statistical1__1down"                , "Jets"   , "40", "Jet EffNP Statistical1"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical2"            ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Statistical2__1up"                , "CategoryReduction_JET_EffectiveNP_Statistical2__1down"                , "Jets"   , "40", "Jet EffNP Statistical2"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical3"            ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Statistical3__1up"                , "CategoryReduction_JET_EffectiveNP_Statistical3__1down"                , "Jets"   , "40", "Jet EffNP Statistical3"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical4"            ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Statistical4__1up"                , "CategoryReduction_JET_EffectiveNP_Statistical4__1down"                , "Jets"   , "40", "Jet EffNP Statistical4"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical5"            ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Statistical5__1up"                , "CategoryReduction_JET_EffectiveNP_Statistical5__1down"                , "Jets"   , "40", "Jet EffNP Statistical5"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical6"            ] = NTSysTree2s("CategoryReduction_JET_EffectiveNP_Statistical6__1up"                , "CategoryReduction_JET_EffectiveNP_Statistical6__1down"                , "Jets"   , "40", "Jet EffNP Statistical6"            , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_Modelling"         ] = NTSysTree2s("CategoryReduction_JET_EtaIntercalibration_Modelling__1up"           , "CategoryReduction_JET_EtaIntercalibration_Modelling__1down"           , "Jets"   , "40", "Jet EtaIntercal Modelling"         , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_18data" ] = NTSysTree2s("CategoryReduction_JET_EtaIntercalibration_NonClosure_2018data__1up" , "CategoryReduction_JET_EtaIntercalibration_NonClosure_2018data__1down" , "Jets"   , "40", "Jet Etaintercal NonClosure Data18" , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_highE"  ] = NTSysTree2s("CategoryReduction_JET_EtaIntercalibration_NonClosure_highE__1up"    , "CategoryReduction_JET_EtaIntercalibration_NonClosure_highE__1down"    , "Jets"   , "40", "Jet EtaIntercal NonClosure highE"  , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_negEta" ] = NTSysTree2s("CategoryReduction_JET_EtaIntercalibration_NonClosure_negEta__1up"   , "CategoryReduction_JET_EtaIntercalibration_NonClosure_negEta__1down"   , "Jets"   , "40", "Jet EtaIntercal NonClosure negEta" , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_posEta" ] = NTSysTree2s("CategoryReduction_JET_EtaIntercalibration_NonClosure_posEta__1up"   , "CategoryReduction_JET_EtaIntercalibration_NonClosure_posEta__1down"   , "Jets"   , "40", "Jet EtaIntercal NonClosure posEta" , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_TotalStat"         ] = NTSysTree2s("CategoryReduction_JET_EtaIntercalibration_TotalStat__1up"           , "CategoryReduction_JET_EtaIntercalibration_TotalStat__1down"           , "Jets"   , "40", "Jet EtaIntercal TotalStat"         , False)
SYS_TREES_TWOSIDED["Jet_Flavor_Composition"            ] = NTSysTree2s("CategoryReduction_JET_Flavor_Composition__1up"                      , "CategoryReduction_JET_Flavor_Composition__1down"                      , "Jets"   , "40", "Jet Flavor Composition"            , False)
SYS_TREES_TWOSIDED["Jet_Flavor_Response"               ] = NTSysTree2s("CategoryReduction_JET_Flavor_Response__1up"                         , "CategoryReduction_JET_Flavor_Response__1down"                         , "Jets"   , "40", "Jet Flavor Response"               , False)
SYS_TREES_TWOSIDED["Jet_Pileup_OffsetMu"               ] = NTSysTree2s("CategoryReduction_JET_Pileup_OffsetMu__1up"                         , "CategoryReduction_JET_Pileup_OffsetMu__1down"                         , "Jets"   , "40", "Jet Pileup OffsetMu"               , False)
SYS_TREES_TWOSIDED["Jet_Pileup_OffsetNPV"              ] = NTSysTree2s("CategoryReduction_JET_Pileup_OffsetNPV__1up"                        , "CategoryReduction_JET_Pileup_OffsetNPV__1down"                        , "Jets"   , "40", "Jet Pileup OffsetNPV"              , False)
SYS_TREES_TWOSIDED["Jet_Pileup_PtTerm"                 ] = NTSysTree2s("CategoryReduction_JET_Pileup_PtTerm__1up"                           , "CategoryReduction_JET_Pileup_PtTerm__1down"                           , "Jets"   , "40", "Jet Pileup PtTerm"                 , False)
SYS_TREES_TWOSIDED["Jet_Pileup_RhoTopology"            ] = NTSysTree2s("CategoryReduction_JET_Pileup_RhoTopology__1up"                      , "CategoryReduction_JET_Pileup_RhoTopology__1down"                      , "Jets"   , "40", "Jet Pileup RhoTopology"            , False)
SYS_TREES_TWOSIDED["Jet_PunchThrough_MC16"             ] = NTSysTree2s("CategoryReduction_JET_PunchThrough_MC16__1up"                       , "CategoryReduction_JET_PunchThrough_MC16__1down"                       , "Jets"   , "40", "Jet PunchThrough MC16"             , False)
SYS_TREES_TWOSIDED["Jet_SingleParticle_HighPt"         ] = NTSysTree2s("CategoryReduction_JET_SingleParticle_HighPt__1up"                   , "CategoryReduction_JET_SingleParticle_HighPt__1down"                   , "Jets"   , "40", "Jet SingleParticle HighPt"         , False)
SYS_TREES_TWOSIDED["MET_SoftTrk_Scale"                 ] = NTSysTree2s("MET_SoftTrk_ScaleUp"                                                , "MET_SoftTrk_ScaleDown"                                                , "MET"    , "40", "MET SoftTrk Scale"                 , False)
SYS_TREES_TWOSIDED["MUON_ID"                           ] = NTSysTree2s("MUON_ID__1up"                                                       , "MUON_ID__1down"                                                       , "LeptonInstrum"   , "40", "Muon ID"                  , False)
SYS_TREES_TWOSIDED["MUON_MS"                           ] = NTSysTree2s("MUON_MS__1up"                                                       , "MUON_MS__1down"                                                       , "LeptonInstrum"   , "40", "Muon MS"                  , False)
SYS_TREES_TWOSIDED["MUON_SAGITTA_RESBIAS"              ] = NTSysTree2s("MUON_SAGITTA_RESBIAS__1up"                                          , "MUON_SAGITTA_RESBIAS__1down"                                          , "LeptonInstrum"   , "40", "Muon Sagitta Resbias"     , False)
SYS_TREES_TWOSIDED["MUON_SAGITTA_RHO"                  ] = NTSysTree2s("MUON_SAGITTA_RHO__1up"                                              , "MUON_SAGITTA_RHO__1down"                                              , "LeptonInstrum"   , "40", "Muon Sagitta Rho"         , False)
SYS_TREES_TWOSIDED["MUON_SCALE"                        ] = NTSysTree2s("MUON_SCALE__1up"                                                    , "MUON_SCALE__1down"                                                    , "LeptonInstrum"   , "40", "Muon Scale"               , False)

SYS_TREES_ONESIDED = OrderedDict()
SYS_TREES_ONESIDED["MET_SoftTrk_ResoPara"          ] = NTSysTree1s("MET_SoftTrk_ResoPara"                                    , "MET"   , "40", "MET SoftTrk ResoPara"      , False)
SYS_TREES_ONESIDED["MET_SoftTrk_ResoPerp"          ] = NTSysTree1s("MET_SoftTrk_ResoPerp"                                    , "MET"   , "40", "MET SoftTrk ResoPerp"      , False)
SYS_TREES_ONESIDED["Jet_JER_DataVsMC"              ] = NTSysTree1s("CategoryReduction_JET_JER_DataVsMC_MC16__1up"            , "JER"   , "40", "JER DataVsMC"              , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_1"               ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_1__1up"            , "JER"   , "40", "JER EffNP 1"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_2"               ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_2__1up"            , "JER"   , "40", "JER EffNP 2"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_3"               ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_3__1up"            , "JER"   , "40", "JER EffNP 3"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_4"               ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_4__1up"            , "JER"   , "40", "JER EffNP 4"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_5"               ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_5__1up"            , "JER"   , "40", "JER EffNP 5"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_6"               ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_6__1up"            , "JER"   , "40", "JER EffNP 6"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffectiveNP_7restTerm" ] = NTSysTree1s("CategoryReduction_JET_JER_EffectiveNP_7restTerm__1up"    , "JER"   , "40", "JER EffectiveNP 7restTerm" , False)
# fmt:  on

def _get_sys_weights():
    blocks = []
    for name, properties in SYS_WEIGHTS.items():
        block = '''\
        Systematic: "{name}"
          Category: "{category}"
          Title: "{title}"
          WeightUp: "{branch_up}"
          WeightDown: "{branch_down}"
          Type: HISTO
          Symmetrisation: TWOSIDED
          Samples: tW,ttbar\n'''.format(
              name=name,
              category=properties.category,
              title=properties.title,
              branch_up=properties.branch_up,
              branch_down=properties.branch_down
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


def _get_pdf_weights():
    blocks = []
    for name, properties in PDF_WEIGHTS.items():
        block = '''\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          Title: "{title}"
          WeightUp: "{branch}"
          ReferenceSample: ttbar_PDF
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: ttbar
          ReferenceSample: ttbar_PDF

        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          Title: "{title}"
          WeightUp: "{branch}"
          ReferenceSample: tW_PDF
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: tW
          ReferenceSample: tW_PDF\n'''.format(
              name=name,
              category=properties.category,
              title=properties.title,
              branch=properties.branch,
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


def _get_twosided_trees():
    blocks = []
    for name, properties in SYS_TREES_TWOSIDED.items():
        block = '''\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
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
          Title: "{title}"
          NtupleFilesUp: tW_DR_410648_FS_MC16a_{tree_up},tW_DR_410648_FS_MC16d_{tree_up},tW_DR_410648_FS_MC16e_{tree_up},tW_DR_410649_FS_MC16a_{tree_up},tW_DR_410649_FS_MC16d_{tree_up},tW_DR_410649_FS_MC16e_{tree_up}
          NtupleFilesDown: tW_DR_410648_FS_MC16a_{tree_down},tW_DR_410648_FS_MC16d_{tree_down},tW_DR_410648_FS_MC16e_{tree_down},tW_DR_410649_FS_MC16a_{tree_down},tW_DR_410649_FS_MC16d_{tree_down},tW_DR_410649_FS_MC16e_{tree_down}
          NtupleNameUp: "WtLoop_{tree_up}"
          NtupleNameDown: "WtLoop_{tree_down}"
          Samples: tW
          Type: HISTO
          Symmetrisation: TWOSIDED\n'''.format(
              name=name,
              category=properties.category,
              title=properties.title,
              tree_up=properties.branch_up,
              tree_down=properties.branch_down,
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


def _get_onesided_trees():
    blocks = []
    for name, properties in SYS_TREES_ONESIDED.items():
        block = '''\
        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          Title: "{title}"
          NtupleFilesUp: ttbar_410472_FS_MC16a_{tree_up},ttbar_410472_FS_MC16d_{tree_up},ttbar_410472_FS_MC16e_{tree_up}
          NtupleNameUp: "WtLoop_{tree_up}"
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: ttbar

        Systematic: "{name}"
          NuisanceParameter: "{name}"
          Category: "{category}"
          Title: "{title}"
          NtupleFilesUp: tW_DR_410648_FS_MC16a_{tree_up},tW_DR_410648_FS_MC16d_{tree_up},tW_DR_410648_FS_MC16e_{tree_up},tW_DR_410649_FS_MC16a_{tree_up},tW_DR_410649_FS_MC16d_{tree_up},tW_DR_410649_FS_MC16e_{tree_up}
          NtupleNameUp: "WtLoop_{tree_up}"
          Type: HISTO
          Symmetrisation: ONESIDED
          Samples: tW\n'''.format(
              name=name,
              title=properties.title,
              category=properties.category,
              tree_up=properties.branch
        )
        blocks.append(dedent(block))
    return "\n".join(blocks)


SAMPLE_BLOCKS = '''\
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
  MCweight: "weight_nominal"

Sample: "ttbar_PDF"
  Title: "ttbar_PDF"
  Type: GHOST
  NtupleFiles: ttbar_410472_FS_MC16a_nominal,ttbar_410472_FS_MC16e_nominal,ttbar_410472_FS_MC16d_nominal
  MCweight: "weight_sys_PDFset_90900"

Sample: "Data"
  HistoNameSuff: "_Data"
  Type: DATA
  Title: "Data"
  NtupleFiles: Data16_data16_Data_Data_nominal,Data18_data18_Data_Data_nominal,Data17_data17_Data_Data_nominal,Data15_data15_Data_Data_nominal
  MCweight: "weight_nominal"

Sample: "tW"
  NtupleFiles: tW_DR_410648_FS_MC16a_nominal,tW_DR_410648_FS_MC16d_nominal,tW_DR_410649_FS_MC16d_nominal,tW_DR_410648_FS_MC16e_nominal,tW_DR_410649_FS_MC16e_nominal,tW_DR_410649_FS_MC16a_nominal
  Title: "#it{tW}"
  TexTitle: "$tW$"
  FillColor: 862
  LineColor: 1
  Type: SIGNAL
  MCweight: "weight_nominal"

Sample: "ttbar"
  NtupleFiles: ttbar_410472_FS_MC16a_nominal,ttbar_410472_FS_MC16e_nominal,ttbar_410472_FS_MC16d_nominal
  Title: "#it{t#bar{t}}"
  TexTitle: "$t\bar{t}$"
  FillColor: 634
  LineColor: 1
  Type: BACKGROUND
  MCweight: "weight_nominal"

Sample: "Zjets"
  Title: "#it{Z}+jets"
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
'''

NORMFACTOR_BLOCKS = '''\
NormFactor: "SigXsecOverSM"
  Max: 2
  Nominal: 1
  Min: 0
  Samples: tW
  Title: "#it{#mu}_{#it{tW}}"

NormFactor: "mu_ttbar"
  Max: 1.5
  Nominal: 1
  Min: 0.5
  Samples: ttbar
  Title: "#it{#mu}_{#it{t#bar{t}}}"
'''

SYS_MINOR_BLOCKS = '''\
Systematic: "Norm_Diboson_1j1b"
  Type: OVERALL
  Title: "Norm Diboson 1j1b"
  Regions: reg1j1b
  Samples: Diboson
  OverallUp: 0.22
  OverallDown: -0.22
  Category: "Norms"

Systematic: "Norm_Diboson_2j1b"
  Type: OVERALL
  Title: "Norm Diboson 2j1b"
  Regions: reg2j1b
  Samples: Diboson
  OverallUp: 0.22
  OverallDown: -0.22
  Category: "Norms"

Systematic: "Norm_Diboson_2j2b"
  Type: OVERALL
  Title: "Norm Diboson 2j2b"
  Regions: reg2j2b
  Samples: Diboson
  OverallUp: 0.13
  OverallDown: -0.13
  Category: "Norms"

Systematic: "Norm_Zjets_1j1b"
  Type: OVERALL
  Title: "Norm Zjets 1j1b"
  Regions: reg1j1b
  Samples: Zjets
  OverallUp: 0.11
  OverallDown: -0.11
  Category: "Norms"

Systematic: "Norm_Zjets_2j1b"
  Type: OVERALL
  Title: "Norm Zjets 2j1b"
  Regions: reg2j1b
  Samples: Zjets
  OverallUp: 0.11
  OverallDown: -0.11
  Category: "Norms"

Systematic: "Norm_Zjets_2j2b"
  Type: OVERALL
  Title: "Norm Zjets 2j2b"
  Regions: reg2j2b
  Samples: Zjets
  OverallUp: 0.17
  OverallDown: -0.17
  Category: "Norms"

Systematic: "Norm_MCNP_1j1b"
  Type: OVERALL
  Title: "Norm MCNP 1j1b"
  Regions: reg1j1b
  Samples: MCNP
  OverallUp: 0.5
  OverallDown: -0.5
  Category: "Norms"

Systematic: "Norm_MCNP_2j1b"
  Type: OVERALL
  Title: "Norm MCNP 2j1b"
  Regions: reg2j1b
  Samples: MCNP
  OverallUp: 0.5
  OverallDown: -0.5
  Category: "Norms"

Systematic: "Norm_MCNP_2j2b"
  Type: OVERALL
  Title: "Norm MCNP 2j2b"
  Regions: reg2j2b
  Samples: MCNP
  OverallUp: 0.5
  OverallDown: -0.5
  Category: "Norms"

Systematic: "Lumi"
  OverallDown: -0.017
  Category: Instrumental
  OverallUp: 0.017
  Title: "Lumi"
  Samples: tW,ttbar
  Type: OVERALL
'''

SYS_WEIGHT_BLOCKS = _get_sys_weights()
SYS_PDF_WEIGHT_BLOCKS = _get_pdf_weights()
SYS_TWOSIDED_TREE_BLOCKS = _get_twosided_trees()
SYS_ONESIDED_TREE_BLOCKS = _get_onesided_trees()


def tW_shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b):
    overall, m1j1b, m2j1b, m2j2b = norm_uncertainties_tW(
        ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b
    )
    return dedent(
        """\
    Systematic: "tW_PS_norm"
      Category: "Modeling"
      Title: "tW Parton Shower Norm"
      Type: OVERALL
      OverallUp: {0}
      OverallDown: -{0}
      Samples: tW

    Systematic: "tW_PS_migration"
      Category: "Modeling"
      Title: "tW Parton Shower Migration"
      NuisanceParameter: "tW_PS_migration"
      Type: OVERALL
      OverallUp: {1}
      OverallDown: -{1}
      Samples: tW
      Regions: reg1j1b

    Systematic: "tW_PS_migration"
      Category: "Modeling"
      Title: "tW Parton Shower Migration"
      NuisanceParameter: "tW_PS_migration"
      Type: OVERALL
      OverallUp: {2}
      OverallDown: -{2}
      Samples: tW
      Regions: reg2j1b

    Systematic: "tW_PS_migration"
      Category: "Modeling"
      Title: "tW Parton Shower Migration"
      NuisanceParameter: "tW_PS_migration"
      Type: OVERALL
      OverallUp: {3}
      OverallDown: -{3}
      Samples: tW
      Regions: reg2j2b""".format(
            overall, m1j1b, m2j1b, m2j2b
        )
    )


def ttbar_shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b):
    overall, m1j1b, m2j1b, m2j2b = norm_uncertainties_ttbar(
        ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b
    )
    return dedent(
        """\
    Systematic: "ttbar_PS_norm"
      Category: "Modeling"
      Title: "ttbar Parton Shower Norm"
      Type: OVERALL
      OverallUp: {0}
      OverallDown: -{0}
      Samples: ttbar

    Systematic: "ttbar_PS_migration"
      Category: "Modeling"
      Title: "ttbar Parton Shower Migration"
      NuisanceParameter: "ttbar_PS_migration"
      Type: OVERALL
      OverallUp: {1}
      OverallDown: -{1}
      Samples: ttbar
      Regions: reg1j1b

    Systematic: "ttbar_PS_migration"
      Category: "Modeling"
      Title: "ttbar Parton Shower Migration"
      NuisanceParameter: "ttbar_PS_migration"
      Type: OVERALL
      OverallUp: {2}
      OverallDown: -{2}
      Samples: ttbar
      Regions: reg2j1b

    Systematic: "ttbar_PS_migration"
      Category: "Modeling"
      Title: "ttbar Parton Shower Migration"
      NuisanceParameter: "ttbar_PS_migration"
      Type: OVERALL
      OverallUp: {3}
      OverallDown: -{3}
      Samples: ttbar
      Regions: reg2j2b""".format(
            overall, m1j1b, m2j1b, m2j2b
        )
    )


def shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b):
    tW = tW_shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b)
    ttbar = ttbar_shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b)
    return "{}\n\n{}".format(tW, ttbar)


def modeling_blocks(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b):
    shower_norm_blocks = shower_norms(ntup_dir, sel_1j1b, sel_2j1b, sel_2j2b)
    return '''\
Systematic: "tW_DRDS"
  Category: "Modeling"
  Symmetrisation: ONESIDED
  Samples: tW
  Title: "tW DR vs DS"
  Type: HISTO
  NtupleFilesUp: tW_DS_410657_FS_MC16d_nominal,tW_DS_410657_FS_MC16e_nominal,tW_DS_410657_FS_MC16a_nominal,tW_DS_410656_FS_MC16e_nominal,tW_DS_410656_FS_MC16a_nominal,tW_DS_410656_FS_MC16d_nominal

{0}

Systematic: "tW_PS_1j1b"
  Category: "Modeling"
  Title: "tW Parton Shower Shape 1j1b"
  ReferenceSample: tW_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: tW
  Type: HISTO
  Regions: reg1j1b
  NtupleFilesUp: tW_DR_411038_AFII_MC16a_nominal,tW_DR_411038_AFII_MC16d_nominal,tW_DR_411039_AFII_MC16a_nominal,tW_DR_411039_AFII_MC16d_nominal,tW_DR_411038_AFII_MC16e_nominal,tW_DR_411039_AFII_MC16e_nominal

Systematic: "tW_PS_2j1b"
  Category: "Modeling"
  Title: "tW Parton Shower Shape 2j1b"
  ReferenceSample: tW_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: tW
  Type: HISTO
  Regions: reg2j1b
  NtupleFilesUp: tW_DR_411038_AFII_MC16a_nominal,tW_DR_411038_AFII_MC16d_nominal,tW_DR_411039_AFII_MC16a_nominal,tW_DR_411039_AFII_MC16d_nominal,tW_DR_411038_AFII_MC16e_nominal,tW_DR_411039_AFII_MC16e_nominal

Systematic: "tW_PS_2j2b"
  Category: "Modeling"
  Title: "tW Parton Shower Shape 2j2b"
  ReferenceSample: tW_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: tW
  Type: HISTO
  Regions: reg2j2b
  NtupleFilesUp: tW_DR_411038_AFII_MC16a_nominal,tW_DR_411038_AFII_MC16d_nominal,tW_DR_411039_AFII_MC16a_nominal,tW_DR_411039_AFII_MC16d_nominal,tW_DR_411038_AFII_MC16e_nominal,tW_DR_411039_AFII_MC16e_nominal

Systematic: "ttbar_PS_1j1b"
  Category: "Modeling"
  Title: "ttbar Parton Shower Shape 1j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b
  NtupleFilesUp: ttbar_411234_AFII_MC16a_nominal,ttbar_411234_AFII_MC16d_nominal,ttbar_411234_AFII_MC16e_nominal

Systematic: "ttbar_PS_2j1b"
  Category: "Modeling"
  Title: "ttbar Parton Shower Shape 2j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b
  NtupleFilesUp: ttbar_411234_AFII_MC16a_nominal,ttbar_411234_AFII_MC16d_nominal,ttbar_411234_AFII_MC16e_nominal

Systematic: "ttbar_PS_2j2b"
  Category: "Modeling"
  Title: "ttbar Parton Shower Shape 2j2b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  DropNorm: all
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b
  NtupleFilesUp: ttbar_411234_AFII_MC16a_nominal,ttbar_411234_AFII_MC16d_nominal,ttbar_411234_AFII_MC16e_nominal

Systematic: "tW_AR_ISR_scale_muR_1j1b"
  Category: "Modeling"
  Title: "tW ISR Scale muR Variation 1j1b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_ISR_scale_muR_2j1b"
  Category: "Modeling"
  Title: "tW ISR Scale muR Variation 2j1b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_ISR_scale_muR_2j2b"
  Category: "Modeling"
  Title: "tW ISR Scale muR Variation 2j2b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "tW_AR_ISR_scale_muF_1j1b"
  Category: "Modeling"
  Title: "tW ISR Scale muF Variation 1j1b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_ISR_scale_muF_2j1b"
  Category: "Modeling"
  Title: "tW ISR Scale muF Variation 2j1b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_ISR_scale_muF_2j2b"
  Category: "Modeling"
  Title: "tW ISR Scale muF Variation 2j2b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "tW_AR_ISR_A14_1j1b"
  Category: "Modeling"
  Title: "tW ISR A14 1j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_ISR_A14_2j1b"
  Category: "Modeling"
  Title: "tW ISR A14 2j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_ISR_A14_2j2b"
  Category: "Modeling"
  Title: "tW ISR A14 2j2b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "tW_AR_FSR_1j1b"
  Category: "Modeling"
  Title: "tW FSR 1j1b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg1j1b

Systematic: "tW_AR_FSR_2j1b"
  Category: "Modeling"
  Title: "tW FSR 2j1b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j1b

Systematic: "tW_AR_FSR_2j2b"
  Category: "Modeling"
  Title: "tW FSR 2j2b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: tW
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_ISR_scale_muR_1j1b"
  Category: "Modeling"
  Title: "ttbar ISR Scale muR Variation 1j1b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_ISR_scale_muR_2j1b"
  Category: "Modeling"
  Title: "ttbar ISR Scale muR Variation 2j1b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_ISR_scale_muR_2j2b"
  Category: "Modeling"
  Title: "ttbar ISR Scale muR Variation 2j2b"
  WeightUp: "weight_sys_scale_muR_20"
  WeightDown: "weight_sys_scale_muR_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_ISR_scale_muF_1j1b"
  Category: "Modeling"
  Title: "ttbar ISR Scale muF Variation 1j1b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_ISR_scale_muF_2j1b"
  Category: "Modeling"
  Title: "ttbar ISR Scale muF Variation 2j1b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_ISR_scale_muF_2j2b"
  Category: "Modeling"
  Title: "ttbar ISR Scale muF Variation 2j2b"
  WeightUp: "weight_sys_scale_muF_20"
  WeightDown: "weight_sys_scale_muF_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_ISR_A14_1j1b"
  Category: "Modeling"
  Title: "ttbar ISR A14 1j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_ISR_A14_2j1b"
  Category: "Modeling"
  Title: "ttbar ISR A14 2j1b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_ISR_A14_2j2b"
  Category: "Modeling"
  Title: "ttbar ISR A14 2j2b"
  WeightUp: "weight_sys_isr_alphaS_Var3cUp"
  WeightDown: "weight_sys_isr_alphaS_Var3cDown"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_AR_FSR_1j1b"
  Category: "Modeling"
  Title: "ttbar FSR 1j1b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_AR_FSR_2j1b"
  Category: "Modeling"
  Title: "ttbar FSR 2j1b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_AR_FSR_2j2b"
  Category: "Modeling"
  Title: "ttbar FSR 2j2b"
  WeightUp: "weight_sys_fsr_muR_20"
  WeightDown: "weight_sys_fsr_muR_05"
  Symmetrisation: TWOSIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b

Systematic: "ttbar_hdamp_1j1b"
  Category: "Modeling"
  Title: "ttbar hdamp 1j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b
  NtupleFilesUp: ttbar_410482_AFII_MC16a_nominal,ttbar_410482_AFII_MC16d_nominal,ttbar_410482_AFII_MC16e_nominal

Systematic: "ttbar_hdamp_2j1b"
  Category: "Modeling"
  Title: "ttbar hdamp 2j1b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b
  NtupleFilesUp: ttbar_410482_AFII_MC16a_nominal,ttbar_410482_AFII_MC16d_nominal,ttbar_410482_AFII_MC16e_nominal

Systematic: "ttbar_hdamp_2j2b"
  Category: "Modeling"
  Title: "ttbar hdamp 2j2b"
  ReferenceSample: ttbar_AFII
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b
  NtupleFilesUp: ttbar_410482_AFII_MC16a_nominal,ttbar_410482_AFII_MC16d_nominal,ttbar_410482_AFII_MC16e_nominal

Systematic: "ttbar_ptreweight_1j1b"
  Category: "Modeling"
  Title: "ttbar pt reweight 1j1b"
  WeightUp: "weight_sys_noreweight"
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg1j1b

Systematic: "ttbar_ptreweight_2j1b"
  Category: "Modeling"
  Title: "ttbar pt reweight 2j1b"
  WeightUp: "weight_sys_noreweight"
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j1b

Systematic: "ttbar_ptreweight_2j2b"
  Category: "Modeling"
  Title: "ttbar pt reweight 2j2b"
  WeightUp: "weight_sys_noreweight"
  Symmetrisation: ONESIDED
  Samples: ttbar
  Type: HISTO
  Regions: reg2j2b
'''.format(shower_norm_blocks)
