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

SYS_WEIGHTS["B_ev_B_00"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_0_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_0_down", "WeightFT_B", "40", "b-tag eigenv B00", False)
SYS_WEIGHTS["B_ev_B_01"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_1_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_1_down", "WeightFT_B", "40", "b-tag eigenv B01", False)
SYS_WEIGHTS["B_ev_B_02"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_2_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_2_down", "WeightFT_B", "40", "b-tag eigenv B02", False)
SYS_WEIGHTS["B_ev_B_03"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_3_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_3_down", "WeightFT_B", "40", "b-tag eigenv B03", False)
SYS_WEIGHTS["B_ev_B_04"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_4_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_4_down", "WeightFT_B", "40", "b-tag eigenv B04", False)
SYS_WEIGHTS["B_ev_B_05"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_5_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_5_down", "WeightFT_B", "40", "b-tag eigenv B05", False)
SYS_WEIGHTS["B_ev_B_06"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_6_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_6_down", "WeightFT_B", "40", "b-tag eigenv B06", False)
SYS_WEIGHTS["B_ev_B_07"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_7_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_7_down", "WeightFT_B", "40", "b-tag eigenv B07", False)
SYS_WEIGHTS["B_ev_B_08"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_8_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_8_down", "WeightFT_B", "40", "b-tag eigenv B08", False)
SYS_WEIGHTS["B_ev_B_09"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_9_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_9_down", "WeightFT_B", "40", "b-tag eigenv B09", False)
SYS_WEIGHTS["B_ev_B_10"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_10_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_10_down", "WeightFT_B", "40", "b-tag eigenv B10", False)
SYS_WEIGHTS["B_ev_B_11"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_11_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_11_down", "WeightFT_B", "40", "b-tag eigenv B11", False)
SYS_WEIGHTS["B_ev_B_12"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_12_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_12_down", "WeightFT_B", "40", "b-tag eigenv B12", False)
SYS_WEIGHTS["B_ev_B_13"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_13_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_13_down", "WeightFT_B", "40", "b-tag eigenv B13", False)
SYS_WEIGHTS["B_ev_B_14"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_14_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_14_down", "WeightFT_B", "40", "b-tag eigenv B14", False)
SYS_WEIGHTS["B_ev_B_15"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_15_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_15_down", "WeightFT_B", "40", "b-tag eigenv B15", False)
SYS_WEIGHTS["B_ev_B_16"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_16_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_16_down", "WeightFT_B", "40", "b-tag eigenv B16", False)
SYS_WEIGHTS["B_ev_B_17"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_17_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_17_down", "WeightFT_B", "40", "b-tag eigenv B17", False)
SYS_WEIGHTS["B_ev_B_18"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_18_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_18_down", "WeightFT_B", "40", "b-tag eigenv B18", False)
SYS_WEIGHTS["B_ev_B_19"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_19_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_19_down", "WeightFT_B", "40", "b-tag eigenv B19", False)
SYS_WEIGHTS["B_ev_B_20"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_20_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_20_down", "WeightFT_B", "40", "b-tag eigenv B20", False)
SYS_WEIGHTS["B_ev_B_21"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_21_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_21_down", "WeightFT_B", "40", "b-tag eigenv B21", False)
SYS_WEIGHTS["B_ev_B_22"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_22_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_22_down", "WeightFT_B", "40", "b-tag eigenv B22", False)
SYS_WEIGHTS["B_ev_B_23"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_23_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_23_down", "WeightFT_B", "40", "b-tag eigenv B23", False)
SYS_WEIGHTS["B_ev_B_24"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_24_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_24_down", "WeightFT_B", "40", "b-tag eigenv B24", False)
SYS_WEIGHTS["B_ev_B_25"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_25_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_25_down", "WeightFT_B", "40", "b-tag eigenv B25", False)
SYS_WEIGHTS["B_ev_B_26"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_26_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_26_down", "WeightFT_B", "40", "b-tag eigenv B26", False)
SYS_WEIGHTS["B_ev_B_27"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_27_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_27_down", "WeightFT_B", "40", "b-tag eigenv B27", False)
SYS_WEIGHTS["B_ev_B_28"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_28_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_28_down", "WeightFT_B", "40", "b-tag eigenv B28", False)
SYS_WEIGHTS["B_ev_B_29"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_29_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_29_down", "WeightFT_B", "40", "b-tag eigenv B29", False)
SYS_WEIGHTS["B_ev_B_30"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_30_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_30_down", "WeightFT_B", "40", "b-tag eigenv B30", False)
SYS_WEIGHTS["B_ev_B_31"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_31_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_31_down", "WeightFT_B", "40", "b-tag eigenv B31", False)
SYS_WEIGHTS["B_ev_B_32"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_32_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_32_down", "WeightFT_B", "40", "b-tag eigenv B32", False)
SYS_WEIGHTS["B_ev_B_33"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_33_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_33_down", "WeightFT_B", "40", "b-tag eigenv B33", False)
SYS_WEIGHTS["B_ev_B_34"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_34_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_34_down", "WeightFT_B", "40", "b-tag eigenv B34", False)
SYS_WEIGHTS["B_ev_B_35"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_35_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_35_down", "WeightFT_B", "40", "b-tag eigenv B35", False)
SYS_WEIGHTS["B_ev_B_36"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_36_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_36_down", "WeightFT_B", "40", "b-tag eigenv B36", False)
SYS_WEIGHTS["B_ev_B_37"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_37_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_37_down", "WeightFT_B", "40", "b-tag eigenv B37", False)
SYS_WEIGHTS["B_ev_B_38"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_38_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_38_down", "WeightFT_B", "40", "b-tag eigenv B38", False)
SYS_WEIGHTS["B_ev_B_39"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_39_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_39_down", "WeightFT_B", "40", "b-tag eigenv B39", False)
SYS_WEIGHTS["B_ev_B_40"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_40_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_40_down", "WeightFT_B", "40", "b-tag eigenv B40", False)
SYS_WEIGHTS["B_ev_B_41"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_41_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_41_down", "WeightFT_B", "40", "b-tag eigenv B41", False)
SYS_WEIGHTS["B_ev_B_42"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_42_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_42_down", "WeightFT_B", "40", "b-tag eigenv B42", False)
SYS_WEIGHTS["B_ev_B_43"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_43_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_43_down", "WeightFT_B", "40", "b-tag eigenv B43", False)
SYS_WEIGHTS["B_ev_B_44"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_44_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_B_44_down", "WeightFT_B", "40", "b-tag eigenv B44", False)

SYS_WEIGHTS["B_ev_C_00"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_0_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_0_down", "WeightFT_C", "40", "b-tag eigenv C0", False)
SYS_WEIGHTS["B_ev_C_01"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_1_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_1_down", "WeightFT_C", "40", "b-tag eigenv C1", False)
SYS_WEIGHTS["B_ev_C_02"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_2_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_2_down", "WeightFT_C", "40", "b-tag eigenv C2", True)
SYS_WEIGHTS["B_ev_C_03"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_3_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_3_down", "WeightFT_C", "40", "b-tag eigenv C3", True)
SYS_WEIGHTS["B_ev_C_04"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_4_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_4_down", "WeightFT_C", "40", "b-tag eigenv C4", True)
SYS_WEIGHTS["B_ev_C_05"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_5_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_5_down", "WeightFT_C", "40", "b-tag eigenv C5", True)
SYS_WEIGHTS["B_ev_C_06"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_6_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_6_down", "WeightFT_C", "40", "b-tag eigenv C6", True)
SYS_WEIGHTS["B_ev_C_07"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_7_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_7_down", "WeightFT_C", "40", "b-tag eigenv C7", True)
SYS_WEIGHTS["B_ev_C_08"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_8_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_8_down", "WeightFT_C", "40", "b-tag eigenv C8", True)
SYS_WEIGHTS["B_ev_C_09"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_9_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_9_down", "WeightFT_C", "40", "b-tag eigenv C9", True)
SYS_WEIGHTS["B_ev_C_10"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_10_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_10_down", "WeightFT_C", "40", "b-tag eigenv C10", True)
SYS_WEIGHTS["B_ev_C_11"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_11_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_11_down", "WeightFT_C", "40", "b-tag eigenv C11", True)
SYS_WEIGHTS["B_ev_C_12"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_12_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_12_down", "WeightFT_C", "40", "b-tag eigenv C12", True)
SYS_WEIGHTS["B_ev_C_13"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_13_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_13_down", "WeightFT_C", "40", "b-tag eigenv C13", True)
SYS_WEIGHTS["B_ev_C_14"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_14_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_14_down", "WeightFT_C", "40", "b-tag eigenv C14", True)
SYS_WEIGHTS["B_ev_C_15"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_15_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_15_down", "WeightFT_C", "40", "b-tag eigenv C15", True)
SYS_WEIGHTS["B_ev_C_16"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_16_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_16_down", "WeightFT_C", "40", "b-tag eigenv C16", True)
SYS_WEIGHTS["B_ev_C_17"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_17_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_17_down", "WeightFT_C", "40", "b-tag eigenv C17", True)
SYS_WEIGHTS["B_ev_C_18"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_18_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_18_down", "WeightFT_C", "40", "b-tag eigenv C18", True)
SYS_WEIGHTS["B_ev_C_19"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_19_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_C_19_down", "WeightFT_C", "40", "b-tag eigenv C19", True)

SYS_WEIGHTS["B_ev_L_00"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_0_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_0_down", "WeightFT_L", "40", "b-tag eigenv L0", False)
SYS_WEIGHTS["B_ev_L_01"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_1_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_1_down", "WeightFT_L", "40", "b-tag eigenv L1", False)
SYS_WEIGHTS["B_ev_L_02"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_2_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_2_down", "WeightFT_L", "40", "b-tag eigenv L2", False)
SYS_WEIGHTS["B_ev_L_03"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_3_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_3_down", "WeightFT_L", "40", "b-tag eigenv L3", False)
SYS_WEIGHTS["B_ev_L_04"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_4_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_4_down", "WeightFT_L", "40", "b-tag eigenv L4", False)
SYS_WEIGHTS["B_ev_L_05"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_5_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_5_down", "WeightFT_L", "40", "b-tag eigenv L5", False)
SYS_WEIGHTS["B_ev_L_06"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_6_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_6_down", "WeightFT_L", "40", "b-tag eigenv L6", False)
SYS_WEIGHTS["B_ev_L_07"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_7_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_7_down", "WeightFT_L", "40", "b-tag eigenv L7", False)
SYS_WEIGHTS["B_ev_L_08"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_8_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_8_down", "WeightFT_L", "40", "b-tag eigenv L8", False)
SYS_WEIGHTS["B_ev_L_09"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_9_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_9_down", "WeightFT_L", "40", "b-tag eigenv L9", False)
SYS_WEIGHTS["B_ev_L_10"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_10_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_10_down", "WeightFT_L", "40", "b-tag eigenv L10", False)
SYS_WEIGHTS["B_ev_L_11"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_11_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_11_down", "WeightFT_L", "40", "b-tag eigenv L11", False)
SYS_WEIGHTS["B_ev_L_12"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_12_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_12_down", "WeightFT_L", "40", "b-tag eigenv L12", False)
SYS_WEIGHTS["B_ev_L_13"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_13_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_13_down", "WeightFT_L", "40", "b-tag eigenv L13", False)
SYS_WEIGHTS["B_ev_L_14"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_14_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_14_down", "WeightFT_L", "40", "b-tag eigenv L14", False)
SYS_WEIGHTS["B_ev_L_15"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_15_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_15_down", "WeightFT_L", "40", "b-tag eigenv L15", False)
SYS_WEIGHTS["B_ev_L_16"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_16_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_16_down", "WeightFT_L", "40", "b-tag eigenv L16", False)
SYS_WEIGHTS["B_ev_L_17"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_17_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_17_down", "WeightFT_L", "40", "b-tag eigenv L17", False)
SYS_WEIGHTS["B_ev_L_18"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_18_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_18_down", "WeightFT_L", "40", "b-tag eigenv L18", False)
SYS_WEIGHTS["B_ev_L_19"] = NTSysWeight("weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_19_up", "weight_sys_bTagSF_MV2c10_Continuous_eigenvars_Light_19_down", "WeightFT_L", "40", "b-tag eigenv L19", False)


PDF_WEIGHTS = OrderedDict()
#PDF_WEIGHTS["PDFset90900"] = NTSysPDF("weight_sys_PDFset_90900", "PDF", "40", "PDF 90900", False)
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
SYS_TREES_TWOSIDED["EG_RES_ALL"                        ] = NTSysTree2s("EG_RESOLUTION_ALL__1up"                                               , "EG_RESOLUTION_ALL__1down"                                               , "LeptonInstrum" , "40", "EGamma Resolution"                 , False)
SYS_TREES_TWOSIDED["EG_SCALE_ALL"                      ] = NTSysTree2s("EG_SCALE_ALL__1up"                                                    , "EG_SCALE_ALL__1down"                                                    , "LeptonInstrum" , "40", "EGamma Scale"                      , False)
SYS_TREES_TWOSIDED["Jet_BJES_Response"                 ] = NTSysTree2s("JET_CategoryReduction_JET_BJES_Response__1up"                         , "JET_CategoryReduction_JET_BJES_Response__1down"                         , "Jets"   , "40", "Jet BJES Response"                 , False)
SYS_TREES_TWOSIDED["Jet_EffectiveNP_Detector1"         ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Detector1__1up"                 , "JET_CategoryReduction_JET_EffectiveNP_Detector1__1down"                 , "Jets"   , "40", "Jet EffectiveNP Detector1"         , False)
SYS_TREES_TWOSIDED["Jet_EffectiveNP_Detector2"         ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Detector2__1up"                 , "JET_CategoryReduction_JET_EffectiveNP_Detector2__1down"                 , "Jets"   , "40", "Jet EffectiveNP Detector2"         , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Mixed1"                  ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Mixed1__1up"                    , "JET_CategoryReduction_JET_EffectiveNP_Mixed1__1down"                    , "Jets"   , "40", "Jet EffNP Mixed1"                  , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Mixed2"                  ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Mixed2__1up"                    , "JET_CategoryReduction_JET_EffectiveNP_Mixed2__1down"                    , "Jets"   , "40", "Jet EffNP Mixed2"                  , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Mixed3"                  ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Mixed3__1up"                    , "JET_CategoryReduction_JET_EffectiveNP_Mixed3__1down"                    , "Jets"   , "40", "Jet EffNP Mixed3"                  , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling1"              ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Modelling1__1up"                , "JET_CategoryReduction_JET_EffectiveNP_Modelling1__1down"                , "Jets"   , "40", "Jet EffNP Modelling1"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling2"              ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Modelling2__1up"                , "JET_CategoryReduction_JET_EffectiveNP_Modelling2__1down"                , "Jets"   , "40", "Jet EffNP Modelling2"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling3"              ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Modelling3__1up"                , "JET_CategoryReduction_JET_EffectiveNP_Modelling3__1down"                , "Jets"   , "40", "Jet EffNP Modelling3"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Modelling4"              ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Modelling4__1up"                , "JET_CategoryReduction_JET_EffectiveNP_Modelling4__1down"                , "Jets"   , "40", "Jet EffNP Modelling4"              , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical1"            ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Statistical1__1up"              , "JET_CategoryReduction_JET_EffectiveNP_Statistical1__1down"              , "Jets"   , "40", "Jet EffNP Statistical1"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical2"            ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Statistical2__1up"              , "JET_CategoryReduction_JET_EffectiveNP_Statistical2__1down"              , "Jets"   , "40", "Jet EffNP Statistical2"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical3"            ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Statistical3__1up"              , "JET_CategoryReduction_JET_EffectiveNP_Statistical3__1down"              , "Jets"   , "40", "Jet EffNP Statistical3"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical4"            ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Statistical4__1up"              , "JET_CategoryReduction_JET_EffectiveNP_Statistical4__1down"              , "Jets"   , "40", "Jet EffNP Statistical4"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical5"            ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Statistical5__1up"              , "JET_CategoryReduction_JET_EffectiveNP_Statistical5__1down"              , "Jets"   , "40", "Jet EffNP Statistical5"            , False)
SYS_TREES_TWOSIDED["Jet_EffNP_Statistical6"            ] = NTSysTree2s("JET_CategoryReduction_JET_EffectiveNP_Statistical6__1up"              , "JET_CategoryReduction_JET_EffectiveNP_Statistical6__1down"              , "Jets"   , "40", "Jet EffNP Statistical6"            , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_Modelling"         ] = NTSysTree2s("JET_CategoryReduction_JET_EtaIntercalibration_Modelling__1up"         , "JET_CategoryReduction_JET_EtaIntercalibration_Modelling__1down"         , "Jets"   , "40", "Jet EtaIntercal Modelling"         , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_highE"  ] = NTSysTree2s("JET_CategoryReduction_JET_EtaIntercalibration_NonClosure_highE__1up"  , "JET_CategoryReduction_JET_EtaIntercalibration_NonClosure_highE__1down"  , "Jets"   , "40", "Jet EtaIntercal NonClosure highE"  , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_negEta" ] = NTSysTree2s("JET_CategoryReduction_JET_EtaIntercalibration_NonClosure_negEta__1up" , "JET_CategoryReduction_JET_EtaIntercalibration_NonClosure_negEta__1down" , "Jets"   , "40", "Jet EtaIntercal NonClosure negEta" , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_NonClosure_posEta" ] = NTSysTree2s("JET_CategoryReduction_JET_EtaIntercalibration_NonClosure_posEta__1up" , "JET_CategoryReduction_JET_EtaIntercalibration_NonClosure_posEta__1down" , "Jets"   , "40", "Jet EtaIntercal NonClosure posEta" , False)
SYS_TREES_TWOSIDED["Jet_EtaIntercal_TotalStat"         ] = NTSysTree2s("JET_CategoryReduction_JET_EtaIntercalibration_TotalStat__1up"         , "JET_CategoryReduction_JET_EtaIntercalibration_TotalStat__1down"         , "Jets"   , "40", "Jet EtaIntercal TotalStat"         , False)
SYS_TREES_TWOSIDED["Jet_Flavor_Composition"            ] = NTSysTree2s("JET_CategoryReduction_JET_Flavor_Composition__1up"                    , "JET_CategoryReduction_JET_Flavor_Composition__1down"                    , "Jets"   , "40", "Jet Flavor Composition"            , False)
SYS_TREES_TWOSIDED["Jet_Flavor_Response"               ] = NTSysTree2s("JET_CategoryReduction_JET_Flavor_Response__1up"                       , "JET_CategoryReduction_JET_Flavor_Response__1down"                       , "Jets"   , "40", "Jet Flavor Response"               , False)
SYS_TREES_TWOSIDED["Jet_Pileup_OffsetMu"               ] = NTSysTree2s("JET_CategoryReduction_JET_Pileup_OffsetMu__1up"                       , "JET_CategoryReduction_JET_Pileup_OffsetMu__1down"                       , "Jets"   , "40", "Jet Pileup OffsetMu"               , False)
SYS_TREES_TWOSIDED["Jet_Pileup_OffsetNPV"              ] = NTSysTree2s("JET_CategoryReduction_JET_Pileup_OffsetNPV__1up"                      , "JET_CategoryReduction_JET_Pileup_OffsetNPV__1down"                      , "Jets"   , "40", "Jet Pileup OffsetNPV"              , False)
SYS_TREES_TWOSIDED["Jet_Pileup_PtTerm"                 ] = NTSysTree2s("JET_CategoryReduction_JET_Pileup_PtTerm__1up"                         , "JET_CategoryReduction_JET_Pileup_PtTerm__1down"                         , "Jets"   , "40", "Jet Pileup PtTerm"                 , False)
SYS_TREES_TWOSIDED["Jet_Pileup_RhoTopology"            ] = NTSysTree2s("JET_CategoryReduction_JET_Pileup_RhoTopology__1up"                    , "JET_CategoryReduction_JET_Pileup_RhoTopology__1down"                    , "Jets"   , "40", "Jet Pileup RhoTopology"            , False)
SYS_TREES_TWOSIDED["Jet_PunchThrough_MC16"             ] = NTSysTree2s("JET_CategoryReduction_JET_PunchThrough_MC16__1up"                     , "JET_CategoryReduction_JET_PunchThrough_MC16__1down"                     , "Jets"   , "40", "Jet PunchThrough MC16"             , False)
SYS_TREES_TWOSIDED["Jet_SingleParticle_HighPt"         ] = NTSysTree2s("JET_CategoryReduction_JET_SingleParticle_HighPt__1up"                 , "JET_CategoryReduction_JET_SingleParticle_HighPt__1down"                 , "Jets"   , "40", "Jet SingleParticle HighPt"         , False)
SYS_TREES_TWOSIDED["MET_SoftTrk_Scale"                 ] = NTSysTree2s("MET_SoftTrk_ScaleUp"                                                  , "MET_SoftTrk_ScaleDown"                                                  , "MET"    , "40", "MET SoftTrk Scale"                 , False)
SYS_TREES_TWOSIDED["MUON_ID"                           ] = NTSysTree2s("MUON_ID__1up"                                                         , "MUON_ID__1down"                                                         , "LeptonInstrum"   , "40", "Muon ID"                           , False)
SYS_TREES_TWOSIDED["MUON_MS"                           ] = NTSysTree2s("MUON_MS__1up"                                                         , "MUON_MS__1down"                                                         , "LeptonInstrum"   , "40", "Muon MS"                           , False)
SYS_TREES_TWOSIDED["MUON_SAGITTA_RESBIAS"              ] = NTSysTree2s("MUON_SAGITTA_RESBIAS__1up"                                            , "MUON_SAGITTA_RESBIAS__1down"                                            , "LeptonInstrum"   , "40", "Muon Sagitta Resbias"              , False)
SYS_TREES_TWOSIDED["MUON_SAGITTA_RHO"                  ] = NTSysTree2s("MUON_SAGITTA_RHO__1up"                                                , "MUON_SAGITTA_RHO__1down"                                                , "LeptonInstrum"   , "40", "Muon Sagitta Rho"                  , False)
SYS_TREES_TWOSIDED["MUON_SCALE"                        ] = NTSysTree2s("MUON_SCALE__1up"                                                      , "MUON_SCALE__1down"                                                      , "LeptonInstrum"   , "40", "Muon Scale"                        , False)

SYS_TREES_ONESIDED = OrderedDict()
SYS_TREES_ONESIDED["MET_SoftTrk_ResoPara"          ] = NTSysTree1s("MET_SoftTrk_ResoPara"                                        , "MET"   , "40", "MET SoftTrk ResoPara"          , False)
SYS_TREES_ONESIDED["MET_SoftTrk_ResoPerp"          ] = NTSysTree1s("MET_SoftTrk_ResoPerp"                                        , "MET"   , "40", "MET SoftTrk ResoPerp"          , False)
SYS_TREES_ONESIDED["Jet_JER_DataVsMC"              ] = NTSysTree1s("JET_CategoryReduction_JET_JER_DataVsMC_MC16__1up"            , "JER"   , "40", "Jet JER DataVsMC"              , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_1"               ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_1__1up"            , "JER"   , "40", "Jet JER EffNP 1"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_2"               ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_2__1up"            , "JER"   , "40", "Jet JER EffNP 2"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_3"               ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_3__1up"            , "JER"   , "40", "Jet JER EffNP 3"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_4"               ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_4__1up"            , "JER"   , "40", "Jet JER EffNP 4"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_5"               ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_5__1up"            , "JER"   , "40", "Jet JER EffNP 5"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffNP_6"               ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_6__1up"            , "JER"   , "40", "Jet JER EffNP 6"               , False)
SYS_TREES_ONESIDED["Jet_JER_EffectiveNP_7restTerm" ] = NTSysTree1s("JET_CategoryReduction_JET_JER_EffectiveNP_7restTerm__1up"    , "JER"   , "40", "Jet JER EffectiveNP 7restTerm" , False)


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
  Samples: ttbar

Systematic: "{name}"
  NuisanceParameter: "{name}"
  Category: "{category}"
  Title: "{title}"
  NtupleFilesUp: tW_DR_410648_FS_MC16a_{tree_up},tW_DR_410648_FS_MC16d_{tree_up},tW_DR_410648_FS_MC16e_{tree_up},tW_DR_410649_FS_MC16a_{tree_up},tW_DR_410649_FS_MC16d_{tree_up},tW_DR_410649_FS_MC16e_{tree_up}
  NtupleNameUp: "WtLoop_{tree_up}"
  Type: HISTO
  Samples: tW'''.format(
      name=name,
      title=properties.title,
      category=properties.category,
      tree_up=properties.branch
  )
    print(block)
