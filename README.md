# SimHae (심해 心解)

### **"심해 心解 – 꿈으로 무의식을 의식화하다"**

> 꿈 기록을 바탕으로 무의식 속 감정을 해석하고 심리적 통찰을 제공

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7104fd3a-152d-4da9-9731-822a7e84f25b" />


## 아키텍처
<img width="1655" height="893" alt="스크린샷 2025-09-17 오후 6 37 38" src="https://github.com/user-attachments/assets/b42aca7d-4213-4231-8549-672b4df92a72" />

## 서비스 구조 설계
| 분류             | 작업             | 내용                                                   |
| ---------------- | ---------------- | ---------------------------------------------------- |
| **인프라 구성**       | VPC 생성          | 가상 프라이빗 클라우드, AWS 리소스를 배치하는 보안 기본 영역       |
|        | 서브넷 생성       | VPC IP 주소 할당 범위 정의                               |
|        | Internet Gateway 생성 | VPC와 인터넷 간 통신 게이트웨이                           |
|       | NAT Gateway 생성  | 프라이빗 서브넷 인스턴스의 인터넷 연결 또는 외부 접근 차단  |
|        | 라우트 테이블 생성 | 서브넷과 게이트웨이 간 트래픽 전송 경로 규칙               |
|        | 보안 그룹 생성    | 인바운드·아웃바운드 트래픽 제어, 포트·프로토콜 설정         |
| **애플리케이션 배포** | 로드 밸런서 생성  | HTTP·HTTPS 요청 인스턴스에 부하 분산                        |
|  | Cloud Shell 환경 생성 | 브라우저 기반 CLI 환경, 코드 작성·실행·디버깅               |
| **ECR 구성**          | ECR 생성          | AWS 컨테이너 이미지 저장소 생성, 이미지 저장                |
|           | 도커 이미지 빌드  | Dockerfile 기반 애플리케이션 이미지 빌드                   |
|           | 도커 이미지 업로드 | 생성한 이미지 AWS ECR에 업로드                             |
| **ECS 구성**          | 클러스터 생성     | EC2+네트워크 기반 ECS 클러스터 구성                        |
|          | 작업 정의 생성     | 컨테이너 실행 리소스, 환경, 볼륨 정의                       |
|         | 서비스 생성       | 지정된 수의 작업 정의 인스턴스 실행 및 유지 관리             |

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
