# Molo - Compiler for visual novels

# Install & Usage
* Just download this repo/package
* Use `moloc.py` as compiler: `moloc.py story` or `moloc.py story auto` for auto compilation
* To run compilation make sure that `moloc.py` in your `PATH` environment variable
* Use provided template or write yourself
    * To create new project just copy `moloproj` project to new directory and make changes
    * Use `build.sh` or `python moloc.py story` instead to compile

# Language
* Create chapter
```
:chapter_name
This is chapter
```
* Put a comment
```
== This is a comment
```
* Add command
```
.command arg1, arg2, "arg3", etc
```

# JS API
```js
// Start compiled story
molostart();

// Change scene to other
mgoto(name);

// Update current scene
mgoto();

// Print something to the screen
mprint(text);

// Clear the screen
mclear();

// The rest should be provided by a template
```

# How to use compiled code
* Code will be compiled using template-provided api and functions
* Then resulting js file need to be connected to your _browser_ OR _UI app_
* Then `molostart()` need to be runned

# Basi functions
* This default functions need to be implemented:
```js
// Print something to the screen
mprint(text);

// Clear the screen
mclear();
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

# JavaScript inline
* Just add `.js` line and write on the next line js code up to `.endjs` line.
    * Warning: No arguments needed for `.js` or `.endjs`. Otherwise fail
* Variables created with inline js _WILL NOT_ be saved, so make sure you have variable storage. For example global `store` with game stuff
```
.js
    console.log("Hello!");
.endjs
```

# Template
* Please, use template `moloproj` for your new projects
