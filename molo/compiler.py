from typing import Dict, List, Tuple

class CompileError(RuntimeError): pass

class Command:
    def __init__(self, name: str, args: str) -> None:
        self.name = name
        self.args = args
    def __str__(self) -> str:
        return f"Command<{self.name}: {self.args}>"
    def __repr__(self) -> str:
        return self.__str__()

class CommandRegistry:
    def __init__(self):
        self.reg: Dict[str, str] = {}
    def renderCommand(self, cmd: Command) -> str:
        val = self.reg.get(cmd.name, None)
        if val == None: return f"// no such function: {cmd.name}"
        # TODO: also replace "##" with escaped "args"
        return val.replace("$$", cmd.args)
    def register(self, name: str, val: str):
        self.reg[name] = val

def readCommandsFromSpecs(reg: CommandRegistry, specs: List[str]) -> List[str]:
    newspecs = []
    for spec in specs:
        creg = detectSpecIsRegisterCommand(spec)
        if creg: reg.register(creg[0], creg[1]); continue
        newspecs.append(spec)
    return newspecs

def readSpecs(lines: List[str]) -> List[str]:
    newLines: List[str] = []
    specs: List[str] = []
    specMode = True
    for line in lines:
        if specMode:
            spec = detectSpecial(line)
            if spec: specs.append(spec); continue
            if detectChapter(line):
                specMode = False
        newLines.append(line)
    return specs, lines

def compileFile(src: str) -> Tuple[str, List[str]]:
    lines = src.splitlines()
    # Register all needed stuff
    commandRegistry = CommandRegistry()
    currentChapter: str = None
    chapterLines: List[str] = []
    chapters = {}
    # Read specs from lines
    specs, lines = readSpecs(lines)
    # Read command registry from specs and exclude $register commands
    specs = readCommandsFromSpecs(commandRegistry, specs)
    # Begin processing
    for line in lines:
        line = line.lstrip()
        # Skip comments
        if detectComment(line): continue
        # Parse chapter heading
        chapter = detectChapter(line)
        if chapter:
            # Add all lines to previous chapter before create new one
            if currentChapter != None and len(chapterLines) > 0:
                chapters[currentChapter] = chapterLines
                chapterLines = []
            # Change current chapter name to new one
            currentChapter = chapter
            continue
        # Add non empty lines to current chapter
        if currentChapter != None and len(line) > 0:
            chapterLines.append(line)
    if len(chapterLines) > 0:
        chapters[currentChapter] = chapterLines
    # Process all the chapters
    processedChapters = processAllChapters(commandRegistry, chapters)
    # Now make all the chapters 'mscene' callbacks
    sb: List[str] = []
    for name, text in processedChapters.items():
        sb.append(makeChapterAsScene(name, text))
    # Concatenate all the scene functions into one string
    return ("\n".join(sb), specs)

def makeChapterAsScene(chapterName: str, text: str) -> str:
    tabtext = "    " + text.replace("\n", "\n    ")
    return f"mscene(`{chapterName}`, async function() {{\n{tabtext}\n}});"

def processChapter(creg: CommandRegistry, chapterLines: List[str]) -> List[str]:
    "Replaces lines with commands"
    arr: List[Command] = []
    for line in chapterLines:
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

def detectSpecIsRegisterCommand(spec: str):
    if not spec.startswith("register "): return
    spec = spec[9:] # Skip "register "
    arr = spec.split(" ", 1)
    if len(arr) < 2: return None
    return arr
    

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

if __name__ == "__main__":
    def _f():
        import sys
        args = sys.argv[1:]
        if len(args) < 1:
            print("Please enter file name")
        filename = args[0]
        with open(filename) as f:
            src = f.read()
            chapters, specs = compileFile(src)
            print(chapters)
    _f()