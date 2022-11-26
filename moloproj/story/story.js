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
window.music = new Audio();
window.sound = new Audio();

window._timers = [];
window.textTransition = 500;

function percentOf(num, percent) {
    return (num / 100) * percent
}

function _setTimeout(cb, time) {
    let t = setTimeout(cb, time);
    window._timers.push(t);
    return t;
}

function _setInterval(cb, time) {
    let it = setInterval(cb, time);
    window._timers.push(it);
    return it;
}

function _clearTimers() {
    window._timers.forEach(t => clearInterval(t));
    window._timers = [];
}

function _fadeAdd(source, elem, transitionMS) {
    if (transitionMS < 100) transitionMS = 100;
    elem.style.transition = transitionMS+"ms";
    elem.style.opacity = "0%";
    source.appendChild(elem);
    return new Promise(ok => {
        _setTimeout(() => {
            elem.style.opacity = "100%";
            _setTimeout(ok, transitionMS-50);
        }, 50)
    })
}

function mprint(text, nextLine=true, transition=window.textTransition) {
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

async function printContinue(text) {
    await mprint(text, false);
    return new Promise(async ok => {
        let b = await button(">>", () => {
            ok();
            b.parentElement.removeChild(b);
        });
        await mprint("");
    });
}

async function printLetter(text, time=1000, nextLine=true) {
    let p = document.createElement("span");
    let timePerLetter = time / text.length;
    let ptr = 0;
    let textEl = document.getElementById("text");
    return new Promise(async ok => {
        let interval = 0;
        interval = _setInterval(async () => {
            if (ptr < text.length) {
                p.innerHTML += text[ptr++];
            } else {
                clearInterval(interval);
                if (nextLine) textEl.appendChild(document.createElement("br"))
                _setTimeout(ok, timePerLetter);
            }
        }, timePerLetter)
        await _fadeAdd(textEl, p, 100);
    })
}


function mclear() {
    _clearTimers();
    document.body.style['scale'] = 0.75;
    document.getElementById("text").innerHTML = "";
    setTimeout(() => {
        document.body.style['scale'] = 1;
    }, 100);
}

async function button(name, onclick) {
    let el = document.getElementById("text");
    let b = document.createElement("button");
    b.innerText = name;
    b.onclick = onclick;
    await _fadeAdd(el, b, 50);
    return b;
}

async function buttonX(name, sceneToGo, func = ()=>{}) {
    if (sceneToGo === "" || sceneToGo === 0 || sceneToGo === null) sceneToGo = mscene_cur
    return await button(name, () => { func(); mgoto(sceneToGo); });
}

function addImage(src, sizew=100, sizeh=sizew) {
    let img = document.createElement("img");
    let br = document.createElement("br");
    img.src = src;

    // Set width/height in percents
    img.style.width = "" + sizew + "%"; // This line no need to calculate
    img.style.height = "" + percentOf(window.innerHeight, sizeh) + "px";

    let text = document.getElementById("text");
    let promise = _fadeAdd(text, img, window.textTransition);
    text.appendChild(br);
    return promise;
}

function addImageCenter(src) {
    let img = document.createElement("img");
    img.src = src;
    img.className = "centered";
    let text = document.getElementById("text");
    return _fadeAdd(text, img, window.textTransition);
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

function bgImage(src) {
    document.body.style['background-size'] = "100% " + window.innerHeight + "px";
    document.body.style['background-image'] = 'linear-gradient(rgba(0, 0, 0, 0.60), rgba(0, 0, 0, 0.60)), url("' + src + '")';
    document.body.style['background-repeat'] = "no-repeat";
    document.body.style['background-attachment'] = "fixed";
    document.body.style['transition'] = "200ms";
    bgPosisition("center"); // Change position back to normal
    bgScale(1, 1); // Change scale back to normal
}

function bgPosisition(posString) {
    document.body.style['background-position'] = posString;
}

function bgTransition(n) {
    document.body.style.transition = n + "ms";
}

function bgScale(scaleX, scaleY) {
    document.body.style['background-size'] = (window.innerWidth * scaleX) + "px " + (window.innerHeight * scaleY) + "px";
}

function bgSwipe(pos1, pos2, transitionMS) {
    return new Promise(ok => {
        bgTransition(0);
        bgScale(2, 2);
        bgPosisition(pos1);

        _setTimeout(ok, transitionMS);
    
        _setTimeout(() => {
            bgTransition(transitionMS - transitionMS * .1)
            bgPosisition(pos2)
        }, transitionMS * .1)
    })
}

function bgZoom(size1, size2, transitionMS) {
    return new Promise(ok => {
        bgTransition(0);
        bgScale(size1, size1);
        bgPosisition("center");

        _setTimeout(ok, transitionMS);
    
        _setTimeout(() => {
            bgScale(size2, size2);
            bgTransition(transitionMS - transitionMS * .1)
            bgPosisition("center")
        }, transitionMS * .1)
    })
}

function wait(n) {
    return new Promise(ok => {
        _setTimeout(ok, n);
    })
}

function waitToMusicTime(time) {
    return new Promise(ok => {
        if (music.paused || music.currentTime >= time) {
            ok();
            return;
        }
        let interval = 0;
        interval = _setInterval(() => {
            if (music.currentTime >= time) {
                ok();
                clearInterval(interval);
            }
        }, 1000);
    })
}

function title(text) {
    let t = document.createElement("h1");
    t.style.textAlign = "center";
    t.innerHTML = text;
    return _fadeAdd(document.getElementById('text'), t, textTransition);
}
mscenes[`myalert`] = async function() {
    window.alert("Hello from alert scene. I am used as function");
};
mscenes[`main`] = async function() {
    bgImage("res/bg.jpg");
    await title("Some title");
    addImageCenter("res/divider.png");
    await mprint(`Some text`);
};