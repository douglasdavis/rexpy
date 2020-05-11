import os


def job_params(workspace, executable, **kwargs):
    universe = kwargs.get("universe", "vanilla")
    getenv = kwargs.get("getenv", True)
    notification = kwargs.get("notification", "Error")
    request_memory = kwargs.get("request_memory", "2GB")
    extra_lines = kwargs.get("extra_lines", ["email = ddavis@phy.duke.edu"])
    return dict(
        executable=executable,
        universe=universe,
        getenv=getenv,
        notification=notification,
        request_memory=request_memory,
        extra_lines=extra_lines,
        submit=os.path.join(workspace, "sub"),
        error=os.path.join(workspace, "err"),
        output=os.path.join(workspace, "out"),
        log=os.path.join(workspace, "log")
    )
