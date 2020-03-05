#!/bin/bash

## This will setup a good ROOT environment via AtlasSetup and also set
## the shell PATH to find rexuple's apps and scripts.

lsetup "root 6.18.04-x86_64-centos7-gcc8-opt" --quiet

REXUPLE_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))
REXUPLE_SCRIPT_DIR=$REXUPLE_DIR/scripts
REXUPLE_APP_DIR=$REXUPLE_DIR/app

export PATH=$PATH:$REXUPLE_SCRIPT_DIR:$REXUPLE_APP_DIR
