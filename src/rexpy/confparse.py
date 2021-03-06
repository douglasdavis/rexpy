"""A module for parsing TRExFitter configs and results"""

# stdlib
from pathlib import PosixPath


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
                    lambda line: str(line).startswith("%s: " % block_type),
                    f.readlines(),
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
                filter(
                    lambda line: str(line).startswith("  %s: " % key),
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


def unblind(config):
    """Ensure a config is unblinded.

    Parameters
    ----------
    config : str or os.PathLike
        Path of the config file.

    Returns
    -------
    pathlib.PosixPath
        Config file Path.

    """
    conf_path = PosixPath(config)
    full_config = conf_path.read_text()
    full_config = full_config.replace("  FitBlind: TRUE\n", "  FitBlind: FALSE\n")
    conf_path.write_text(full_config)
    return conf_path
