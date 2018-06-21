#!/usr/bin/env python3

import os
import os.path as pathTools
import sys
import re
import argparse

vanilla = {'bang','change','float','int','makefilename','moses','pack','print','receive','route','select','send','spigot','swap','symbol','trigger','unpack','until','value','choice','&','|','<<','>>','&&','||','%','+','-','*','/','pow','>','>=','=','<=','<','clip','max','min','mod','div','sin','cos','tan','atan','atan2','exp','log','abs','sqrt','pow','mtof','ftom','dbtorms','rmstodb','dbtopow','powtodb','random','wrap','expr','cputime','delay','line','metro','pipe','realtime','timer','makenote','notein','ctlin','pgmin','bendin','touchin','polytouchin','midiin','sysexin','noteout','ctlout','pgmout','bendout','touchout','polytouchout','midiout','stripnote','tabread','tabread4','tabwrite','soundfiler','loadbang','serial','netsend','netreceive','qlist','textfile','openpanel','savepanel','bag','poly','key','keyup','keyname','declare','adc~','dac~','bang~','block~','switch~','catch~','throw~','line~','vline~','threshold~','snapshot~','vsnapshot~','samplerate~','readsf~','receive~','send~','writesf~','sig~','+~','-~','*~','/~','max~','min~','clip~','q8_rsqrt~','q8_sqrt~','wrap~','fft~','ifft~','rfft~','rifft~','framp~','mtof~','ftom~','rmstodb~','dbtorms~','rmstopow~','powtorms~','pow~','log~','exp~','abs~','expr~','fexpr~','phasor~','cos~','osc~','tabwrite~','tabplay~','tabread~','tabread4~','tabosc4~','tabsend~','tabreceive~','bonk~','fiddle~','env~','vcf~','noise~','hip~','lop~','bp~','biquad~','samphold~','print~','rpole~','rzero~','rzero_rev~','cpole~','czero~','czero_rev~','complex-mod~','hilbert~','rev1~','rev2~','rev3~','delwrite~','delread~','vd~','pd','inlet','outlet','inlet~','outlet~','table','drawcurve','filledcurve','drawpolygon','filledpolygon','plot','drawnumber','struct','pointer','get','set','element','getsize','setsize','append','sublist','t','f','until','list','s','hsl','nbx','length','del','tgl','r','bng','sel','gate','i','r~','s~'}

def lint(path, abstractions, extended=None, verbose=False):
    '''Lint a single file'''
    global vanilla
    if verbose:
        print('Linting ' + pathTools.relpath(path))
    with open(path, 'r') as pdFile:
        canvasStack = [None]

        # shortcircuit if format doesn't seem like regular pd
        try:
            if pdFile.readline().split()[0] != '#N':
                return

            for lineNumber, contents in enumerate(pdFile):
                words = contents.split()
                if len(words) >= 5:
                    if words[1] == 'canvas' and re.match('.*[^\d;]', words[6]):
                        canvasStack.append(words[6])
                    elif words[1] == 'restore':
                        canvasStack.pop()
                    elif words[1] == 'obj': 
                        objectName = words[4].strip(';')
                        if objectName not in vanilla and objectName not in abstractions:
                            pickTheLint(objectName, lineNumber, path, canvasStack[-1], extended)

        except UnicodeDecodeError:
            return

def pickTheLint(object, line, path, subpatch=None, extended=None):
    '''Output what we've found'''
    path = pathTools.relpath(path)
    subpatchMessage = ' (subpatch %s)' % subpatch if subpatch else ''

    extendedMessage = ''
    if extended != None:
        if object in extended:
            libraryName = pathTools.split(extended[object])[0].split('/')[-1]
            extendedMessage = ' (%s)' % libraryName
        else:
            extendedMessage = ' (not found in extended)'

    message = 'Line {}{} of {}: {}{}'.format(line, subpatchMessage, path, object, extendedMessage)
    print(message)

def recursePath(path, verbose=False, ignore={}):
    '''Build a dictionary of {filename: path}s, scanning the given path recursively'''
    tail = pathTools.split(path)[1]
    if len(tail) and tail[0] == '.':
        return {}
    if pathTools.isfile(path):
        filename, extension = pathTools.splitext(tail)
        if extension == '.pd' or extension == '.pd_linux':
            if verbose:
                print('Found pd file ' + filename + extension)
            return {filename: path}
    if pathTools.isdir(path):
        if pathTools.abspath(path) in ignore:
            if verbose:
                print('Ignoring ' + pathTools.relpath(path))
            return {}
        if verbose:
            print('Preparing directory ' + pathTools.relpath(path))
        paths = {}
        for subfile in os.listdir(path):
            subpath = pathTools.join(path, subfile)
            paths = {**paths, **recursePath(subpath, verbose, ignore)}
        if verbose:
            print('Done with directory ' + pathTools.relpath(path))
        return paths
    return {}

def main(args):
    extended = None
    if args.e != None:
        extended = {}
        for path in args.e:
            extended = {**extended, **recursePath(path)}

    ignore = {}
    if args.i != None:
        ignore = {pathTools.abspath(ignorepath) for ignorepath in args.i}

    pathdict = {}
    for path in args.f:
        pathdict = {**pathdict, **recursePath(path, args.verbose, ignore)}

    for _, path in pathdict.items():
        lint(path, pathdict, extended, args.verbose)

if __name__ == '__main__':
    eHelp = 'Path(s) to Pd-extended or similar collection of libraries. The linter will tell you which library each linted object comes from.'
    fHelp = 'Pd files or directories to scan. If none are given, current working directory is scanned. Directories are scanned recursively.'
    argParser = argparse.ArgumentParser(description='Scan pd files for non-vanilla objects.')
    argParser.add_argument('-f', nargs='+', metavar='PATH', default=[os.getcwd()], help=fHelp)
    argParser.add_argument('-e', nargs='+', metavar='PATH', help=eHelp)
    argParser.add_argument('-i', nargs='+', metavar='PATH', help='Directories to ignore when scanning recursively')
    argParser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = argParser.parse_args()

    main(args)
