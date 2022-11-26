window.mscenes = {};
window.mscene_cur = "main";
window.mvars = {};

function mgoto(name=mscene_cur) {
    mclear();
    window.mscene_cur = name;
    window.mscenes[name]();
}

function molostart() {
    window.mscenes[window.mscene_cur]();
}
window.music = new Audio();
window.sound = new Audio();

window._timers = [];
window.textTransition = 1000;

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
    elem.style.transition = transitionMS+"ms";
    elem.style.opacity = "0%";
    source.appendChild(elem);
    return new Promise(ok => {
        _setTimeout(() => {
            elem.style.opacity = "100%";
            _setTimeout(ok, transitionMS);
        })
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
    document.getElementById("text").innerHTML = "";
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

function wait(n) {
    return new Promise(ok => {
        _setTimeout(ok, n);
    })
}
mscenes[`myalert`] = async function() {
    window.alert("Hello from alert scene. I am used as function");
};
mscenes[`main`] = async function() {
    await addImage("res/logo.png", 100, 20);
    await printLetter("This is your story");
    await printContinue("Let's start");
    mclear();
    bgImage("res/bg.jpg");
    await printLetter("As you can see bg image changed. '.bg' command doing that");
    await printLetter("Look closer");
    bgScale(2, 2);
    await printLetter("Left side", 1000);
    bgPosisition("left");
    await printLetter("Or right side", 1000);
    bgPosisition("right");
    await wait(1000);
    bgPosisition("center");
    bgScale(1, 1);
    await printLetter("We done with background!");
    await printContinue("Let's go next");
    await printLetter("Hi all and everything which am added to be it here", 3000);
    await printContinue("Let's start with a new story");
    await printContinue("Write your new world with Molo");
    mclear();
    await printContinue("Cleared screen, is better than polished");
    await buttonX("Next chapter", "chapter2");
    window.mvars['cnt'] = 0;
};
mscenes[`chapter2`] = async function() {
    await button("JS button", () => window.mscenes['myalert']());
    await buttonX("Advanced button", "", () => window.alert("Hello from advanced buttons"));
    await buttonX("Advanced JS button", "", () => window.alert("Hello from JS advanced buttons"))
    await button("Count: " + window.mvars['cnt'], () => { window.mvars['cnt'] += 1; mgoto(); });
    for (let i = 0; i < 10; i++) {
    await button(`B${i}`, () => window.alert(`Count is: ${i}`));
    }
};