mscenes = {};
mscene_cur = "main"

function mscene(name, func) {
    mscene[name] = func;
}

function mgoto(name=mscene_cur) {
    mscenes[name]();
    mscene_cur = name;
}

function molostart() {
    mscenes[mscene_cur]();
}