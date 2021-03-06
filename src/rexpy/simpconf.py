from pathlib import Path


##################################################
####### Default constants ########################
##################################################
ON_SPAR = Path("/atlasgpfs01/usatlas/data/ddavis").exists()
NTUP_PROD = "WTA02_20200821"

TTBAR_AUX_WEIGHT = "1.0"

DEF_1j1b_var = "bdtres10"
DEF_1j1b_nbin = 12
DEF_1j1b_xmin = 0.17
DEF_1j1b_xmax = 0.76
DEF_1j1b_lo_cut = 0.35

DEF_2j1b_var = "bdtres10"
DEF_2j1b_nbin = 12
DEF_2j1b_xmin = 0.22
DEF_2j1b_xmax = 0.85
DEF_2j1b_hi_cut = 0.70

DEF_2j2b_var = "bdtres10"
DEF_2j2b_nbin = 12
DEF_2j2b_xmin = 0.20
DEF_2j2b_xmax = 0.90
DEF_2j2b_lo_cut = 0.45
DEF_2j2b_hi_cut = 0.775

DEF_STAB_LIST = [
    "ttbar_ptreweight_1j1b",
    "ttbar_ptreweight_2j1b",
    "ttbar_ptreweight_2j2b",
    "ttbar_hdamp_1j1b",
    "ttbar_hdamp_2j1b",
    "ttbar_hdamp_2j2b",
    "ttbar_PS_1j1b",
    "ttbar_PS_2j1b",
    "ttbar_PS_2j2b",
    "ttbar_PS_migration",
    "ttbar_AR_FSR_2j1b",
    "ttbar_AR_FSR_1j1b",
    "tW_DRDS",
    "tW_PS_1j1b",
    "tW_PS_2j1b",
    "tW_PS_2j2b",
    "MET_SoftTrk_Scale",
    "Jet_Pileup_RhoTopology",
    "Jet_JER_EffectiveNP_7restTerm",
    "Jet_JER_EffNP_1",
    "Jet_JER_DataVsMC",
    "Jet_Flavor_Response",
    "Jet_Flavor_Composition",
    "B_ev_B_0",
]
##################################################

def ntuple_directory():
    if ON_SPAR:
        return f"/atlasgpfs01/usatlas/data/ddavis/wtloop/{NTUP_PROD}"
    return f"/ddd/atlas/data/wtloop/{NTUP_PROD}"


def r1j1b_selection(apply_cuts=False):
    if apply_cuts:
        return f"reg1j1b == 1 && OS == 1 && {DEF_1j1b_var} > {DEF_1j1b_lo_cut}"
    return "reg1j1b == 1 && OS == 1"


def r2j1b_selection(apply_cuts=False):
    if apply_cuts:
        return f"reg2j1b == 1 && OS == 1 && {DEF_2j1b_var} < {DEF_2j1b_hi_cut}"
    return "reg2j1b == 1 && OS == 1"


def r2j2b_selection(apply_cuts=False):
    if apply_cuts:
        return f"reg2j2b == 1 && OS == 1 && {DEF_2j2b_var} < {DEF_2j2b_hi_cut} && {DEF_2j2b_var} > {DEF_2j2b_lo_cut}"
    return "reg2j2b == 1 && OS == 1"


def r1j1b_bins():
    return f"{DEF_1j1b_nbin},{DEF_1j1b_xmin},{DEF_1j1b_xmax}"


def r2j1b_bins():
    return f"{DEF_2j1b_nbin},{DEF_2j1b_xmin},{DEF_2j1b_xmax}"


def r2j2b_bins():
    return f"{DEF_2j2b_nbin},{DEF_2j2b_xmin},{DEF_2j2b_xmax}"


def r1j1b_var():
    return f"{DEF_1j1b_var}"


def r2j1b_var():
    return f"{DEF_2j1b_var}"


def r2j2b_var():
    return f"{DEF_2j2b_var}"


def regular_stability_test_list():
    return DEF_STAB_LIST
