mscenes = {};
mscene_cur = "main"

function mgoto(name=mscene_cur) {
    mscenes[name]();
    mscene_cur = name;
}

function molostart() {
    mscenes[mscene_cur]();
}