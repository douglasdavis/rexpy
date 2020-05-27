#!/bin/bash

## This will setup a good ROOT environment via AtlasSetup and also set
## the shell PATH to find rexpy's apps and scripts.

if [ "$(uname)" == "Darwin" ]; then
    setupPyenv
    pyenv activate py2
else
    setupATLAS -q
    lsetup "root 6.18.04-x86_64-centos7-gcc8-opt" --quiet
fi

REXUPLE_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
REXUPLE_SCRIPT_DIR=$REXUPLE_DIR/scripts
REXUPLE_APP_DIR=$REXUPLE_DIR/app

export PATH=$PATH:$REXUPLE_SCRIPT_DIR:$REXUPLE_APP_DIR
export PATH=$PATH:$REXUPLE_SCRIPT_DIR/specific_studies
export PATH=$PATH:$REXUPLE_SCRIPT_DIR/utilities
export PYTHONPATH=$PYTHONPATH:$REXUPLE_DIR
