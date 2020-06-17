#!/usr/bin/env python

# stdlib
from pathlib import PosixPath
import shutil

# thid party
import click


class Result:
    def __init__(self, a, b, c, d, p):
        self.mu_uncertainty_plus = a
        self.mu_uncertainty_minus = b
        self.impact_up = c
        self.impact_down = d
        self.path = p

        self.mu_uncertainty_mean = round(
            (self.mu_uncertainty_plus - self.mu_uncertainty_minus) * 0.5, 3
        )
        self.impact_mean = round((abs(self.impact_up) + abs(self.impact_down)) * 0.5, 3)

    def __repr__(self):
        return f"{self.path.name}: {self.mu_uncertainty_mean} // {self.impact_mean}"


def get_mu_err(fit_dir):
    plus, minus = 0, 0
    with open(fit_dir / "Fits" / "tW.txt", "r") as f:
        for line in f.readlines():
            if line.startswith("SigXsec"):
                elements = line.split()
                plus = float(elements[2])
                minus = float(elements[3])
                return plus, minus


def get_prefit_drds(fit_dir):
    plus, minus = 0, 0
    entries = (fit_dir / "Fits" / "NPRanking_tW_DRDS.txt").read_text().split()
    plus = float(entries[6])
    minus = float(entries[7])
    return plus, minus


def results_from_matrix_run(directory, fit_name: str = "tW"):
    toplevel = PosixPath(directory)
    results = []
    for p in toplevel.iterdir():
        if p.is_file():
            continue
        fit_dir = p / fit_name
        mu_unc_plus, mu_unc_down = get_mu_err(fit_dir)
        impact_up, impact_down = get_prefit_drds(fit_dir)
        res = Result(mu_unc_plus, mu_unc_down, impact_up, impact_down, p)
        results.append(res)
    return results


@click.command()
@click.option("-t", "--top-level", type=click.Path(resolve_path=True), multiple=True)
@click.option("-s", "--sort-by", type=click.Choice(["impact", "dmu"]))
@click.option("-c", "--copy-best", is_flag=True)
@click.option("-n", "--n-prints", type=int, default=15)
def main(top_level, sort_by, copy_best, n_prints):
    for tl in top_level:
        print("===========" * 6)
        print(f"-- {tl}:")
        results = results_from_matrix_run(tl)
        if sort_by == "impact":
            results = sorted(results, key=lambda r: r.impact_mean)
        else:
            sort_by = "dmu"
            results = sorted(results, key=lambda r: r.mu_uncertainty_mean)
        for r in results[:n_prints]:
            print(r)
        print("===========" * 6)

        if copy_best:
            best_dir = PosixPath(tl) / f"best_by_{sort_by}"
            shutil.rmtree(best_dir, ignore_errors=True)
            shutil.copytree(results[0].path, best_dir)


if __name__ == "__main__":
    main()
