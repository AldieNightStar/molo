from typing import Dict, List, Tuple
from molo.data import *
from molo.processors import *

def readImportsFromSpecs(creg: CommandRegistry, specs: List[str]) -> Tuple[List[str], List[str]]:
    "read specs and excludes imports. Returns: importedFilesSource, specs"
    imports: List[str] = []
    newSpecs: List[str] = []
    array: List[str] = []
    # Filter all import to imports array
    # Rest specs push to newSpecs
    for spec in specs:
        imp = detectSpecIsImport(spec)
        if imp: imports.append(imp); continue
        newSpecs.append(spec)
    # Process imports by importing files from that list and adding everything to lines array
    # Command Registries will be merged to current one
    for imp in imports:
        with open(imp) as f:
            src = f.read()
            compiled, specs, creg2 = compile(src)
            array.append(compiled)
            creg.merge(creg2)
    return array, newSpecs

def compile(src: str) -> Tuple[str, List[str], CommandRegistry]:
    "Reads source and returns: compiledSource, specs, commandRegistry"
    chapters, specs, creg = readFile(src)
    srcs, specs = readImportsFromSpecs(creg, specs)
    compiledSrc, specs = compileFile(chapters, specs, creg)
    return "\n".join(("\n".join(srcs), compiledSrc)), specs, creg

def compileFile(chapters: Dict[str, List[str]], specs: List[str], creg: CommandRegistry) -> Tuple[
                                                                                            str,
                                                                                            List[str]]:
    "Compiles file into a string and return: source, specs"
    # Process all the chapters
    processedChapters = processAllChapters(creg, chapters)
    # Now make all the chapters 'mscene' callbacks
    sb: List[str] = []
    for name, text in processedChapters.items():
        sb.append(makeChapterAsScene(name, text))
    # Concatenate all the scene functions into one string
    return ("\n".join(sb), specs)

def readFile(src: str) -> Tuple[
                            Dict[str, List[str]],
                            List[str],
                            CommandRegistry]:
    "reads file and returns: chapters, specs, commandRegistry"
    lines = src.splitlines()
    # Register all needed stuff
    commandRegistry = CommandRegistry()
    currentChapter: str = None
    chapterLines: List[str] = []
    chapters: Dict[str, List[str]] = {}
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
    return chapters, specs, commandRegistry