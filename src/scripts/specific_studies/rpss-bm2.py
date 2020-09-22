#!/usr/bin/env python

import itertools
import shutil
import pathlib
import subprocess

import click

import rexpy.pycondor as pycondor
import rexpy.batch as rpb

CUT_MATRIX = {
    "1j1b_min": [0.280, 0.310, 0.340],
    "2j1b_max": [0.600, 0.650, 0.700],
    "2j2b_min": [0.400, 0.500, 0.600],
    "2j2b_max": [0.700, 0.725, 0.750],
}


FITVAR = "bdtres03"
R1J1B_XMAX = 0.76
R2J1B_XMIN = 0.22


@click.command()
@click.argument("ntupdir", type=click.Path(resolve_path=True))
@click.argument("outdir", type=str)
@click.option("--fit-var", type=str, default=FITVAR, help="Branch name", show_default=True)
@click.option("--r1j1b-xmax", type=float, default=R1J1B_XMAX, help="1j1b max", show_default=True)
@click.option("--r2j1b-xmin", type=float, default=R2J1B_XMIN, help="2j1b min", show_default=True)
@click.option("--submit/--no-submit", default=False, help="Submit jobs", show_default=True)
def prepare_configs(ntupdir, outdir, fit_var, r1j1b_xmax, r2j1b_xmin, submit):
    itr = itertools.product(
        CUT_MATRIX["1j1b_min"],
        CUT_MATRIX["2j1b_max"],
        CUT_MATRIX["2j2b_min"],
        CUT_MATRIX["2j2b_max"],
    )

    outdir = pathlib.Path(outdir).resolve()
    (outdir / "configs").mkdir(exist_ok=True, parents=True)

    const_args = f"--asimov-fit --ntup-dir {ntupdir} --var-all {fit_var}"

    all_args = []
    for i, (r1j1b_xmin, r2j1b_xmax, r2j2b_xmin, r2j2b_xmax) in enumerate(itr):
        fname = "{:0.3f}_{:0.3f}_{:0.3f}_{:0.3f}.conf".format(
            r1j1b_xmin, r2j1b_xmax, r2j2b_xmin, r2j2b_xmax
        )
        sel_1j1b = f'"reg1j1b==1&&OS==1&&{fit_var}>{r1j1b_xmin}"'
        sel_2j1b = f'"reg2j1b==1&&OS==1&&{fit_var}<{r2j1b_xmax}"'
        sel_2j2b = f'"reg2j2b==1&&OS==1&&{fit_var}>{r2j2b_xmin}&&{fit_var}<{r2j2b_xmax}"'
        bin_1j1b = f"12,{r1j1b_xmin},{r1j1b_xmax}"
        bin_2j1b = f"12,{r2j1b_xmin},{r2j1b_xmax}"
        bin_2j2b = f"12,{r2j2b_xmin},{r2j2b_xmax}"
        args = (
            f"{const_args} "
            f"--sel-1j1b {sel_1j1b} "
            f"--sel-2j1b {sel_2j1b} "
            f"--sel-2j2b {sel_2j2b} "
            f"--bin-1j1b {bin_1j1b} "
            f"--bin-2j1b {bin_2j1b} "
            f"--bin-2j2b {bin_2j2b} "
        )
        full_arg = f"-m rexpy config gen {outdir}/configs/{fname} {args}"
        all_args.append((full_arg, fname))

    total = len(all_args)
    for i, (arg, fname) in enumerate(all_args):
        subprocess.call(f"python {arg}", shell=True)
        subprocess.call(f"python -m rexpy run condor {outdir}/configs/{fname} --submit", shell=True)
        print(f"{i}/{total}")

    # dag = pycondor.Dagman("bmdag", submit=str(outdir / "confgen" / "sub"))
    # jargs = rpb.job_params(outdir / "confgen", shutil.which("python"))
    # j = pycondor.Job(name="bm", dag=dag, **jargs)
    # j.add_args([a[0] for a in all_args])
    # if submit:
    #     dag.build_submit()
    # else:
    #     dag.build()


if __name__ == "__main__":
    prepare_configs()
