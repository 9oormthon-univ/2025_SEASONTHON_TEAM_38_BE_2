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
    category: str

class UnconsciousAnalyzeRequest(BaseModel):
    recentDreamAnalyses: List[str]

class UnconsciousAnalysisResponse(BaseModel):
    title: str
    analysis: str
    suggestion: str

class OverallUnconsciousResponse(BaseModel):
    analysis: str  # overall에서는 analysis만 필요

class SuggestionResponse(BaseModel):
    suggestion: str

class OverallAnalysisResponse(BaseModel):
    restate: DreamRestateResponse
    unconscious: OverallUnconsciousResponse
    suggestion: SuggestionResponse