# Template `moloproj`

# Commands
* Just print text
```
Hello there!
```
* Button
```
== Just add the button with goto operation
.button "Go to scene2", "scene2"

== Add the button with goto and func
.button "Go to scene2 and do some stuff", "scene2", () => {$$score += 1}

== Add the button with func and update operation
.button "Do some stuff and update scene", "", () => {$$score += 1}
```
* Music/Sound operations
```
== Play
.music "res/audio.mp3", 0.5
.sound "res/effect1.wav", 0.5

== Stop
.stopmusic
.stopsound
```
* Add image (`100` is percents)
```
== Add image with 100% width and height
.image "res/image.png", 100, 100

== Add image with 100% width but 50% height
.image "res/image.png", 100, 50

== Add image with 20% size (width and height)
.image "res/image.png", 20
```
* Colors
```
== Background color
.bgcolor "black"

== Default background color
.bgcolor defaultColor

== Font color
.fontcolor "yellow"
```
* Print
```
== Print big text (TITLE)
.title "I am biggest"

== Print and wait for a key press to continue
.continue "Hello there"

== Print letter by letter (1000 is time in milliseconds)
.print-letter "Hello there", 1000

== Print text with button
== To continue need to press that button
.continue "This is awaiten text"
```
* Clear everything on the screen
```
.clear
```
* Background Operations
```
== Set the background picture
.bg "res/back"

== Clear the background picture
.bg ""

== Set background scale (Default: 1, 1)
== Works with ".bgpos" command
.bgscale 1, 1
.bgscale 2, 2

== Set background position (Default: center)
== Better with: .bgscale: 2, 2
.bgpos "left top"
.bgpos "right top"
.bgpos "left bottom"
.bgpos "right bottom"
.bgpos "top"
.bgpos "bottom"
.bgpos "left"
.bgpos "right"
.bgpos "center"

== Set background transition speed in ms
.bgtransition 1000

== Set background swipe from left to right within 1000 ms
== .bgswipe! - will not wait until end of animation
.bgswipe "left", "right", 1000

== Zoom out withing 1000 ms
== .bgzoom! - will not wait until end of animation
.bgzoom 2, 1, 1000

== Zoom in within 1000 ms
== .bgzoom! - will not wait until end of animation
.bgzoom 1, 2, 1000

```
* Timing
```
== Wait for 1000 milliseconds
.wait 1000

== Wait for Music 10th second. "T0_10" means 0:10
== Will not wait if music is not playing or 10 seconds is already passed
.wait-music T0_10
```

# JavaScript API
```js
// ============================================
// TIMING
// ============================================

// Wait 1000 milliseconds
await wait(1000);

// Wait for Music 10th second. "T0_10" means 0:10
// Will not wait if music is not playing or 10 seconds is already passed
await waitToMusicTime(T0_10);

// Set timeout while current scene is active
_setTimeout(func, ms)

// Set interval calls while current scene is active
_setInterval(func, ms)

// ============================================
// PRINT
// ============================================

// Print text with nextline
await mprint(text);

// Print without nextline
await mprint(text, false);

// Print text with nextline and with 1000 ms transition
await mprint(text, true, 1000);

// Print text with letter by letter for ms time
await printLetter(text, ms, nextLine=true);

// Print text and wait for key press
await printContinue(text);

// Clear the scene and timers
mclear();

// Print title text
await title("I am big");

// ============================================
// BUTTON
// ============================================

// Add simple button (No scene changing or refreshing)
let b = await button(caption, onclick);

// Add button with only goto operation
let b = await buttonX(caption, sceneName);

// Add button with goto operation AND function before goto
let b = await buttonX(caption, sceneName, () => $$score += 1);

// Add button which just update current scene with function
// Just instead of name - use one off:
//   0   null   ""
let b = await buttonX(caption, "", () => $$score += 1);

// ============================================
// IMAGE
// ============================================

// Add image (width/height in percents)
await addImage(src, width, height=width);

// ============================================
// MUSIC / SOUND
// ============================================

// Play music
playMusic(src, volume=0.5);

// Stop the music
stopMusic();

// Play the sound
playSound(src, vol=.5);

// Stop the sound
stopSound();

// ============================================
// COLORS
// ============================================

// Set Background color
bgColor(color);
bgColor(defaultColor);

// Set Font color
fontColor(color);

// Get Background color
let color = bgColor();

// Get Font color
let color = fontColor();

// Default background color
defaultColor

// ============================================
// BACKGROUND
// ============================================

// Set the background image
bgImage("res/background.jpg");

// Clear the background image
bgImage("");

// Set background scale (default: 1, 1)
bgScale(scaleX, scaleY);

// Set background transition speed in ms
bgTransition(1000);

// Background position (Better with scale: 2, 2)
bgPosition("left top");
bgPosition("right top");
bgPosition("left bottom");
bgPosition("right bottom");
bgPosition("top");
bgPosition("bottom");
bgPosition("left");
bgPosition("right");
bgPosition("center");

// Swipe background from left to right side within 1000 milliseconds
await bgSwipe("left", "right", 1000);

// Zoom out withing 1000 ms
await bgZoom(2, 1, 1000);

// Zoom in within 1000 ms
await bgZoom(1, 2, 1000);
```
