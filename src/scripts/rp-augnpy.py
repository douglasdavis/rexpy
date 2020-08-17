#!/usr/bin/env python

from rexpy.augnpy import augment
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Augment a set of ROOT files using a set of .npy files")
    parser.add_argument("rootfiledir", type=str, help="Directory with ROOT files")
    parser.add_argument("npyfiledir", type=str, help="Directory with npyfiles")
    parser.add_argument("--dry", action="store_true", help="dry run, don't execute")
    parser.add_argument("--condor-sub", type=str, help="generate condor submission workspace (for BNL use)")
    parser.add_argument("--dont-submit", action="store_true", help="dont submit condor")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    augment(args.rootfiledir, args.npyfiledir, args.dry, args.condor_sub, args.dont_submit)
