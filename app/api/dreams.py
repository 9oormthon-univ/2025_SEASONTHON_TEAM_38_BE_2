from fastapi import APIRouter
from app.models.dtos import (
    DreamAnalyzeRequest,
    OverallAnalysisResponse,
    UnconsciousAnalysisResponse,
    UnconsciousAnalyzeRequest
)
from app.services.ai_service import analyze_overall, analyze_unconscious

router = APIRouter()

@router.post("/overall", response_model=OverallAnalysisResponse)
def overall_analysis(request: DreamAnalyzeRequest):
    """
    전체 꿈 분석 엔드포인트
    - 재진술, 무의식 분석, AI 제안 포함
    """
    return analyze_overall(request)


@router.post("/unconscious", response_model=UnconsciousAnalysisResponse)
def get_unconscious_analysis(request: UnconsciousAnalyzeRequest):
    """
    무의식 분석 엔드포인트
    - 최근 7개 꿈 재해석을 전달
    """
    return analyze_unconscious(request)