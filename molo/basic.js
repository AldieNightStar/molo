window.mscenes = {};
window.mscene_cur = "main";
window.mvars = {};

function mgoto(name=mscene_cur) {
    mclear();
    window.mscenes[name]();
    window.mscene_cur = name;
}

function molostart() {
    window.mscenes[window.mscene_cur]();
}