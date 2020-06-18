#!/bin/bash

rp-conf.py tunable main_preselection_plots.conf \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --var-1j1b 'bdtres03' \
           --var-2j1b 'bdtres03' \
           --var-2j2b 'bdtres03' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1' \
           --skip-tables \
           --skip-syst-plots \
           --do-valplots \
           --is-preselection

rp-conf.py tunable main_allplots.conf \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --var-1j1b 'bdtres03' \
           --var-2j1b 'bdtres03' \
           --var-2j2b 'bdtres03' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --skip-tables \
           --skip-syst-plots \
           --do-valplots \
           --fit-data

rp-conf.py tunable main_fitdata.conf \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --var-1j1b 'bdtres03' \
           --var-2j1b 'bdtres03' \
           --var-2j2b 'bdtres03' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --fit-data

rp-conf.py tunable main_fitasimov.conf \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --var-1j1b 'bdtres03' \
           --var-2j1b 'bdtres03' \
           --var-2j2b 'bdtres03' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
