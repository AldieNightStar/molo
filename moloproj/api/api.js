window.music = new Audio();
window.sound = new Audio();

window._timers = [];

function _setTimeout(cb, time) {
    window._timers.push(setTimeout(cb, time));
}

function _setInterval(cb, time) {
    window._timers.push(setInterval(cb, time));
}

function _clearTimers() {
    window._timers.forEach(t => clearInterval(t));
    window._timers = [];
}

function _fadeAdd(source, elem, transitionMS) {
    elem.style.transition = transitionMS+"ms";
    elem.style.opacity = "0%";
    source.appendChild(elem)
    return new Promise(ok => {
        _setTimeout(() => {
            elem.style.opacity = "100%";
            _setTimeout(ok, transitionMS);
        })
    })
}

function mprint(text, nextLine=true, transition=1000) {
    let t = document.createElement("span");
    t.innerText = text;
    let textEl = document.getElementById("text");
    let promise = _fadeAdd(textEl, t, transition);
    if (nextLine) {
        let br = document.createElement("br");
        textEl.appendChild(br);
    }
    return promise;
}

function printContinue(text) {
    mprint(text, false);
    return new Promise(ok => {
        let b = button(">>", () => {
            ok();
            b.parentElement.removeChild(b);
        });
        mprint("");
    });
}
function mclear() {
    _clearTimers();
    document.getElementById("text").innerHTML = "";
}
function button(name, onclick) {
    let el = document.getElementById("text");
    let b = document.createElement("button");
    b.innerText = name;
    b.onclick = onclick;
    el.appendChild(b);
    return b;
}

function buttonX(name, sceneToGo, func = ()=>{}) {
    if (sceneToGo === "" || sceneToGo === 0 || sceneToGo === null) sceneToGo = mscene_cur
    return button(name, () => { func(); mgoto(sceneToGo); });
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

window.defaultColor = "rgb(27, 20, 0)";

function bgColor(color) {
    if (color) {
        document.body.style.backgroundColor = color;
    }
    return document.body.style.backgroundColor ? document.body.style.backgroundColor : defaultColor;
}

function fontColor(color) {
    if (color) {
        document.body.style.color = color;
    }
    return document.body.style.color ? document.body.style.color : "white";
}
