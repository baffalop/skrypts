#!/usr/bin/env bash

cmd="$1";
ext="$2";

for i in ${@:3}; do
    ${cmd/'#'/$i} "${i%.*}.$ext"
done
