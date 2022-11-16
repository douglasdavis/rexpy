import logging
from typing import Optional
from textwrap import dedent

log = logging.getLogger(__name__)

# fmt: off
try:
    import ROOT
    ROOT.gROOT.SetBatch()
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    RDataFrame = ROOT.ROOT.RDataFrame
    import rexpy.simpconf as rps
    if not rps.ON_SPAR:
        ROOT.ROOT.EnableImplicitMT()
except ImportError:
    log.debug("ROOT was not imported; some rexpy.shower module functions require it")
# fmt: on


def norm_uncertainties(
    ntup_dir: str,
    pp8_files: str,
    ph7_files: str,
    sel_1j1b: Optional[str] = None,
    sel_2j1b: Optional[str] = None,
    sel_2j2b: Optional[str] = None,
):
    log.info("Calculating shower norm uncertainties")
    pp8_files = ["{}/{}.root".format(ntup_dir, f) for f in pp8_files.split(",")]
    ph7_files = ["{}/{}.root".format(ntup_dir, f) for f in ph7_files.split(",")]
    chain_pp8 = ROOT.TChain("WtLoop_nominal")
    chain_ph7 = ROOT.TChain("WtLoop_nominal")
    log.info("PowPy8 Files:")
    for f in pp8_files:
        chain_pp8.Add(f)
        log.info(" - %s" % f)
    log.info("PowH7 Files:")
    for f in ph7_files:
        chain_ph7.Add(f)
        log.info(" - %s" % f)

    df_pp8 = RDataFrame(chain_pp8)
    df_ph7 = RDataFrame(chain_ph7)

    log.info("1j1b selection: '%s'" % sel_1j1b)
    log.info("2j1b selection: '%s'" % sel_2j1b)
    log.info("2j2b selection: '%s'" % sel_2j2b)

    r1j1b_pp8, r1j1b_ph7 = 0.0, 0.0
    r2j1b_pp8, r2j1b_ph7 = 0.0, 0.0
    r2j2b_pp8, r2j2b_ph7 = 0.0, 0.0
    if sel_1j1b is not None:
        r1j1b_pp8 = df_pp8.Filter(str(sel_1j1b)).Sum("weight_nominal")
        r1j1b_ph7 = df_ph7.Filter(str(sel_1j1b)).Sum("weight_nominal")
    if sel_2j1b is not None:
        r2j1b_pp8 = df_pp8.Filter(str(sel_2j1b)).Sum("weight_nominal")
        r2j1b_ph7 = df_ph7.Filter(str(sel_2j1b)).Sum("weight_nominal")
    if sel_2j2b is not None:
        r2j2b_pp8 = df_pp8.Filter(str(sel_2j2b)).Sum("weight_nominal")
        r2j2b_ph7 = df_ph7.Filter(str(sel_2j2b)).Sum("weight_nominal")

    if sel_1j1b is not None:
        r1j1b_pp8 = r1j1b_pp8.GetValue()
        r1j1b_ph7 = r1j1b_ph7.GetValue()
    if sel_2j1b is not None:
        r2j1b_pp8 = r2j1b_pp8.GetValue()
        r2j1b_ph7 = r2j1b_ph7.GetValue()
    if sel_2j2b is not None:
        r2j2b_pp8 = r2j2b_pp8.GetValue()
        r2j2b_ph7 = r2j2b_ph7.GetValue()

    raw_pp8 = r1j1b_pp8 + r2j1b_pp8 + r2j2b_pp8
    raw_ph7 = r1j1b_ph7 + r2j1b_ph7 + r2j2b_ph7

    scale_fac_for_ph7 = raw_pp8 / raw_ph7
    overall_norm_unc = abs(raw_ph7 - raw_pp8) / raw_pp8

    r1j1b_ph7 = r1j1b_ph7 * scale_fac_for_ph7
    r2j1b_ph7 = r2j1b_ph7 * scale_fac_for_ph7
    r2j2b_ph7 = r2j2b_ph7 * scale_fac_for_ph7

    mig_1j1b = (abs(r1j1b_ph7 - r1j1b_pp8) / r1j1b_pp8) if sel_1j1b is not None else 0.0
    mig_2j1b = (abs(r2j1b_ph7 - r2j1b_pp8) / r2j1b_pp8) if sel_2j1b is not None else 0.0
    mig_2j2b = (abs(r2j2b_ph7 - r2j2b_pp8) / r2j2b_pp8) if sel_2j2b is not None else 0.0

    log.info("-------------------------")
    log.info("Overall:         %f" % overall_norm_unc)
    if sel_1j1b is not None:
        log.info("Migration 1j1b:  %f" % mig_1j1b)
    if sel_2j1b is not None:
        log.info("Migration 2j1b:  %f" % mig_2j1b)
    if sel_2j2b is not None:
        log.info("Migration 2j2b:  %f" % mig_2j2b)
    log.info("-------------------------")

    return (
        round(overall_norm_unc, 4),
        round(mig_1j1b, 4),
        round(mig_2j1b, 4),
        round(mig_2j2b, 4),
    )


