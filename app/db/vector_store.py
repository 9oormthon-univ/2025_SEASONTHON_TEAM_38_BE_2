from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from app.core.config import settings
from app.utils.file_parser import parse_csv, parse_pdf
import re

embeddings = OpenAIEmbeddings()

def get_vector_db() -> Chroma:
    """Vector DB 객체 반환"""
    return Chroma(persist_directory=settings.VECTOR_DB_DIR, embedding_function=embeddings)

def sentence_split(text: str):
    """문장 단위로 분리"""
    return [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]

def vector_db_search(query: str, k: int = 5):
    """query에 대해 상위 k개의 유사 문서 반환 (중복 제거)"""
    vector_db = get_vector_db()
    results = vector_db.similarity_search(query, k=k*5)
    unique_texts = []
    seen = set()
    for r in results:
        text = r.page_content
        if text not in seen:
            seen.add(text)
            unique_texts.append(text)
        if len(unique_texts) >= k:
            break
    return unique_texts

def build_vector_db(csv_path: str = None, pdf_path: str = None):
    """CSV/PDF 텍스트 수집 → 문장 단위 분리 → chunking → DB 저장"""
    vector_db = get_vector_db()
    texts = []

    # CSV/PDF 텍스트 수집 후 문장 단위 분리
    if csv_path:
        for t in parse_csv(csv_path):
            texts.extend(sentence_split(t))
    if pdf_path:
        for t in parse_pdf(pdf_path):
            texts.extend(sentence_split(t))

    # 중복 제거
    texts = list(set(texts))

    # chunking
    splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=15)
    chunked_texts = []
    for t in texts:
        chunked_texts.extend(splitter.split_text(t))

    # DB에 추가
    if chunked_texts:
        vector_db.add_texts(chunked_texts)
        vector_db.persist()