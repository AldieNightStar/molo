from typing import Dict, List
from molo.data import CommandRegistry

from molo.processors import detectChapter, detectCommand, detectComment
from molo.replacer import replaceScenes, replaceTime, replaceVars

def processJS(line: str) -> str:
    "Function which processes js lines and add some abilities to it"
    # Replace variables: @@@scene_name to window.mscenes['scene_name']
    line = replaceScenes(line)
    # Replace variables: @@a to window.mvars['a']
    line = replaceVars(line)
    # Process time lines T1:25 to 85 (Convert time representation string to number)
    line = replaceTime(line)
    return line

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
        # Lines starting with "*" is JS code as well
        if line.startswith("*") and not line.startswith("**"):
            # Process js line
            jsline = processJS(line[1:].lstrip())
            arr.append(jsline)
            continue
        # Js mode allows to add { ... } blocks of js code
        if jsMode:
            # If line is ".endjs" then we ending
            if line == ".endjs": arr.append("}"); jsMode = False; continue\
            # Process js line
            line = processJS(line)
            # Add some tabulation
            arr.append("    " + line)
            continue
        # .js command allows to set jsMode
        if line == ".js":
            jsMode = True
            arr.append("{")
            continue
        # Parse command and render by command registry
        command = detectCommand(line)
        if command: arr.append(creg.renderCommand(command)); continue
        # If no command etc, then add default print command
        line = line.replace("`", "'")
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