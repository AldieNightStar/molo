# How to write first story

# Install
* Make sure you have installed `moloc.py` in your `PATH` env variable
* On windows you should have `git-bash` to work with `molo`

# Prepare
* Open bash and type `moloc.py new mynovel` - it will create `mynovel` folder with project
* `story.txt` - it's your story to modify
* `build.sh` - it's automated builder file.
* `api` - folder with `api` for your story
    * You can put your own functions there
* `story` - story that could be shared with friends after it get done.
    * It contains `index.html` which you can run to test your story

# First chapter
* `main` is a starter scene
```
:main
    .bg "res/bg.jpg"
    Hello world!
    This is my first chapter
```
* `bg` is a command which set's your background
* `Hello world!` - your text to print
For more commands, check [[Template Commands|moloproj/README]]
* Let's see how it would work with buttons:
```
:main
    Press to go to next chapter
    .button "next chapter", "chapter2"

:chapter2
    Ok. It's works
```
* We can also use chapters as a functions:
    * When you click screen will not be cleared
    * `I am the second chapter!` will be printed
```
:main
    This is chapter 1
    .button "Call chapter2", "", () => $$$chapter2()
    
:chapter2
    I am the second chapter!
    Hello!
```
* By checking more in [[Template Commands|moloproj/README]] we can create new chapters and add more interesting stuff