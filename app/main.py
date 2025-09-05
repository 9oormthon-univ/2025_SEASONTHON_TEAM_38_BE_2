from fastapi import FastAPI
from app.api import dreams
from app.db.vector_store import build_vector_db
from app.core.exception_handlers import register_exception_handlers
from app.core.category_loader import load_categories

app = FastAPI()

register_exception_handlers(app)

# 기존 꿈 해몽 CSV → 벡터 DB
build_vector_db(
    csv_path="app/data/cleaned_dream_interpretations.csv",
    # pdf_path="app/data/example.pdf"
)

# 꿈 카테고리 CSV 로드 (FastAPI에서는 category 코드만 사용)
CATEGORIES = load_categories("app/data/dream_categories.csv")

app.include_router(dreams.router, prefix="/ai/dreams", tags=["꿈 분석"])