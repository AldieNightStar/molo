from molo import compile

if __name__ == "__main__":
    def _f():
        import sys
        args = sys.argv[1:]
        if len(args) < 1:
            print("Please enter file name")
        filename = args[0]
        with open(filename) as f:
            src = f.read()
            chapters, specs, creg = compile(src)
            print(chapters)
    _f()
