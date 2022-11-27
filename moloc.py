#!/bin/env python
import shutil
from time import sleep
from molo import compile
import os.path
import io
import sys

# Get real project directory name
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Ensure script will use local packages
sys.path.insert(0, CURRENT_DIR)

USAGE = """moloc.py [filename] [outfilename] [auto]
    moloc.py filename outfilename auto  - rebuild file every 5 seconds
    moloc.py filename outfilename       - build file
    moloc.py new name                   - create project based on moloproj template
"""

def auto(filename, outname):
    while True:
        print("Rebuild...")
        buildFile(filename, outname)
        sleep(5)

def buildFile(filename, outname=None):
    chapters, _ = compile(filename)
    if outname == None: outname = filename + ".js"
    with io.open(outname, 'w', encoding="UTF-8") as f:
        f.write(chapters)

def buildProj(name):
    shutil.copytree(CURRENT_DIR+"/moloproj", "./"+name)

def main():
    argIter = iter(sys.argv[1:])
    firstArg = next(argIter, None)
    if firstArg == None: print(USAGE); return
    if firstArg == "new":
        projname = next(argIter, None)
        if projname == None: print(USAGE); return
        buildProj(projname)
        print("OK")
        return
    # If first args is file name
    filename = firstArg
    outfile = next(argIter, None)
    if outfile == None: print(USAGE); return
    
    isAuto = next(argIter, "") == "auto"
    if not os.path.isfile(filename):
        print(f"ERR: File \"{filename}\" not exists")
        return
    if isAuto:
        auto(filename, outfile)
    else:
        buildFile(filename, outfile)
        print("OK")

if __name__ == "__main__": main()
