mscenes = {};

function mscene(name, func) {
    mscene[name] = func;
}

function mgoto(name) {
    mscenes[name]();
}

function molostart() {
    mscenes["main"]();
}