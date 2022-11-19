import re

VAR_WORD = re.compile(r"\$\$[\wа-яієї]+")
VAR_WORD_SCENE = re.compile(r"\$\$\$[\wа-яієї]+")
TIME_WORD = re.compile(r"T\d+\:\d\d")

def processVariables(line: str) -> str:
    "Function which processes js lines and add some abilities to it"
    # Replace variables: @@@scene_name to window.mscenes['scene_name']
    line = replaceScenes(line)
    # Replace variables: @@a to window.mvars['a']
    line = replaceVars(line)
    # Process time lines T1.25 to 85 (Convert time representation string to number)
    line = replaceTime(line)
    return line

def __def_converter_specvar(s: str) -> str:
    if s.startswith("$$"): s = s[2:]
    return f"window.mvars['{s}']"

def __def_converter_specvar_scene(s: str) -> str:
    if s.startswith("$$$"): s = s[3:]
    return f"window.mscenes['{s}']"

def __def_converter_time(s: str) -> str:
    if not ":" in s: return
    if s.startswith("T"): s = s[1:]
    arr = s.split(".", 1)
    if len(arr) != 2: raise RuntimeError("Time string is not m:ss format")
    min, sec = int(arr[0]), int(arr[1])
    return f"{(min*60)+sec}"

def replaceByRe(re: re.Pattern[str], src: str, converterFn) -> str:
    for x in re.finditer(src):
        s = x.group(0)
        if s == None: continue
        src = src.replace(s, converterFn(s))
    return src

def replaceScenes(src: str, converterFn=__def_converter_specvar_scene):
    return replaceByRe(VAR_WORD_SCENE, src, converterFn)

def replaceVars(src: str, converterFn=__def_converter_specvar) -> str:
    return replaceByRe(VAR_WORD, src, converterFn)

def replaceTime(src: str, converterFn=__def_converter_time) -> str:
    return replaceByRe(TIME_WORD, src, converterFn)