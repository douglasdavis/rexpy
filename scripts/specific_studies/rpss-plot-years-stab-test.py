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


def get_B00(fit_file):
    central, up, down = -1, -1, -1
    with open(fit_file, "r") as f:
        for line in f.readlines():
            if "B_ev_B_00" in line:
                res_line = line
                break
    elements = line.split()
    assert elements[0] == "B_ev_B_00"
    central = round(float(elements[1]), 5)
    up = round(float(elements[2]), 5)
    down = round(float(elements[3]), 5)
    return central, up, down


def year_stability_test(nominal_file, testfiles):
    nom_central, nom_up, nom_down = get_mu(nominal_file)
    deltas = []
    errs_up = []
    errs_down = []
    for test in testfiles:
        sys_central, sys_up, sys_down = get_mu(test)
        deltas.append(nom_central - sys_central)
        errs_up.append(math.sqrt(sys_up ** 2 + nom_up ** 2))
        errs_down.append(math.sqrt(sys_down ** 2 + nom_down ** 2))

    xvals = np.array(deltas)
    xerlo = np.array(errs_down)
    xerhi = np.array(errs_up)
    yvals = np.arange(1, len(xvals) + 1)
    ylabs = ["2015/16", "2017", "2018"]

    fig, ax = plt.subplots(figsize=(5.0, 2.0 + len(deltas) * 0.315))
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
    fig.subplots_adjust(left=0.35, right=0.95, bottom=0.2, top=0.8)
    fig.savefig("years.pdf")
    plt.close(fig)
    return 0


def year_b00_test(nominal_file, testfiles):
    nom_bcentral, nom_bup, nom_bdown = get_B00(nominal_file)
    centrals = []
    ups = []
    downs = []
    for test in testfiles:
        central, up, down = get_B00(test)
        centrals.append(central)
        ups.append(up)
        downs.append(down)
    centrals.append(nom_bcentral)
    ups.append(nom_bup)
    downs.append(nom_bdown)
    xvals = np.array(centrals)
    xerlo = np.array(downs)
    xerhi = np.array(ups)
    yvals = np.arange(1, len(xvals) + 1)
    ylabs = ["2015/16", "2017", "2018", "Complete"]

    fig, ax = plt.subplots(figsize=(5.0, 2.0 + len(centrals) * 0.315))
    ax.set_title("B ev B 00 NP")
    ax.set_xlim([-2.25, 2.25])
    ax.fill_betweenx([-50, 500], -2, 2,
                     color="yellow", alpha=0.8)
    ax.fill_betweenx([-50, 500], -1, 1,
                     color="green", alpha=0.8)
    ax.set_xlabel(r"$(\hat{\theta} - \theta_0)/\Delta\theta$")
    ax.set_yticks(yvals)
    ax.set_yticklabels(ylabs)
    ax.set_ylim([0.0, len(yvals) + 1])
    ax.errorbar(xvals, yvals, xerr=[abs(xerlo), xerhi],
                fmt="ko", lw=2, elinewidth=2.25, capsize=3.5)
    ax.grid(color="black", alpha=0.15)
    fig.subplots_adjust(left=0.35, right=0.95, bottom=0.2, top=0.8)
    fig.savefig("b00.pdf")
    plt.close(fig)
    return 0


@click.command()
@click.argument("nominal", type=str)
@click.argument("fitmc16a", type=str)
@click.argument("fitmc16d", type=str)
@click.argument("fitmc16e", type=str)
def year_tests(nominal, fitmc16a, fitmc16d, fitmc16e):
    """Plot delta(mu) for some stability tests"""
    nominal_file = "{}/Fits/tWrw.txt".format(nominal)
    fitmc16a_file = "{}/Fits/tW1516.txt".format(fitmc16a)
    fitmc16d_file = "{}/Fits/tW17.txt".format(fitmc16d)
    fitmc16e_file = "{}/Fits/tW18.txt".format(fitmc16e)
    testfiles = [fitmc16a_file, fitmc16d_file, fitmc16e_file]
    #year_stability_test(nominal_file, testfiles)
    year_b00_test(nominal_file, testfiles)
    return 0


if __name__ == '__main__':
    year_tests()
