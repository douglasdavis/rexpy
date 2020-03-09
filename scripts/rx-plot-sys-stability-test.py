#!/usr/bin/env python

from __future__ import print_function

import glob
import math
import os

import click
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_mu(fit_file):
    central, up, down = -1, -1, -1
    with open(fit_file, "r") as f:
        for line in f.readlines():
            if "SigXsec" in line:
                res_line = line
                break
    elements = line.split()
    assert elements[0] == "SigXsecOverSM"
    central = round(float(elements[1]), 5)
    up = round(float(elements[2]), 5)
    down = round(float(elements[3]), 5)
    return central, up, down


@click.command()
@click.argument("nominal", type=str)
@click.argument("tests", type=str)
def plot_stab_test(nominal, tests):
    """Plot delta(mu) for some stability tests"""
    nominal_directory = os.path.abspath(nominal)
    test_directory = os.path.abspath(tests)
    test_itr = glob.iglob("{}/**/tWrw/Fits/tWrw.txt".format(test_directory))
    nominal_file = "{}/Fits/tWrw.txt".format(nominal_directory)

    nom_central, nom_up, nom_down = get_mu(nominal_file)

    deltas = []
    errs_up = []
    errs_down = []
    systematics = []
    for test in test_itr:
        systematic = test.split("/")[-4]
        if systematic == "base_fit":
            continue
        sys_central, sys_up, sys_down = get_mu(test)
        systematics.append(systematic)
        deltas.append(nom_central - sys_central)
        errs_up.append(math.sqrt(sys_up ** 2 + nom_up ** 2))
        errs_down.append(math.sqrt(sys_down ** 2 + nom_down ** 2))

    for n, d, up, down in zip(systematics, deltas, errs_up, errs_down):
        print(n, d, up, down)

    xvals = np.array(deltas)
    xerlo = np.array(errs_down)
    xerhi = np.array(errs_up)
    yvals = np.arange(1, len(xvals) + 1)
    ylabs = [
        sys.
        replace("_", " ").
        replace("tW", r"$tW$").
        replace("ttbar", r"$t\bar{t}$")
        for sys in systematics
    ]

    fig, ax = plt.subplots(figsize=(5.2, 1.0 + len(systematics) * 0.315))
    fig.subplots_adjust(left=0.35, right=0.95)
    ax.set_xlim(-0.425, 0.425)
    ax.fill_betweenx([-50, 500], nom_down, nom_up,
                     color="gray", alpha=0.5, label="Main Fit Uncertainty")
    ax.set_xlabel(r"$\Delta \mu$")
    ax.set_yticks(yvals)
    ax.set_yticklabels(ylabs)
    ax.set_ylim([0.0, len(yvals) + 1])
    ax.errorbar(xvals, yvals, xerr=[abs(xerlo), xerhi],
                fmt="ko", lw=2, elinewidth=2.25, capsize=3.5)
    ax.grid(color="black", alpha=0.15)
    ax.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc="lower left")
    fig.savefig("uncertainty_stability_test.pdf")


if __name__ == '__main__':
    plot_stab_test()
