# Sentiment Analysis API

A Rest API built with **FastAPI** that performs sentiment analysis on text inputs.  
Supports single and batch analysis, returning sentiment (`POSITIVE`, `NEGATIVE`, or `NEUTRAL`) along with a confidence score.

## Features
- Analyze sentiment of individual text inputs
- Batch sentiment analysis of multiple texts
- Returns confidence scores with each prediction
- JSON-based REST API with **FastAPI Swagger UI**
- Lightweight and fast (Uvicorn ASGI server)
## Project Structure
```
C:.
sentiment-api/
├── app/                          # Core application package
│   ├── __init__.py               # Marks directory as a Python package
│   ├── main.py                   # FastAPI app entry point (endpoints)
│   ├── models.py                 # Pydantic models (request/response schemas)
│   ├── sentiment.py              # Sentiment analysis logic (Hugging Face pipeline)
│   └── utils.py                  # Helper functions (clean text, UUIDs, IST timestamps)
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_api.py               # Tests for API endpoints (/analyze, /batch-analyze)
│   └── test_sentiment.py         # Unit tests for sentiment analysis logic
│
├── .gitignore                    # Git ignore file (venv, coverage, cache, etc.)
├── requirements.txt              # Dependencies (FastAPI, transformers, torch, pytest, etc.)
├── README.md                     # Project documentation (setup, usage, API docs, testing)
├── run.py                        # Application runner (starts Uvicorn server)
└── .coverage                     # Test coverage report (created after pytest with --cov)
```
## Requirements

Make sure you have the following installed on **Windows**:

- Python 3.9+
- pip (Python package manager)
- Git (optional, if cloning repository)
- Virtualenv (recommended)

## Installation

In Windows PowerShell:

### 1. Clone the repository (if using Git)
```
git clone https://github.com/your-username/sentiment-analysis-api.git
cd sentiment-analysis-api
```
### 2. Create a virtual environment
```
python -m venv venv
```
### 3. Activate the virtual environment
```
.\venv\Scripts\Activate
```
### 4. Install dependencies 
```
pip install --upgrade pip
pip install -r requirements.txt
```
### 5. Run the FastAPI server
```
uvicorn run:app --reload

```
### API will be running at:
```
  http://127.0.0.1:8000/docs

```
### API Endpoints
### 1️ Analyze Single Text 

### POST /api/analyze
* **Request Body:**
```
{
  "text": "I love this product! It is amazing.",
  "include_confidence": true
}

* **Response (example):**

{
  "analysis_id": "uuid",
  "text": "I love this product! It is amazing.",
  "sentiment": "POSITIVE",
  "confidence": 0.9998,
  "timestamp": "2025-09-10T10:55:38Z"
}
### 2️ Batch Analyze Multiple Texts

### POST /api/batch-analyze
* **Request Body:**

{
  "items": [
    { "text": "I love this product!" },
    { "text": "This is terrible." },
    { "text": "It’s okay, nothing special." }
  ]
}
```

* **Response (example):**:
```
{
  "results": [
    {
      "analysis_id": "uuid",
      "text": "I love this product!",
      "sentiment": "POSITIVE",
      "confidence": 0.9997,
      "timestamp": "2025-09-10T10:55:38Z"
    },
    {
      "analysis_id": "uuid",
      "text": "This is terrible.",
      "sentiment": "NEGATIVE",
      "confidence": 0.9996,
      "timestamp": "2025-09-10T10:55:38Z"
    },
    {
      "analysis_id": "uuid",
      "text": "It’s okay, nothing special.",
      "sentiment": "NEGATIVE",
      "confidence": 0.9975,
      "timestamp": "2025-09-10T10:55:38Z"
    }
  ],
  "metrics": {
    "processed": 3,
    "failed": 0,
    "time_seconds": 0.147
  }
}
```
 ### Testing in Swagger UI

You can test your API using Swagger UI at
```
http://127.0.0.1:8000/docs 
```

### Run all tests
```
pytest
```
### Run with coverage
```
pytest --cov=app --cov-report=term-missing 
```
##  Design Decisions

### 1. Libraries

* **FastAPI**:

  * Chosen for its **speed**, **async support**, and **built-in Swagger UI** (`/docs`) which makes testing endpoints easy.
  * Better developer experience compared to Flask because of native Pydantic integration.

* **Pydantic**:

  * Used for **data validation** and enforcing request/response models.
  * Ensures input JSON matches expected schema (e.g., prevents empty/invalid `items` in batch API).

* **Transformers (Hugging Face)**:

  * Provides **state-of-the-art NLP models**.
  * Used `distilbert-base-uncased-finetuned-sst-2-english`, a lightweight yet high-performing sentiment model.
  * Allows confidence scoring, which NLTK/TextBlob don’t support as well.

* **Pytest + httpx**:

  * For automated **unit and integration tests**.
  * `httpx` allows ASGI testing of FastAPI apps without running a server.

* **Black + Flake8**:

  * Enforce code formatting and linting → maintain readability and follow PEP8.

---

### 2. Handling Edge Cases

* **Empty Text**:

  * If input text is empty or only spaces, API raises `400 Bad Request`.
  * Prevents wasting model resources.

* **Special Characters**:

  * Cleaned using regex in `utils.py` (`clean_text`) to normalize whitespace and remove noise.

* **Confidence Scores**:

  * Neutral cutoff applied (if confidence < `0.55`, sentiment forced to `"NEUTRAL"`).
  * Prevents false positives on ambiguous text.

* **Batch Size Limit**:

  * Maximum 100 items enforced (`413 Payload Too Large` if exceeded).
  * Keeps response times predictable and prevents overloading.

* **Partial Failures in Batch**:

  * If one text fails (e.g., empty), API still returns results for others + an error object.
  * This ensures robustness in production workloads.

* **Timestamps in IST**:

  * All responses use IST (`Asia/Kolkata` timezone) via `utils.utc_now_iso()`.
  * Matches business requirement (Kalkura team based in India).

---

### 3. Assumptions Made

* Input texts are **short (≤1000 chars)** — longer texts truncated before model inference.
* Users primarily care about **3-class sentiment**: `POSITIVE`, `NEGATIVE`, `NEUTRAL`.
* Confidence values are meaningful only when `include_confidence` is explicitly set to `true`.
* API will run on **CPU** (Jetson Nano / developer laptops), so we used `distilbert` (lightweight model).
* Basic authentication/security is **out of scope** for this assessment (to be added in production).
* Error messages are returned in JSON consistently, to simplify integration.

