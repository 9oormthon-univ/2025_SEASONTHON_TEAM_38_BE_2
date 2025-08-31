import pandas as pd
import fitz  # PyMuPDF

"""
꿈 해석과 관련된 기존 데이터베이스를 구성하는 원본 텍스트를 제공하는 역할
"""

# CSV 파일에서 "Description" 컬럼의 모든 값을 리스트로 변환해서 반환
def parse_csv(path: str):
    df = pd.read_csv(path)
    return df["Description"].tolist()

# PDF의 각 페이지를 순회하며 텍스트 추출
def parse_pdf(path: str):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text.split("\n")