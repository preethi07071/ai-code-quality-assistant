"""Starter rule-based analyzer. Submitted code is never executed."""
import ast
import re

def analyze_code(code: str, language: str) -> dict:
    findings = []
    lines = code.splitlines()

    def add(line, severity, title, explanation, suggestion):
        findings.append({"line": max(1, int(line)), "severity": severity,
                         "title": title, "explanation": explanation, "suggestion": suggestion})

    if language == "python":
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            add(exc.lineno or 1, "high", "Python syntax error", exc.msg or "Could not parse code.",
                "Fix the syntax at or near this line, then analyze again.")
            tree = None
        if tree is not None:
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    add(node.lineno, "medium", "Bare except", "Catching every exception can hide unexpected failures.",
                        "Catch the specific exception types you expect.")
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == "eval":
                        add(node.lineno, "high", "Use of eval()", "eval() can execute arbitrary expressions and is risky with untrusted input.",
                            "Prefer explicit parsing or a safe mapping of allowed operations.")
                    elif node.func.id == "exec":
                        add(node.lineno, "high", "Use of exec()", "exec() dynamically executes code and can create security risks.",
                            "Replace dynamic execution with explicit functions or safer data-driven logic.")
                if isinstance(node, ast.Compare) and isinstance(node.left, ast.Constant) and node.left.value is None:
                    if any(isinstance(op, ast.Eq) for op in node.ops):
                        add(node.lineno, "low", "Compare with None", "Python convention is to use identity comparison for None.",
                            "Use `is None` instead of `== None`.")
                if isinstance(node, ast.FunctionDef) and len(node.body) > 40:
                    add(node.lineno, "low", "Large function", "This function has many statements and may be harder to test or maintain.",
                        "Consider extracting cohesive helper functions.")
    elif language == "javascript":
        for i, line in enumerate(lines, 1):
            if re.search(r'\beval\s*\(', line):
                add(i, "high", "Use of eval()", "eval() executes a string as code and can be dangerous with untrusted input.",
                    "Use explicit parsing or a safe mapping of allowed operations.")
            if re.search(r'\bvar\s+', line):
                add(i, "low", "Legacy var declaration", "var has function scope and can lead to confusing behavior.",
                    "Prefer const by default, or let when reassignment is needed.")
            if re.search(r'==(?!=)', line):
                add(i, "low", "Loose equality", "Loose equality performs type coercion that may produce surprising results.",
                    "Consider strict equality (`===`) when appropriate.")
            if re.search(r'console\.log\s*\(', line):
                add(i, "info", "Console logging", "Debug logs can clutter production output or expose data.",
                    "Remove or replace with an appropriate logging strategy before production.")
    elif language == "java":
        for i, line in enumerate(lines, 1):
            if re.search(r'\bSystem\.out\.print', line):
                add(i, "info", "Console output", "Direct console output may not suit production applications.",
                    "Use a logging framework when appropriate.")
            if re.search(r'catch\s*\(\s*Exception\b', line):
                add(i, "medium", "Broad exception catch", "Catching Exception broadly can hide failures that should be handled separately.",
                    "Catch the specific exception types expected here.")
            if re.search(r'\.equals\s*\(', line) and re.search(r'\bnull\b', line):
                add(i, "medium", "Review null handling", "A method call on a possibly null reference can cause NullPointerException.",
                    "Check the receiver for null or use a safe comparison pattern.")

    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            add(i, "low", "Long line", f"This line is {len(line)} characters long, which may be hard to scan.",
                "Consider breaking the expression into smaller lines.")
        if re.search(r'(password|api[_-]?key|secret)\s*=\s*["\'][^"\']+["\']', line, re.I):
            add(i, "high", "Possible hard-coded secret", "A credential-like value appears embedded in source code.",
                "Move secrets to environment variables or a secret manager; rotate any real exposed credential.")

    unique, seen = [], set()
    for item in findings:
        key = (item["line"], item["severity"], item["title"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    rank = {"high": 0, "medium": 1, "low": 2, "info": 3}
    unique.sort(key=lambda x: (rank[x["severity"]], x["line"]))
    summary = {level: sum(1 for f in unique if f["severity"] == level)
               for level in ("high", "medium", "low", "info")}
    return {"language": language, "findings": unique,
            "summary": {"total": len(unique), **summary},
            "note": "Starter heuristic analysis only; findings may be false positives or miss issues. Submitted code is never executed."}
