"""Module for handling batch steps."""

# stdlib
import multiprocessing
import subprocess
import os
import pathlib
import shutil
from functools import wraps

# rexpy
import rexpy.pycondor as pycondor
from rexpy.confparse import (
    regions_from,
    systematics_from,
    sub_block_values,
)


TREX_EXE = shutil.which("trex-fitter")


def rank_arguments(config, specific_sys=None):
    """Get a set of trex-fitter executable arguments for ranking.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments.
    """
    systematics = systematics_from(config, specific_sys=specific_sys)
    args = ["r {} Ranking={}".format(config, sys) for sys in systematics]
    return args


def grouped_impact_arguments(config):
    """Get a set of trex-fitter executable arguments for grouped impact.

    Parameters
    ----------
    config : str
        Path of the config file.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments
    """
    groups = sub_block_values(config, "SubCategory")
    groups = list(groups) + ["Gammas", "FullSyst"]
    args = ["i {} GroupedImpact={}".format(config, g) for g in groups]
    return args


def draw_argument(config, specific_sys=None):
    """Get the draw trex-fitter step argument"

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    str
        the fit step argument
    """
    if specific_sys is not None:
        systs = ",".join(systematics_from(config, specific_sys))
        arg = "dp {} Systematics={}".format(config, systs)
    else:
        arg = "dp {}".format(config)

    return arg


def fit_argument(config, specific_sys=None, dont_fit_vr=True):
    """Get the fit trex-fitter step argument.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        Specific systematics to use; if None (the default), uses all
        discovered systematics.
    dont_fit_vr : bool
        Do not include VR regions in fit argument.

    Returns
    -------
    str
        the fit step argument
    """
    region_arg = ""
    if dont_fit_vr:
        regions = regions_from(config)
        regions = [r for r in regions if not r.startswith("VR")]
        region_arg = " Regions={}".format(",".join(regions))

    arg = f"wf {config}{region_arg}"
    arg = arg.strip()

    if specific_sys is not None:
        systematics = systematics_from(config, specific_sys=specific_sys)
        systematics = ",".join(systematics)
        arg = f"{arg}:Systematics={systematics}"

    return arg


def ntuple_arguments_granular(config, fitname="tW"):
    """Get the set of granular trex-fitter ntupling instructions

    Parameters
    ----------
    config : str
        Path of the config file.
    fitname : str
        Name of the fit.

    Returns
    -------
    list(str)
        trex-fitter n step arguments.
    list(str)
        hupdate.exe execution instructions.

    """
    regions = regions_from(config)
    systematics = systematics_from(config)
    region_hupdate_files = {r: [] for r in regions}
    args = []
    for r in regions:
        for s in systematics:
            if "1j1b" in s and "1j1b" not in r:
                continue
            if "2j1b" in s and "2j1b" not in r:
                continue
            if "2j2b" in s and "2j2b" not in r:
                continue
            args.append(f"n {config} Regions={r}:Systematics={s}:SaveSuffix=_{s}")
            region_hupdate_files[r].append(
                f"{fitname}/Histograms/{fitname}_{r}_histos_{s}.root"
            )
    updates = []
    for k, v in region_hupdate_files.items():
        a1 = f"{fitname}/Histograms/{fitname}_{k}_histos.root"
        a2 = " ".join(v)
        updates.append(f"{a1} {a2}")
    return args, updates


def ntuple_arguments(config, specific_sys=None):
    """Get the set of trex-fitter executable arguments for ntupling.

    Parameters
    ----------
    config : str
        Path of the config file.
    specific_sys : iterable(str), optional
        The set of systematics to use; if None (the default), uses all
        discovered systematics.

    Returns
    -------
    list(str)
        The list of trex-fitter arguments

    """
    regions = regions_from(config)

    # first no specific systematics
    if specific_sys is None:
        return ["n {} Regions={}".format(config, r) for r in regions]

    # otherwise, construct for specific systematics
    systematics = systematics_from(config, specific_sys=specific_sys)
    systematics = ",".join(systematics)
    return [
        "n {} Regions={}:Systematics={}".format(config, r, systematics) for r in regions
    ]


def job_params(wkspace, executable, **kwargs):
    """Turn a set of keyword arguments into a condor preamble.

    Parameters
    ----------
    wkspace : str
        Path of the condor workspace to create.
    executable : str
        Executable path (``trex-fitter``).
    kwargs : dict
        Args used to build the submission script preamble.

    Returns
    -------
    dict
        Arguments for use with pycondor.

    """
    universe = kwargs.get("universe", "vanilla")
    getenv = kwargs.get("getenv", True)
    notification = kwargs.get("notification", "Error")
    request_memory = kwargs.get("request_memory", "2GB")
    extra_lines = kwargs.get("extra_lines", ["notify_user = ddavis@phy.duke.edu"])
    return dict(
        executable=executable,
        universe=universe,
        getenv=getenv,
        notification=notification,
        request_memory=request_memory,
        extra_lines=extra_lines,
        submit=os.path.join(wkspace, "sub"),
        error=os.path.join(wkspace, "err"),
        output=os.path.join(wkspace, "out"),
        log=os.path.join(wkspace, "log"),
    )


