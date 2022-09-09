from typing import Dict, List, Tuple
from molo.data import *
from molo.processors import *
from molo.reader import readFileToLinesWithImports

import os.path

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
BASIC_JS_FILE_NAME = THIS_FOLDER + "/basic.js"

def compile(filename: str) -> Tuple[str, CommandRegistry]:
    "Reads source and returns: compiledSource, commandRegistry"
    chapters, specs, creg = readFile(filename)
    compiledSrc = compileFile(chapters, specs, creg)
    # Add basic api to compiled source
    with open(BASIC_JS_FILE_NAME) as f:
        basicApi = f.read() + "\n"
        return basicApi + compiledSrc, creg

def compileFile(chapters: Dict[str, List[str]], specs: List[str], creg: CommandRegistry) -> str:
    "Compiles file into a string and return: source"
    # Process all the chapters
    processedChapters = processAllChapters(creg, chapters)
    # Now make all the chapters 'mscene' callbacks
    sb: List[str] = []
    for name, text in processedChapters.items():
        sb.append(makeChapterAsScene(name, text))
    # Find $js commands and import js files if needed
    jsFiles = readJsFromSpecs(specs)
    # Concatenate jsFiles
    jsFiles = "\n".join(jsFiles)
    # Concatenate all the scene functions into one string
    scenes = "\n".join(sb)
    # Concat js files and scenes
    return jsFiles + "\n" + scenes

def readFile(filename: str) -> Tuple[Dict[str, List[str]], List[str],CommandRegistry]:
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