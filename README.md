# Sentiment Analysis API

A API built with **FastAPI** that performs sentiment analysis on text inputs.  
Supports single and batch analysis, returning sentiment (`POSITIVE`, `NEGATIVE`, or `NEUTRAL`) along with a confidence score.

## 🚀 Features
- Analyze sentiment of individual text inputs
- Batch sentiment analysis of multiple texts
- Returns confidence scores with each prediction
- JSON-based REST API with **FastAPI Swagger UI**
- Lightweight and fast (Uvicorn ASGI server)

## Requirements

Make sure you have the following installed on **Windows**:

- Python 3.9+
- pip (Python package manager)
- Git (optional, if cloning repository)
- Virtualenv (recommended)

##  Running the API

In Windows PowerShell:

# 1. Clone the repository (if using Git)
git clone https://github.com/your-username/sentiment-analysis-api.git
cd sentiment-analysis-api

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate

# 4. Install dependencies 
pip install --upgrade pip
pip install -r requirements.txt

# 5. Run the FastAPI server
uvicorn app.main:app --reload


API will be running at:
   http://127.0.0.1:8000/docs


 API Endpoints
1️ Analyze Single Text

POST /api/analyze
Request Body:

{
  "text": "I love this product! It is amazing.",
  "include_confidence": true
}

Response:

{
  "analysis_id": "uuid",
  "text": "I love this product! It is amazing.",
  "sentiment": "POSITIVE",
  "confidence": 0.9998,
  "timestamp": "2025-09-10T10:55:38Z"
}

2️ Batch Analyze Multiple Texts

POST /api/batch-analyze
Request Body:

{
  "items": [
    { "text": "I love this product!" },
    { "text": "This is terrible." },
    { "text": "It’s okay, nothing special." }
  ]
}


Response (example):

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

 Testing in Swagger UI

You can test your API using Swagger UI at http://127.0.0.1:8000/docs 


# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing 

# Design Decisions

   FastAPI chosen for async speed + built-in docs (Swagger UI at /docs)

  Transformers used for high-accuracy sentiment, with TextBlob fallback for lightweight mode

  Pydantic models enforce strict request validation

  IST timestamps for local compliance

  Batch API supports partial results + metrics for robustness

  PEP8 compliance ensured using black + flake8
