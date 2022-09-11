window.music = new Audio();
window.sound = new Audio();

function mprint(text, nextLine=true) {
    let t = document.createElement("span");
    t.innerText = text;
    let textEl = document.getElementById("text");
    textEl.appendChild(t);
    if (nextLine) {
        let br = document.createElement("br");
        textEl.appendChild(br);
    }
}

function printContinue(text) {
    mprint(text, false);
    return new Promise(ok => {
        button(">>", ok);
        mprint("");
    });
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

function playSound(src, vol=.5) {
    sound.src = src;
    sound.loop = false;
    sound.volume = vol;
    sound.currentTime = 0;
    sound.play();
}

function stopSound() {
    sound.pause();
    sound.currentTime = 0;
}