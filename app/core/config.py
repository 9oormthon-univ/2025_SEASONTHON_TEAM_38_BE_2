import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    VECTOR_DB_DIR: str = os.getenv("VECTOR_DB_DIR", "./data/vector_store")
    TOP_K: int = 5  # RAG 검색 top K (가장 유사한 문서 5개)
    """
    예시:
    입력 - "시험 보는 꿈"
	DB 저장 - "Dream about taking an exam often symbolizes anxiety and self-evaluation."
	임베딩 모델이 의미를 파악해서 “시험 ↔ exam”, “불안 ↔ anxiety”를 연결해줄 수 있음.
    """

settings = Settings()