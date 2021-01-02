# Skrypts

Useful scripts, of all stripes.

## Grab

Wrapper for ffmpeg commands I use for processing screengrabs. Scale, speed up, convert to gif...

`grab -h` for help

### Example
```bash
grab -gs2 -o processed input.mov
```

...will run...

```bash
ffmpeg -i input.mov -vf fps=20,setpts=.5*PTS,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse processed.gif
```

## Vanillinter

Now with extended library search! Scans [pure data](https://puredata.info/) patches or directories for non-vanilla Pd objects, outputting where they are found (line number, subpatch, file) and which library they belong to.

Requires Python 3. Made for Mac but should hopefully work on Windows as well.

### Arguments:
 -  **-f** Pd files or directories to scan. If none are given, current working directory is scanned. Directories are scanned recursively.
 -  **-e** Path(s) to Pd-extended or similar collection of libraries. The linter will tell you which library each linted object comes from.
 -  **-i** Directories to ignore when scanning recursively.
 -  **-v** Verbose output
 -  **-h** Help

### Example:
`vanillinter.py -f main.pd my-abstractions/ -e ~/Pd/lib/Pd-extended/ -i samples-n-junk/ big-horrible-dir/`

The set of vanilla objects might be incomplete at this point. If you encounter any false negatives, please let me know.

## Recky

Wee utility script for executing a file processing command over a globbed pattern, and setting the output file to the original file with a different extension/suffix. Particularly useful for batch processing with ffmpeg or ImageMagick.

### Example:
`recky.sh 'ffmpeg -i # -f mp3' mp3 sample*.wav` (sample01.wav is converted to sample01.mp3 etc.)
