#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import re
import sys

import click
from pathlib2 import PosixPath


BNL_CONDOR_HEADER = """
Universe        = vanilla
notification    = Error
notify_user     = ddavis@phy.duke.edu
GetEnv          = True
Executable      = {0}
Output          = logs/job.out.{1}.$(cluster).$(process)
Error           = logs/job.err.{1}.$(cluster).$(process)
Log             = /tmp/ddavis/log.$(cluster).$(process)
request_memory  = 2.0G
"""

CONTEXT_SETTINGS = {"max_content_width": 92}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command("ntup")
@click.argument("config")
@click.option("--quick", is_flag=True, help="generate a 'quick' submission (Lumi sys only)")
@click.option("--this-sys", type=str, help="do a single user defined systematic")
def ntup(config, quick, this_sys):
    """Generate a condor submission script for the ntuple creation step of TRExFitter"""
    config_name = PosixPath(config).name
    if quick:
        if this_sys is not None:
            print("--quick and --this-sys cannot be used together")
            exit(1)
        outfile = "condor.ntup.quick.{}.sub".format(config_name)
    elif this_sys is not None:
        outfile = "condor.ntup.{}.{}.sub".format(this_sys, config_name)
    else:
        outfile = "condor.ntup.{}.sub".format(config_name)
    full_config = str(PosixPath(config).resolve())
    commands = []
    with open(full_config, "r") as f:
        for line in f.readlines():
            if line.startswith(r"%"):
                continue
            elif line.startswith("Region:"):
                reg = line.strip().split("Region: ")[-1].replace('"', "")
                if quick:
                    commands.append("n {} Systematics=Lumi:Regions={}".format(full_config, reg))
                elif this_sys is not None:
                    commands.append("n {} Systematics={}:Regions={}".format(full_config, this_sys, reg))
                else:
                    commands.append("n {} Regions={}".format(full_config, reg))

    with open(outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe, "ntup"), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)


@cli.command("fit")
@click.option("--config", "-c", multiple=True, type=str, help="config file(s) to fit")
def fit(config):
    """Generate a condor submission script to run the fit step on some config files"""
    configs = [str(PosixPath(c).resolve()) for c in config]
    outfile = "condor.fit.sub"
    with open(outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe, "fit"), file=f)
        for conf in configs:
            print("Arguments = wf {}".format(conf), file=f)
            print("Queue\n", file=f)


@cli.command("draw")
@click.option("--config", "-c", multiple=True, type=str, help="config file(s) to draw")
@click.option("--postfit", "-p", is_flag=True, help="also run the postfit draw step")
def draw(config, postfit):
    """Generate a condor submission script to run the drawing steps on some config files"""
    region_re = re.compile(r"^Region: \"\w+\"")
    def get_arguments(config_file, do_postfit):
        regions = []
        with open(config_file, "r") as f:
            for line in f.readlines():
                if region_re.match(line):
                    region = line.strip().split("Region: ")[-1].replace('"', "")
                    regions.append(region)
        arguments = []
        prefix = "dp" if do_postfit else "d"
        for region in regions:
            arguments.append("{} {} Regions={}".format(prefix, config_file, region))
        return arguments

    configs = [str(PosixPath(c).resolve()) for c in config]
    outfile = "condor.draw.sub"
    with open(outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe, "draw"), file=f)
        for conf in configs:
            args = get_arguments(conf, postfit)
            for arg in args:
                print("Arguments = {}".format(arg), file=f)
                print("Queue\n", file=f)


@cli.command("rank")
@click.argument("config", type=str)
def rank(config):
    """Generate a condor submission script to do the ranking plot steps"""
    config_file = PosixPath(config)
    config_name = config_file.name
    full_config = str(config_file.resolve())
    systematics, commands = [], []
    with open(full_config, "r") as f:
        for line in f.readlines():
            if line.startswith(r"%"):
                continue
            elif line.startswith("Systematic:"):
                s = line.strip().split("Systematic: ")[-1].replace('"', "")
                systematics.append(s)
    systematics = set(systematics)
    for s in systematics:
        commands.append("r {} Ranking={}".format(full_config, s))

    outfile = "condor.rank.{}.sub".format(config_name)
    with open(outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe, "rank"), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)


if __name__ == "__main__":
    PosixPath("logs").mkdir(exist_ok=True)
    cli()
