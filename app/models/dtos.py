from pydantic import BaseModel, Field
from datetime import date

from typing import List

class DreamAnalyzeRequest(BaseModel):
    content: str
    dreamDate: date = Field(..., alias="dreamDate")

class DreamRestateResponse(BaseModel):
    emoji: str
    title: str
    content: str

class UnconsciousAnalyzeRequest(BaseModel):
    recentDreamAnalyses: List[str]

class UnconsciousAnalysisResponse(BaseModel):
    analysis: str

class SuggestionResponse(BaseModel):
    suggestion: str

class OverallAnalysisResponse(BaseModel):
    restate: DreamRestateResponse
    unconscious: UnconsciousAnalysisResponse
    suggestion: SuggestionResponse