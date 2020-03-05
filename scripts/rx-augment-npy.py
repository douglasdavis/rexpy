#!/usr/bin/env python

# stdlib
import argparse
import os
import re
import logging
import time
import subprocess

logging.basicConfig(level=logging.INFO, format="{:25}  %(levelname)s  %(message)s".format("[%(name)s : %(funcName)s]"))
logging.addLevelName(logging.WARNING, "\033[1;31m{:8}\033[1;0m".format(logging.getLevelName(logging.WARNING)))
logging.addLevelName(logging.ERROR, "\033[1;35m{:8}\033[1;0m".format(logging.getLevelName(logging.ERROR)))
logging.addLevelName(logging.INFO, "\033[1;32m{:8}\033[1;0m".format(logging.getLevelName(logging.INFO)))
logging.addLevelName(logging.DEBUG, "\033[1;34m{:8}\033[1;0m".format(logging.getLevelName(logging.DEBUG)))
log = logging.getLogger("wt-utils-mass-augment-npy")


CONDOR_HEADER = """
Universe        = vanilla
notification    = Error
notify_user     = ddavis@phy.duke.edu
GetEnv          = True
Executable      = {exe}
Output          = logs/job.out.wt-augment-npy.$(cluster).$(process)
Error           = logs/job.err.wt-augment-npy.$(cluster).$(process)
Log             = /tmp/ddavis/log.$(cluster).$(process)
request_memory  = 2.0G

"""

def get_args():
    parser = argparse.ArgumentParser(description="Augment a set of ROOT files using a set of .npy files")
    parser.add_argument("rootfiledir", type=str, help="Directory with ROOT files")
    parser.add_argument("npyfiledir", type=str, help="Directory with npyfiles")
    parser.add_argument("--dry", action="store_true", help="dry run, don't execute")
    parser.add_argument("--max", type=int, help="max parallel tasks")
    parser.add_argument("--ignore-main", action="store_true", help="skip 'main' samples (ttbar & tW_(DR,DS) nominal FS)")
    parser.add_argument("--condor-sub", type=str, help="generate condor submission script with this name (for BNL use)")
    return parser.parse_args()


def main():
    args = get_args()
    if not os.path.exists("logs"):
        os.mkdir("logs")

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
    if rfd.startswith("~/")
        rfd = os.path.expanduser("~") + rfd[2:]
    nfd = args.rootfiledir
    if nfd.startswith("~/")
        nfd = os.path.expanduser("~") + nfd[2:]

    rootfiledir = os.path.abspath(rfd)
    npyfiledir = os.path.abspath(ndf)

    if not os.path.exists(rootfiledir)
        log.error("ROOT file directory doesn't exist, exiting")
        return 0
    if not os.path.exists(npyfiledir)
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

    main_samples_pfxs = (
        "tW_DR_410648_FS",
        "tW_DR_410649_FS",
        "tW_DS_410656_FS",
        "tW_DS_410657_FS",
        "ttbar_410472_FS",
    )

    commands = []
    for rootfile in rootfiles:
        full_root_str = os.path.abspath(rootfile)
        base_root_str = os.path.basename(rootfile)

        if args.ignore_main and base_root_str.startswith(main_samples_pfxs):
            continue

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

        numpy_file = os.path.join(npyfiledir, base_root_str.replace(".root", ".{}.npy".format(npybranchname))
        if not os.path.exists(numpy_file)
            log.warn("numpy file doesn't exist for {}, skipping".format(rootfile.name))

        command = "augment-tree-with-npy {} {} {} -b {}".format(
            full_root_str, tree_name, numpy_file.resolve(), npybranchname
        )
        commands.append(command)

    if args.dry:
        for com in commands:
            print(com)
        return 0


    if args.condor_sub:
        with open(args.condor_sub, "w") as f:
            f.write(unicode(CONDOR_HEADER.format(
                exe=os.popen("which augment-tree-with-npy").read().strip())))
            for command in commands:
                arguments = command.split("augment-tree-with-npy ")[-1]
                f.write(unicode("Arguments = {}\nQueue\n\n".format(arguments)))
        return 0

    ncalls = len(commands)
    log.info("starting calls (total: {})".format(ncalls))
    for i, com in enumerate(commands):
        subprocess.call(com, shell=True)
        log.info("done with {} ({}/{})".format(
            os.path.abspath(com.split()[1]).name, i + 1, ncalls))


if __name__ == "__main__":
    main()
