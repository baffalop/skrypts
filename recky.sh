#!/usr/bin/env bash

if [[ ${#@} < 3 ]]; then
    echo "Usage: $0 COMMAND EXTENSION [FILES|GLOB]"
    exit 65
fi

cmd="$1";
ext="$2";

for i in ${@:3}; do
    ${cmd/'#'/$i} "${i%.*}.$ext"
done
