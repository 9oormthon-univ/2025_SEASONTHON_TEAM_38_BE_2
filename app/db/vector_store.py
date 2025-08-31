from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from app.core.config import settings
from app.utils.file_parser import parse_csv, parse_pdf

embeddings = OpenAIEmbeddings()

# 벡터 DB 초기화
def get_vector_db() -> Chroma:
    """
    Vector DB 객체를 함수 호출 시마다 가져오기
    - 서버 시작 시 전역 객체 의존 최소화
    """
    return Chroma(persist_directory=settings.VECTOR_DB_DIR, embedding_function=embeddings)

# 입력 query에 대해 가장 유사한 상위 k개 문서를 가져옴
def vector_db_search(query: str, k: int = 5):
    vector_db = get_vector_db()
    results = vector_db.similarity_search(query, k=k)
    return [r.page_content for r in results]

# CSV/PDF를 파싱하여 텍스트 수집
def build_vector_db(csv_path: str = None, pdf_path: str = None):
    vector_db = get_vector_db()
    texts = []
    if csv_path:
        texts.extend(parse_csv(csv_path))
    if pdf_path:
        texts.extend(parse_pdf(pdf_path))
    if texts:
        vector_db.add_texts(texts)
        vector_db.persist()