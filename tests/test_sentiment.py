from app.sentiment import analyze_text, get_pipeline

def test_analyze_basic_positive():
    label, score = analyze_text("I love this product, it works great!")
    assert label in {"POSITIVE", "NEUTRAL"}
    assert isinstance(score, float)

def test_analyze_empty():
    label, score = analyze_text("")
    assert label == "NEUTRAL"
    assert score == 0.0

def test_analyze_low_confidence(monkeypatch):
    """Force pipeline to return low confidence (<0.55) → should return NEUTRAL"""

    def fake_pipeline(_):
        return [{"label": "POSITIVE", "score": 0.4}]

    monkeypatch.setattr("app.sentiment.get_pipeline", lambda: fake_pipeline)

    label, score = analyze_text("meh, it's fine")
    assert label == "NEUTRAL"
    assert score == 0.4
