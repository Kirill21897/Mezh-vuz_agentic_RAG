from pydantic import BaseModel, Field
from typing import List, Optional

class SearchResult(BaseModel):
    content: str
    metadata: dict = Field(default_factory=dict)
    score: float = 0.0

class RAGResponse(BaseModel):
    answer: str
    sources: List[SearchResult]
