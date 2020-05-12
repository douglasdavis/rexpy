#!/usr/bin/env python

# stdlib
import argparse
import glob
import logging
import os
import re
import time
import subprocess

from rexuple.batch import job_params
import rexuple.pycondor as pycondor
from rexuple import setup_logging
setup_logging()

log = logging.getLogger("rx-augment-npy")


def get_args():
    parser = argparse.ArgumentParser(description="Augment a set of ROOT files using a set of .npy files")
    parser.add_argument("rootfiledir", type=str, help="Directory with ROOT files")
    parser.add_argument("npyfiledir", type=str, help="Directory with npyfiles")
    parser.add_argument("--dry", action="store_true", help="dry run, don't execute")
    parser.add_argument("--condor-sub", type=str, help="generate condor submission workspace (for BNL use)")
    parser.add_argument("--dont-submit", action="store_true", help="dont submit condor")
    return parser.parse_args()


def main():
    args = get_args()

    npyfile_re = re.compile(r"((?P<name>\w+)\.(?P<branch>\w+)\.npy)")
    sample_info_re = re.compile(
        r"""(?P<phy_process>\w+)_
        (?P<dsid>[0-9]{6})_
        (?P<sim_type>(FS|AFII))_
        (?P<campaign>MC16(a|d|e))_
        (?P<tree>\w+)
        (\.\w+|$)""",
        re.X,
    )

    rfd = args.rootfiledir
    if rfd.startswith("~/"):
        rfd = os.path.expanduser("~") + rfd[2:]
    nfd = args.npyfiledir
    if nfd.startswith("~/"):
        nfd = os.path.expanduser("~") + nfd[2:]

    rootfiledir = os.path.abspath(rfd)
    npyfiledir = os.path.abspath(nfd)

    if not os.path.exists(rootfiledir):
        log.error("ROOT file directory doesn't exist, exiting")
        return 0
    if not os.path.exists(npyfiledir):
        log.error("numpy file directory doesn't exist, exiting")
        return 0

    npyfiles = glob.glob("{}/*.npy".format(npyfiledir))
    rootfiles = glob.glob("{}/*.root".format(rootfiledir))

    log.info("ROOT directory: {}".format(rootfiledir))
    log.info("numpy directory: {}".format(npyfiledir))

    npybranchname = None
    for npyfile in npyfiles:
        reres = re.match(npyfile_re, os.path.basename(npyfile))
        if reres:
            npybranchname = reres.group("branch")
            if npybranchname:
                break

    if npybranchname is None:
        log.error("couldn't determine numpy array -> branch name, exiting")
        return 0

    log.info("Determined numpy branch name: {}".format(npybranchname))

    commands = []
    for rootfile in rootfiles:
        full_root_str = os.path.abspath(rootfile)
        base_root_str = os.path.basename(rootfile)

        if not full_root_str.endswith(".root"):
            continue
        if "Data_Data" in base_root_str:
            tree_name = "nominal"
        else:
            try:
                tree_name = re.match(sample_info_re, base_root_str).group("tree")
            except IndexError:
                continue

        tree_name = "WtLoop_{}".format(tree_name)

        numpy_file = os.path.join(npyfiledir, base_root_str.replace(".root", ".{}.npy".format(npybranchname)))
        if not os.path.exists(numpy_file):
            log.warn("numpy file doesn't exist for {}, skipping".format(rootfile.name))

        command = "{} {} {} {}".format(
            full_root_str, tree_name, os.path.abspath(numpy_file), npybranchname
        )
        commands.append(command)

    if args.dry:
        for com in commands:
            print(com)
        return 0

    if args.condor_sub:
        workspace = os.path.abspath(args.condor_sub)
        os.mkdir(workspace)
        dagman = pycondor.Dagman(name="rx-augment-npy", submit=os.path.join(workspace, "sub"))
        params = job_params(workspace, os.popen("which augment-tree-with-npy").read().strip())
        augjob = pycondor.Job(name="augment", dag=dagman, **params)
        augjob.add_args(commands)
        orig_path = os.getcwd()
        os.chdir(workspace)
        if args.dont_submit:
            dagman.build()
        else:
            dagman.build_submit()
        os.chdir(orig_path)
        return 0

    ncalls = len(commands)
    log.info("starting calls (total: {})".format(ncalls))
    for i, com in enumerate(commands):
        subprocess.call("augment-tree-with-npy {}".format(com), shell=True)
        log.info("done with {} ({}/{})".format(
            os.path.abspath(com.split()[1]).name, i + 1, ncalls))


if __name__ == "__main__":
    main()
