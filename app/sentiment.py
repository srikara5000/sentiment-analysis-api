from typing import Tuple
from transformers import pipeline
from .utils import clean_text

_sentiment_pipe = None

def get_pipeline():
    global _sentiment_pipe
    if _sentiment_pipe is None:
        _sentiment_pipe = pipeline("sentiment-analysis")
    return _sentiment_pipe

def analyze_text(text: str) -> Tuple[str, float]:
    t = clean_text(text)
    if not t:
        return "NEUTRAL", 0.0
    pipe = get_pipeline()
    result = pipe(t[:1000])[0]
    label = result.get("label", "NEUTRAL").upper()
    score = float(result.get("score", 0.0))
    if score < 0.55:
        label = "NEUTRAL"
    return label, score
