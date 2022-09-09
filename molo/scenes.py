from typing import Dict, List

from molo.processors import detectChapter, detectComment

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