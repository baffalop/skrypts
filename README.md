# Skrypts

Useful scripts, of all stripes.

## Vanillinter

Now with extended library search! Scans pd patches or directories for non-vanilla Pd objects, outputting where they are found (line number, subpatch, file) and which library they belong to.

Requires Python 3. Made for Mac but should hopefully work on Windows as well (though perhaps not without arguments as './' won't be understood).

**Arguments:**
 -  -e Optional path to a directory containing Pd-extended libraries. The linter will say which library each object it finds comes from.
 -  A list of paths, either pd files or directories, to scan. Directories will be scanned recursively.
 -  -h for help

**Example:** `vanillinter.py -e ~/Pd/lib/Pd-extended/ main.pd my-abstractions/`

The set of vanilla objects might be incomplete at this point. If you encounter any false negatives, please let me know.
