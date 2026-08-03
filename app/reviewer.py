"""Static Python code-review rules."""

from __future__ import annotations

import ast
from typing import Any


Finding = dict[str, Any]


class CodeReviewVisitor(ast.NodeVisitor):
    """Inspect Python syntax for basic quality and security issues."""

    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def add_finding(
        self,
        rule: str,
        message: str,
        line: int,
        severity: str,
        deduction: int,
    ) -> None:
        """Add one finding while avoiding duplicate rule/line results."""

        finding: Finding = {
            "rule": rule,
            "message": message,
            "line": line,
            "severity": severity,
            "deduction": deduction,
        }

        duplicate = any(
            existing["rule"] == rule and existing["line"] == line
            for existing in self.findings
        )

        if not duplicate:
            self.findings.append(finding)

    def visit_Call(self, node: ast.Call) -> None:
        """Detect unsafe function calls."""

        if isinstance(node.func, ast.Name) and node.func.id == "eval":
            self.add_finding(
                rule="PY002",
                message="Avoid eval(); it can execute untrusted Python code.",
                line=node.lineno,
                severity="high",
                deduction=30,
            )

        if isinstance(node.func, ast.Name) and node.func.id == "exec":
            self.add_finding(
                rule="PY003",
                message="Avoid exec(); it can execute untrusted Python code.",
                line=node.lineno,
                severity="high",
                deduction=30,
            )

        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Detect mutable default arguments."""

        self._check_mutable_defaults(node)
        super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Detect mutable defaults in asynchronous functions."""

        self._check_mutable_defaults(node)
        super().generic_visit(node)

    def _check_mutable_defaults(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        mutable_types = (ast.List, ast.Dict, ast.Set)

        all_defaults = list(node.args.defaults) + [
            default
            for default in node.args.kw_defaults
            if default is not None
        ]

        for default in all_defaults:
            if isinstance(default, mutable_types):
                self.add_finding(
                    rule="PY004",
                    message=(
                        "Avoid mutable default arguments; use None and create "
                        "the object inside the function."
                    ),
                    line=default.lineno,
                    severity="medium",
                    deduction=20,
                )


def review_code(code: str) -> tuple[int, list[Finding]]:
    """
    Review Python source code.

    Returns:
        A tuple containing:
        - score from 0 to 100
        - list of detected findings
    """

    if not isinstance(code, str):
        raise TypeError("code must be a string")

    if not code.strip():
        return 100, []

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        finding: Finding = {
            "rule": "PY001",
            "message": f"Python syntax error: {exc.msg}",
            "line": exc.lineno or 1,
            "severity": "high",
            "deduction": 40,
        }
        return 60, [finding]

    visitor = CodeReviewVisitor()
    visitor.visit(tree)

    findings = sorted(
        visitor.findings,
        key=lambda item: (item["line"], item["rule"]),
    )

    total_deduction = sum(
        int(finding["deduction"])
        for finding in findings
    )

    score = max(0, 100 - total_deduction)

    return score, findings