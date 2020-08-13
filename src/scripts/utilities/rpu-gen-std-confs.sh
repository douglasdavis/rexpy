#!/bin/bash

function usage() {
    echo "rpu-gen-std-confs.sh"
    echo ""
    echo "Flags and options:"
    echo "  -o, --outdir    Output directory."
    echo "  -s, --shower    Herwg showering version to use (704 or 713)."
    echo "  -h, --help      Print help message and exit."
    echo "  -f, --fitvar    Fit variable (default is bdtres03)."
    echo ""
}

OUTDIR=$(pwd)
SHOWER="713"
FITVAR="bdtres03"

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -h|--help)
            usage
            exit 0
            ;;
        -f|--fitvar)
            shift
            FITVAR="$1"
            ;;
        -o|--outdir)
            shift
            OUTDIR="$1"
            ;;
        -s|--shower)
            shift
            SHOWER="$1"
            ;;
        *)
            echo "Unknown option '$key'"
            usage
            exit 1
            ;;
    esac
    shift
done

echo "Saving configs to: ${OUTDIR}"
echo "Fit variable: ${FITVAR}"
echo "Showering version: ${SHOWER}"
mkdir -p $OUTDIR

rp-conf.py generate $OUTDIR/main.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --do-tables \
           --do-sys-plots \

rp-conf.py generate $OUTDIR/main_plots.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --do-valplots

rp-conf.py generate $OUTDIR/main_singlebin2j2b.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '1,0.0,1.0' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --do-tables \
           --do-sys-plots


rp-conf.py generate $OUTDIR/main_1j1b.conf \
           --var-1j1b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --herwig-version $SHOWER \
           --drop-2j1b \
           --drop-2j2b

rp-conf.py generate $OUTDIR/main_2j1b.conf \
           --var-2j1b $FITVAR \
           --bin-2j1b '12,0.22,0.70' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --herwig-version $SHOWER \
           --drop-1j1b \
           --drop-2j2b

rp-conf.py generate $OUTDIR/main_2j2b.conf \
           --var-2j2b $FITVAR \
           --bin-2j2b '12,0.45,0.775' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --drop-1j1b \
           --drop-2j1b

rp-conf.py generate $OUTDIR/main_1j1b2j1b.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --herwig-version $SHOWER \
           --drop-2j2b

rp-conf.py generate $OUTDIR/main_1j1b2j2b.conf \
           --var-1j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --drop-2j1b

rp-conf.py generate $OUTDIR/main_only1516.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --only-1516

rp-conf.py generate $OUTDIR/main_only17.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --only-17

rp-conf.py generate $OUTDIR/main_only18.conf \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --bin-1j1b '12,0.35,0.76' \
           --bin-2j1b '12,0.22,0.70' \
           --bin-2j2b '12,0.45,0.775' \
           --sel-1j1b 'reg1j1b == 1 && OS == 1 && bdtres03 > 0.35' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1 && bdtres03 < 0.70' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1 && bdtres03 > 0.45 && bdtres03 < 0.775' \
           --herwig-version $SHOWER \
           --only-18

rp-conf.py generate $OUTDIR/presel_plots.conf \
           --is-preselection \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --sel-1j1b 'reg1j1b == 1 && OS == 1' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1' \
           --herwig-version $SHOWER \
           --do-valplots

rp-conf.py generate $OUTDIR/presel.conf \
           --is-preselection \
           --var-1j1b $FITVAR \
           --var-2j1b $FITVAR \
           --var-2j2b $FITVAR \
           --sel-1j1b 'reg1j1b == 1 && OS == 1' \
           --sel-2j1b 'reg2j1b == 1 && OS == 1' \
           --sel-2j2b 'reg2j2b == 1 && OS == 1' \
           --herwig-version $SHOWER \
           --do-tables \
           --do-sys-plots
