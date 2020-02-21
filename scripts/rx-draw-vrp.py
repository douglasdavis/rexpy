#!/usr/bin/env python

from __future__ import print_function

import argparse
import subprocess
import time
import os

DESCRIPTION = "run the trex-fitter dp step on a config"


def get_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("config", type=str, help="trex-fitter config")
    parser.add_argument("--skip", type=str, nargs="+", help="skip VRP")
    parser.add_argument("--max", dest="maxn", type=int, default=6, help="max parallel jobs")
    parser.add_argument("--dry", action="store_true", help="dry run it")
    parser.add_argument("--steps", type=str, default="dp",
                        choices=["d", "p", "dp"], help="trex-fitter step incantation")
    return parser.parse_args()


def get_regions(config_file, skips):
    regions = []
    skips = skips if skips is not None else []
    with open(config_file, "r") as f:
        for line in f.readlines():
            if "Region: " in line and "VRP" in line:
                region = line.strip().split("Region: ")[-1].replace('"', "")
                if region in skips:
                    continue
                regions.append(region)
    return regions


def runem(tasks, max_n):
    coms = tasks[:]
    taskn, procs, todo, done = 0, [], len(tasks), 0
    FNULL = open(os.devnull, "w")
    while True:
        while coms and len(procs) < max_n:
            task = coms.pop()
            taskn += 1
            procs.append(subprocess.Popen(task, shell=True, stdout=FNULL, stderr=FNULL))

        for p in procs:
            if p.poll() is not None:
                if p.returncode == 0:
                    done += 1
                    print("done with {}/{}".format(done, todo))
                    procs.remove(p)
                else:
                    print("return code is nonzero ({}) for pid {}".format(p.returncode, p.pid))

        if not procs and not coms:
            break
        else:
            time.sleep(0.25)

    FNULL.close()
    return 0


def main():
    args = get_args()
    regions = get_regions(args.config, args.skip)
    tasks = [
        "trex-fitter {} {} Regions={}".format(
            args.steps, args.config, r
        ) for r in regions
    ]
    if args.dry:
        for t in tasks:
            print(t)
        return 0
    runem(tasks, args.maxn)


if __name__ == "__main__":
    main()
