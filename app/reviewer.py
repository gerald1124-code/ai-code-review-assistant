import ast
from dataclasses import dataclass, asdict

@dataclass
class Finding:
    rule: str
    severity: str
    line: int
    message: str
    suggestion: str

class CodeReviewer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def add(self, rule, severity, line, message, suggestion):
        self.findings.append(Finding(rule, severity, line, message, suggestion))

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if any(alias.name == "*" for alias in node.names):
            self.add(
                "PY001", "medium", node.lineno,
                "Wildcard import reduces clarity and may shadow names.",
                "Import only the names you use."
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            self.add(
                "PY002", "high", node.lineno,
                f"Use of {node.func.id} can execute untrusted code.",
                "Use a safe parser or explicit mapping instead."
            )
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.add(
                "PY003", "medium", node.lineno,
                "Bare except catches system-exiting exceptions.",
                "Catch a specific exception type."
            )
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        defaults = list(node.args.defaults) + [d for d in node.args.kw_defaults if d]
        for default in defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.add(
                    "PY004", "high", node.lineno,
                    "Mutable default argument can retain state between calls.",
                    "Use None and initialize the value inside the function."
                )
        end_line = getattr(node, "end_lineno", node.lineno)
        if end_line - node.lineno + 1 > 40:
            self.add(
                "PY005", "low", node.lineno,
                "Function is longer than 40 lines.",
                "Split the function into smaller focused helpers."
            )
        self.generic_visit(node)

def review_code(code: str) -> tuple[int, list[dict]]:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        finding = Finding(
            "PY000", "high", exc.lineno or 1,
            f"Syntax error: {exc.msg}",
            "Fix the syntax before running further checks."
        )
        return 0, [asdict(finding)]

    reviewer = CodeReviewer()
    reviewer.visit(tree)
    penalties = {"high": 25, "medium": 15, "low": 5}
    score = max(0, 100 - sum(penalties[f.severity] for f in reviewer.findings))
    return score, [asdict(f) for f in reviewer.findings]
