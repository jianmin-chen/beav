from sys import exit

TOKEN_TYPE = {
    "Word": "Word",
    "Number": "Number",
    "String": "String",
    "Var": "Var",
    "If": "If",
    "Else": "Else",
    "While": "While",
    "For": "For",
    "True": "True",
    "False": "False",
    "And": "And",
    "Or": "Or",
    "Return": "Return",
    "To": "To",
    "End": "End",
    "LeftParen": "LeftParen",
    "RightParen": "RightParen",
    "LeftBracket": "LeftBracket",
    "RightBracket": "RightBracket",
    "Plus": "Plus",
    "Minus": "Minus",
    "Times": "Times",
    "Divide": "Divide",
    "Modulo": "Modulo",
    "Equal": "Equal",
    "Equality": "Equality",
    "LessThan": "LessThan",
    "LessThanOrEqual": "LessThanOrEqual",
    "GreaterThan": "GreaterThan",
    "GreaterThanOrEqual": "GreaterThan",
    "Colon": "Colon",
}

KEYWORDS = {
    "to": TOKEN_TYPE["To"],
    "repeat": TOKEN_TYPE["For"],
    "output": TOKEN_TYPE["Return"],
    "end": TOKEN_TYPE["End"],
    "make": TOKEN_TYPE["Var"],
    "if": TOKEN_TYPE["If"],
    "else": TOKEN_TYPE["Else"]
}


def new_token(kind, value, content):
    return {"type": kind, "value": value, "content": content}


class Lexer:
    current:int
    source:str
    tokens:list
    line:int
    incomplete:bool

    def __init__(self, source: str="", current:int=0, tokens:list=[], line:int=0):
        self.current = current
        self.source = source.lower()
        self.tokens = tokens
        self.line = line
        self.incomplete = False

    def peek(self):
        if self.current >= len(self.source):
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def advance(self):
        if self.current >= len(self.source):
            return "\0"
        res = self.peek()
        self.current += 1
        return res

    def match(self, char):
        if self.peek() == char:
            self.advance()
            return True
        return False

    def add_token(self, kind, value, content):
        self.tokens.append(new_token(kind, value, content))


def scan_token(lexer):
    char = lexer.advance()

    def is_alphanumeric(char):
        return char != " " and (char.isalpha() or char.isnumeric() or char == "_")

    def string(kind):
        text = ""
        while lexer.peek() != kind and lexer.peek() != "\0":
            if lexer.peek() == "\n":
                lexer.line += 1
            text += lexer.advance()
        if lexer.peek() == "\0":
            # Reached end of file, but string hasn't been terminated
            raise Exception(f"Unterminated string: {lexer.line}")
        lexer.advance()  # Consume the closing quote
        lexer.add_token(TOKEN_TYPE["String"], text, text)

    def number():
        text = ""
        while lexer.peek().isnumeric():
            text += lexer.advance()
        if lexer.peek() == "." and lexer.peek_next().isnumeric():
            text += lexer.advance()
            while lexer.peek().isnumeric():
                text += lexer.advance()
        lexer.add_token(TOKEN_TYPE["Number"], float(text), text)

    def identifier():
        text = ""
        while is_alphanumeric(lexer.peek()):
            text += lexer.advance()
        kind = KEYWORDS.get(text, None)
        if kind is None:
            kind = TOKEN_TYPE["Word"]
        lexer.add_token(kind, text, text)

    match char:
        case "(":
            lexer.add_token(TOKEN_TYPE["LeftParen"], "(", "(")
        case ")":
            lexer.add_token(TOKEN_TYPE["RightParen"], ")", ")")
        case "[":
            lexer.add_token(TOKEN_TYPE["LeftBracket"], "[", "[")
        case "]":
            lexer.add_token(TOKEN_TYPE["RightBracket"], "]", "]")
        case "+":
            lexer.add_token(TOKEN_TYPE["Plus"], "+", "+")
        case "-":
            lexer.add_token(TOKEN_TYPE["Minus"], "-", "-")
        case "*":
            lexer.add_token(TOKEN_TYPE["Times"], "*", "*")
        case "/":
            lexer.add_token(TOKEN_TYPE["Divide"], "/", "/")
        case "%":
            lexer.add_token(TOKEN_TYPE["Modulo"], "%", "%")
        case "=":
            if lexer.peek() == "=":
                lexer.advance()
                lexer.add_token(TOKEN_TYPE["Equality"], "==", "==")
            else:
                lexer.add_token(TOKEN_TYPE["Equal"], "=", "=")
        case "<":
            if lexer.peek() == "=":
                lexer.advance()
                lexer.add_token(TOKEN_TYPE["LessThanOrEqual"], "<=", "<=")
            else:
                lexer.add_token(TOKEN_TYPE["LessThan"], "<", "<")
        case ">":
            if lexer.peek() == "=":
                lexer.advance()
                lexer.add_token(TOKEN_TYPE["GreaterThanOrEqual"], ">=", ">=")
            else:
                lexer.add_token(TOKEN_TYPE["GreaterThan"], ">", ">")
        case ":":
            lexer.add_token(TOKEN_TYPE["Colon"], ":", ":")
        case ";":
            while lexer.peek() != "\n" and lexer.peek() != "\0":
                lexer.advance()
            lexer.line += 1
        case "\n":
            lexer.line += 1
        case " ":
            return
        case "\t":
            return
        case _:
            if char.isalpha():
                lexer.current -= 1
                identifier()
            elif char.isnumeric():
                lexer.current -= 1
                number()
            else:
                raise Exception(f"Unexpected character: {char} at line {lexer.line + 1}")
            

def scan_tokens(lexer):
    while lexer.current < len(lexer.source):
        scan_token(lexer)
    lexer.add_token(TOKEN_TYPE["Eof"], "", "")
    return lexer.tokens