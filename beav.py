from sys import argv

if __name__ == "__main__":
    if len(argv) == 2:
        with open(argv[1], "r") as f:
            source = f.read()
            lexer = Lexer(source)
            scan_tokens(lexer)
            parser = Parser(lexer.tokens)
            ast = program(parser)
            run(ast)
    else:
        # Interactive
        while True:
            command = input(">")
            lexer = Lexer(command)
            if lexer.incomplete:
                command = [command]
                while lexer.incomplete:
                    command.append(input(""))
                    lexer = Lexer("\n".join(command))
            scan_tokens(lexer)
            parser = Parser(lexer.tokens)
            ast = program(parser)
            run(ast)
