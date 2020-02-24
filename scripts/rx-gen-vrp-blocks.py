#!/usr/bin/env python

from __future__ import print_function

import argparse
import yaml

BLOCK_TEMPLATE = """Region: "VRP_{region}_{var}"
  VariableTitle: "{title}"
  ShortLabel: "{region}"
  Selection: "{selection}"
  Type: VALIDATION
  Label: "{region}"
  Variable: "{var}",{nbins},{xmin},{xmax}
"""


def block(region, selection, var, title, nbins, xmin, xmax):
    return BLOCK_TEMPLATE.format(
        region=region,
        var=var,
        title=title,
        selection=selection,
        nbins=nbins,
        xmin=xmin,
        xmax=xmax,
    )


DESCRIPTION = (
    "Generate validation region TRExFitter blocks for plotting "
    "pre and post fit distributions of kinematic/bdt input featuress."
)


def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("metafile", type=str, help="metadata YAML file")
    return parser.parse_args()


def main():
    args = get_args()
    with open(args.metafile, "r") as f:
        metatable = yaml.load(f, Loader=yaml.Loader)
    title_table = metatable.pop("titles")
    region_table = metatable.pop("regions")
    blocks = []
    for entry in region_table["r1j1b"]:
        var = entry["var"]
        bk = block(
            "1j1b",
            "reg1j1b == 1 && OS == 1",
            var,
            title_table[var]["rex"],
            entry["nbins"],
            entry["xmin"],
            entry["xmax"],
        )
        blocks.append(bk)
    for entry in region_table["r2j1b"]:
        var = entry["var"]
        bk = block(
            "2j1b",
            "reg2j1b == 1 && OS == 1",
            var,
            title_table[var]["rex"],
            entry["nbins"],
            entry["xmin"],
            entry["xmax"],
        )
        blocks.append(bk)
    for entry in region_table["r2j2b"]:
        var = entry["var"]
        bk = block(
            "2j2b",
            "reg2j2b == 1 && OS == 1",
            var,
            title_table[var]["rex"],
            entry["nbins"],
            entry["xmin"],
            entry["xmax"],
        )
        blocks.append(bk)

    for bk in blocks:
        print(bk)


if __name__ == "__main__":
    main()
