import json
import logging
from typing import List, Dict
from openai import OpenAI
from app.models.dtos import (
    OverallAnalysisResponse,
    DreamRestateResponse,
    UnconsciousAnalysisResponse,
    SuggestionResponse,
    DreamAnalyzeRequest,
    UnconsciousAnalyzeRequest, OverallUnconsciousResponse
)
from app.db.vector_store import vector_db_search
from app.utils.prompt_builder import build_overall_prompt, build_unconscious_prompt
from app.core.config import settings
from app.core.category_loader import load_categories

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_overall(request: DreamAnalyzeRequest) -> OverallAnalysisResponse:
    """
    꿈 해몽
    """
    # 1. 입력: 사용자로부터 전달받은 꿈 내용
    content = request.content

    # 2. RAG 검색: 입력과 유사한 문서 top K 검색
    retrieved_docs = vector_db_search(content, k=settings.TOP_K)
    log_vector_search(content, retrieved_docs)

    categories = load_categories("app/data/dream_categories.csv")
    category_codes = [c["category_code"] for c in categories]

    # 3. 프롬프트 생성: 검색 결과와 입력을 기반으로 GPT에게 전달할 프롬프트 구성
    prompt = build_overall_prompt(content, retrieved_docs, category_codes)

    # 4. GPT 호출: Chat Completions API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=700
    )

    # 5. 결과 파싱: GPT 응답 JSON 파싱
    content = response.choices[0].message.content
    data = json.loads(content)

    # 6. 출력: OverallAnalysisResponse 객체 생성 및 반환
    return OverallAnalysisResponse(
        restate=DreamRestateResponse(**data["restate"]),
        unconscious=OverallUnconsciousResponse(analysis=data["unconscious"]["analysis"]),
        suggestion=SuggestionResponse(**data["suggestion"])
    )


def analyze_unconscious(request: UnconsciousAnalyzeRequest) -> UnconsciousAnalysisResponse:
    """
    무의식 분석 (최근 7개의 꿈을 종합)
    """
    # 1. 입력: 최근 7개의 꿈 해석 내용 리스트
    dream_texts_list = request.recentDreamAnalyses

    # 2. 꿈 텍스트 합치기: 여러 꿈 텍스트를 하나의 문자열로 결합
    dream_texts = "\n".join(dream_texts_list)

    # 3. RAG 검색: 각 꿈 텍스트마다 관련 문서 검색 후 합치기
    retrieved_docs = []
    for text in dream_texts_list:
        docs_for_text = vector_db_search(text, k=settings.TOP_K)
        log_vector_search(text, docs_for_text)
        retrieved_docs.extend(docs_for_text)

    # 4. 프롬프트 생성: 결합된 꿈 텍스트와 검색 결과로 GPT 프롬프트 구성
    prompt = build_unconscious_prompt(dream_texts, retrieved_docs)

    # 5. GPT 호출: Chat Completions API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200
    )

    # 6. JSON 파싱: ```json``` 제거 후 JSON으로 변환
    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("GPT 원문 응답:", content)
        raise

    # 7. 출력: UnconsciousAnalysisResponse 객체 생성 및 반환
    return UnconsciousAnalysisResponse(
        analysis=data.get("analysis", ""),
        title=data.get("title", ""),
        suggestion=data.get("suggestion", "")
    )

def log_vector_search(prompt: str, retrieved_docs: List[Dict]):
    """
    Vector DB 검색 시 전달된 프롬프트와 검색 결과를 로그로 기록
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("=== Vector DB Search Log Start ===")
    logger.info("Prompt sent to Vector DB / GPT:")
    logger.info(prompt)
    logger.info("Retrieved Documents (Top K):")
    for i, doc in enumerate(retrieved_docs, 1):
        logger.info(f"{i}. Text: {doc[:100]}...")
    logger.info("=== Vector DB Search Log End ===")