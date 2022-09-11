from typing import Dict, List, Tuple
from molo.data import *
from molo.processors import *
from molo.reader import readFileToLinesWithImports
from molo.chapter import makeChapterAsScene, parseChapters, processAllChapters

import os.path
import io

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
BASIC_JS_FILE_NAME = THIS_FOLDER + "/basic.js"

def compile(filename: str) -> Tuple[str, CommandRegistry]:
    "Reads source and returns: compiledSource, commandRegistry"
    chapters, specs, creg = readFile(filename)
    compiledSrc = compileFile(chapters, specs, creg)
    # Add basic api to compiled source
    with io.open(BASIC_JS_FILE_NAME, encoding="UTF-8") as f:
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
    # Concatenate all the scene functions into one string
    scenes = "\n".join(sb)
    # Find $js commands and import js files if needed
    jsFiles = "\n".join(readJsFromSpecs(specs))
    # Concat js files and scenes
    return jsFiles + "\n" + scenes

def readFile(filename: str) -> Tuple[Dict[str, List[str]], List[str], CommandRegistry]:
    "Reads file and returns: chapters, specs, commandRegistry"
    lines = readFileToLinesWithImports(filename)
    commandRegistry = CommandRegistry()
    # Read specs from lines
    specs, lines = readSpecs(lines)
    # Read command registry from specs and exclude $register commands
    specs = readCommandsFromSpecs(commandRegistry, specs)
    # Read the chapters from the lines
    chapters = parseChapters(lines)
    # Return everything up
    return chapters, specs, commandRegistry