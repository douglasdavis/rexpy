#!/bin/bash

## This will set the shell PATH to find rexuple's scripts

REXUPLE_SCRIPT_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))/scripts
REXUPLE_APP_DIR=$(realpath $(dirname "${BASH_SOURCE[0]}"))/app
export PATH=$PATH:$REXUPLE_SCRIPT_DIR:$REXUPLE_APP_DIR
