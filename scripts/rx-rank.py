#!/usr/bin/env python

from __future__ import print_function

import sys
import os

import click

try:
    from pathlib import PosixPath
except ImportError:
    try:
        from pathlib2 import PosixPath
    except ImportError:
        try:
            from WtPyext.pathlib import PosixPath
        except ImportError:
            print("cannot import PosixPath from anywhere; exiting")
            exit(0)


BNL_CONDOR_HEADER = """
Universe        = vanilla
notification    = Error
notify_user     = ddavis@phy.duke.edu
GetEnv          = True
Executable      = {}
Output          = logs/job.out.trexntup.$(cluster).$(process)
Error           = logs/job.err.trexntup.$(cluster).$(process)
Log             = /tmp/ddavis/log.$(cluster).$(process)
request_memory  = 2.0G
"""

@click.command()
@click.argument("config", type=str)
def rx_rank(config):
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

    outfile = "condor.r.{}.sub".format(config_name)
    with open(outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)

    PosixPath("logs").mkdir(exist_ok=True)


if __name__ == "__main__":
    rx_rank()
