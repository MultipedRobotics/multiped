#!/bin/bash

BINARY="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"

# this fisrt and only argument is the definition of the stl export, it defines the $fn variable in openscad
if [[ "$#" -eq 0 ]]; then
    ARG="\$fn=90"
    echo "No argument supplied, using: fn=${ARG}"
  else
    ARG="\$fn=$1"
fi

echo "Generating parts with ${ARG}"

# clear out old STL files
if [[ -d "./stl" ]]; then
    rm -fr ./stl
    mkdir stl
fi

# generate all filename.scad files and output stls in ./stl/filename.stl
for SCAD in *.scad; do
  if [[ "${SCAD}" != "parts.scad" && "${SCAD}" != "common.scad" && "${SCAD}" != "misc.scad" ]]; then
      FNAME=${SCAD%.scad}
      echo "> Processing file: ${SCAD}"
      ${BINARY} -o stl/${FNAME}.stl ${SCAD} -D ${ARG}
      ${BINARY} -o pics/${FNAME}.png ${SCAD} --imgsize=640,480 --viewall
  fi
done
