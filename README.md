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
│   │   └── dreams.csv      # 샘플 데이터 / CSV
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
