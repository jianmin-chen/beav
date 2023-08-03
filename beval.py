from bast import AST_TYPE
from copy import deepcopy
from sys import _ExitCode
from pprint import pformat
from bbuiltins import builtins
import inspect

initial = builtins

# PEMDAS
SORTED_OPS = {
    "-": 0,
    "+": 0,
    "or": 1,
    "and": 1,
    "/": 1,
    "*": 1,
    "%": 1,
    "==": 1,
    ">": 1,
    "<": 1,
    ">=": 1,
    "<=": 1,
}


class ReturnException(Exception):
    def __repr__(self) -> str:
        return pformat(self.args[0])


def execute(ast, scope=initial):
    kind = ast["type"]
    if kind == AST_TYPE["Func"]:

        def func(*args):
            local_scope = deepcopy(scope)
            for i in range(0, len(ast["args"])):
                local_scope[ast["args"][i]] = args[i]
            try:
                for command in ast["body"]:
                    execute(command, local_scope)
            except ReturnException as return_value:
                return return_value.args[0]
            except Exception:
                exit(2)
            return None

        scope[ast["name"]] = func
    elif kind == AST_TYPE["Var"]:
        scope[ast["name"]] = evaluate(ast["value"], scope)
    elif kind == AST_TYPE["Return"]:
        raise ReturnException(evaluate(ast["value"], scope))
    elif kind == AST_TYPE["If"]:
        if evaluate(ast["condition"], scope):
            for command in ast["body"]:
                execute(command, scope)
        else:
            for command in ast["else"]:
                execute(command, scope)
    else:
        evaluate(ast, scope)


def evaluate(ast, scope=initial):
    kind = ast["type"]
    if (
        kind == AST_TYPE["Number"]
        or kind == AST_TYPE["String"]
        or kind == AST_TYPE["Bool"]
    ):
        return ast["value"]
    elif kind == AST_TYPE["Var"]:
        if ast["name"] in scope.keys():
            return scope[ast["name"]]
        raise Exception("Variable " + ast["name"] + " does not exist")
    elif kind == AST_TYPE["BinOp"]:

        def calculate(left, right, op):
            if op == "*":
                return left * right
            elif op == "/":
                return left / right
            elif op == "%":
                return left % right
            elif op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "==":
                return left == right
            elif op == "<":
                return left < right
            elif op == "<=":
                return left <= right
            elif op == ">":
                return left > right
            elif op == ">=":
                return left >= right
            elif op == "and":
                return left and right
            elif op == "or":
                return left or right

        if ast["right"]["type"] != AST_TYPE["BinOp"]:
            return calculate(
                evaluate(ast["left"], scope), evaluate(ast["right"], scope), ast["op"]
            )

        # Shunting yard algorithm otherwise
        n = [evaluate(ast["left"], scope)]
        ops = [ast["op"]]
        expr = ast["right"]
        while expr["type"] == AST_TYPE["BinOp"]:
            expr_op = expr["op"]
            if len(ops) and (SORTED_OPS[expr_op] <= SORTED_OPS[ops[-1]]):
                left = n.pop()
                right = expr if expr["wrapped"] else expr["left"]
                op = ops.pop()
                n.append(calculate(left, evaluate(right, scope), op))
                while len(ops) and (SORTED_OPS[op] < SORTED_OPS[op[-1]]):
                    right = n.pop()
                    left = n.pop()
                    op = ops.pop()
                    n.append(calculate(left, evaluate(right, scope), op))
            else:
                n.append(evaluate(expr["left"], scope))
            if expr["wrapped"]:
                expr = None
                break
            ops.append(expr_op)
            expr = expr["right"]
        if expr:
            n.append(evaluate(expr, scope))
            if len(ops) > 1 and (SORTED_OPS[op[1]] > SORTED_OPS[ops[0]]):
                right = n.pop()
                left = n.pop()
                op = ops.pop()
                n.append(calculate(left, right, op))
        while len(n) > 1:
            left = n.pop(0)
            right = n.pop(0)
            ops = ops.pop(0)
            n.insert(0, calculate(left, right, op))
        return n[0]


def run(ast):
    new_scope = initial
    for node in ast:
        execute(node, new_scope)
