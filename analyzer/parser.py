import ast

def parse_code(code: str):
    try:
        return ast.parse(code)
    except SyntaxError:
        return None