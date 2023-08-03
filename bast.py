from blexer import TOKEN_TYPE
from sys import exit


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek_token(self):
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current]

    def peek_token_type(self):
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current].get("type")

    def eat(self, type):
        if self.peek_token_type() == type:
            res = self.tokens[self.current]
            self.current += 1
            return res
        token = self.peek_token()
        raise Exception(f"Expected {type} but got {token.get('TYPE')}")


def stmt(parser):
    curr = parser.peek_token_type()
    if curr == TOKEN_TYPE["To"]:
        return func_stmt(parser)
    elif curr == TOKEN_TYPE["If"]:
        return if_stmt(parser)
    else:
        return expr(parser)


def simple(parser):
    token = parser.eat(parser.peek_token_type())
    kind = token["type"]
    if kind == TOKEN_TYPE["Word"]:
        return new_var(token)
    elif kind == TOKEN_TYPE["Minus"]:
        # Negative number
        return new_number(-simple(parser)["value"])
    elif kind == TOKEN_TYPE["String"]:
        return new_string(token["value"])
    elif kind == TOKEN_TYPE["True"]:
        return new_bool(True)
    elif kind == TOKEN_TYPE["False"]:
        return new_bool(False)
    elif kind == TOKEN_TYPE["LeftParen"]:
        # Left parentheses
        left = expr(parser, True)
        parser.eat(TOKEN_TYPE["RightParen"])
        return left
    elif kind == TOKEN_TYPE["LeftBracket"]:
        items = []
        if parser.peek_token_type() != TOKEN_TYPE["RightBracket"]:
            items.append(expr(parser))
            while parser.peek_token_type() == TOKEN_TYPE["Comma"]:
                parser.eat(TOKEN_TYPE["Comma"])
                items.append(expr(parser))
        parser.eat(TOKEN_TYPE["RightBracket"])
        return new_array(items)
    raise Exception("Expected expression but got " + kind)


def is_op(token):
    return token["type"] in [
        TOKEN_TYPE["Plus"],
        TOKEN_TYPE["Minus"],
        TOKEN_TYPE["Times"],
        TOKEN_TYPE["Divide"],
        TOKEN_TYPE["Modulo"],
        TOKEN_TYPE["LessThan"],
        TOKEN_TYPE["LessThanOrEqual"],
        TOKEN_TYPE["GreaterThan"],
        TOKEN_TYPE["GreaterThanOrEqual"],
        TOKEN_TYPE["Equality"],
        TOKEN_TYPE["Equal"],
        TOKEN_TYPE["And"],
        TOKEN_TYPE["Or"],
    ]


def call(parser):
    res = simple(parser)
    if (parser.peek_token_type() == TOKEN_TYPE["LeftParen"] or parser.peek_token_type() == TOKEN_TYPE["LeftBracket"]):
        chain = []
        while parser.peek_token_type() == TOKEN_TYPE["LeftParen"] or parser.peek_token_type() == TOKEN_TYPE["LeftBracket"]:
            if parser.peek_token_type() == TOKEN_TYPE["LeftParen"]:
                parser.eat(TOKEN_TYPE["LeftParen"])
                args = expr_list(parser)
                parser.eat(TOKEN_TYPE["RightParen"])
                chain.append(new_call(args))
            else:
                parser.eat(TOKEN_TYPE["LeftBracket"])
                if parser.peek


def var_stmt(parser):
    parser.eat(TOKEN_TYPE["Var"])
    id = parser.eat(TOKEN_TYPE["Word"])["value"]
    parser.eat(TOKEN_TYPE["Equal"])
    value = expr(parser)
    return new_var(id, value)


def program(parser):
    parsed = []
    while parser.peek_token_type() != TOKEN_TYPE["Eof"]:
        parsed.append(stmt(parser))
    return parsed
