#!/usr/bin/env python3

import os
import sys
import re
import argparse

vanilla = {'bang','change','float','int','makefilename','moses','pack','print','receive','route','select','send','spigot','swap','symbol','trigger','unpack','until','value','choice','&','|','<<','>>','&&','||','%','+','-','*','/','pow','>','>=','=','<=','<','clip','max','min','mod','div','sin','cos','tan','atan','atan2','exp','log','abs','sqrt','pow','mtof','ftom','dbtorms','rmstodb','dbtopow','powtodb','random','wrap','expr','cputime','delay','line','metro','pipe','realtime','timer','makenote','notein','ctlin','pgmin','bendin','touchin','polytouchin','midiin','sysexin','noteout','ctlout','pgmout','bendout','touchout','polytouchout','midiout','stripnote','tabread','tabread4','tabwrite','soundfiler','loadbang','serial','netsend','netreceive','qlist','textfile','openpanel','savepanel','bag','poly','key','keyup','keyname','declare','adc~','dac~','bang~','block~','switch~','catch~','throw~','line~','vline~','threshold~','snapshot~','vsnapshot~','samplerate~','readsf~','receive~','send~','writesf~','sig~','+~','-~','*~','/~','max~','min~','clip~','q8_rsqrt~','q8_sqrt~','wrap~','fft~','ifft~','rfft~','rifft~','framp~','mtof~','ftom~','rmstodb~','dbtorms~','rmstopow~','powtorms~','pow~','log~','exp~','abs~','expr~','fexpr~','phasor~','cos~','osc~','tabwrite~','tabplay~','tabread~','tabread4~','tabosc4~','tabsend~','tabreceive~','bonk~','fiddle~','env~','vcf~','noise~','hip~','lop~','bp~','biquad~','samphold~','print~','rpole~','rzero~','rzero_rev~','cpole~','czero~','czero_rev~','complex-mod~','hilbert~','rev1~','rev2~','rev3~','delwrite~','delread~','vd~','pd','inlet','outlet','inlet~','outlet~','table','drawcurve','filledcurve','drawpolygon','filledpolygon','plot','drawnumber','struct','pointer','get','set','element','getsize','setsize','append','sublist','t','f','until','list','s','hsl','nbx','length','del','tgl','r','bng','sel','gate','i','r~','s~'}

def lint(path, abstractions, extended=None):
    global vanilla
    # print('Scanning ' + path)
    with open(path, 'r') as pdFile:
        canvasStack = [None]
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

def pickTheLint(object, line, path, subpatch=None, extended=None):
    subpatchMessage = ' (subpatch %s)' % subpatch if subpatch else ''
    
    extendedMessage = ''
    if extended != None:
        if object in extended:
            libraryName = os.path.split(extended[object])[0].split('/')[-1]
            extendedMessage = ' (%s)' % libraryName
        else:
            extendedMessage = ' (not found in extended)'
    
    message = 'Line {}{} of {}: {}{}'.format(line, subpatchMessage, path, object, extendedMessage)
    print(message)

def recursePath(path):
    '''Build a dictionary of {filename: path}s, scanning the given path recursively'''
    tail = os.path.split(path)[1]
    if len(tail) and tail[0] == '.':
        return {}
    if os.path.isfile(path):
        filename, extension = os.path.splitext(tail)
        if extension == '.pd' or extension == '.pd_linux':
            return {filename: path}
    if os.path.isdir(path):
        paths = {}
        for subfile in os.listdir(path):
            subpath = os.path.join(path, subfile)
            paths = {**paths, **recursePath(subpath)}
        return paths
    return {}

def main(args):
    extended = None
    if args.e != None:
        extended = {}
        for path in args.e:
            extended = {**extended, **recursePath(path[0])}
    
    pathdict = {}
    for path in args.paths:
        pathdict = {**pathdict, **recursePath(path)}
    
    for _, path in pathdict.items():
        lint(path, pathdict, extended)

if __name__ == '__main__':
    eHelp = 'Path to Pd-extended or similar collection of libraries. The linter will tell you which library each linted object comes from.'
    pathHelp = 'Pd files or directories to scan. If none are given, current working directory is scanned. Directories are scanned recursively.'
    argParser = argparse.ArgumentParser(description='Scan pd files for non-vanilla objects.')
    argParser.add_argument('-e', nargs=1, metavar='PATH', action='append', help=eHelp)
    argParser.add_argument('paths', nargs='*', metavar='PATH', default='./', help=pathHelp)
    
    args = argParser.parse_args()
    
    main(args)
