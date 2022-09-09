from typing import Dict, List, Tuple
from molo.data import *
from molo.processors import *
from molo.reader import readFileToLinesWithImports

def compile(filename: str) -> Tuple[str, CommandRegistry]:
    "Reads source and returns: compiledSource, specs, commandRegistry"
    chapters, specs, creg = readFile(filename)
    compiledSrc = compileFile(chapters, specs, creg)
    return compiledSrc, creg

def compileFile(chapters: Dict[str, List[str]], specs: List[str], creg: CommandRegistry) -> Tuple[str]:
    "Compiles file into a string and return: source, specs"
    # Process all the chapters
    processedChapters = processAllChapters(creg, chapters)
    # Now make all the chapters 'mscene' callbacks
    sb: List[str] = []
    for name, text in processedChapters.items():
        sb.append(makeChapterAsScene(name, text))
    # Concatenate all the scene functions into one string
    return "\n".join(sb)

def readFile(filename: str) -> Tuple[
                            Dict[str, List[str]],
                            List[str],
                            CommandRegistry]:
    "reads file and returns: chapters, specs, commandRegistry"
    lines = readFileToLinesWithImports(filename)
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