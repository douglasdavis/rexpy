import multiprocessing
import subprocess
import os
import pathlib
import shutil

from rexpy.confparse import regions_from, systematics_from, grouped_impact_arguments


TREX_EXE = shutil.which("trex-fitter")


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


def create_workspace(config, run_type, suffix):
    """Create workspace to run steps.

    Parameters
    ----------
    config : str or os.PathLike
        Original TRExFitter config file.
    run_type : str
        Run environment type: 'condor' or 'local'
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
    config_name = config_path.name
    workspace = (config_path.parent / f"rexpy-{run_type}-{config_path.stem}")
    if suffix:
        workspace = pathlib.PosixPath(f"{workspace}__{suffix}")
    workspace.mkdir(exist_ok=False)
    shutil.copyfile(config_path, workspace / "fit.conf")
    return workspace, workspace / "fit.conf"


def _run_n_step(args):
    p = subprocess.Popen(f"{args[0]} n {args[1]} Regions={args[2]}", shell=True)
    return p.wait()


def _run_wf_step(args):
    p = subprocess.Popen(f"{args[0]} wf {args[1]}", shell=True)
    return p.wait()


def _run_wf_step_blind(args):
    p = subprocess.Popen(f"{args[0]} wf {args[1]} FitBlind=True:Suffix=_asimov", shell=True)
    return p.wait()


def _run_dp_step(args):
    p = subprocess.Popen(f"{args[0]} dp {args[1]}", shell=True)
    return p.wait()


def _run_dp_step_blind(args):
    p = subprocess.Popen(f"{args[0]} dp {args[1]} FitBlind=True:Suffix=_asimov", shell=True)
    return p.wait()


def _run_r_draw_step(args):
    p = subprocess.Popen(f"{args[0]} r {args[1]} Ranking=plot", shell=True)
    return p.wait()


def _run_r_draw_step_blind(args):
    p = subprocess.Popen(
        f"{args[0]} r {args[1]} Ranking=plot:FitBlind=True:Suffix=_asimov", shell=True
    )
    return p.wait()


def _run_r_step(args):
    p = subprocess.Popen(f"{args[0]} r {args[1]} Ranking={args[2]}", shell=True)
    return p.wait()


def _run_r_step_blind(args):
    p = subprocess.Popen(
        f"{args[0]} r {args[1]} Ranking={args[2]}:FitBlind=True:Suffix=_asimov", shell=True
    )
    return p.wait()


def _run_i_step(args):
    p = subprocess.Popen(f"{args[0]} i {args[1]} GroupedImpact={args[2]}", shell=True)
    return p.wait()


def _run_i_step_blind(args):
    p = subprocess.Popen(
        f"{args[0]} i {args[1]} GroupedImpact={args[2]}:FitBlind=True:Suffix=_asimov",
        shell=True,
    )
    return p.wait()


def _run_i_combine_step(args):
    p = subprocess.Popen(f"{args[0]} i {args[1]} GroupedImpact=combine", shell=True)
    return p.wait()


def _run_i_combine_step_blind(args):
    p = subprocess.Popen(
        f"{args[0]} i {args[1]} GroupedImpact=combine:FitBlind=True:Suffix=_asimov",
        shell=True,
    )
    return p.wait()


def parallel_n_step(config, regions=None):
    """Parallelize the ntuple step via multiprocessing.

    Parameters
    ----------
    config : str
        Path of the config file.
    regions : list(str), optional
        Manually define regions.

    """
    curdir = os.getcwd()
    run_dir = pathlib.PosixPath(config).resolve().parent
    os.chdir(run_dir)
    if regions is None:
        regions = regions_from(config)
    args = [(TREX_EXE, config, region) for region in regions]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(_run_n_step, args)
    os.chdir(curdir)


def wfdp_step(config, do_blind=False):
    """Execute the wftp steps.

    Parameters
    ----------
    config : str
        Path of the config file.
    do_blind : bool
        Also run step in Asimov setup.

    """
    curdir = os.getcwd()
    run_dir = pathlib.PosixPath(config).resolve().parent
    os.chdir(run_dir)
    _run_wf_step((TREX_EXE, config))
    _run_dp_step((TREX_EXE, config))
    if do_blind:
        _run_wf_step_blind((TREX_EXE, config))
        _run_dp_step_blind((TREX_EXE, config))
    os.chdir(curdir)


def parallel_r_step(config, systematics=None, do_blind=False):
    """Parallelize the impart ranking step via multiprocessing.

    Parameters
    ----------
    config : str
        Path of the config file.
    systematics : list(str), optional
        Manually define the systematics.
    do_blind : bool
        Also run step in Asimov setup.

    """
    curdir = os.getcwd()
    run_dir = pathlib.PosixPath(config).resolve().parent
    os.chdir(run_dir)
    if systematics is None:
        systematics = systematics_from(config)
    args = [(TREX_EXE, config, sys) for sys in systematics]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(_run_r_step, args)
    if do_blind:
        pool.map(_run_r_step_blind, args)
    os.chdir(curdir)


def r_draw_step(config, do_blind=False):
    """Execute the ranking plot drawing step.

    Parameters
    ----------
    config : str
        Path of the config file.
    do_blind : bool
        Also run step in Asimov setup.

    """
    curdir = os.getcwd()
    run_dir = pathlib.PosixPath(config).resolve().parent
    os.chdir(run_dir)
    _run_r_draw_step((TREX_EXE, config))
    if do_blind:
        _run_r_draw_step_blind((TREX_EXE, config))
    os.chdir(curdir)


def parallel_i_step(config, do_blind=False):
    """Parallelize the grouped impact step via multiprocessing.

    Parameters
    ----------
    config : str
        Path of the config file.
    do_blind : bool
        Also run step in Asimov setup.

    """
    curdir = os.getcwd()
    run_dir = pathlib.PosixPath(config).resolve().parent
    os.chdir(run_dir)
    args = grouped_impact_arguments(config)
    groups = [a.split()[-1].split("=")[-1] for a in args]
    args = [(TREX_EXE, config, g) for g in groups]
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(_run_i_step, args)
    if do_blind:
        pool.map(_run_i_step_blind, args)
    os.chdir(curdir)


def i_combine_step(config, do_blind=False):
    """Execute the grouped impact combine step.

    Parameters
    ----------
    config : str
        Path of the config file.
    do_blind : bool
        Also run step in Asimov setup.

    """
    curdir = os.getcwd()
    run_dir = pathlib.PosixPath(config).resolve().parent
    os.chdir(run_dir)
    _run_i_combine_step((TREX_EXE, config))
    if do_blind:
        _run_i_combine_step_blind((TREX_EXE, config))
    os.chdir(curdir)
