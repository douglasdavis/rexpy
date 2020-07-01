#!/bin/bash

## This will setup a good ROOT environment via AtlasSetup and also set
## the shell PATH to find rexpy's apps and scripts.

if [ "$(uname)" == "Darwin" ]; then
    setupPyenv
    pyenv activate rexpy
else
    setupATLAS -q
    lsetup "views LCG_97apython3 x86_64-centos7-gcc9-opt"
fi

# directories
REXPY_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}")/..)
REXPY_SCRIPT_DIR=$REXPY_DIR/src/scripts
REXPY_APP_DIR=$REXPY_DIR/src/app

# executables
export PATH=$PATH:$REXPY_SCRIPT_DIR:$REXPY_APP_DIR
export PATH=$PATH:$REXPY_SCRIPT_DIR/specific_studies
export PATH=$PATH:$REXPY_SCRIPT_DIR/utilities

# python
export PYTHONPATH=$PYTHONPATH:$REXPY_DIR/src
