"""A module for parsing TRExFitter configs"""


def get_systematics(config, specific_sys=None):
    """Get list of relevant systematics.

    If `specific_sys` is None (default), this will return all of
    the systematics in the config. If `specific_sys` is not None,
    the entries will be tested against all possible systematics found
    in the config file and that list will be returned.

    Parameters
    ----------
    config : str
        The path of the config file.
    specific_sys : iterable(str), optional
        A set of desired systematics.

    Returns
    -------
    list(str)
        The relevant systematics.

    """

    systematics = []
    with open(config, "r") as f:
        for line in f.readlines():
            if line.startswith(r"%"):
                continue
            elif line.startswith("Systematic:"):
                sys = line.strip().split(":")[-1].strip().replace('"', '')
                systematics.append(sys)
    systematics = sorted(set(systematics), key=str.lower, reverse=True)
    if specific_sys is None:
        return systematics
    elif len(specific_sys) == 0:
        return systematics
    else:
        req_sys = []
        for s in specific_sys:
            s = str(s)
            if s not in systematics:
                raise ValueError("systematic {} not possible".format(s))
            req_sys.append(s)
        return sorted(set(req_sys), key=str.lower, reverse=True)


def get_regions(config):
    """Get the list of regions in a config file.

    Parameters
    ----------
    config : str
        The path of the config file.

    Returns
    -------
    list(str)
        The list of regions in the config file.

    """
    regions = []
    with open(config, "r") as f:
        for line in f.readlines():
            if line.startswith("%"):
                continue
            elif line.startswith("Region:"):
                reg = line.strip().split(":")[-1].strip().replace('"', '')
                regions.append(reg)
    return regions


def gen_rank_arguments(config, specific_sys=None):
    """Get a set of trex-fitter executable arguments for ranking.

    Parameters
    ----------
    config : str
        The path of the config file.
    specific_sys : iterable(str), optional
        The set of systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments.

    """
    systematics = get_systematics(config, specific_sys=specific_sys)
    return ["r {} Ranking={}".format(config, sys) for sys in systematics]


def gen_fit_argument(config, specific_sys=None, dont_fit_vr=True):
    """Get the fit trex-fitter step argument.

    Parameters
    ----------
    config : str
        The path of the config file.
    specific_sys : iterable(str), optional
        The set of systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    str
        the fit step argument
    """
    region_arg = ""
    if dont_fit_vr:
        regions = get_regions(config)
        regions = [r for r in regions if not r.startswith("VR")]
        region_arg = "Regions={}".format(",".join(regions))

    if specific_sys is None:
        return "wf {} {}".format(config, region_arg).strip()

    systematics = get_systematics(config, specific_sys=specific_sys)
    systematics = ",".join(systematics)

    if not region_arg:
        return "wf {} Systematics={}".format(config, systematics)
    else:
        return "wf {} {}:Systematics={}".format(config, region_arg, systematics)


def gen_ntuple_arguments(config, specific_sys=None):
    """Get the set of trex-fitter executable arguments for ntupling.

    config : str
        The path of the config file.
    specific_sys : iterable(str), optional
        The set of systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments

    """
    regions = get_regions(config)

    ## first no specific systematics
    if specific_sys is None:
        return ["n {} Regions={}".format(config, r) for r in regions]

    ## otherwise, construct for specific systematics
    systematics = get_systematics(config, specific_sys=specific_sys)
    systematics = ",".join(systematics)
    return ["n {} Regions={}:Systematics={}".format(config, r, systematics) for r in regions]
