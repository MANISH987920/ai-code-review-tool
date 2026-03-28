import ast

class MetricsAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.total_lines = 0
        self.complexity = 1
        self.functions = 0

    def visit_FunctionDef(self, node):
        self.functions += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += 1
        self.generic_visit(node)


def analyze_metrics(tree, code: str):
    analyzer = MetricsAnalyzer()
    analyzer.total_lines = len(code.split("\n"))
    analyzer.visit(tree)

    return {
        "total_lines": analyzer.total_lines,
        "functions": analyzer.functions,
        "complexity": analyzer.complexity
    }