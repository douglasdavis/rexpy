import logging
log = logging.getLogger(__name__)

try:
    import ROOT
    ROOT.gROOT.SetBatch()
    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    log.warn("ROOT was not imported; this module requires it.")

from textwrap import dedent


def norm_uncertainties(
    ntup_dir, pp8_files, ph7_files, sel_1j1b, sel_2j1b, sel_2j2b,
):
    log.info("Calculating shower norm uncertainties")
    RDataFrame = ROOT.ROOT.RDataFrame
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

    r1j1b_pp8 = df_pp8.Filter(str(sel_1j1b)).Sum("weight_nominal")
    r1j1b_ph7 = df_ph7.Filter(str(sel_1j1b)).Sum("weight_nominal")
    r2j1b_pp8 = df_pp8.Filter(str(sel_2j1b)).Sum("weight_nominal")
    r2j1b_ph7 = df_ph7.Filter(str(sel_2j1b)).Sum("weight_nominal")
    r2j2b_pp8 = df_pp8.Filter(str(sel_2j2b)).Sum("weight_nominal")
    r2j2b_ph7 = df_ph7.Filter(str(sel_2j2b)).Sum("weight_nominal")

    r1j1b_pp8 = r1j1b_pp8.GetValue()
    r2j1b_pp8 = r2j1b_pp8.GetValue()
    r2j2b_pp8 = r2j2b_pp8.GetValue()
    r1j1b_ph7 = r1j1b_ph7.GetValue()
    r2j1b_ph7 = r2j1b_ph7.GetValue()
    r2j2b_ph7 = r2j2b_ph7.GetValue()

    raw_pp8 = r1j1b_pp8 + r2j1b_pp8 + r2j2b_pp8
    raw_ph7 = r1j1b_ph7 + r2j1b_ph7 + r2j2b_ph7

    scale_fac_for_ph7 = raw_pp8 / raw_ph7
    overall_norm_unc = abs(raw_ph7 - raw_pp8) / raw_pp8

    r1j1b_ph7 = r1j1b_ph7 * scale_fac_for_ph7
    r2j1b_ph7 = r2j1b_ph7 * scale_fac_for_ph7
    r2j2b_ph7 = r2j2b_ph7 * scale_fac_for_ph7

    mig_1j1b = abs(r1j1b_ph7 - r1j1b_pp8) / r1j1b_pp8
    mig_2j1b = abs(r2j1b_ph7 - r2j1b_pp8) / r2j1b_pp8
    mig_2j2b = abs(r2j2b_ph7 - r2j2b_pp8) / r2j2b_pp8

    log.info("-------------------------")
    log.info("Overall:         %f" % overall_norm_unc)
    log.info("Migration 1j1b:  %f" % mig_1j1b)
    log.info("Migration 2j1b:  %f" % mig_2j1b)
    log.info("Migration 2j2b:  %f" % mig_2j2b)
    log.info("-------------------------")

    return (round(overall_norm_unc, 4), round(mig_1j1b, 4), round(mig_2j1b, 4), round(mig_2j2b, 4))


def norm_uncertainties_ttbar(
    ntup_dir="/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
    sel_1j1b="OS==1 && reg1j1b==1",
    sel_2j1b="OS==1 && reg2j1b==1",
    sel_2j2b="OS==1 && reg2j2b==1",
):
    pp8_files = (
        "ttbar_410472_AFII_MC16a_nominal,"
        "ttbar_410472_AFII_MC16d_nominal,"
        "ttbar_410472_AFII_MC16e_nominal"
    )
    ph7_files = (
        "ttbar_411234_AFII_MC16a_nominal,"
        "ttbar_411234_AFII_MC16d_nominal,"
        "ttbar_411234_AFII_MC16e_nominal"
    )
    return norm_uncertainties(
        ntup_dir, pp8_files, ph7_files, sel_1j1b, sel_2j1b, sel_2j2b
    )


def norm_uncertainties_tW(
    ntup_dir="/atlasgpfs01/usatlas/data/ddavis/wtloop/WTA01_20200506",
    sel_1j1b="OS==1 && reg1j1b==1",
    sel_2j1b="OS==1 && reg2j1b==1",
    sel_2j2b="OS==1 && reg2j2b==1",
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
