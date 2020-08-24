from pathlib import Path


######################################
####### Default constants ############
######################################
ON_SPAR = Path("/atlasgpfs01/usatlas/data/ddavis").exists()
NTUP_DIR = None
if ON_SPAR:
    NTUP_DIR = "/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA02_20200821"
else:
    NTUP_DIR = "/ddd/atlas/data/wtloop/WTA02_20200821"

TTBAR_AUX_WEIGHT = "1.0"

DEF_1j1b_sels = "reg1j1b == 1 && OS == 1"
DEF_1j1b_swmc = "reg1j1b == 1 && OS == 1 && mass_lep1jet1 < 155 && mass_lep2jet1 < 155"
DEF_1j1b_vari = "bdtres10"
DEF_1j1b_nbin = 12
DEF_1j1b_xmin = 0.17
DEF_1j1b_xmax = 0.76
DEF_1j1b_bins = "{},{},{}".format(DEF_1j1b_nbin, DEF_1j1b_xmin, DEF_1j1b_xmax)

DEF_2j1b_sels = "reg2j1b == 1 && OS == 1"
DEF_2j1b_swmc = "reg2j1b == 1 && OS == 1 && mass_lep1jetb < 155 && mass_lep2jetb < 155"
DEF_2j1b_vari = "bdtres10"
DEF_2j1b_nbin = 12
DEF_2j1b_xmin = 0.22
DEF_2j1b_xmax = 0.85
DEF_2j1b_bins = "{},{},{}".format(DEF_2j1b_nbin, DEF_2j1b_xmin, DEF_2j1b_xmax)

DEF_2j2b_sels = "reg2j2b == 1 && OS == 1"
DEF_2j2b_swmc = "reg2j2b == 1 && OS == 1 && minimaxmbl < 155"
DEF_2j2b_vari = "bdtres10"
DEF_2j2b_nbin = 12
DEF_2j2b_xmin = 0.20
DEF_2j2b_xmax = 0.90
DEF_2j2b_bins = "{},{},{}".format(DEF_2j2b_nbin, DEF_2j2b_xmin, DEF_2j2b_xmax)
######################################
