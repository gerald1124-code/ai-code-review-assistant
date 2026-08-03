from app.reviewer import review_code

def test_detects_eval_and_mutable_default():
    score, findings = review_code("def f(x=[]):\n    return eval('1+1')")
    rules = {item["rule"] for item in findings}
    assert "PY002" in rules
    assert "PY004" in rules
    assert score < 100

def test_clean_code_scores_100():
    score, findings = review_code("def add(a: int, b: int) -> int:\n    return a + b")
    assert score == 100
    assert findings == []
