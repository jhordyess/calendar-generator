#!/bin/bash
#? pip3 install python-dateutil
# Generate tex file
python3 index.py
# Compile
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error index.tex
# Clean
find . -type f \( -iname \*.aux -o -iname \*.log -o -iname \*.synctex.gz \) -delete