def norm_uncertainties_ttbar(
    ntup_dir: str,
    sel_1j1b: Optional[str] = None,
    sel_2j1b: Optional[str] = None,
    sel_2j2b: Optional[str] = None,
    herwig_dsid: str = "410558",
):
    pp8_files = (
        "ttbar_410472_AFII_MC16a_nominal,"
        "ttbar_410472_AFII_MC16d_nominal,"
        "ttbar_410472_AFII_MC16e_nominal"
    )
    ph7_files = (
        f"ttbar_{herwig_dsid}_AFII_MC16a_nominal,"
        f"ttbar_{herwig_dsid}_AFII_MC16d_nominal,"
        f"ttbar_{herwig_dsid}_AFII_MC16e_nominal"
    )
    return norm_uncertainties(
        ntup_dir, pp8_files, ph7_files, sel_1j1b, sel_2j1b, sel_2j2b
    )


def norm_uncertainties_tW(
    ntup_dir: str,
    sel_1j1b: Optional[str] = None,
    sel_2j1b: Optional[str] = None,
    sel_2j2b: Optional[str] = None,
):
    pp8_files = (
        "tW_DR_410648_AFII_MC16a_nominal,"
        "tW_DR_410648_AFII_MC16d_nominal,"
        "tW_DR_410648_AFII_MC16e_nominal,"
        "tW_DR_410649_AFII_MC16a_nominal,"
        "tW_DR_410649_AFII_MC16d_nominal,"
        "tW_DR_410649_AFII_MC16e_nominal"
    )
    ph7_files = (
        "tW_DR_411038_AFII_MC16a_nominal,"
        "tW_DR_411038_AFII_MC16d_nominal,"
        "tW_DR_411038_AFII_MC16e_nominal,"
        "tW_DR_411039_AFII_MC16a_nominal,"
        "tW_DR_411039_AFII_MC16d_nominal,"
        "tW_DR_411039_AFII_MC16e_nominal"
    )
    return norm_uncertainties(
        ntup_dir, pp8_files, ph7_files, sel_1j1b, sel_2j1b, sel_2j2b
    )


def norm_uncertainties_ttbar_splits(
    ntup_dir: str = "/ddd/atlas/data/wtloop/WTA01_20200916",
    herwig_dsid: str = "410558",
):

    sel_1j1b = "reg1j1b == 1 && OS == 1 && bdtres03 > 0.35"
    sel_1j1bL = "{} && bdtres03 < 0.555".format(sel_1j1b)
    sel_1j1bH = "{} && bdtres03 > 0.555".format(sel_1j1b)
    sel_2j1b = "reg2j1b == 1 && OS == 1 && bdtres03 < 0.70"
    sel_2j1bL = "{} && bdtres03 < 0.34".format(sel_2j1b)
    sel_2j1bH = "{} && bdtres03 > 0.34".format(sel_2j1b)
    sel_2j2b =  "reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775"

    pp8_files = (
        "ttbar_410472_AFII_MC16a_nominal,"
        "ttbar_410472_AFII_MC16d_nominal,"
        "ttbar_410472_AFII_MC16e_nominal"
    )
    ph7_files = (
        f"ttbar_{herwig_dsid}_AFII_MC16a_nominal,"
        f"ttbar_{herwig_dsid}_AFII_MC16d_nominal,"
        f"ttbar_{herwig_dsid}_AFII_MC16e_nominal"
    )
    return norm_uncertainties_splits(
        ntup_dir,
        pp8_files,
        ph7_files,
        sel_1j1bL,
        sel_1j1bH,
        sel_2j1bL,
        sel_2j1bH,
        sel_2j2b,
    )


