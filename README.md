rexpy
=====

Libraries and scripts to guide
[TRExFitter](https://gitlab.cern.ch/TRExStats/TRExFitter) with a real
programming language (Python).

Setup
-----

Working in an ATLAS environment is not very vanilla, so we can't just
install this with `pip` and move on with our lives (unfortunately).
The `atlas-init.sh` script tries to make this a little easier, CVMFS
installed with the standard LHC Computing Grid repositories are
required; just run:

```
$ . src/atlas-init.sh
```
