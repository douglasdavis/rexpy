#!/usr/bin/env python

from __future__ import print_function

import argparse
import fileinput
import re

DESCRIPTION = (
    "Toggle the blind fit setting in a "
    "trex-fitter configuration file. This "
    "will augment '_asimov' to the end of the "
    "fit name if it's set to unblinded mode. "
    "If the script is set to blind mode, it "
    "expects an '_asimov' suffix to exist in "
    "the Job and Fit name and it will remove that suffix"
)


def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "inputfile", type=str, help="input file to asimov-ify or unasimov-ify"
    )
    return parser.parse_args()


def main():
    args = get_args()
    is_asimov = False
    with open(args.inputfile, "r") as f:
        for line in f.readlines():
            if "FitBlind: TRUE" in line:
                is_asimov = True
                print("already asimov")
                break

    lines = []
    if is_asimov:
        with open(args.inputfile, "r") as f:
            for line in f:
                if 'Job: "tW' in line or 'Fit: "tW' in line:
                    line = line.replace("_asimov", "")
                elif "FitBlind: TRUE" in line:
                    line = line.replace("TRUE", "FALSE")
                lines.append(line)
        with open(args.inputfile, "w") as f:
            for line in lines:
                f.write(line)
        exit(0)

    else:
        with open(args.inputfile, "r") as f:
            for line in f:
                if 'Job: "tW' in line or 'Fit: "tW' in line:
                    line = '{}_asimov"\n'.format(line[:-2])
                elif "FitBlind: FALSE" in line:
                    line = line.replace("FALSE", "TRUE")
                lines.append(line)
        with open(args.inputfile, "w") as f:
            for line in lines:
                f.write(line)


if __name__ == "__main__":
    main()
