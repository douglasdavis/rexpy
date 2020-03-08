#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
import os

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

DESCRIPTION = (
    "Generate a condor submission script which "
    "generates histograms one region at a time "
    "via the trex-fitter 'n' option"
)


def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("config", type=str, help="TRExFitter config file")
    parser.add_argument("--quick", action="store_true", help="generate a quick submission (Lumi systematic only")
    return parser.parse_args()


def main():
    args = get_args()
    config_name = PosixPath(args.config).name
    if args.quick:
        outfile = "condor.ntup.quick.{}.sub".format(config_name)
    else:
        outfile = "condor.ntup.{}.sub".format(config_name)
    full_config = str(PosixPath(args.config).resolve())
    commands = []
    with open(full_config, "r") as f:
        for line in f.readlines():
            if line.startswith(r"%"):
                continue
            elif line.startswith("Region:"):
                reg = line.strip().split("Region: ")[-1].replace('"', "")
                if args.quick:
                    commands.append("n {} Systematics=Lumi:Regions={}".format(full_config, reg))
                else:
                    commands.append("n {} Regions={}".format(full_config, reg))

    with open(outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)

    PosixPath("logs").mkdir(exist_ok=True)


if __name__ == "__main__":
    main()
