#!/bin/bash

readonly prefix='/tmp/bnl304a' # location of conda env; change as you see fit

declare -ar packages=( pyqt numpy scipy matplotlib pandas networkx sympy )
conda create --prefix "${prefix}" "${packages[@]}"
