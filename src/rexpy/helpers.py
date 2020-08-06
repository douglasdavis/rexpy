import os


def trex_fitter_exe():
    return os.popen("which trex-fitter").read().strip()


def selection_with_period(raw, only_1516=False, only_17=False, only_18=False):
    """Augment a selection to require a specific data taking period.

    Parameters
    ----------
    raw : str
        Raw selection string.
    only_1516 : bool
        Require 2015/2016
    only_17 : bool
        Require 2017
    only_18 : bool
        Require 2018

    Returns
    -------
    str
        Updated selection string
    """
    if only_1516:
        return f"({raw}) && (isMC16a == 1)"
    elif only_17:
        return f"({raw}) && (isMC16d == 1)"
    elif only_18:
        return f"({raw}) && (isMC16e == 1)"
    else:
        return raw
