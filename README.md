# AI Code Review Assistant

A FastAPI service that performs deterministic static checks on Python source code.

## Features
- detects bare `except`
- detects mutable default arguments
- detects `eval` and `exec`
- detects very long functions
- detects wildcard imports
- returns structured JSON findings
- includes tests and Docker support

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Example request

```json
{
  "filename": "example.py",
  "code": "def f(items=[]):\n    try:\n        eval('1+1')\n    except:\n        pass"
}
```
