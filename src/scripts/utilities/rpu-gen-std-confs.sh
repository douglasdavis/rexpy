#!/bin/bash

function usage() {
    echo "rpu-gen-std-confs.sh"
    echo ""
    echo "Flags and options:"
    echo "  -h, --help        Print help message and exit."
    echo "  -o, --outdir      Output directory."
    echo "  -s, --shower      Herwg showering version to use (704 or 713)."
    echo "  -f, --fitvar      Fit variable (default is bdtres10)."
    echo "  -n, --ntup-dir    Ntuple path directry."
    echo "      --nbin-1j1b   Number of bins for 1j1b region."
    echo "      --nbin-2j1b   Number of bins for 2j1b region."
    echo "      --nbin-2j2b   Number of bins for 2j2b region."
    echo "      --xmin-1j1b   Minimum for 1j1b region."
    echo "      --xmin-2j1b   Minimum for 2j1b region."
    echo "      --xmin-2j2b   Minimum for 2j2b region."
    echo "      --xmax-1j1b   Maximum for 1j1b region."
    echo "      --xmax-2j1b   Maximum for 2j1b region."
    echo "      --xmax-2j2b   Maximum for 2j2b region."
    echo "      --ttbar-aux   Auxiliary weight for ttbar sample."
    echo ""
}

OUTDIR=$(pwd)
SHOWER="704"
FITVAR="bdtres10"
NTUPDIR="/ddd/atlas/data/wtloop/WTA01_20200827"
NBIN_1j1b="12"
NBIN_2j1b="12"
NBIN_2j2b="12"
XMIN_1j1b="0.35"
XMAX_1j1b="0.76"
XMIN_2j1b="0.22"
XMAX_2j1b="0.70"
XMIN_2j2b="0.45"
XMAX_2j2b="0.775"
TTBAR_AUX="none"

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
        -n|--ntup-dir)
            shift
            NTUPDIR="$1"
            ;;
        --nbin-1j1b)
            shift
            NBIN_1j1b="$1"
            ;;
        --nbin-2j1b)
            shift
            NBIN_2j1b="$1"
            ;;
        --nbin-2j2b)
            shift
            NBIN_2j2b="$1"
            ;;
        --xmin-1j1b)
            shift
            XMIN_1j1b="$1"
            ;;
        --xmin-2j1b)
            shift
            XMIN_2j1b="$1"
            ;;
        --xmin-2j2b)
            shift
            XMIN_2j2b="$1"
            ;;
        --xmax-1j1b)
            shift
            XMAX_1j1b="$1"
            ;;
        --xmax-2j1b)
            shift
            XMAX_2j1b="$1"
            ;;
        --xmax-2j2b)
            shift
            XMAX_2j2b="$1"
            ;;
        --ttbar-aux)
            shift
            TTBAR_AUX="$1"
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
echo "Ntuple dir: ${NTUPDIR}"
mkdir -p $OUTDIR

python -m rexpy config gen $OUTDIR/main.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b ${FITVAR} \
       --var-2j1b ${FITVAR} \
       --var-2j2b ${FITVAR} \
       --bin-1j1b "${NBIN_1j1b},${XMIN_1j1b},${XMAX_1j1b}" \
       --bin-2j1b "${NBIN_2j1b},${XMIN_2j1b},${XMAX_2j1b}" \
       --bin-2j2b "${NBIN_2j2b},${XMIN_2j2b},${XMAX_2j2b}" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && ${FITVAR} > ${XMIN_1j1b}" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --do-tables \
       --do-sys-plots

python -m rexpy config gen $OUTDIR/main_plots.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --bin-2j2b "$NBIN_2j2b,$XMIN_2j2b,$XMAX_2j2b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --do-valplots

python -m rexpy config gen $OUTDIR/main_singlebin2j2b.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --bin-2j2b "1,0.0,1.0" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --do-tables \
       --do-sys-plots


python -m rexpy config gen $OUTDIR/main_1j1b.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --herwig-version $SHOWER \
       --drop-2j1b \
       --drop-2j2b

python -m rexpy config gen $OUTDIR/main_2j1b.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-2j1b $FITVAR \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --herwig-version $SHOWER \
       --drop-1j1b \
       --drop-2j2b

python -m rexpy config gen $OUTDIR/main_2j2b.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-2j2b $FITVAR \
       --bin-2j2b "$NBIN_2j2b,$XMIN_2j2b,$XMAX_2j2b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --drop-1j1b \
       --drop-2j1b

python -m rexpy config gen $OUTDIR/main_1j1b2j1b.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --herwig-version $SHOWER \
       --drop-2j2b

python -m rexpy config gen $OUTDIR/main_1j1b2j2b.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j2b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j2b "$NBIN_2j2b,$XMIN_2j2b,$XMAX_2j2b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --drop-2j1b

python -m rexpy config gen $OUTDIR/main_only1516.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --bin-2j2b "$NBIN_2j2b,$XMIN_2j2b,$XMAX_2j2b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --only-1516

python -m rexpy config gen $OUTDIR/main_only17.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --bin-2j2b "$NBIN_2j2b,$XMIN_2j2b,$XMAX_2j2b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --only-17

python -m rexpy config gen $OUTDIR/main_only18.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --bin-1j1b "$NBIN_1j1b,$XMIN_1j1b,$XMAX_1j1b" \
       --bin-2j1b "$NBIN_2j1b,$XMIN_2j1b,$XMAX_2j1b" \
       --bin-2j2b "$NBIN_2j2b,$XMIN_2j2b,$XMAX_2j2b" \
       --sel-1j1b "reg1j1b == 1 && OS == 1 && $FITVAR > $XMIN_1j1b" \
       --sel-2j1b "reg2j1b == 1 && OS == 1 && $FITVAR < $XMAX_2j1b" \
       --sel-2j2b "reg2j2b == 1 && OS == 1 && $FITVAR > $XMIN_2j2b && $FITVAR < $XMAX_2j2b" \
       --herwig-version $SHOWER \
       --only-18

python -m rexpy config gen $OUTDIR/presel_plots.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --is-preselection \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --sel-1j1b "reg1j1b == 1 && OS == 1" \
       --sel-2j1b "reg2j1b == 1 && OS == 1" \
       --sel-2j2b "reg2j2b == 1 && OS == 1" \
       --herwig-version $SHOWER \
       --do-valplots

python -m rexpy config gen $OUTDIR/presel.conf \
       --ntup-dir ${NTUPDIR} \
       --ttbar-aux-weight $TTBAR_AUX \
       --is-preselection \
       --var-1j1b $FITVAR \
       --var-2j1b $FITVAR \
       --var-2j2b $FITVAR \
       --sel-1j1b "reg1j1b == 1 && OS == 1" \
       --sel-2j1b "reg2j1b == 1 && OS == 1" \
       --sel-2j2b "reg2j2b == 1 && OS == 1" \
       --herwig-version $SHOWER \
       --do-tables \
       --do-sys-plots
