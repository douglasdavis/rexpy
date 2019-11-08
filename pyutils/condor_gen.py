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
Output          = .condor_stdout/job.out.trexntup.$(cluster).$(process)
Error           = .condor_stderr/job.err.trexntup.$(cluster).$(process)
Log             = /tmp/ddavis/log.$(cluster).$(process)
request_memory  = 2.0G
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="TRExFitter config file")
    parser.add_argument("outfile", type=str, help="output condor submit script")
    args = parser.parse_args()


def main():
    args = parse_args()
    full_config = str(PosixPath(args.config).resolve())
    commands = []
    with open(full_config, "r") as f:
        for line in f.readlines():
            if line.startswith(r"%"):
                continue
            elif line.startswith("Region:"):
                reg = line.strip().split("Region: ")[-1].replace('"', "")
                commands.append("n {} Region={}".format(full_config, reg))

    with open(args.outfile, "w") as f:
        exe = os.popen("which trex-fitter").read().strip()
        print(BNL_CONDOR_HEADER.format(exe), file=f)
        for com in commands:
            print("Arguments = {}".format(com), file=f)
            print("Queue\n", file=f)

if __name__ == "__main__":
    main()
