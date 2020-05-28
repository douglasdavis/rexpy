from __future__ import print_function

import os
import yaml
import six
from pathlib2 import PosixPath

from rexpy.confparse import regions_from


BLOCK_TEMPLATE = """\
Region: "VRP_reg{region}_{var}"
  VariableTitle: "{title}"
  ShortLabel: "{region}"
  Selection: "{selection}"
  Type: VALIDATION
  Label: "{region}"
  Variable: "{var}",{nbins},{xmin},{xmax}
  LogScale: {logscale}"""


def load_meta_table(metafile):
    """Generate table of metadata information.

    Parmaters
    ---------
    metafile : str
        Path to the file defining the metadata.

    Returns
    -------
    dict
        Metadata for plots in dict form.
    """
    with open(metafile, "r") as f:
        metatable = yaml.load(f, Loader=yaml.Loader)
    return metatable


def block(region, selection, var, title, nbins, xmin, xmax, logscale):
    """Generate a VRP block.

    Paramters
    ---------
    region : str
        Main region.
    selection : str
        Selection string.
    var : str
        Variable in the tree.
    title : str
        Axis title.
    nbins : int
        Number of bins.
    xmin : float
        Minimum axis limit.
    xmax : float
        Maximum axis limit.
    logscale : bool
        To turn on log scale option.

    Returns
    -------
    str
        VRP block.
    """
    return BLOCK_TEMPLATE.format(
        region=region,
        var=var,
        title=title,
        selection=selection,
        nbins=nbins,
        xmin=xmin,
        xmax=xmax,
        logscale=logscale,
    )


def blocks_for_region(meta, region, selection):
    """Create VRP blocks for a specific region and selection.

    Parameters
    ----------
    meta : dict
        Metadata table
    region : str
        Region as a string ("1j1b", "2j1b", "2j2b")
    selection : str
        Selection string for tree

    Returns
    -------
    list(str)
        VRP blocks
    """
    titles = meta["titles"]
    regions = meta["regions"]["r{}".format(region)]
    blocks = []
    for entry in regions:
        var = entry["var"]
        logscale = "TRUE" if entry["log"] else "FALSE"
        unit = titles[var]["unit"]
        unit = " [{}]".format(unit) if unit else ""
        bk = block(
            region,
            selection,
            var,
            "{}{}".format(titles[var]["rex"], unit),
            entry["nbins"],
            entry["xmin"],
            entry["xmax"],
            logscale,
        )
        blocks.append(bk)
    return blocks


def all_three_regions(meta, sel_1j1b, sel_2j1b, sel_2j2b):
    """Short cut function to get string for all region blocks.

    Parameters
    ----------
    meta : dict
        Metadata table
    sel_1j1b : str
        Selection for 1j1b region
    sel_2j1b : str
        Selection for 2j1b region
    sel_2j2b : str
        Selection for 2j2b region

    Returns
    -------
    str
        Joining of all blocks as a string
    """
    b1j1b = blocks_for_region(meta, "1j1b", sel_1j1b)
    b2j1b = blocks_for_region(meta, "2j1b", sel_2j1b)
    b2j2b = blocks_for_region(meta, "2j2b", sel_2j2b)
    return "{}\n\n{}\n\n{}".format(
        "\n\n".join(b1j1b),
        "\n\n".join(b2j1b),
        "\n\n".join(b2j2b)
    )


def fix_systematics(config):
    """Fix systematic definitions to work with validation plots.

    This will remove the config file and replace it with a new
    modified config with proper systematic definitions.

    Parameters
    ----------
    config : str
        Path of the config file.
    """
    whole = six.ensure_str(PosixPath(config).read_text())
    regions = regions_from(config)
    valplots = filter(lambda r: "VRP_" in r, regions)
    valplots_1j1b = [v for v in valplots if "1j1b" in v]
    valplots_2j1b = [v for v in valplots if "2j1b" in v]
    valplots_2j2b = [v for v in valplots if "2j2b" in v]
    valplots_1j1b = ",".join(valplots_1j1b)
    valplots_2j1b = ",".join(valplots_2j1b)
    valplots_2j2b = ",".join(valplots_2j2b)
    whole = whole.replace(
        "  Regions: reg1j1b", "  Regions: reg1j1b,{}".format(
            valplots_1j1b
        )
    ).replace(
        "  Regions: reg2j1b", "  Regions: reg2j1b,{}".format(
            valplots_2j1b
        )
    ).replace(
        "  Regions: reg2j2b", "  Regions: reg2j2b,{}".format(
            valplots_2j2b
        )
    )
    os.remove(config)
    with open(config, "w") as f:
        print(whole, file=f)
