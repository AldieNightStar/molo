function mprint(text) {
    let t = document.createElement("span");
    let br = document.createElement("br");
    t.innerText = text;
    let textEl = document.getElementById("text");
    textEl.appendChild(t);
    textEl.appendChild(br);
}
function mclear() {
    document.getElementById("text").innerHTML = "";
}
function button(name, onclick) {
    let el = document.getElementById("text");
    let b = document.createElement("button");
    b.innerText = name;
    b.onclick = onclick;
    el.appendChild(b);
}

window.store = {}
music = new Audio();

window.вкл = true;
window.выкл = false;
window.вимк = false;

function buttonX(name, sceneToGo) {
    button(name, () => mgoto(sceneToGo));
}

function addImage(src, size) {
    let img = document.createElement("img");
    let br = document.createElement("br");
    img.src = src;
    if (size !== undefined) {
        img.style.width = "" + size + "%";
    }
    let text = document.getElementById("text");
    text.appendChild(img);
    text.appendChild(br);
}

function playMusic(src, vol=.5) {
    if (music.last_src === src && !music.paused) return;
    music.src = src;
    music.last_src = src;
    music.loop = true;
    music.volume = vol;
    music.currentTime = 0;
    music.play();
}

function stopMusic() {
    music.pause();
    music.currentTime = 0;
}

function mstore_set(name, value) {
    window.store[name] = value;
}

function mstore_get(name) {
    return window.store[name]
}

function mstore_switch(name) {
    let val = window.store[name];
    if (!(val instanceof Boolean)) {
        val = true;
    }
    val = !val;
    window.store[name] = val;
}

function mstore_count(name, num=1) {
    let val = window.store[name];
    if (!(val instanceof Number)) {
        val = 0;
    }
    val += num;
    window.store[name] = val;
}