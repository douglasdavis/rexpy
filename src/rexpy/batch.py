import os


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
        log=os.path.join(wkspace, "log")
    )