def create_workspace(config, suffix=None):
    """Create workspace to run steps and store results.

    Parameters
    ----------
    config : str or os.PathLike
        Original TRExFitter config file.
    suffix : str, optional
        Add a suffix to the workspace

    Returns
    -------
    pathlib.PosixPath
        Created workspace path.
    pathlib.PosixPath
        Copy of configuration file in the workspace.

    """
    config_path = pathlib.PosixPath(config)
    workspace = config_path.parent / f"{config_path.stem}.d"
    if suffix is not None:
        workspace = pathlib.PosixPath(f"{config_path.stem}.{suffix}.d")
    workspace.mkdir(exist_ok=True)
    if not (workspace / "fit.conf").exists():
        shutil.copyfile(config_path, workspace / "fit.conf")
    return workspace.absolute(), (workspace / "fit.conf").absolute()


def run_and_wait(command):
    p = subprocess.Popen(command, shell=True)
    return p.wait()


def parallel_run(commands, processes=None):
    pool = multiprocessing.Pool(processes=processes)
    pool.map(run_and_wait, commands)


def _run_n_step(args):
    p = subprocess.Popen(f"{args[0]} n {args[1]} Regions={args[2]}", shell=True)
    return p.wait()


def _run_wf_step(args):
    p = subprocess.Popen(f"{args[0]} wf {args[1]}", shell=True)
    return p.wait()


def _run_dp_step(args):
    p = subprocess.Popen(f"{args[0]} dp {args[1]}", shell=True)
    return p.wait()


def _run_r_draw_step(args):
    p = subprocess.Popen(f"{args[0]} r {args[1]} Ranking=plot", shell=True)
    return p.wait()


def _run_r_step(args):
    p = subprocess.Popen(f"{args[0]} r {args[1]} Ranking={args[2]}", shell=True)
    return p.wait()


def _run_i_step(args):
    p = subprocess.Popen(f"{args[0]} i {args[1]} GroupedImpact={args[2]}", shell=True)
    return p.wait()


def _run_i_combine_step(args):
    p = subprocess.Popen(f"{args[0]} i {args[1]} GroupedImpact=combine", shell=True)
    return p.wait()


def restore_cwd(func):
    """Decorator to enforce preservation of current working directory.

    Functions executing TRExFitter steps locally are designed to
    execute TRExFitter from the directory where the config file lives.
    We are not always running the python executable from that
    directory, so we change to the config file's parent directory with
    :py:func:`os.chdir` in all of those functions. This decorator
    ensures that we return back to the current working directory
    before that function was called.

    Parameters
    ----------
    func : callable
        Function to call (expected to call :py:func:`os.chdir`)

    """

    @wraps(func)
    def decorator(*args, **kwargs):
        cwd = os.getcwd()
        res = func(*args, **kwargs)
        os.chdir(cwd)
        return res

    return decorator


@restore_cwd
def parallel_n_step(config, regions=None, processes=None):
    """Parallelize the ntuple step via multiprocessing.

    Parameters
    ----------
    config : str
        Path of the config file.
    regions : list(str), optional
        Manually define regions.
    processes : int, optional
        Max number of processes to run in parallel

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    if regions is None:
        regions = regions_from(config)
    args = [(TREX_EXE, config, region) for region in regions]
    pool = multiprocessing.Pool(processes=processes)
    pool.map(_run_n_step, args)


@restore_cwd
def wfdp_step(config):
    """Execute the wftp steps.

    Parameters
    ----------
    config : str
        Path of the config file.

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    _run_wf_step((TREX_EXE, config))
    _run_dp_step((TREX_EXE, config))


@restore_cwd
def wf_step(config):
    """Execute the wf steps.

    Parameters
    ----------
    config : str
        Path of the config file.

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    _run_wf_step((TREX_EXE, config))


@restore_cwd
def dp_step(config):
    """Execute the dp steps.

    Parameters
    ----------
    config : str
        Path of the config file.

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    _run_dp_step((TREX_EXE, config))


