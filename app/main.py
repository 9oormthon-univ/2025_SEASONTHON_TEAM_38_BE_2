from fastapi import FastAPI
from app.api import dreams
from app.db.vector_store import build_vector_db
from app.core.exception_handlers import register_exception_handlers

app = FastAPI()

# 글로벌 예외 처리 등록
register_exception_handlers(app)

# 벡터 DB 초기화 (한 번만 수행)
build_vector_db(
    csv_path="app/data/cleaned_dream_interpretations.csv",
    # pdf_path="app/data/example.pdf"
)

# 라우터 등록
app.include_router(dreams.router, prefix="/ai/dreams", tags=["꿈 분석"])