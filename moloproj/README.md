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
* Play music (`0.5` means half a volume)
```
.music "audio.mp3", 0.5
```
* Stop the music
```
.stopmusic
```
* Add image (`100` is percents)
```
.image "image.png", 100
```
* Prints text that waits for the button to be pressed
```
.continue "This is awaiten text"
```

# JavaScript API
```js
// Print text with nextline
mprint(text);

// Print without nextline
mprint(text, false);

// Clear
mclear();

// Add button
button(caption, onclick);

// Add button with only goto operation
button(caption, sceneName);

// Add image (width in percents)
addImage(src, width);

// Play music
playMusic(src, volume=0.5);

// Stop the music
stopMusic();
```
