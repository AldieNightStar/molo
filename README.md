# Molo - Compiler for visual novels

# Install & Usage
* Install
    * Download this repo/package
    * Make sure `moloc.py` in your `PATH` environment variable
    * On Windows use git-bash or something like that
    * Use `moloc.py` as compiler
        * `moloc.py story.txt`
        * `moloc.py story.txt auto`
    * `moloc.py new name` - Create new project (Copy from `moloproj` template)
* Usage
    * Run `build.sh` and begin to edit your `story.txt` file.
    * To test run `index.html` for your story

# Release your novel
* Delete files:
    * `build.sh` file
    * `README.md` file
    * `story.txt` file
    * `api` folder
* Publish to a web server

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

* Command call
```
.command arg1, arg2, "arg3", etc
```

* Add js block
    * `$$variables` are mapped to `window.mvars['variables']` under the hood
    * `$$$scene_name` are mapped to `window.mscenes['scene_name']` under the hood
```
.js
    console.log($$count);
.endjs
```

* Add js inline
```
* console.log($$count);
```

* String interpolation
    * just add `${ }` and contents inside. For example `$$name`
```
Hello ${ $$name }
```

# JS API
```js
// Time token
// Will be replaced to seconds number. In our case: 85
// Format: Tmm_ss
let seconds = T1_25

// Set internal variable
// Syntactic sugar: $$name replaced with window.mvars['name']
// You can have whatever name for the variable. Ex: $$score
$$name = 123;

// Get internal variable
// Syntactic sugar: $$name replaced with window.mvars['name']
// You can have whatever name for the variable. Ex: $$score
let name = $$name;

// Get scene by name as variable
// Syntactic sugar: $$$name replaced with window.mscenes['name']
// You can have whatever name for the scene. Ex: $$$myscene
let scene = $$$main;

// Call scene directly as function
// Also 'await' could be used here if needed
// Syntactic sugar: $$$name replaced with window.mscenes['name']
// You can have whatever name for the scene. Ex: $$$myscene
$$$main();

// Variables storage. Could be used to save game state
// To make it available, make your stories using (syntax): $$variables
mvars

// Start compiled story
molostart();

// Change scene to another
mgoto(name);

// Update current scene
mgoto();

// Print something to the screen
await mprint(text);

// Clear the screen
mclear();

// The rest functions should be provided by the template
```

# How to use compiled code
* Code will be compiled using template-provided api and functions
* Then resulting js file need to be connected to your _browser_ OR _UI app_
* Then `molostart()` need to be runned

# Basic functions
* This functions need to be implemented:
```js
// Print something to the screen
await mprint(text);

// Clear the screen
mclear();
```

# Custom commands
* Config commands starts with `$`. At runtime they are not exist
* To register _custom command_ do: ...
    * `$$` will be replaced with arguments.
    * Syntax: `$register (name of the command) (js string until nextline)`
```
$register log console.log($$);
$register лог console.log($$);
$register debug console.log("DEBUG", $$);
```
* They could be run like: `log "Hello!", 123, $$variable, etc()`

# Include other stories
```
$import myfile.txt
$import ua_commands.txt
$import ru_commands.txt
$import en_commands.txt
```

# Include js files
* They are appended at the start
```
$js api.js
$js test.js
$js super_commands.js
```

# JavaScript inline
* Just add `.js` line and write on the next line js code up to `.endjs` line.
    * Warning: No arguments needed for `.js` or `.endjs`. Otherwise fail
```
.js
    console.log("Hello!");
    $$money = 100;
.endjs
```
