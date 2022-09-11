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
.buttonjs "Click me", () => console.log("WOW")
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
* Variable operations
```
== Assign value
.set name, value

== Turn on/off the value (boolean)
.switch name

== Count numeric variables (Each time + 1)
.count name
.count name, 1

== Count numeric variables (Each time - 1)
.count name, -1
```
* Evaluate `JavaScript` directly
```
.eval console.log("Hello!");
```
* Prints text that waits for button to be pressed to continue
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

// Set variable value
mstore_set(name, value);

// Get variable value
let val = mstore_get(name);

// If there are bool: change true to false and so forth
// If there another type it will be converted to false
mstore_switch(name);

// Count (Each time + num)
mstore_count(name, num=1)

// Print text and wait for button to be pressed to continue
await printContinue(text)
```
