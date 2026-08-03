# AI Code Review Assistant

A lightweight FastAPI application that performs static analysis of Python
source code.

## Features

- Detects use of `eval()`
- Detects use of `exec()`
- Detects mutable default arguments
- Detects Python syntax errors
- Produces a code-quality score
- Includes automated tests
- Includes GitHub Actions CI
- Supports Docker

## Project structure

```text
app/
├── __init__.py
├── main.py
├── reviewer.py
└── schemas.py

tests/
├── __init__.py
└── test_reviewer.py