@restore_cwd
def parallel_r_step(config, systematics=None, processes=None):
    """Parallelize the impart ranking step via multiprocessing.

    Parameters
    ----------
    config : str
        Path of the config file.
    systematics : list(str), optional
        Manually define the systematics.
    processes : int, optional
        Max number of processes to run in parallel

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    if systematics is None:
        systematics = systematics_from(config)
    args = [(TREX_EXE, config, sys) for sys in systematics]
    pool = multiprocessing.Pool(processes=processes)
    pool.map(_run_r_step, args)


@restore_cwd
def r_draw_step(config):
    """Execute the ranking plot drawing step.

    Parameters
    ----------
    config : str
        Path of the config file.

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    _run_r_draw_step((TREX_EXE, config))


@restore_cwd
def parallel_i_step(config, processes=None):
    """Parallelize the grouped impact step via multiprocessing.

    Parameters
    ----------
    config : str
        Path of the config file.
    processes : int, optional
        Max number of processes to run in parallel

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    args = grouped_impact_arguments(config)
    groups = [a.split()[-1].split("=")[-1] for a in args]
    args = [(TREX_EXE, config, g) for g in groups]
    pool = multiprocessing.Pool(processes=processes)
    pool.map(_run_i_step, args)


@restore_cwd
def i_combine_step(config):
    """Execute the grouped impact combine step.

    Parameters
    ----------
    config : str
        Path of the config file.

    """
    os.chdir(pathlib.PosixPath(config).resolve().parent)
    _run_i_combine_step((TREX_EXE, config))


def condor_n_step(wkspace, sys=None, job_name="ntuple", dag=None):
    """Generate a condor job for running the ntuple step.

    Parameters
    ----------
    wkspace : pathlib.Path
        Path of the config file.
    sys : list(str), optional
        Specific ystematics to use.
    job_name : str
        Name for the condor job.
    dag : pycondor.Dagman, optional
        Dagman to assign the job to.

    Returns
    -------
    pycondor.Job
        Condor job with necessary arguments.

    """
    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    ntup_args = ntuple_arguments(config, specific_sys=sys)
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_args(ntup_args)
    return j


def condor_dp_step(wkspace, sys=None, job_name="draw", dag=None):
    """Generate a condor job for running the drawing steps.

    Parameters
    ----------
    wkspace : pathlib.Path
        Path of the config file.
    sys : list(str), optional
        Specific ystematics to use.
    job_name : str
        Name for the condor job.
    dag : pycondor.Dagman, optional
        Dagman to assign the job to.

    Returns
    -------
    pycondor.Job
        Condor job with necessary arguments.

    """
    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_arg(draw_argument(config, specific_sys=sys))
    return j


def condor_wf_step(wkspace, sys=None, job_name="wf", dag=None):
    """Generate a condor job for running the fitting steps.

    Parameters
    ----------
    wkspace : pathlib.Path
        Path of the config file.
    sys : list(str), optional
        Specific ystematics to use.
    job_name : str
        Name for the condor job.
    dag : pycondor.Dagman, optional
        Dagman to assign the job to.

    Returns
    -------
    pycondor.Job
        Condor job with necessary arguments.

    """
    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    fit_arg = fit_argument(config, specific_sys=sys)
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_arg(fit_arg)
    return j


def condor_r_step(wkspace, sys=None, job_name="rank", dag=None):
    """Generate a condor job for running the ranking steps.

    Parameters
    ----------
    wkspace : pathlib.Path
        Path of the config file.
    sys : list(str), optional
        Specific ystematics to use.
    job_name : str
        Name for the condor job.
    dag : pycondor.Dagman, optional
        Dagman to assign the job to.

    Returns
    -------
    pycondor.Job
        Condor job with necessary arguments.

    """
    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    rank_args = rank_arguments(config, specific_sys=sys)
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_args(rank_args)
    return j


def condor_rplot_step(wkspace, job_name="rplot", dag=None):
    """Generate a condor job for running the ranking steps.

    Parameters
    ----------
    wkspace : pathlib.Path
        Path of the config file.
    job_name : str
        Name for the condor job.
    dag : pycondor.Dagman, optional
        Dagman to assign the job to.

    Returns
    -------
    pycondor.Job
        Condor job with necessary arguments.

    """

    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_arg(f"r {config} Ranking=plot")
    return j


def condor_i_step(wkspace, job_name="impact", dag=None):
    """Generate a condor job for running the ranking steps.

    Parameters
    ----------
    wkspace : pathlib.Path
        Path of the config file.
    job_name : str
        Name for the condor job.
    dag : pycondor.Dagman, optional
        Dagman to assign the job to.

    Returns
    -------
    pycondor.Job
        Condor job with necessary arguments.

    """
    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    impact_args = grouped_impact_arguments(config)
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_args(impact_args)
    return j


def condor_icombine_step(wkspace, job_name="impactcomb", dag=None):
    jp = job_params(wkspace, TREX_EXE)
    config = wkspace / "fit.conf"
    j = pycondor.Job(name=job_name, dag=dag, **jp)
    j.add_arg(f"i {config} GroupedImpact=combine")
    return j
