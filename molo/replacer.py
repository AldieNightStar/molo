import re

SPEC_WORD = re.compile(r"\@\@[\wа-яієї]+")

def __def_converter(s: str) -> str:
    if s.startswith("@@"): s = s[2:]
    return f"window.mvars['{s}']"

def replaceVars(src: str, converterFn=__def_converter) -> str:
    for x in SPEC_WORD.finditer(src):
        s = x.group(0)
        if s == None: continue
        src = src.replace(s, converterFn(s))
    return src
