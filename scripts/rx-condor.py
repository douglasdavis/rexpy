#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
import os

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
    PosixPath("logs").mkdir(exist_ok=True)
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


@cli.command("rank")
@click.argument("config", type=str)
def rank(config):
    """Generate a condor submission script to do the ranking plot steps"""
    PosixPath("logs").mkdir(exist_ok=True)
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
    cli()
