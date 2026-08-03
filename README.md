# AI Code Review Assistant

> AI-powered Python code review service built with FastAPI.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![Pytest](https://img.shields.io/badge/Pytest-8.4-orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![CI](https://github.com/gerald1124-code/ai-code-review-assistant/actions/workflows/ci.yml/badge.svg)

## Overview

AI Code Review Assistant is a lightweight REST API that performs static analysis on Python source code.

The application automatically detects common security issues, code quality problems, and programming mistakes while generating a code quality score.

It is designed as a portfolio project demonstrating:

- FastAPI development
- Static code analysis
- REST API design
- Automated testing
- GitHub Actions CI
- Docker deployment

---

## Features

- Static Python code analysis
- Code quality scoring (0–100)
- Detects unsafe `eval()` usage
- Detects unsafe `exec()` usage
- Detects mutable default arguments
- Detects Python syntax errors
- REST API with FastAPI
- Docker support
- GitHub Actions Continuous Integration
- Unit tests using Pytest

---

## Tech Stack

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- Docker
- GitHub Actions

---

## Project Structure

```text
ai-code-review-assistant
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── reviewer.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   └── test_reviewer.py
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/gerald1124-code/ai-code-review-assistant.git
```

Move into the project

```bash
cd ai-code-review-assistant
```

Create a virtual environment

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

## Example Request

```json
{
  "code": "def f(x=[]):\n    return eval('1+1')"
}
```

---

## Example Response

```json
{
  "score": 50,
  "findings": [
    {
      "rule": "PY004",
      "message": "Avoid mutable default arguments.",
      "line": 1,
      "severity": "medium",
      "deduction": 20
    },
    {
      "rule": "PY002",
      "message": "Avoid eval(); it can execute arbitrary code.",
      "line": 2,
      "severity": "high",
      "deduction": 30
    }
  ]
}
```

---

## Running Tests

```bash
pytest -v
```

---

## Docker

Build

```bash
docker build -t ai-code-review-assistant .
```

Run

```bash
docker run -p 8000:8000 ai-code-review-assistant
```

---

## Continuous Integration

GitHub Actions automatically:

- Installs dependencies
- Runs unit tests
- Validates every push
- Validates every pull request

---

## Future Improvements

- Support additional Python security rules
- Generate HTML reports
- GitHub Pull Request review integration
- AI-powered code improvement suggestions
- Severity customization
- JSON report export
- Code complexity metrics

---

## License

This project is licensed under the MIT License.

---

## Author

**Gerald Johnson**

GitHub:
https://github.com/gerald1124-code