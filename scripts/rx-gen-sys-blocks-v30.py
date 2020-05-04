#!/usr/bin/env python

from __future__ import print_function
from collections import OrderedDict, namedtuple


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


for name, properties in SYS_WEIGHTS.items():
    block = '''
Systematic: "{name}"
  Category: "{category}"
  Title: "{title}"
  WeightUp: "{branch_up}"
  WeightDown: "{branch_down}"
  Type: HISTO
  Symmetrisation: TWOSIDED
  Samples: tW,ttbar'''.format(
      name=name,
      category=properties.category,
      title=properties.title,
      branch_up=properties.branch_up,
      branch_down=properties.branch_down
  )
    print(block)

for name, properties in PDF_WEIGHTS.items():
    block = '''
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
  ReferenceSample: tW_PDF'''.format(
      name=name,
      category=properties.category,
      title=properties.title,
      branch=properties.branch,
  )
    print(block)

for name, properties in SYS_TREES_TWOSIDED.items():
    block = '''
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

Systematic: "{name}"
  NuisanceParameter: "{name}"
  Category: "{category}"
  Title: "{title}"
  NtupleFilesUp: tW_DR_410648_FS_MC16a_{tree_up},tW_DR_410648_FS_MC16d_{tree_up},tW_DR_410648_FS_MC16e_{tree_up},tW_DR_410649_FS_MC16a_{tree_up},tW_DR_410649_FS_MC16d_{tree_up},tW_DR_410649_FS_MC16e_{tree_up}
  NtupleFilesDown: tW_DR_410648_FS_MC16a_{tree_down},tW_DR_410648_FS_MC16d_{tree_down},tW_DR_410648_FS_MC16e_{tree_down},tW_DR_410649_FS_MC16a_{tree_down},tW_DR_410649_FS_MC16d_{tree_down},tW_DR_410649_FS_MC16e_{tree_down}
  NtupleNameUp: "WtLoop_{tree_up}"
  NtupleNameDown: "WtLoop_{tree_down}"
  Samples: tW
  Type: HISTO'''.format(
      name=name,
      category=properties.category,
      title=properties.title,
      tree_up=properties.branch_up,
      tree_down=properties.branch_down,
  )
    print(block)

for name, properties in SYS_TREES_ONESIDED.items():
    block = '''
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
  Samples: tW'''.format(
      name=name,
      title=properties.title,
      category=properties.category,
      tree_up=properties.branch
  )
    print(block)
