#!/usr/bin/env python

from __future__ import print_function

import click

from rexuple.parse_conf import get_blocks


def remove_region(config_blocks, region):
    new_blocks = []
    for block in config_blocks:
        if block.startswith("Region:"):
            if region in block:
                continue
        if block.startswith("Systematic:"):
            if region in block:
                continue
        new_blocks.append(block)

    summary_plot_regions_o = new_blocks[0].split("SummaryPlotRegions: ")[-1].split()[0]
    summary_plot_regions_n = summary_plot_regions_o.split(",")
    if region in summary_plot_regions_n:
        summary_plot_regions_n.remove(region)
    new_blocks[0] = new_blocks[0].replace(
        summary_plot_regions_o, ",".join(summary_plot_regions_n)
    )
    return new_blocks


@click.command()
@click.argument("config", type=click.Path(exists=True))
@click.option("-r", "--region", type=str, multiple=True)
def main(config, region):
    blocks = get_blocks(config)
    for r in region:
        blocks = remove_region(blocks, r)
    print("\n\n".join(blocks))


if __name__ == "__main__":
    main()
