window.mscenes = {};
window.mscene_cur = "main"

function mgoto(name=mscene_cur) {
    window.mscenes[name]();
    window.mscene_cur = name;
}

function molostart() {
    window.mscenes[window.mscene_cur]();
}