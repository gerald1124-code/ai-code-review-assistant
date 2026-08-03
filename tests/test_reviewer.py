from app.reviewer import review_code


def test_detects_eval_and_mutable_default():
    code = "def f(x=[]):\n    return eval('1+1')"

    score, findings = review_code(code)

    rules = {item["rule"] for item in findings}

    assert "PY002" in rules
    assert "PY004" in rules
    assert score < 100


def test_clean_code_scores_100():
    code = "def add(a: int, b: int) -> int:\n    return a + b"

    score, findings = review_code(code)

    assert score == 100
    assert findings == []


def test_detects_exec():
    score, findings = review_code("exec('print(1)')")

    rules = {item["rule"] for item in findings}

    assert "PY003" in rules
    assert score == 70


def test_detects_syntax_error():
    score, findings = review_code("def broken(")

    assert score == 60
    assert findings[0]["rule"] == "PY001"


def test_empty_code_is_clean():
    score, findings = review_code("")

    assert score == 100
    assert findings == []