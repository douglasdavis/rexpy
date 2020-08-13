"""A module for parsing TRExFitter configs and results"""

# stdlib
from pathlib import PosixPath

BLIND_ARGS = "FitBlind=TRUE:Suffix=_asimov"


def all_blocks(config, delimiter="\n\n"):
    """Get all blocks in a config based on a delimiter.

    The TRExFitter configuration schema is pretty rigid. We nominally
    expect exactly one blank line between all blocks, so the delimiter
    between two blocks should be exactly two new newlines.

    Parameters
    ----------
    config : str
        Path of the config file.
    delimiter : str
        Delimiter to use on the config string to separate into
        blocks. This should only overwrite the default in very special
        cases, a double new line is standard.

    Returns
    -------
    list(str)
        Configuration blocks.
    """
    config_str = PosixPath(config).read_text()
    return config_str.split(delimiter)


def top_block_titles(config, block_type):
    """Extract the set of titles associated with a block type.

    Each top level TRExFitter block has a title and we can extract the
    titles of a specific top level block type.

    Parameters
    ----------
    config : str
        Path of the config file.
    block_type : str
        Block type the titles are associated with.

    Returns
    -------
    set(str)
        Titles of the requested blocks.

    Examples
    --------
    A config with some blocks of the form::

      Region: "reg2j2b"
        Label: "..."
        ShortLabel: "..."
        Selection: "..."
        Binning ...

      Region: "reg2j1b"
        Label: "..."
        ShortLabel: "..."
        Selection: "..."
        Binning ...

    will yield::

      >>> top_block_titles("/path/to/fit.conf", "Region")
      ["reg2j2b", "reg2j1b"]

    """
    with open(config, "r") as f:
        return set(
            map(
                lambda line: line.split(": ")[1].replace('"', "").strip(),
                filter(
                    lambda line: str(line).startswith("%s: " % block_type), f.readlines(),
                ),
            )
        )


def sub_block_values(config, key):
    """Extract set of values associated with a sub block key

    Parameters
    ----------
    config : str
        Path of the config file.
    key : str
        Sub block key (e.g. "SubCategory")

    Returns
    -------
    set(str)
        Unique values of the given key
    """
    with open(config, "r") as f:
        return set(
            map(
                lambda line: line.split(": ")[1].replace('"', "").strip(),
                filter(lambda line: str(line).startswith("  %s: " % key), f.readlines(),),
            )
        )


def systematics_from(config, specific_sys=None):
    """Get list of relevant systematics.

    If `specific_sys` is None (default), this will return all of
    the systematics in the config. If `specific_sys` is not None,
    the entries will be tested against all possible systematics found
    in the config file and that list will be returned.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    list(str)
        The relevant systematics.
    """
    systs = top_block_titles(config, "Systematic")
    if specific_sys is None or len(specific_sys) == 0:
        return systs
    else:
        return list(filter(lambda s: s in systs, specific_sys))


def regions_from(config, exclude=None):
    """Get the list of regions in a config file.

    Parameters
    ----------
    config : str
        Path of the config file.
    exclude : list(str)
        Regions to skip (if present in config).

    Returns
    -------
    list(str)
        The list of regions in the config file.
    """
    regs = top_block_titles(config, "Region")
    if exclude is not None:
        return list(filter(lambda r: r not in exclude, regs))
    else:
        return regs


def rank_arguments(config, specific_sys=None, as_blind=False):
    """Get a set of trex-fitter executable arguments for ranking.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.
    as_blind : bool
        Include command line arguments for performing blind fit.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments.
    """
    systematics = systematics_from(config, specific_sys=specific_sys)
    args = ["r {} Ranking={}".format(config, sys) for sys in systematics]
    if as_blind:
        args = [f"{arg}:{BLIND_ARGS}" for arg in args]
    return args


def grouped_impact_arguments(config, as_blind=False):
    """Get a set of trex-fitter executable arguments for grouped impact.

    Parameters
    ----------
    config : str
        Path of the config file.
    as_blind : bool
        Include command line arguments for performing blind fit.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments
    """
    groups = sub_block_values(config, "SubCategory")
    groups = list(groups) + ["Gammas", "FullSyst"]
    args = ["i {} GroupedImpact={}".format(config, g) for g in groups]
    if as_blind:
        args = [f"{arg}:{BLIND_ARGS}" for arg in args]
    return args


