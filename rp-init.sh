#!/bin/bash

## This will setup a good ROOT environment via AtlasSetup and also set
## the shell PATH to find rexpy's apps and scripts.

if [ "$(uname)" == "Darwin" ]; then
    setupPyenv
else
    setupATLAS -q
    lsetup "views LCG_96bpython3 x86_64-centos7-gcc8-opt"
fi

REXPY_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
REXPY_SCRIPT_DIR=$REXPY_DIR/scripts
REXPY_APP_DIR=$REXPY_DIR/app

export PATH=$PATH:$REXPY_SCRIPT_DIR:$REXPY_APP_DIR
export PATH=$PATH:$REXPY_SCRIPT_DIR/specific_studies
export PATH=$PATH:$REXPY_SCRIPT_DIR/utilities
export PYTHONPATH=$PYTHONPATH:$REXPY_DIR
