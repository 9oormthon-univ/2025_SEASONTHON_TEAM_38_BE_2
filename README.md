## 패키지 구조
```
com.simhae.project
│
├── app                     # FastAPI 애플리케이션
│   ├── api
│   │   └── dreams.py       # 엔드포인트 정의 (라우터)
│   ├── core
│   │   ├── config.py       # 환경설정, 설정값 로딩
│   │   └── exception_handlers.py  # 예외 처리 핸들러
│   ├── db
│   │   └── vector_store.py # 벡터 DB 연동 관련 코드
│   ├── data
│   │   ├── dreams.csv      # 꿈/해몽 관련 데이터셋 (꿈 키워드, 해석 매핑 정보)
│   │   └── psychology_research.pdf  # 심리학·정신분석학 논문 자료 (프로이트 이론, 아들러의 개인 심리학)
│   ├── models
│   │   └── dtos.py         # Pydantic 모델 (Request/Response DTO)
│   ├── services
│   │   └── ai_service.py   # AI 관련 비즈니스 로직
│   ├── utils
│   │   ├── file_parser.py  # 파일 처리 유틸리티
│   │   └── prompt_builder.py # 프롬프트 생성 유틸리티
│   └── main.py             # FastAPI 앱 실행 진입점
├── vector_store            # 벡터 DB 파일 저장 디렉토리
├── .env                    
├── .gitignore              
└── requirements.txt        
```

### 💻 서버 실행
```
uvicorn app.main:app --reload
```

## RAG 파이프라인

1. 데이터 로딩 & 파싱
   - PDF: PyPDF2, fitz(PyMuPDF)로 텍스트 추출
   - CSV: pandas로 로드 및 파싱
   - app.utils.file_parser에서 공통 파싱 처리

2. 문서 청크 분할 (Chunking)
   - 텍스트를 langchain.schema.Document 객체로 변환 후 일정 단위로 분할

3. 임베딩 생성 & 벡터 DB 구축
   - OpenAIEmbeddings를 사용해 임베딩 생성
   - Chroma(chromadb)에 저장 및 인덱싱

4. 쿼리 검색 (Vector DB Search)
   - 사용자의 질의(query)를 임베딩 후 vector_db_search 실행
   - 벡터 DB에서 유사도가 높은 상위 K개 문서 검색

5. 프롬프트 빌드 (Prompt Builder)
   - build_overall_prompt, build_unconscious_prompt 등을 활용
   - 검색된 문서를 기반으로 GPT 입력 프롬프트 생성

6. LLM 호출 & 응답 생성
   - openai 패키지를 통해 GPT 호출
   - 구성된 프롬프트를 전달하여 최종 답변 생성