def draw_argument(config, specific_sys=None, as_blind=False):
    """Get the draw trex-fitter step argument"

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.
    as_blind : bool
        Include command line arguments for performing blind fit.

    Returns
    -------
    str
        the fit step argument
    """
    if specific_sys is not None:
        systs = ",".join(systematics_from(config, specific_sys))
        arg = "dp {} Systematics={}".format(config, systs)
    else:
        arg = "dp {}".format(config)

    if as_blind:
        arg = f"{arg}:{BLIND_ARGS}"

    return arg


def fit_argument(config, specific_sys=None, dont_fit_vr=True, as_blind=False):
    """Get the fit trex-fitter step argument.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.
    dont_fit_vr : bool
        Do not include VR regions in fit argument.
    as_blind : bool
        Include command line arguments for performing blind fit.

    Returns
    -------
    str
        the fit step argument
    """
    region_arg = ""
    if dont_fit_vr:
        regions = regions_from(config)
        regions = [r for r in regions if not r.startswith("VR")]
        region_arg = " Regions={}".format(",".join(regions))

    arg = f"wf {config}{region_arg}"
    arg = arg.strip()

    if specific_sys is not None:
        systematics = systematics_from(config, specific_sys=specific_sys)
        systematics = ",".join(systematics)
        arg = f"{arg}:Systematics={systematics}"

    if as_blind:
        arg = f"{arg}:{BLIND_ARGS}"

    return arg


def ntuple_arguments_granular(config, fitname="tW"):
    """Get the set of granular trex-fitter ntupling instructions

    Parameters
    ----------
    config : str
        Path of the config file.
    fitname : str
        Name of the fit.

    Returns
    -------
    list(str)
        trex-fitter n step arguments.
    list(str)
        hupdate.exe execution instructions.

    """
    regions = regions_from(config)
    systematics = systematics_from(config)
    region_hupdate_files = {r: [] for r in regions}
    args = []
    for r in regions:
        for s in systematics:
            if "1j1b" in s and "1j1b" not in r:
                continue
            if "2j1b" in s and "2j1b" not in r:
                continue
            if "2j2b" in s and "2j2b" not in r:
                continue
            args.append(f"n {config} Regions={r}:Systematics={s}:SaveSuffix=_{s}")
            region_hupdate_files[r].append(
                f"{fitname}/Histograms/{fitname}_{r}_histos_{s}.root"
            )
    updates = []
    for k, v in region_hupdate_files.items():
        a1 = f"{fitname}/Histograms/{fitname}_{k}_histos.root"
        a2 = " ".join(v)
        updates.append(f"{a1} {a2}")
    return args, updates


def ntuple_arguments(config, specific_sys=None):
    """Get the set of trex-fitter executable arguments for ntupling.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        The set of systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments

    """
    regions = regions_from(config)

    ## first no specific systematics
    if specific_sys is None:
        return ["n {} Regions={}".format(config, r) for r in regions]

    ## otherwise, construct for specific systematics
    systematics = systematics_from(config, specific_sys=specific_sys)
    systematics = ",".join(systematics)
    return [
        "n {} Regions={}:Systematics={}".format(config, r, systematics) for r in regions
    ]


def drop_systematics(blocks, systematics):
    """Drop a systematic from a set of blocks.

    Parameters
    ----------
    blocks : list(str)
        All TRExFitter blocks.
    systematics : list(str)
        Name of the systematic to drop.

    Returns
    -------
    list(str)
        Blocks without desired systematic.
    """
    result = blocks[:]
    to_drop = []
    for s in systematics:
        itr = filter(lambda x: x.startswith(f'Systematic: "{s}"'), blocks)
        for i in itr:
            to_drop.append(i)
    for drop in to_drop:
        result.remove(drop)
    return result


def drop_region(blocks, region):
    """Drop a region from a set of blocks.

    Parameters
    ----------
    blocks : list(str)
        All TRExFitter blocks.
    region : str
        Region to drop.

    Returns
    -------
    list(str)
        Blocks without dropped region.
    """
    new_blocks = []
    for block in blocks:
        if block.startswith("Region:"):
            if region in block:
                continue
        if block.startswith("Systematic:"):
            if region in block:
                continue
        new_blocks.append(block)
    new_blocks[0] = new_blocks[0].replace(
        "SummaryPlotRegions: reg1j1b,reg2j1b,reg2j2b\n  ", ""
    )
    return new_blocks
