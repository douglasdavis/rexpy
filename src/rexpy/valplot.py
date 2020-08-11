# stdlib
import logging
import os
from pathlib import PosixPath

# third party
import requests
import yaml

# rexpy
from rexpy.confparse import regions_from


log = logging.getLogger(__name__)


BLOCK_TEMPLATE = """\
Region: "VRP_reg{region}_{var}"
  VariableTitle: "{title}"
  ShortLabel: "{region}"
  Selection: "{selection}"
  Type: VALIDATION
  Label: "{region}"
  Variable: "{var}",{nbins},{xmin},{xmax}
  LogScale: {logscale}"""


def block(region, selection, var, title, nbins, xmin, xmax, logscale):
    """Generate a VRP block.

    Parameters
    ----------
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


def blocks_for_region(meta, region, selection, is_preselection=False):
    """Create VRP blocks for a specific region and selection.

    Parameters
    ----------
    meta : dict
        Metadata table
    region : str
        Region as a string ("1j1b", "2j1b", "2j2b")
    selection : str
        Selection string for tree
    is_preselection : bool
        Use the preselection plotting definitions

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
        if not is_preselection:
            xmin = entry["xmin"]
            xmax = entry["xmax"]
        else:
            xmin = entry["xmin_pre"]
            xmax = entry["xmax_pre"]
            if xmin is None:
                xmin = entry["xmin"]
            if xmax is None:
                xmax = entry["xmax"]
        bk = block(
            region,
            selection,
            var,
            "{}{}".format(titles[var]["rex"], unit),
            entry["nbins"],
            xmin,
            xmax,
            logscale,
        )
        blocks.append(bk)
        log.info(
            "Validation plot block created in %s: %s (%s, %s, %s)"
            % (region, var, entry["nbins"], xmin, xmax)
        )
    return blocks


def blocks_for_all_regions(meta, sel_1j1b, sel_2j1b, sel_2j2b, is_preselection=False):
    """Shortcut function to get string for all region blocks.

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
    is_preselection : bool
        Use the preselection plotting definitions

    Returns
    -------
    str
        Joining of all blocks as a string
    """
    b1j1b = blocks_for_region(meta, "1j1b", sel_1j1b, is_preselection)
    b2j1b = blocks_for_region(meta, "2j1b", sel_2j1b, is_preselection)
    b2j2b = blocks_for_region(meta, "2j2b", sel_2j2b, is_preselection)
    return "{}\n\n{}\n\n{}\n".format(
        "\n\n".join(b1j1b), "\n\n".join(b2j1b), "\n\n".join(b2j2b)
    )


def default_vrp_blocks(sel_1j1b, sel_2j1b, sel_2j2b, is_preselection=False):
    meta_req = requests.get("https://cern.ch/ddavis/tdub_data/meta.yml")
    meta = yaml.full_load(meta_req.content)
    return blocks_for_all_regions(
        meta, sel_1j1b, sel_2j1b, sel_2j2b, is_preselection=is_preselection
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
    whole = PosixPath(config).read_text()
    regions = regions_from(config)
    valplots = list(filter(lambda r: "VRP_" in r, regions))
    valplots_1j1b = sorted([v for v in valplots if "1j1b" in v], key=str.lower)
    valplots_2j1b = sorted([v for v in valplots if "2j1b" in v], key=str.lower)
    valplots_2j2b = sorted([v for v in valplots if "2j2b" in v], key=str.lower)
    valplots_1j1b = ",".join(valplots_1j1b)
    valplots_2j1b = ",".join(valplots_2j1b)
    valplots_2j2b = ",".join(valplots_2j2b)
    log.info("replacing 'Regions: reg1j1b' with:")
    log.info("'  Regions : reg1j1b,%s'" % valplots_1j1b)
    log.info("replacing 'Regions: reg2j1b' with:")
    log.info("'  Regions : reg2j1b,%s'" % valplots_2j1b)
    log.info("replacing 'Regions: reg2j2b' with:")
    log.info("'  Regions : reg2j2b,%s'" % valplots_2j2b)
    whole = (
        whole.replace("  Regions: reg1j1b", "  Regions: reg1j1b,{}".format(valplots_1j1b))
        .replace("  Regions: reg2j1b", "  Regions: reg2j1b,{}".format(valplots_2j1b))
        .replace("  Regions: reg2j2b", "  Regions: reg2j2b,{}".format(valplots_2j2b))
    )
    os.remove(config)
    with open(config, "w") as f:
        print(whole, file=f)
