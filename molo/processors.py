from typing import Dict, List, Tuple

from molo.data import *

def readJsFromSpecs(specs: List[str]) -> List[str]:
    jsFiles = []
    arr = []
    for spec in specs:
        if spec.startswith("js "):
            jsFiles.append(spec[3:])
            continue
    for jsFile in jsFiles:
        with open(jsFile) as f:
            arr.append(f.read())
    return arr

def readSpecs(lines: List[str]) -> List[str]:
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

def makeChapterAsScene(chapterName: str, text: str) -> str:
    tabtext = "    " + text.replace("\n", "\n    ")
    return f"mscene(`{chapterName}`, async function() {{\n{tabtext}\n}});"

def detectSpecIsRegisterCommand(spec: str):
    if not spec.startswith("register "): return
    spec = spec[9:] # Skip "register "
    arr = spec.split(" ", 1)
    if len(arr) < 2: return None
    return arr

def detectSpecIsImport(spec: str):
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

def processChapter(creg: CommandRegistry, chapterLines: List[str]) -> List[str]:
    "Replaces lines with commands"
    arr: List[str] = []
    jsMode = False
    for line in chapterLines:
        if jsMode:
            if line == ".endjs": arr.append("}"); jsMode = False; continue
            arr.append("    " + line)
            continue
        if line == ".js":
            jsMode = True
            arr.append("{")
            continue
        # Parse command and render by command registry
        command = detectCommand(line)
        if command: arr.append(creg.renderCommand(command)); continue
        # If no command etc, then add default print command
        # TODO: replace "`" to "'" symbols
        arr.append(f"mprint(`{line}`);")
    return arr

def processAllChapters(creg: CommandRegistry, chapters: Dict[str, List[str]]) -> Dict[str, str]:
    newChapters: Dict[str, List[str]] = {}
    for name, chapterLines in chapters.items():
        # Replace chapter lines with commands
        newChapters[name] = "\n".join(processChapter(creg, chapterLines))
    return newChapters
