# CodeLens — AI Code Quality & Bug Detection Assistant

A portfolio starter for reviewing Python, Java, and JavaScript source for common risky patterns. It provides line-specific findings, severity labels, explanations, and suggestions in a responsive dashboard.

## Important scope note
This version uses **static, rule-based heuristics**. It does not call an LLM, execute submitted code, or prove that code is secure or correct. Findings may be false positives or miss issues. Describe it accurately as a code-quality assistant prototype.

## Features
- Responsive dark dashboard
- Python syntax parsing and starter rules
- Basic heuristic checks for Java and JavaScript
- Severity summary and line-specific recommendations
- Input length validation
- Submitted code is not executed by the app

## Requirements
Python 3.10+ and pip.

## Run on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
If activation is blocked, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` then `.\.venv\Scripts\python.exe app.py`.

## Run on macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Structure
- `app.py` — Flask web server and API
- `analyzer.py` — static heuristic rules
- `templates/index.html` — interface
- `static/style.css` — styling
- `static/app.js` — API calls and report rendering

## API
`POST /api/analyze` with JSON such as:
```json
{"language":"python","code":"print('hello')"}
```
Supported languages: `python`, `java`, `javascript`.

## Recommended next steps
1. Add unit tests for analyzer rules and API behavior.
2. Add proper language linters (Ruff, ESLint, Checkstyle).
3. Add an optional LLM explanation/fix feature with API keys stored server-side in environment variables.
4. Show suggested fixes as diffs and require tests to pass before accepting them.
5. If running submitted code is ever added, use a strict isolated sandbox.

## Security note
Educational prototype only; not a replacement for professional static analysis, code review, or security testing. Do not send confidential source code to third-party AI services without permission.
