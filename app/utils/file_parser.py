import pandas as pd
import fitz  # PyMuPDF

"""
꿈 해석과 관련된 기존 데이터베이스를 구성하는 원본 텍스트를 제공하는 역할
"""

def parse_csv(path: str):
    """기존 꿈 해몽 데이터 CSV에서 Description 컬럼 추출"""
    df = pd.read_csv(path)
    return df["Description"].tolist()

def parse_category_csv(path: str):
    """꿈 카테고리 CSV에서 category 코드 반환"""
    df = pd.read_csv(path)
    return {row["category_code"]: {"name": row["name"], "description": row["description"]} for _, row in df.iterrows()}

def parse_pdf(path: str):
    """PDF 텍스트 추출"""
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text.split("\n")