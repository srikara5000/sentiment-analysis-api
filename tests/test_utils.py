from app.utils import clean_text, make_id, ist_now_iso
import re

def test_clean_text_with_none():
    """clean_text should return empty string when input is None"""
    assert clean_text(None) == ""

def test_clean_text_normalizes_spaces_and_removes_specials():
    text = "Hello!!!   World???"
    cleaned = clean_text(text)
    assert cleaned == "Hello World"  # unwanted removed
    assert "!" not in cleaned and "?" not in cleaned

def test_make_id_unique_and_valid():
    id1 = make_id()
    id2 = make_id()
    assert id1 != id2
    assert re.match(r"^[a-f0-9\-]{36}$", id1)

def test_ist_now_iso_format():
    ts = ist_now_iso()
    assert "T" in ts
    assert ts.endswith("+05:30")  # should always be IST
