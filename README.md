# Molor - Compile for visual novels

# Language & Usage
```
== Comment
:chapter
.command
Simple text
.link "Link to next chapter", "chapter2"

:chapter2
Another text

:chapter3
Some text etc

::special_chapter
== Chapters with "::" prefix is a special chapters
==   which makes text print wait on "next" link press
This will be waited for next
And this one too
And this too
This is the last
== Link "next" adds at the end of printed text. So only then other commands could be printed
```

# How to use compiled code
* Include to your browser/nodejs/UI app
* Then use code below to start
```js
// It will start to use your API with mprint
molostart();
```

# Basic functions it uses
* This functions need to be implemented by your graphic engine/browser
```js
// Clears everything up
mclear();

// Print function
mprint(text);

// Print function with next line
mprintln(text);

// Add link after printed text (no nextline)
mlink(text, onclick);
```

# JavaScript inline
* Just add `.js` line and write on next line js code up to `.endjs` line.
    * Warning: No arguments needed for `.js` or `.endjs`. Otherwise fail
```
.js
    console.log("Hello!");
.endjs
```

# Custom commands
* Config commands starts with `$` before first chapter token. At runtime they are not exist
* To register _custom command_ add register command
    * `$$` will be replaced with arguments. Sample: `.log "Hello world", 123, "abc"`
    * `##` will be replaced with arguments but inside `" "` symbols with `"` escapes
    * Syntax: `$register (name of the command) (js string up to '\n' symbol)`
```
$register log console.log($$);
$register лог console.log($$);
$register debug console.log("DEBUG", $$);
```

# Include other stories/js files
```
$import myfile.txt
$import ua_commands.txt
$import ru_commands.txt
$import en_commands.txt
```

# Include js files
```
$js api.js
$js test.js
$js super_commands.js
```

# Global files
* _Global files_ are the files which are in the root folder with compiler. Like `global.txt` and `global.js` which is embedding into each story file outputs