#!/bin/env python
from time import sleep
from molo import compile
import sys

USAGE = """moloc.py [filename] [auto]
    moloc.py filename       - build file
    moloc.py filename auto  - rebuild file every 5 seconds
"""

def watch(filename):
    while True:
        sleep(5)
        print("Rebuild...")
        buildFile(filename)

def buildFile(filename):
    chapters, _ = compile(filename)
    with open(filename + ".js", 'w') as f:
        f.write(chapters)

if __name__ == "__main__":
    def _f():
        args = sys.argv[1:]
        if len(args) < 1:
            print("Please enter file name")
            return
        filename = args[0]
        if "watch" in args:
            watch(filename)
        else:
            buildFile(filename)
            print("OK")
    _f()
