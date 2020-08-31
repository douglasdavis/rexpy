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
    weight_expression: str = "weight_nominal",
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

    if weight_expression == "weight_nominal * 1.0":
        weight_expression = "weight_nominal"

    log.info("1j1b selection: '%s'" % sel_1j1b)
    log.info("2j1b selection: '%s'" % sel_2j1b)
    log.info("2j2b selection: '%s'" % sel_2j2b)

    log.info("Weight expression: '%s'" % weight_expression)

    r1j1b_pp8, r1j1b_ph7 = 0.0, 0.0
    r2j1b_pp8, r2j1b_ph7 = 0.0, 0.0
    r2j2b_pp8, r2j2b_ph7 = 0.0, 0.0
    if sel_1j1b is not None:
        if weight_expression == "weight_nominal":
            r1j1b_pp8 = df_pp8.Filter(str(sel_1j1b)).Sum("weight_nominal")
            r1j1b_ph7 = df_ph7.Filter(str(sel_1j1b)).Sum("weight_nominal")
        else:
            r1j1b_pp8 = df_pp8.Filter(str(sel_1j1b)).Define("wtu", weight_expression).Sum("wtu")
            r1j1b_ph7 = df_ph7.Filter(str(sel_1j1b)).Define("wtu", weight_expression).Sum("wtu")
    if sel_2j1b is not None:
        if weight_expression == "weight_nominal":
            r2j1b_pp8 = df_pp8.Filter(str(sel_2j1b)).Sum("weight_nominal")
            r2j1b_ph7 = df_ph7.Filter(str(sel_2j1b)).Sum("weight_nominal")
        else:
            r2j1b_pp8 = df_pp8.Filter(str(sel_2j1b)).Define("wtu", weight_expression).Sum("wtu")
            r2j1b_ph7 = df_ph7.Filter(str(sel_2j1b)).Define("wtu", weight_expression).Sum("wtu")
    if sel_2j2b is not None:
        if weight_expression == "weight_nominal":
            r2j2b_pp8 = df_pp8.Filter(str(sel_2j2b)).Sum("weight_nominal")
            r2j2b_ph7 = df_ph7.Filter(str(sel_2j2b)).Sum("weight_nominal")
        else:
            r2j2b_pp8 = df_pp8.Filter(str(sel_2j2b)).Define("wtu", weight_expression).Sum("wtu")
            r2j2b_ph7 = df_ph7.Filter(str(sel_2j2b)).Define("wtu", weight_expression).Sum("wtu")

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
    ntup_dir: str = "/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
    sel_1j1b: Optional[str] = None,
    sel_2j1b: Optional[str] = None,
    sel_2j2b: Optional[str] = None,
    herwig_dsid: str = "410558",
    weight_expression: str = "weight_nominal",
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
        ntup_dir, pp8_files, ph7_files, sel_1j1b, sel_2j1b, sel_2j2b, weight_expression
    )


def norm_uncertainties_tW(
    ntup_dir: str = "/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
    sel_1j1b: Optional[str] = None,
    sel_2j1b: Optional[str] = None,
    sel_2j2b: Optional[str] = None,
    weight_expression: str = "weight_nominal",
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
        ntup_dir, pp8_files, ph7_files, sel_1j1b, sel_2j1b, sel_2j2b, weight_expression
    )
