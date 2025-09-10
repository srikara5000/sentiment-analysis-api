from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class AnalyzeRequest(BaseModel):
    text: str
    include_confidence: bool = True

class AnalyzeResponse(BaseModel):
    analysis_id: str
    text: str
    sentiment: str
    confidence: Optional[float] = None
    timestamp: datetime

class BatchItem(BaseModel):
    text: str
    include_confidence: bool = True   

class BatchRequest(BaseModel):
    items: List[BatchItem]
