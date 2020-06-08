#!/usr/bin/env python

from __future__ import print_function

import itertools
import os
import subprocess
import sys
import yaml


# matrix_without_masscuts = r"""
# r1j1b_min: [0.250, 0.275, 0.300, 0.325, 0.350]
# r1j1b_max: [0.760]
# r2j1b_min: [0.220]
# r2j1b_max: [0.600, 0.625, 0.650, 0.675, 0.700]
# r2j2b_min: [0.300, 0.400, 0.500, 0.600]
# r2j2b_max: [0.750, 0.775, 0.800, 0.825]
# """


matrix_without_masscuts = r"""
r1j1b_min: [0.250, 0.300, 0.350]
r1j1b_max: [0.760]
r2j1b_min: [0.220]
r2j1b_max: [0.600, 0.650, 0.700]
r2j2b_min: [0.300, 0.450, 0.600]
r2j2b_max: [0.775, 0.825]
"""
matrix_without_masscuts = yaml.full_load(matrix_without_masscuts)
var_without_masscuts = "bdtres00"

matrix_with_masscuts = r"""
r1j1b_min: [0.20, 0.25, 0.30]
r1j1b_max: [0.745]
r2j1b_min: [0.220]
r2j1b_max: [0.600, 0.700, 0.800]
r2j2b_min: [0.300, 0.400, 0.500]
r2j2b_max: [0.7, 0.8]
"""
matrix_with_masscuts = yaml.full_load(matrix_with_masscuts)
var_with_masscuts = "bdtres01"


def do_without_masscuts():
    itr = itertools.product(
        matrix_without_masscuts.get("r1j1b_min"),
        matrix_without_masscuts.get("r1j1b_max"),
        matrix_without_masscuts.get("r2j1b_min"),
        matrix_without_masscuts.get("r2j1b_max"),
        matrix_without_masscuts.get("r2j2b_min"),
        matrix_without_masscuts.get("r2j2b_max")
    )
    if not os.path.exists("binmatrix_without_masscuts"):
        os.mkdir("binmatrix_without_masscuts")
    for i, (r1j1b_min, r1j1b_max, r2j1b_min, r2j1b_max, r2j2b_min, r2j2b_max) in enumerate(itr):
        filename = "fit_{}-{}_{}-{}_{}-{}.conf".format(
            r1j1b_min, r1j1b_max, r2j1b_min, r2j1b_max, r2j2b_min, r2j2b_max
        )
        args = ('tunable '
                '--bin-1j1b 12,{0},{1} --sel-1j1b "reg1j1b == 1 && OS == 1 && {6} > {0}" '
                '--bin-2j1b 12,{2},{3} --sel-2j1b "reg2j1b == 1 && OS == 1 && {6} < {3}" '
                '--bin-2j2b 12,{4},{5} --sel-2j2b "reg2j2b == 1 && OS == 1 && {6} > {4} && {6} < {5}" '
                '--skip-syst-plots --skip-tables').format(
                    r1j1b_min, r1j1b_max, r2j1b_min, r2j1b_max, r2j2b_min, r2j2b_max, var_without_masscuts,
                )
        print(args)
        subprocess.call("rp-conf.py {} binmatrix_without_masscuts/{}".format(args, filename), shell=True)


def do_with_masscuts():
    itr = itertools.product(
        matrix_with_masscuts.get("r1j1b_min"),
        matrix_with_masscuts.get("r1j1b_max"),
        matrix_with_masscuts.get("r2j1b_min"),
        matrix_with_masscuts.get("r2j1b_max"),
        matrix_with_masscuts.get("r2j2b_min"),
        matrix_with_masscuts.get("r2j2b_max")
    )
    if not os.path.exists("binmatrix_with_masscuts"):
        os.mkdir("binmatrix_with_masscuts")
    for i, (r1j1b_min, r1j1b_max, r2j1b_min, r2j1b_max, r2j2b_min, r2j2b_max) in enumerate(itr):
        filename = "fit_{}-{}_{}-{}_{}-{}.conf".format(
            r1j1b_min, r1j1b_max, r2j1b_min, r2j1b_max, r2j2b_min, r2j2b_max
        )
        args = ('tunable '
                '--bin-1j1b 12,{0},{1} --var-1j1b bdtres01 '
                '--sel-1j1b "reg1j1b == 1 && OS == 1 && mass_lep1jet1 < 155 && mass_lep2jet1 < 155 && {6} > {0}" '
                '--bin-2j1b 12,{2},{3} --var-2j1b bdtres01 '
                '--sel-2j1b "reg2j1b == 1 && OS == 1 && mass_lep1jetb < 155 && mass_lep2jetb < 155 && {6} < {3}" '
                '--bin-2j2b 12,{4},{5} --var-2j2b bdtres01 '
                '--sel-2j2b "reg2j2b == 1 && OS == 1 && minimaxmbl < 155 && {6} > {4} && {6} < {5}" '
                '--skip-syst-plots --skip-tables').format(
                    r1j1b_min, r1j1b_max, r2j1b_min, r2j1b_max, r2j2b_min, r2j2b_max, var_with_masscuts,
                )
        print(args)
        subprocess.call("rp-conf.py {} binmatrix_with_masscuts/{}".format(args, filename), shell=True)


if len(sys.argv) != 2:
    print("bad arg (with/without)")
    exit(1)
elif sys.argv[1] == "with":
    do_with_masscuts()
elif sys.argv[1] == "without":
    do_without_masscuts()
