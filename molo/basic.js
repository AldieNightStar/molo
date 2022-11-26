window.mscenes = {};
window.mscene_cur = "main";
window.mvars = {};

function mgoto(name=mscene_cur) {
    mclear();
    window.mscene_cur = name;
    window.mscenes[name]();
}

function molostart() {
    mclear();
    window.mscenes[window.mscene_cur]();
}