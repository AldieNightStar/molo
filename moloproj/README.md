# Template `moloproj`

# Commands
* Just print text
```
Hello there!
```
* Button with `goto` operation when click
```
.button "Click me", "scene2"
```
* Button with js callback when click
```
.button "Click me", () => console.log("WOW")
```
* Play music (`0.5` means half a volume)
```
.music "audio.mp3", 0.5
```
* Stop the music
```
.stopmusic
```
* Add image (`100` is pixel size)
```
.image "image.png", 100
```
* `if` operation
```
.if store.key
    You found the key!
    .button "OK", "oldScene"
.end
```

# JavaScript API
```js
// Print text
mprint(text);

// Clear
mclear();

// Add button
button(caption, onclick);

// Add button with only goto operation
button(caption, sceneName);

// Add image
addImage(src, widthPx);

// Play music
playMusic(src, volume=0.5);

// Stop the music
stopMusic();
```