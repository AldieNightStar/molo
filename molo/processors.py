from typing import Dict, List, Tuple

from molo.data import *
import io

from molo.replacer import processJS

def readJsFromSpecs(specs: List[str]) -> List[str]:
    """
    Reads Spec lines and returns js files (src) to concat.
    Also it processing js-lines. So @@vars and @@@scenes are working as well
    """
    jsFiles = []
    arr = []
    for spec in specs:
        if spec.startswith("js "):
            jsFiles.append(spec[3:])
            continue
    for jsFile in jsFiles:
        with io.open(jsFile, encoding="UTF-8") as f:
            src = processJS(f.read())
            arr.append(src)
    return arr

def readSpecs(lines: List[str]) -> Tuple[List[str], List[str]]:
    "Reads specs from lines and remove. Returns: lines, specs"
    newLines: List[str] = []
    specs: List[str] = []
    for line in lines:
        spec = detectSpecial(line)
        if spec: specs.append(spec); continue
        newLines.append(line)
    return specs, lines

def readCommandsFromSpecs(reg: CommandRegistry, specs: List[str]) -> List[str]:
    newspecs = []
    for spec in specs:
        creg = detectSpecIsRegisterCommand(spec)
        if creg: reg.register(creg[0], creg[1]); continue
        newspecs.append(spec)
    return newspecs

def detectSpecIsRegisterCommand(spec: str) -> str:
    if not spec.startswith("register "): return
    spec = spec[9:] # Skip "register "
    arr = spec.split(" ", 1)
    if len(arr) < 2: return None
    return arr

def detectSpecIsImport(spec: str) -> str:
    if not spec.startswith("import "): return None
    return spec[7:]

def detectCommand(line: str) -> Command:
    if len(line) < 2: return
    if line.startswith(".."): return
    if not line.startswith("."): return
    line = line[1:]
    args = line.split(" ", 1)
    if len(args) == 1:
        return Command(line, "")
    else:
        return Command(args[0], args[1])

def detectSpecial(line: str) -> str:
    if line.startswith("$"):
        return line[1:]
    return None

def detectComment(line: str) -> bool:
    return line.startswith("==")

def detectChapter(line: str) -> str:
    if line.startswith(":"):
        return line[1:]
