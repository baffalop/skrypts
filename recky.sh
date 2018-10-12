#!/usr/bin/env bash

if (( ${#@} < 3 )); then
    echo 'Usage: recky.sh COMMAND EXTENSION [FILES|GLOB]'
    echo "Where: '#' in COMMAND will be replaced by each file in FILES"
    exit 65
fi

cmd="$1";
ext="$2";

for i in ${@:3}; do
    ${cmd/'#'/$i} "${i%.*}.$ext"
done
