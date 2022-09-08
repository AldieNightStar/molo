from types import FunctionType
from typing import List


def readFileToLines(filename) -> List[str]:
    with open(filename) as f:
        return [_noReturnAtEnd(ln) for ln in f.readlines()]

def readFileToLinesWithImports(filename) -> List[str]:
    lines = readFileToLines(filename)
    arr: List[str] = []
    for line in lines:
        imp = _detectImport(line)
        if imp:
            if imp[-1] == "\n": imp = imp[:len(imp)-1]
            arr.extend(readFileToLines(imp))
            continue
        arr.append(line)
    return arr

def _noReturnAtEnd(line: str):
    if line[-1] == "\n": line = line[:len(line)-1]
    return line

def _detectImport(line: str) -> str:
    if line.startswith("$import "):
        return line[8:]