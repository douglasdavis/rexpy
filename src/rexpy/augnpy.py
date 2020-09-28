import glob
import logging
import os
import re
import subprocess
import shutil

from rexpy.batch import job_params
import rexpy.pycondor as pycondor

log = logging.getLogger(__name__)


def get_branch_name(npyfiles):
    npyfile_re = re.compile(r"((?P<name>\w+)\.(?P<branch>\w+)\.npy)")
    npybranchname = None
    for npyfile in npyfiles:
        reres = re.match(npyfile_re, os.path.basename(npyfile))
        if reres:
            npybranchname = reres.group("branch")
            if npybranchname:
                break
    if npybranchname is None:
        log.error("couldn't determine numpy array -> branch name, exiting")
        exit(1)
    log.info("Determined numpy branch name: {}".format(npybranchname))
    return npybranchname


def commands(rootfiledir, npyfiledir):
    npyfiles = glob.glob("{}/*.npy".format(npyfiledir))
    rootfiles = glob.glob("{}/*.root".format(rootfiledir))
    sample_info_re = re.compile(
        r"""(?P<phy_process>\w+)_
        (?P<dsid>[0-9]{6})_
        (?P<sim_type>(FS|AFII))_
        (?P<campaign>MC16(a|d|e))_
        (?P<tree>\w+)
        (\.\w+|$)""",
        re.X,
    )
    npybranchname = get_branch_name(npyfiles)
    coms = []
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
        numpy_file = os.path.join(
            npyfiledir, base_root_str.replace(".root", ".{}.npy".format(npybranchname))
        )
        if not os.path.exists(numpy_file):
            log.warn("numpy file doesn't exist for {}, skipping".format(rootfile.name))
        command = "{} {} {} {}".format(
            full_root_str, tree_name, os.path.abspath(numpy_file), npybranchname
        )
        coms.append(command)
    return coms


def condor(workspace, coms, submit):
    workspace = os.path.abspath(workspace)
    os.mkdir(workspace)
    dagman = pycondor.Dagman(name="rp-augment-npy", submit=os.path.join(workspace, "sub"))
    params = job_params(workspace, shutil.which("augment-tree-with-npy"))
    augjob = pycondor.Job(name="augment", dag=dagman, **params)
    augjob.add_args(coms)
    orig_path = os.getcwd()
    os.chdir(workspace)
    if submit:
        dagman.build_submit()
    else:
        dagman.build()
    os.chdir(orig_path)
    return 0


def local(coms):
    ncalls = len(coms)
    log.info("starting calls (total: {})".format(ncalls))
    for i, com in enumerate(coms):
        subprocess.call("augment-tree-with-npy {}".format(com), shell=True)
        log.info(
            "done with {} ({}/{})".format(
                os.path.abspath(com.split()[1]).name, i + 1, ncalls
            )
        )
    return 0


def augment(rootfiledir, npyfiledir, dry, condor_sub, dont_submit):
    log.info("ROOT directory: {}".format(rootfiledir))
    log.info("numpy directory: {}".format(npyfiledir))
    coms = commands(rootfiledir, npyfiledir)
    if dry:
        for com in coms:
            print(com)
        return 0
    elif condor_sub:
        condor(condor_sub, coms, dont_submit)
    else:
        local(coms)

    return 0
