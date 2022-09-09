from typing import Dict, List
from molo.data import CommandRegistry

from molo.processors import detectChapter, detectCommand, detectComment

def parseChapters(lines: List[str]) -> Dict[str, List[str]]:
    chapters: Dict[str, List[str]] = {}
    chapterLines: List[str] = []
    currentChapter: str = None
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
    return chapters

def processChapter(creg: CommandRegistry, chapterLines: List[str]) -> List[str]:
    "Replaces lines with commands"
    arr: List[str] = ["mclear();"]
    jsMode = False
    for line in chapterLines:
        # Js mode allows to add { ... } blocks of js code
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

def makeChapterAsScene(chapterName: str, text: str) -> str:
    tabtext = "    " + text.replace("\n", "\n    ")
    return f"mscenes[`{chapterName}`] = async function() {{\n{tabtext}\n}};"