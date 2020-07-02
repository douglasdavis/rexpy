#!/usr/bin/env python

import glob
import math
import os

import click
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
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


def get_B0(fit_file):
    central, up, down = -1, -1, -1
    with open(fit_file, "r") as f:
        for line in f.readlines():
            if "B_ev_B_0" in line:
                res_line = line
                break
    elements = line.split()
    assert elements[0] == "B_ev_B_0"
    central = round(float(elements[1]), 5)
    up = round(float(elements[2]), 5)
    down = round(float(elements[3]), 5)
    return central, up, down


def make_plot(fig, ax, nom, nom_down, nom_up, xvals, xerlo, xerhi, yvals, ylabs):
    ax.fill_betweenx([-50, 500], nom_down, nom_up,
                     color="gray", alpha=0.5, label="Main Fit Uncertainty")
    ax.set_xlabel(r"$\Delta \mu = \mu_{tW}^{\mathrm{nominal}} - \mu_{tW}^{\mathrm{test}}$")
    for xv, yv in zip(xvals, yvals):
        t = f"{xv:1.3f}"
        ax.text(xv, yv+0.075, t, ha="center", va="bottom", size=10)
    ax.set_yticks(yvals)
    ax.set_yticklabels(ylabs)
    ax.set_ylim([0.0, len(yvals) + 1])
    ax.errorbar(xvals, yvals, xerr=[abs(xerlo), xerhi], label="Individual tests",
                fmt="ko", lw=2, elinewidth=2.25, capsize=3.5)
    ax.grid(color="black", alpha=0.15)
    ax.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc="lower left")
    return fig, ax


@click.group()
def cli():
    pass


@cli.command("sys-stab-test")
def sys_stab_test():
    """Plot delta(mu) for some removed systematics stability tests"""
    tests = glob.glob("./*without-**/tW/Fits/tW.txt")
    nominal_file = "./rpcc_standard_fitdata/tW/Fits/tW.txt"

    nom_central, nom_up, nom_down = get_mu(nominal_file)
    deltas = []
    errs_up = []
    errs_down = []
    systematics = []
    for test in tests:
        systematic = test.split("/")[-4].split("-without-")[-1]
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
        replace("Effective", "Eff").
        replace("tW", r"$tW$").
        replace("ptreweight", r"$p_\mathrm{T}$ reweight").
        replace("ttbar", r"$t\bar{t}$")
        for sys in systematics
    ]

    fig, ax = plt.subplots(figsize=(5.2, 1.0 + len(xvals) * 0.315))
    fig.subplots_adjust(left=0.35, right=0.95)
    make_plot(fig, ax, nom_central, nom_down, nom_up, xvals, xerlo, xerhi, yvals, ylabs)
    ax.set_xlim([-0.41, 0.41])
    ax.set_xticks([-0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4])
    fig.savefig("uncertainty_stability_test.pdf")


@cli.command("camp-stab-test")
def camp_stab_test():
    """Plot delta(mu) for some individual campaign tests."""
    nominal = "rpcc_standard_fitdata/tW/Fits/tW.txt"
    only_1516 = "rpcc_standard_fitdata_1516/tW/Fits/tW.txt"
    only_17 = "rpcc_standard_fitdata_17/tW/Fits/tW.txt"
    only_18 = "rpcc_standard_fitdata_18/tW/Fits/tW.txt"

    nom_central, nom_up, nom_down = get_mu(nominal)
    deltas = []
    errs_up = []
    errs_down = []
    years = ["2015/16", "2017", "2018"]
    for d in [only_1516, only_17, only_18]:
        y_central, y_up, y_down = get_mu(d)
        deltas.append(nom_central - y_central)
        errs_up.append(math.sqrt(y_up ** 2 + nom_up ** 2))
        errs_down.append(math.sqrt(y_down ** 2 + nom_down ** 2))

    for n, d, up, down in zip(years, deltas, errs_up, errs_down):
        print(n, d, up, down)

    xvals = np.array(deltas)
    xerlo = np.array(errs_down)
    xerhi = np.array(errs_up)
    yvals = np.arange(1, len(xvals) + 1)
    ylabs = years

    fig, ax = plt.subplots(figsize=(5.2, 2.0 + len(xvals) * 0.315))
    fig.subplots_adjust(left=0.35, right=0.95, top=0.8, bottom=0.2)
    make_plot(fig, ax, nom_central, nom_down, nom_up, xvals, xerlo, xerhi, yvals, ylabs)
    ax.set_xlim([-0.45, 0.45])
    ax.set_xticks([-0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4])
    fig.savefig("camp_stability_test.pdf")


@cli.command("year-b0-test")
def year_b0_test():
    """Plot zeroth b eigenvector by year test."""
    nominal_file = "rpcc_standard_fitdata/tW/Fits/tW.txt"
    mc16a_file = "rpcc_standard_fitdata_1516/tW/Fits/tW.txt"
    mc16d_file = "rpcc_standard_fitdata_17/tW/Fits/tW.txt"
    mc16e_file = "rpcc_standard_fitdata_18/tW/Fits/tW.txt"
    nom_bcentral, nom_bup, nom_bdown = get_B0(nominal_file)
    centrals = []
    ups = []
    downs = []
    for test in [mc16a_file, mc16d_file, mc16e_file]:
        central, up, down = get_B0(test)
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

    fig, ax = plt.subplots(figsize=(5.0, 2.0 + (len(centrals) - 1) * 0.315))
    ax.set_title(r"Zeroth $b$-tagging B eigenvector NP")
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

    for xv, yv in zip(xvals, yvals):
        t = f"{xv:1.3f}"
        ax.text(xv, yv+0.075, t, ha="center", va="bottom", size=10)

    ax.grid(color="black", alpha=0.15)
    fig.subplots_adjust(left=0.20, right=0.95, bottom=0.2, top=0.8)
    fig.savefig("b0.pdf")
    plt.close(fig)
    return 0


if __name__ == '__main__':
    cli()
