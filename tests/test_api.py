from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest

pytestmark = pytest.mark.asyncio


async def test_analyze_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post(
            "/api/analyze", json={"text": "I like it", "include_confidence": True}
        )
        assert r.status_code == 200
        data = r.json()
        assert "analysis_id" in data
        assert data["sentiment"] in ["POSITIVE", "NEUTRAL", "NEGATIVE"]


async def test_analyze_empty_text():
    """Should return 400 when text is empty"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/analyze", json={"text": "", "include_confidence": True})
        assert r.status_code == 400


async def test_batch_endpoint_empty():
    """Should return 400 when items list is empty"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/batch-analyze", json={"items": []})
        assert r.status_code == 400


async def test_batch_over_limit():
    """Should return 413 when more than 100 items are sent"""
    items = [{"text": "ok"} for _ in range(101)]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/batch-analyze", json={"items": items})
        assert r.status_code == 413


async def test_batch_with_invalid_item():
    """Should process valid items and count failures for invalid ones"""
    items = [{"text": "good"}, {"text": ""}]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/batch-analyze", json={"items": items})
        assert r.status_code == 200
        data = r.json()
        assert data["metrics"]["failed"] == 1
        assert len(data["results"]) == 2
