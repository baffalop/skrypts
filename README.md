# Skrypts

Useful scripts, of all stripes.

## Vanillinter

Scans pd patches or directories for non-vanilla Pd objects, outputting where they are found (line number, subpatch, file). Directories are scanned recursively. Requires Python 3. Made for Mac but should hopefully work on Windows as well (though perhaps not without arguments as './' won't be understood).

**Arguments:** Currently, arguments are a list of files and/or directories to scan. Example: `vanillinter.py main.pd abstractions/`. If none provided, it will scan the current working directory.

TODO: also search a specified Pd-extended path to tell you which library the object is from.

The set of vanilla objects might be incomplete at this point. If you encounter any false negatives, please let me know.
