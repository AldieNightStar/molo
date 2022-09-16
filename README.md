# Molo - Compiler for visual novels

# Install & Usage
* Just download this repo/package
* Use `moloc.py` as compiler: `moloc.py story` or `moloc.py story auto` for auto compilation
* To run compilation make sure that `moloc.py` in your `PATH` environment variable
* `moloc.py new name` - will create new project based on `moloproj` template

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

* Add js block
    * `@@variables` are mapped to `window.mvars['variables']` under the hood
    * `@@@scene_name` are mapped to `window.mscenes['scene_name']` under the hood
```
.js
    console.log(@@count);
.endjs
```

* Add js inline
```
* console.log(@@count);
```

# JS API
```js
// Time token
// Will be replaced to seconds number. In our case: 85
// Format: Tmm:ss
let seconds = T1:25

// Set internal variable
// Syntactic sugar: @@name replaced with window.mvars['name']
// You can have whatever name for the variable. Ex: @@score
@@name = 123;

// Get internal variable
// Syntactic sugar: @@name replaced with window.mvars['name']
// You can have whatever name for the variable. Ex: @@score
let name = @@name;

// Get scene by name as variable
// Syntactic sugar: @@@name replaced with window.mscenes['name']
// You can have whatever name for the scene. Ex: @@@myscene
let scene = @@@main;

// Call scene directly as function
// Also 'await' could be used here if needed
// Syntactic sugar: @@@name replaced with window.mscenes['name']
// You can have whatever name for the scene. Ex: @@@myscene
@@@main();

// Variables storage. Could be used to save game state
// To make it available, make your stories using (syntax): @@variables
mvars

// Start compiled story
molostart();

// Change scene to another
mgoto(name);

// Update current scene
mgoto();

// Print something to the screen
mprint(text);

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
mprint(text);

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
* They could be run like: `log "Hello!", 123, @@variable, etc()`

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
* Variables created with inline js _WILL NOT_ be saved, so use `@@variables`
```
.js
    console.log("Hello!");
    @@money = 100;
.endjs
```
