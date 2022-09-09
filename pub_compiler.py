from molo import compile

if __name__ == "__main__":
    def _f():
        import sys
        args = sys.argv[1:]
        if len(args) < 1:
            print("Please enter file name")
        filename = args[0]
        chapters, creg = compile(filename)
        print(chapters)
    _f()
