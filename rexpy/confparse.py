"""A module for parsing TRExFitter configs and results"""

from __future__ import print_function

import six
from pathlib2 import PosixPath


def all_blocks(config, delimiter="\n\n"):
    """Get all blocks in a config based on a delimiter.

    The TRExFitter configuration schema is pretty rigid. We nominally
    expect exactly one blank line between all blocks, so the delimiter
    between two blocks should be exactly two new newlines.

    Paramters
    ---------
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
    config_str = six.ensure_str(PosixPath(config).read_text())
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
                    lambda line: str(line).startswith("%s: " % block_type),
                    f.readlines(),
                ),
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


def rank_arguments(config, specific_sys=None):
    """Get a set of trex-fitter executable arguments for ranking.

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
        The list of trex-fitter arguments.
    """
    systematics = systematics_from(config, specific_sys=specific_sys)
    return ["r {} Ranking={}".format(config, sys) for sys in systematics]


def draw_argument(config, specific_sys=None):
    """Get the draw trex-fitter step argument"

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    str
        the fit step argument
    """
    if specific_sys is not None:
        systs = ",".join(systematics_from(config, specific_sys))
        return "dp {} Systematics={}".format(config, systs)
    else:
        return "dp {}".format(config)


def fit_argument(config, specific_sys=None, dont_fit_vr=True):
    """Get the fit trex-fitter step argument.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    str
        the fit step argument
    """
    region_arg = ""
    if dont_fit_vr:
        regions = regions_from(config)
        regions = [r for r in regions if not r.startswith("VR")]
        region_arg = "Regions={}".format(",".join(regions))

    if specific_sys is None:
        return "wf {} {}".format(config, region_arg).strip()

    systematics = systematics_from(config, specific_sys=specific_sys)
    systematics = ",".join(systematics)

    if not region_arg:
        return "wf {} Systematics={}".format(config, systematics)
    else:
        return "wf {} {}:Systematics={}".format(config, region_arg, systematics)


def ntuple_arguments(config, specific_sys=None):
    """Get the set of trex-fitter executable arguments for ntupling.

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
