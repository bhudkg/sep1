from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Pydantic models for API requests/responses

class OptionCreate(BaseModel):
    text: str

class OptionResponse(BaseModel):
    id: str
    option_text: str
    vote_count: int = 0

class PollCreate(BaseModel):
    title: str
    description: Optional[str] = None
    options: List[OptionCreate]

class PollResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: datetime
    options: List[OptionResponse]
    total_votes: int = 0

class PollSummary(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: datetime
    total_votes: int = 0

class VoteRequest(BaseModel):
    option_id: str

class VoteResponse(BaseModel):
    message: str
    poll_id: str
    option_id: str
    option_text: str
    new_vote_count: int
    total_poll_votes: int

class PollResults(BaseModel):
    id: str
    title: str
    description: Optional[str]
    created_at: datetime
    results: List[dict]
