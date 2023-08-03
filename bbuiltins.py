def output(*args):
    for arg in args:
        print(arg, end="")
    print()


builtins = {"print": output}
