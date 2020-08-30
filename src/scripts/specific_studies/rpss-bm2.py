#!/usr/bin/env python

import itertools
import shutil
import pathlib

import click

import rexpy.pycondor as pycondor
import rexpy.batch as rpb

CUT_MATRIX = {
    "1j1b_min": [0.280, 0.310, 0.340],
    "2j1b_max": [0.600, 0.650, 0.700],
    "2j2b_min": [0.400, 0.500, 0.600],
    "2j2b_max": [0.700, 0.725, 0.750],
}


FITVAR = "bdtres40"
R1J1B_XMAX = 0.78
R2J1B_XMIN = 0.25

@click.command()
@click.argument("ntup_dir", type=click.Path(resolve_path=True))
@click.argument("fitvar", type=str)
@click.argument("r1j1b_xmax", type=float)
@click.argument("r2j1b_xmin", type=float)
@click.argument("outdir", type=str)
def prepare_configs(ntup_dir, fitvar, r1j1b_xmax, r2j1b_xmin, outdir):
    itr = itertools.product(
        CUT_MATRIX["1j1b_min"],
        CUT_MATRIX["2j1b_max"],
        CUT_MATRIX["2j2b_min"],
        CUT_MATRIX["2j2b_max"],
    )

    outdir = pathlib.Path(outdir).resolve()
    (outdir / "configs").mkdir(exist_ok=True, parents=True)

    const_args = f"--asimov-fit --ntup-dir {ntup_dir} --var-1j1b {fitvar} --var-2j1b {fitvar} --var-2j2b {fitvar}"

    all_args = []
    for i, (r1j1b_xmin, r2j1b_xmax, r2j2b_xmin, r2j2b_xmax) in enumerate(itr):
        fname = "{:0.3f}_{:0.3f}_{:0.3f}_{:0.3f}.conf".format(
            r1j1b_xmin, r2j1b_xmax, r2j2b_xmin, r2j2b_xmax
        )
        sel_1j1b = f'""reg1j1b==1&&OS==1&&{fitvar}>{r1j1b_xmin}""'
        sel_2j1b = f'""reg2j1b==1&&OS==1&&{fitvar}<{r2j1b_xmax}""'
        sel_2j2b = f'""reg2j2b==1&&OS==1&&{fitvar}>{r2j2b_xmin}&&{fitvar}<{r2j2b_xmax}""'
        bin_1j1b = f'12,{r1j1b_xmin},{r1j1b_xmax}'
        bin_2j1b = f'12,{r2j1b_xmin},{r2j1b_xmax}'
        bin_2j2b = f'12,{r2j2b_xmin},{r2j2b_xmax}'
        args = (
            f"{const_args} "
            f"--sel-1j1b {sel_1j1b} "
            f"--sel-2j1b {sel_2j1b} "
            f"--sel-2j2b {sel_2j2b} "
            f"--bin-1j1b {bin_1j1b} "
            f"--bin-2j1b {bin_2j1b} "
            f"--bin-2j2b {bin_2j2b} "
        )
        full_arg = f'"-m rexpy config gen {outdir}/configs/{fname} {args}"'
        all_args.append(full_arg)

    jargs = rpb.job_params(outdir / "confgen", shutil.which("python"))
    j = pycondor.Job(name="bm", **jargs)
    j.add_args(all_args)
    j.build()


if __name__ == "__main__":
    prepare_configs()
