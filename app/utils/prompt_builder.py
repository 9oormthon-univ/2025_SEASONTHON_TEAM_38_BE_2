from typing import List
from langchain.schema import Document


def build_overall_prompt(content: str, context_docs: List[Document], category_codes: List[str]) -> str:
    """
    GPT에게 전달할 프롬프트 생성
    dream_text: 사용자의 꿈 원문
    context_docs: RAG를 통해 검색된 관련 문서 리스트
    category_codes: CSV에서 로드한 꿈 카테고리 코드 리스트
    """
    context = "\n".join([doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in context_docs])

    prompt = f"""
당신은 전문적인 꿈 해석사이자 정신분석학적 관점을 가진 전문가입니다.
사용자가 경험한 꿈을 분석하고, 다음 지침을 따라 응답해주세요.

지침:
- 응답 길이: 충분히 상세하게 (약 800~1000자 가능)
- 톤: 친근하지만 심리학적 깊이가 느껴지게
- 분석 시 무의식적 동기와 감정, 상징 의미를 포함
- 꿈 재진술, 무의식 분석, AI 제안 순서
- 반드시 한글로 작성

사용자 꿈:
{content}

관련 참고 문서:
{context}

응답은 반드시 JSON 형태로 작성하고, 예시는 다음과 같습니다:

{{
    "restate": {{
        "emoji": "💔",
        "title": "헤어진 후 새로운 사람을 만나는 꿈",
        "content": "여자친구와 헤어진 후, 바로 남자친구가 생기고, 그 이름을 확인해보니 나와 비슷한 사람이었습니다.",
        "category": "DAILY_REFLECTION"
    }},
    "unconscious": {{
        "analysis": "이 꿈은 당신의 인간관계에서 느끼는 불안과 기대가 섞인 심리를 반영합니다."
    }},
    "suggestion": {{
        "suggestion": "현재 감정을 충분히 돌아보고..."
    }}
}}

카테고리 지침:
- 가능한 category 값: {', '.join(category_codes)}
- 위 값 중 하나를 선택해서 JSON의 "category" 필드에 넣으세요
- category 값은 반드시 영어 코드 형태로 작성
"""
    import logging
    logging.info("=== GPT Prompt Preview ===\n%s", prompt)

    return prompt

def build_unconscious_prompt(dream_texts: str, context_docs: List[Document]) -> str:
    """
    최근 꿈 7개를 종합해 무의식 분석을 생성하는 프롬프트
    dream_texts: 최근 꿈 7개의 텍스트를 \n로 연결한 문자열
    context_docs: RAG로 검색된 관련 문서 리스트
    """
    context = "\n".join([doc.page_content if hasattr(doc, "page_content") else str(doc) for doc in context_docs])
    prompt = f"""
당신은 전문적인 정신분석사입니다. 최근 사용자가 경험한 7개의 꿈을 종합해 사용자의 무의식과 심리 상태를 분석해주세요. 
개별 꿈의 내용은 상세히 나열하지 말고, 꿈들에서 나타나는 공통된 패턴과 감정을 중심으로 분석합니다.

지침:
- 한 문단으로 작성
- 분석 길이: 400~600자 내외
- 톤: 친근하면서 전문적인 심리 피드백 느낌
- 출력은 반드시 JSON 형식, 모든 문자열은 escape 처리

최근 꿈 7개:
{dream_texts}

관련 참고 문서:
{context}

출력 예시(JSON):
{{
    "analysis": "최근 꿈들을 종합하면, 당신의 무의식 속에서 창의성과 인간관계, 자기 탐색의 복잡한 감정이 뒤섞여 있는 것으로 보아요. 반복되는 상징과 패턴은 내면에서 새로운 아이디어와 프로젝트를 시도하는 동시에, 과도한 부담과 기대 속에서 자신의 정체성과 감정을 조절하려는 노력을 반영합니다. 이 꿈들은 자기 이해와 감정 조절 능력을 높이기 위한 무의식적 탐색을 보여줍니다."
}}
"""
    return prompt


