from fastapi import FastAPI, HTTPException
from .models import AnalyzeRequest, AnalyzeResponse, BatchRequest
from .utils import make_id, ist_now_iso, clean_text
from .sentiment import analyze_text
import time

app = FastAPI(title="Sentiment Analysis API", version="0.1.0")


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    """Analyze sentiment for a single text input."""
    text = clean_text(req.text)
    if not text:
        raise HTTPException(status_code=400, detail="text must not be empty")

    analysis_id = make_id()
    ts = ist_now_iso()
    label, score = analyze_text(text)

    resp = AnalyzeResponse(
        analysis_id=analysis_id,
        text=text,
        sentiment=label,
        confidence=score if req.include_confidence else None,
        timestamp=ts,  # 👈 IST timestamp
    )
    return resp


@app.post("/api/batch-analyze")
async def batch_analyze(req: BatchRequest):
    """Analyze sentiment for a batch of texts (up to 100)."""
    items = req.items
    if not items:
        raise HTTPException(status_code=400, detail="items must not be empty")
    if len(items) > 100:
        raise HTTPException(status_code=413, detail="max 100 items allowed")

    results = []
    failed = 0
    start = time.time()

    for idx, item in enumerate(items):
        try:
            text = clean_text(item.text)
            if not text:
                raise ValueError("empty text")
            label, score = analyze_text(text)

            results.append({
                "analysis_id": make_id(),
                "text": text,
                "sentiment": label,
                "confidence": score if item.include_confidence else None,
                "timestamp": ist_now_iso(),  # 👈 IST timestamp for each item
            })
        except Exception as e:
            failed += 1
            results.append({
                "error": str(e),
                "index": idx,
                "timestamp": ist_now_iso(),  # 👈 include error timestamp too
            })

    elapsed = time.time() - start
    metrics = {"processed": len(items), "failed": failed, "time_seconds": elapsed}
    return {"results": results, "metrics": metrics}
