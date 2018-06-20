# Skrypts

Useful scripts, of all stripes.

# Documentation

## Vanillinter

Scans pd patches or directories for non-vanilla Pd objects, outputting where they are found (line number, subpatch, file). Made for Mac but should hopefully work on Windows as well (though perhaps not without arguments as './' won't be understood).

TODO: also search a specified Pd-extended path to tell you which library the object is from.

**Arguments:** Currently, arguments are a list of files and/or directories to scan. Example: `vanillinter.py main.pd abstractions/`. If none provided, it will scan the current working directory.
