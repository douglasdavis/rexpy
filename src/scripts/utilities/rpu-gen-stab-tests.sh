#!/bin/bash

[[ -z "$1" ]] && echo "Config file required" && exit 1

full_config=$1
filename=$(basename -- "$full_config")
extension="${filename##*.}"
filename="${filename%.*}"
trexexe=$(which trex-fitter)
to_remove=(
    ttbar_ptreweight_1j1b
    ttbar_ptreweight_2j1b
    ttbar_ptreweight_2j2b
    ttbar_hdamp_1j1b
    ttbar_hdamp_2j1b
    ttbar_hdamp_2j2b
    ttbar_PS_1j1b
    ttbar_PS_2j1b
    ttbar_PS_2j2b
    ttbar_AR_FSR_2j1b
    ttbar_AR_FSR_1j1b
    tW_DRDS
    tW_PS_1j1b
    tW_PS_2j1b
    tW_PS_2j2b
    MET_SoftTrk_Scale
    Jet_Pileup_RhoTopology
    Jet_JER_EffectiveNP_7restTerm
    Jet_JER_EffNP_1
    Jet_JER_DataVsMC
    Jet_Flavor_Response
    Jet_Flavor_Composition
    B_ev_B_0
)

[[ ! -d "rpcc_${filename}/tW/Histograms" ]] && "Existing histograms dir does not exist"

for sys in "${to_remove[@]}"; do
    newfile=$filename-without-$sys.$extension
    rp-conf.py rm-sys $1 -s $sys -n $newfile
    rp-condor.py complete $newfile --copy-histograms-from rpcc_${filename}/tW/Histograms --dont-draw --dont-rank
done
