import os
from pathlib import Path


def get_fit_parameter(wkspace, fit_name="tW", parameter_name="SigXsecOverSM"):
    """Get a value from the fit.

    Parameters
    ----------
    wkspace : str
        Path to the TRExFitter workspace.
    fit_name : str
        Name of the fit (the txt file is dependent on the fit name).
    parameter_name : str
        Name of the fit parameter to extract.

    Returns
    -------
    str
        Parameter name
    float
        Central value
    float
        Up uncertainty
    float
        Down uncertainty
    """
    fit_file = Path(wkspace) / "Fits" / f"{fit_name}.txt"
    with fit_file.open("r") as f:
        for line in f.readlines():
            if parameter_name in line:
                desired_line = line
                break
    name, central, up, down = tuple(desired_line.split())
    central = round(float(central), 5)
    up = round(float(up), 5)
    down = round(float(down), 5)
    return name, central, up, down


def completely_pruned(wkspace):
    """Determine which systematics are completely pruned.

    Parameters
    ----------
    wkspace : str or os.PathLike
        Path of TRExFitter workspace.

    Returns
    -------
    list(str)
        Names of all completely pruned systematics.

    """
    pairs = []
    with (Path(wkspace) / "PruningText.txt").open("r") as f:
        for line in f:
            if not line.startswith(" --->>"):
                continue
            sys, status = line.strip()[7:].split("      ")
            if status == "is not present":
                continue
            pairs.append((sys, status))

    unique = sorted(set([p[0] for p in pairs]))
    tests = {u: 0 for u in unique}
    for sys, status in pairs:
        k = 0
        if status == "is kept":
            k = 1
        elif status == "is shape only":
            k = 1
        elif status == "is norm only":
            k = 1
        tests[sys] += k

    return [k for k, v in tests.items() if v == 0]
