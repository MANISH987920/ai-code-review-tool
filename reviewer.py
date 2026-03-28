import ast
import sys

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = 0
        self.classes = 0
        self.imports = set()
        self.used_names = set()
        self.long_functions = []
        self.security_issues = []
        self.line_count = 0

    # Count functions
    def visit_FunctionDef(self, node):
        self.functions += 1
        
        length = node.end_lineno - node.lineno
        if length > 20:
            self.long_functions.append((node.name, length))

        self.generic_visit(node)

    # Count classes
    def visit_ClassDef(self, node):
        self.classes += 1
        self.generic_visit(node)

    # Track imports
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    # Track used variables
    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    # Detect dangerous calls
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in ["eval", "exec"]:
                self.security_issues.append(
                    f"Dangerous function used: {node.func.id} at line {node.lineno}"
                )
        self.generic_visit(node)


def analyze_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)
    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    analyzer.line_count = len(code.split("\n"))

    print("\n===== AI Code Review Report =====\n")
    print(f"Total Lines: {analyzer.line_count}")
    print(f"Functions: {analyzer.functions}")
    print(f"Classes: {analyzer.classes}")

    # Unused imports
    print("\n---- Unused Imports ----")
    unused = analyzer.imports - analyzer.used_names
    if unused:
        for imp in unused:
            print(f"Unused import detected: {imp}")
    else:
        print("No unused imports")

    # Long functions
    print("\n---- Long Functions (>20 lines) ----")
    if analyzer.long_functions:
        for name, length in analyzer.long_functions:
            print(f"{name} → {length} lines")
    else:
        print("No long functions")

    # Security issues
    print("\n---- Security Issues ----")
    if analyzer.security_issues:
        for issue in analyzer.security_issues:
            print(issue)
    else:
        print("No major security issues detected")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py reviewer.py <python_file>")
    else:
        analyze_code(sys.argv[1])