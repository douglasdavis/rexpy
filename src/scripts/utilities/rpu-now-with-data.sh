#!/bin/bash


[[ -d "./main.d/tW/Histograms" ]]               && rexpy run condor main.conf --copy-hists ./main.d/tW/Histograms --force-data --steps wf --submit && echo "main.d"
[[ -d "./main_plots.d/tW/Histograms" ]]         && rexpy run condor main_plots.conf --copy-hists ./main_plots.d/tW/Histograms --force-data --steps wfdp --submit && echo "main_plots.d"
[[ -d "./main_1j1b.d/tW/Histograms" ]]          && rexpy run condor main_1j1b.conf --copy-hists ./main_1j1b.d/tW/Histograms --force-data --steps wf --submit && echo "main_1j1b.d"
[[ -d "./main_1j1b2j1b.d/tW/Histograms" ]]      && rexpy run condor main_1j1b2j1b.conf --copy-hists ./main_1j1b2j1b.d/tW/Histograms --force-data --steps wf --submit && echo "main_1j1b2j1b.d"
[[ -d "./main_1j1b2j2b.d/tW/Histograms" ]]      && rexpy run condor main_1j1b2j2b.conf --copy-hists ./main_1j1b2j2b.d/tW/Histograms --force-data --steps wf --submit && echo "main_1j1b2j2b.d"
[[ -d "./main_2j1b.d/tW/Histograms" ]]          && rexpy run condor main_2j1b.conf --copy-hists ./main_2j1b.d/tW/Histograms --force-data --steps wf --submit && echo "main_2j1b.d"
[[ -d "./main_2j2b.d/tW/Histograms" ]]          && rexpy run condor main_2j2b.conf --copy-hists ./main_2j2b.d/tW/Histograms --force-data --steps wf --submit && echo "main_2j2b.d"
[[ -d "./main_only1516.d/tW/Histograms" ]]      && rexpy run condor main_only1516.conf --copy-hists ./main_only1516.d/tW/Histograms --force-data --steps wf --submit && echo "main_only1516.d"
[[ -d "./main_only17.d/tW/Histograms" ]]        && rexpy run condor main_only17.conf --copy-hists ./main_only17.d/tW/Histograms --force-data --steps wf --submit && echo "main_only17.d"
[[ -d "./main_only18.d/tW/Histograms" ]]        && rexpy run condor main_only18.conf --copy-hists ./main_only18.d/tW/Histograms --force-data --steps wf --submit && echo "main_only18.d"
[[ -d "./main_singlebin2j2b.d/tW/Histograms" ]] && rexpy run condor main_singlebin2j2b.conf --copy-hists ./main_singlebin2j2b.d/tW/Histograms --force-data --steps wf --submit && echo "main_singlebin2j2b.d"
[[ -d "./presel_plots.d/tW/Histograms" ]]       && rexpy run condor presel_plots.conf --copy-hists ./presel_plots.d/tW/Histograms --force-data --steps wfdp --submit && echo "presel_plots.d"
[[ -d "./presel.d/tW/Histograms" ]]             && rexpy run condor presel.conf --copy-hists ./presel.d/tW/Histograms --force-data --steps wfdp --submit && echo "presel.d"
