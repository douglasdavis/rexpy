#!/bin/bash

STABILITY_TEST_DIR="/usatlas/u/ddavis/ATLAS/analysis/run/rexpy/stability_tests"

uncertainties=(
    tW_PS_1j1b
    tW_DRDS
    ttbar_PS_1j1b
    ttbar_PS_2j1b
    ttbar_PS_2j2b
    ttbar_PS_migration
    tW_AR_FSR_2j2b
    B_ev_B_33
    B_ev_B_09
    B_ev_B_00
    Jet_JER_EffNP_3
    Jet_JER_EffNP_4
    Jet_Flavor_Response
    Jet_Flavor_Composition
)

for SYS in "${uncertainties[@]}"; do
    echo "Universe        = vanilla" > $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "notification    = Error" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "notify_user     = ddavis@phy.duke.edu" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "GetEnv          = True" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "Executable      = /direct/usatlas+u/ddavis/ATLAS/analysis/WtAna/TRExFitter/build/bin/trex-fitter" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "Output          = /usatlas/u/ddavis/ATLAS/analysis/run/rexpy/stability_tests/logs/job.out.trexntup.\$(cluster).\$(process)" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "Error           = /usatlas/u/ddavis/ATLAS/analysis/run/rexpy/stability_tests/logs/job.err.trexntup.\$(cluster).\$(process)" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "Log             = /tmp/ddavis/log.\$(cluster).\$(process)" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "request_memory  = 2.0G" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "Arguments = wf /usatlas/u/ddavis/ATLAS/analysis/run/rexpy/stability_tests/$SYS/fit_tptrw.conf Exclude=$SYS" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "Queue" >> $STABILITY_TEST_DIR/$SYS/condor.sub
    echo "" >> $STABILITY_TEST_DIR/$SYS/condor.sub
done
