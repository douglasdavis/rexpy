#!/bin/bash

OUTDIR=$(pwd)
while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -o|--outdir)
            shift
            OUTDIR="$1"
            ;;
        -s|--submit)
            SUBMIT=1
            ;;
        *)
            echo "Unknown option '$key'"
            ;;
    esac
    shift
done

echo "Saving configs to: ${OUTDIR}"
[[ "${SUBMIT}" == "1" ]] && echo "Submitting"
mkdir -p $OUTDIR

rp-conf.py tunable $OUTDIR/standard_presel_plots.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1' \
           --fit-data \
           --skip-tables \
           --skip-sys-plots \
           --do-valplots \
           --is-preselection

# --bin-1j1b '12,0.35,0.76' \
# --bin-2j1b '12,0.22,0.70' \
# --bin-2j2b '12,0.45,0.775' \

rp-conf.py tunable $OUTDIR/standard_fitdata_allplots.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --skip-tables \
           --skip-sys-plots \
           --do-valplots \
           --fit-data

rp-conf.py tunable $OUTDIR/standard_fitdata.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --fit-data

rp-conf.py tunable $OUTDIR/standard_fitdata_1516.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --fit-data \
           --only-1516

rp-conf.py tunable $OUTDIR/standard_fitdata_17.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --fit-data \
           --only-17

rp-conf.py tunable $OUTDIR/standard_fitdata_18.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --fit-data \
           --only-18

rp-conf.py tunable $OUTDIR/standard_fitasimov.conf \
           --var-1j1b 'bdtres03' --var-2j1b 'bdtres03' --var-2j2b 'bdtres03' \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775'

rp-conf.py rm-region $OUTDIR/standard_fitasimov.conf \
           -r reg2j1b \
           -r reg2j2b \
           -n $OUTDIR/standard_fitasimov_1j1b.conf

rp-conf.py rm-region $OUTDIR/standard_fitasimov.conf \
           -r reg2j2b \
           -n $OUTDIR/standard_fitasimov_1j1b2j1b.conf

rp-conf.py rm-region $OUTDIR/standard_fitasimov.conf \
           -r reg2j1b \
           -n $OUTDIR/standard_fitasimov_1j1b2j2b.conf

rp-conf.py rm-region $OUTDIR/standard_fitdata.conf \
           -r reg2j1b \
           -r reg2j2b \
           -n $OUTDIR/standard_fitdata_1j1b.conf

rp-conf.py rm-region $OUTDIR/standard_fitdata.conf \
           -r reg2j2b \
           -n $OUTDIR/standard_fitdata_1j1b2j1b.conf

rp-conf.py rm-region $OUTDIR/standard_fitdata.conf \
           -r reg2j1b \
           -n $OUTDIR/standard_fitdata_1j1b2j2b.conf

if [[ "${SUBMIT}" == "1" ]]; then
    for c in $OUTDIR/*.conf; do
        rp-condor.py complete $c
    done
fi
