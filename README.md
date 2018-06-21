# Skrypts

Useful scripts, of all stripes.

## Vanillinter

Now with extended library search! Scans pd patches or directories for non-vanilla Pd objects, outputting where they are found (line number, subpatch, file) and which library they belong to.

Requires Python 3. Made for Mac but should hopefully work on Windows as well.

**Arguments:**
 -  -f Pd files or directories to scan. If none are given, current working directory is scanned. Directories are scanned recursively.
 -  -e Path(s) to Pd-extended or similar collection of libraries. The linter will tell you which library each linted object comes from.
 -  -i Directories to ignore when scanning recursively.
 -  -v Verbose output
 -  -h Help

**Example:** `vanillinter.py -f main.pd my-abstractions/ -e ~/Pd/lib/Pd-extended/ -i samples-n-junk/ big-horrible-dir/`

The set of vanilla objects might be incomplete at this point. If you encounter any false negatives, please let me know.
