#!/usr/bin/env bash

usage() {
    echo "Usage: grab [-g (to output gif)] [-o OUTPUT_FILE (if renaming)] [-f FPS (default 20)] [-w WIDTH (if scaling)] [-s SPEED] input_file.mov"
    exit 2
}

args=$( getopt hgo:f:w:s: $* )

if [[ "$?" != '0' ]]; then
    exit 1
fi

echo "args is $args"
eval set -- "$args"

while :
do case "$1" in
    -h )
        usage
        ;;
    -g )
        extension=gif
        ;;
    -o )
        output="$2"
        shift
        ;;
    -f )
        if [ -n "$2" ] && [[ "$2" =~ ^[0-9]+$ ]]; then
            shift; fps="$1"
        else    
            echo "Error: $1 requires numeric argument" >&2
            exit 1
        fi
        ;;
    -w )
        if [ -n "$2" ] && [[ "$2" =~ ^[0-9]+$ ]]; then
            shift; width="$1"
        else    
            echo "Error: $1 requires numeric argument" >&2
            exit 1
        fi
        ;;
    -s )
        if [ -n "$2" ] && [[ "$2" =~ ^[0-9]*\.?[0-9]+$ ]]; then
            shift; frames=$( bc<<<"scale=2; 1/$1" )
        else    
            echo "Error: $1 requires numeric argument" >&2
            exit 1
        fi
        ;;
    --)
        shift; break ;;

    *)
        echo "Error: unrecognised option $1"
        exit 1
        ;;
esac; shift; done

echo "\$1 is $1"

if [ -z "$1" ]; then
    echo 'Error: missing input path' >&2
    exit 1
fi

input=$1
input_base=${input%.*}
output=${output:-$input_base}
extension=${extension:-mp4}

vf="fps=${fps:-20}"

[ -n "$frames" ] && vf="$vf,setpts=${frames}*PTS"
[ -n "$width" ] && vf="$vf,scale=${width}:-1:flags=lanczos"
[[ "$extension" == gif ]] && vf="$vf,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"

echo "ffmpeg -i $input -vf "$vf" $output.$extension"
ffmpeg -i "$input" -vf "$vf" "$output.$extension"
