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

USAGE = """moloc.py [filename] [auto]
    moloc.py filename auto  - rebuild file every 5 seconds
    moloc.py filename       - build file
    moloc.py new name       - create project based on moloproj template
"""

def auto(filename):
    while True:
        print("Rebuild...")
        buildFile(filename)
        sleep(5)

def buildFile(filename):
    chapters, _ = compile(filename)
    with io.open(filename + ".js", 'w', encoding="UTF-8") as f:
        f.write(chapters)

def buildProj(name):
    shutil.copytree(CURRENT_DIR+"/moloproj", "./"+name)

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print(USAGE)
        return
    filename = args[0]
    if filename == "new":
        buildProj(args[1])
        print("OK")
        return
    if "auto" in args:
        auto(filename)
    else:
        buildFile(filename)
        print("OK")

if __name__ == "__main__": main()
