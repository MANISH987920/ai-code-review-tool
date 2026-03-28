import ast

class RuleAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.used_names = set()
        self.security_issues = []
        self.long_functions = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec"]:
                self.security_issues.append(
                    f"Dangerous function used: {node.func.id} at line {node.lineno}"
                )
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        length = node.end_lineno - node.lineno
        if length > 20:
            self.long_functions.append((node.name, length))
        self.generic_visit(node)


def analyze_rules(tree):
    analyzer = RuleAnalyzer()
    analyzer.visit(tree)

    unused_imports = analyzer.imports - analyzer.used_names

    return {
        "unused_imports": list(unused_imports),
        "security_issues": analyzer.security_issues,
        "long_functions": analyzer.long_functions
    }