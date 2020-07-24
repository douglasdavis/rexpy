import os

def get_fit_parameter(workspace, fit_name="tW", parameter_name="SigXsecOverSM"):
    """Get a value from the fit.

    Parameters
    ----------
    workspace : str
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
    fit_file = os.path.join(workspace, "Fits", "{}.txt".format(fit_name))
    with open(fit_file, "r") as f:
        for line in f.readlines():
            if parameter_name in line:
                desired_line = line
                break
    name, central, up, down = tuple(desired_line.split())
    central = round(float(central), 5)
    up = round(float(up), 5)
    down = round(float(down), 5)
    return name, central, up, down