def norm_uncertainties_splits(
    ntup_dir: str,
    pp8_files: str,
    ph7_files: str,
    sel_1j1bL: Optional[str] = None,
    sel_1j1bH: Optional[str] = None,
    sel_2j1bL: Optional[str] = None,
    sel_2j1bH: Optional[str] = None,
    sel_2j2b: Optional[str] = None,
):
    log.info("Calculating shower norm uncertainties")
    pp8_files = ["{}/{}.root".format(ntup_dir, f) for f in pp8_files.split(",")]
    ph7_files = ["{}/{}.root".format(ntup_dir, f) for f in ph7_files.split(",")]
    chain_pp8 = ROOT.TChain("WtLoop_nominal")
    chain_ph7 = ROOT.TChain("WtLoop_nominal")
    log.info("PowPy8 Files:")
    for f in pp8_files:
        chain_pp8.Add(f)
        log.info(" - %s" % f)
    log.info("PowH7 Files:")
    for f in ph7_files:
        chain_ph7.Add(f)
        log.info(" - %s" % f)

    df_pp8 = RDataFrame(chain_pp8)
    df_ph7 = RDataFrame(chain_ph7)

    r1j1bH_pp8, r1j1bH_ph7 = 0.0, 0.0
    r1j1bL_pp8, r1j1bL_ph7 = 0.0, 0.0
    r2j1bH_pp8, r2j1bH_ph7 = 0.0, 0.0
    r2j1bL_pp8, r2j1bL_ph7 = 0.0, 0.0
    r2j1b_pp8, r2j1b_ph7 = 0.0, 0.0
    r2j2b_pp8, r2j2b_ph7 = 0.0, 0.0

    r1j1bL_pp8 = df_pp8.Filter(str(sel_1j1bL)).Sum("weight_nominal")
    r1j1bL_ph7 = df_ph7.Filter(str(sel_1j1bL)).Sum("weight_nominal")
    r1j1bH_pp8 = df_pp8.Filter(str(sel_1j1bH)).Sum("weight_nominal")
    r1j1bH_ph7 = df_ph7.Filter(str(sel_1j1bH)).Sum("weight_nominal")
    r2j1bL_pp8 = df_pp8.Filter(str(sel_2j1bL)).Sum("weight_nominal")
    r2j1bL_ph7 = df_ph7.Filter(str(sel_2j1bL)).Sum("weight_nominal")
    r2j1bH_pp8 = df_pp8.Filter(str(sel_2j1bH)).Sum("weight_nominal")
    r2j1bH_ph7 = df_ph7.Filter(str(sel_2j1bH)).Sum("weight_nominal")
    r2j2b_pp8 = df_pp8.Filter(str(sel_2j2b)).Sum("weight_nominal")
    r2j2b_ph7 = df_ph7.Filter(str(sel_2j2b)).Sum("weight_nominal")

    r1j1bH_pp8 = r1j1bH_pp8.GetValue()
    r1j1bH_ph7 = r1j1bH_ph7.GetValue()
    r1j1bL_pp8 = r1j1bL_pp8.GetValue()
    r1j1bL_ph7 = r1j1bL_ph7.GetValue()
    r2j1bH_pp8 = r2j1bH_pp8.GetValue()
    r2j1bH_ph7 = r2j1bH_ph7.GetValue()
    r2j1bL_pp8 = r2j1bL_pp8.GetValue()
    r2j1bL_ph7 = r2j1bL_ph7.GetValue()
    r2j2b_pp8 = r2j2b_pp8.GetValue()
    r2j2b_ph7 = r2j2b_ph7.GetValue()

    raw_pp8 = r1j1bL_pp8 + r2j1bL_pp8 + r1j1bH_pp8 + r2j1bH_pp8 + r2j2b_pp8
    raw_ph7 = r1j1bL_ph7 + r2j1bL_ph7 + r1j1bH_ph7 + r2j1bH_ph7 + r2j2b_ph7

    overall_norm_unc = abs(raw_ph7 - raw_pp8) / raw_pp8
    norm_unc_1j1bL = abs(r1j1bL_ph7 - r1j1bL_pp8) / r1j1bL_pp8
    norm_unc_1j1bH = abs(r1j1bH_ph7 - r1j1bH_pp8) / r1j1bH_pp8
    norm_unc_2j1bL = abs(r2j1bL_ph7 - r2j1bL_pp8) / r2j1bL_pp8
    norm_unc_2j1bH = abs(r2j1bH_ph7 - r2j1bH_pp8) / r2j1bH_pp8
    norm_unc_2j2b = abs(r2j2b_ph7 - r2j2b_pp8) / r2j2b_pp8

    log.info("-------------------------")
    log.info("Overall:         %f" % overall_norm_unc)

    log.info("1j1bL:           %f" % norm_unc_1j1bL)
    log.info("1j1bH:           %f" % norm_unc_1j1bH)
    log.info("2j1bL:           %f" % norm_unc_2j1bL)
    log.info("2j1bH:           %f" % norm_unc_2j1bH)
    log.info("2j2b:            %f" % norm_unc_2j2b)

    return (
        round(overall_norm_unc, 4),
        round(norm_unc_1j1bL, 4),
        round(norm_unc_1j1bH, 4),
        round(norm_unc_2j1bL, 4),
        round(norm_unc_2j1bH, 4),
        round(norm_unc_2j2b , 4),
    )
