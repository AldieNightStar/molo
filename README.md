# Molo - Compiler for visual novels

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
```

# How to use compiled code
* Code will be compiled using template-provided api and functions
* Then resulted js file need to be connected to your _browser_ OR _UI app_
* Then `molostart()` need to be runned

# Basic functions it uses
* This functions need to be implemented by your template
* The rest are template/api specific
   * To add new functions - use `$register func ...` command
```js
// Clears everything up
mclear();

// Print function
mprint(text);
```

# JavaScript inline
* Just add `.js` line and write on next line js code up to `.endjs` line.
    * Warning: No arguments needed for `.js` or `.endjs`. Otherwise fail
* Variables created with inline js WILL NOT save, so make sure you have variable storage. For example global `object` with game stuff
```
.js
    console.log("Hello!");
.endjs
```

# Custom commands
* Config commands starts with `$`. At runtime they are not exist
* To register _custom command_ do: ...
    * `$$` will be replaced with arguments. Sample: `.log "Hello world", 123, "abc"`
    * Syntax: `$register (name of the command) (js string up to '\n' symbol)`
```
$register log console.log($$);
$register лог console.log($$);
$register debug console.log("DEBUG", $$);
```

# Include other stories
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

# Template
* Please, use template `moloproj` for your new projects
