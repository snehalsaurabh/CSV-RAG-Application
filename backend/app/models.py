from pydantic import BaseModel
from typing import List, Optional

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5

class FounderResult(BaseModel):
    id: str
    founder_name: str
    role: str
    company: str
    location: str
    snippet: str
    similarity_score: float
    matched_fields: List[str]
    row_id: int
    
class FounderDetails(BaseModel):
    id: str
    founder_name: str
    email: str
    role: str
    company: str
    location: str
    idea: str
    about: str
    keywords: str
    stage: str
    linkedin: str
    notes: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    dataset_loaded: bool
    rag_initialized: bool
    total_founders: int
    gemini_available: bool
