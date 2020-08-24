rexpy scripts
=============

The `rexpy.__main__` module provides the core command line interface
for `rexpy`. If `pip` is used to install `rexpy`, then a `rexpy`
executable will be created by `setuptools`. The `rexpy` bash script in
this directory is a wrapper around calling the `rexpy.__main__.cli`
function via Python's `-m` option (for loading a module as a script).

This directory's subdirectories contain more targeted (less flexible)
scripts. They are broken into specific studies and utilities.

specific_studies
----------------

All scripts are prefixed with `rpss-`.

utilities
---------

All scripts are prefixed with `rpu-`.
