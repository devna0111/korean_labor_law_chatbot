# 노동법 RAG 챗봇 프로젝트

## 프로젝트 정보

**프로젝트명**: 노동법 Q&A RAG 챗봇  
**버전**: 1.0.0  
**개발 기간**: **주 (2025.10 - *미정)  
**개발자**: 정종혁

---

## 1. 기획 의도

### 1.1 배경

한국의 근로자와 소규모 사업주는 노동법에 대한 정확한 정보 접근이 어렵습니다:
- 복잡한 법률 용어와 조항
- 실시간 상담의 높은 비용
- 단편적인 온라인 정보의 신뢰성 문제

### 1.2 목적

**즉각적이고 정확한 노동법 정보 제공**을 통해:
1. 근로자의 권리 보호 지원
2. 사업주의 법률 준수 도움
3. 노무 상담 접근성 향상

### 1.3 핵심 가치

- **정확성**: 공식 법조문 기반 답변
- **투명성**: 모든 답변에 출처 명시
- **신뢰성**: 낮은 확신도 시 전문가 상담 권장
- **접근성**: 24/7 무료 이용

---

## 2. 프로젝트 범위

### 2.1 포함 범위

**법률 영역**:
- 근로기준법 (임금, 근로시간, 휴가, 해고)
- 최저임금법
- 근로자퇴직급여보장법

**기능**:
- 자연어 질문 응답
- 관련 법조문 검색
- 판례 기반 실무 안내
- 신뢰도 기반 답변 검증

### 2.2 제외 범위

- 개별 사건에 대한 법률 자문
- 소송 관련 구체적 조언
- 단체협약/취업규칙 해석
- 실시간 법률 업데이트 (수동 업데이트)

---

## 3. 개발 환경

### 3.1 하드웨어

```
GPU: NVIDIA RTX 4060, CUDA 12.9
VRAM: 8GB
RAM: 16GB 이상 권장
Storage: SSD 20GB 이상
```

### 3.2 소프트웨어

**운영체제**:
```
Windows 11
WSL2 (Ubuntu 22.04)
```

**개발 언어**:
```
Python 3.10.12
```

**핵심 프레임워크**:
```
LangChain: 문서 처리 및 RAG 파이프라인
LangGraph: 멀티 에이전트 워크플로우
FastAPI: API 서버 (선택)
```

**LLM 환경**:
```
vLLM: 고성능 추론 서버
모델: Qwen/Qwen2.5-1.5B-Instruct
VRAM 사용량: ~3GB 예상
```

**벡터 데이터베이스**:
```
Weaviate (Docker)
```

**임베딩 모델**:
```
Ollama: bona/bge-m3-korean:latest
크기: 1.2GB
LangChain OllamaEmbeddings를 통한 연동
```

---

## 4. 시스템 아키텍처

### 4.1 전체 구조

```
┌─────────────┐
│   사용자    │
└──────┬──────┘
       │ 질문
       ↓
┌─────────────────────────────────┐
│     LangGraph Workflow          │
│                                 │
│  ┌──────────────────────────┐   │
│  │   질문 분석 Agent        │   │
│  └───────────┬──────────────┘   │
│              │                  │
│  ┌───────────▼──────────────┐   │
│  │   문서 검색 Agent        │   │
│  └───────────┬──────────────┘   │
│              │                  │
│  ┌───────────▼──────────────┐   │
│  │   답변 생성 Agent        │   │
│  └───────────┬──────────────┘   │
│              │                  │
│  ┌───────────▼──────────────┐   │
│  │   검증 Agent             │   │
│  └───────────┬──────────────┘   │
│              │                  │
│  ┌───────────▼──────────────┐   │
│  │   조건부 라우팅          │   │
│  │   High/Medium/Low        │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Weaviate Vector Store         │
│   (근로기준법, FAQ, 판례)        │
└─────────────────────────────────┘ 
```

### 4.2 데이터 플로우

```
1. 문서 수집 → 전처리 → 청킹 → 임베딩 (Ollama) → Weaviate 저장
2. 질문 입력 → 의도 분석 → 벡터 검색 → 컨텍스트 구성
3. LLM 추론 (vLLM) → 답변 생성 → 검증 → 출처 첨부 → 출력
```

---

## 5. 기술 스택

### 5.1 Core Dependencies

```python
# requirements.txt
# LangChain
langchain==0.1.0
langgraph==0.0.40
langchain-community==0.0.20

# LLM
vllm==0.2.7
openai==1.0.0  # vLLM OpenAI 호환

# 벡터스토어
weaviate-client==3.25.0

# 임베딩 (Ollama)
# Ollama는 별도 설치 필요

# 문서 처리
pypdf==3.17.0
python-docx==1.1.0
beautifulsoup4==4.12.0

# 유틸리티
python-dotenv==1.0.0
pydantic==2.5.0

# API (선택)
fastapi==0.109.0
uvicorn==0.25.0
gradio==4.0.0
```

### 5.2 설치 가이드

```bash
# 1. 가상환경 생성
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 2. 패키지 설치
pip install -r requirements.txt

# 3. Ollama 설치 (임베딩용)
# https://ollama.ai/download

# 4. 임베딩 모델 다운로드
ollama pull bona/bge-m3-korean:latest

# 5. Weaviate Docker 실행
docker run -d \
  -p 8080:8080 \
  -p 50051:50051 \
  --name weaviate \
  semitechnologies/weaviate:latest

# 6. vLLM 모델 다운로드
huggingface-cli download Qwen/Qwen2.5-3B-Instruct \
  --local-dir ./models/qwen2.5-3b

# 7. vLLM 서버 시작
python -m vllm.entrypoints.openai.api_server \
  --model ./models/qwen2.5-3b \
  --dtype half \
  --max-model-len 4096 \
  --port 8000
```

---

## 6. 프로젝트 구조

```
labor-law-chatbot/
├── data/
│   ├── raw/                    # 원본 문서
│   │   ├── laws/
│   │   │   ├── 근로기준법.txt
│   │   │   ├── 최저임금법.txt
│   │   │   └── 퇴직급여법.txt
│   │   ├── faqs/
│   │   │   └── 고용노동부FAQ.md
│   │   └── cases/
│   │       └── 판례모음.txt
│   └── processed/              # 전처리된 데이터
│       └── chunks.json
│
├── models/
│   └── qwen2.5-3b/            # vLLM 모델
│
├── agents/
│   ├── __init__.py
│   ├── categorizer.py         # 질문 분류 Agent
│   ├── retriever.py           # 문서 검색 Agent
│   ├── answerer.py            # 답변 생성 Agent
│   └── validator.py           # 검증 Agent
│
├── tools/
│   ├── __init__.py
│   ├── document_loader.py     # 문서 로딩
│   ├── text_splitter.py       # 청킹
│   └── embeddings.py          # Ollama 임베딩
│
├── workflow.py                 # LangGraph 워크플로우
├── config.py                   # 설정 파일
├── main.py                     # 메인 실행 파일
├── requirements.txt
├── .env.example
└── README.md
```

---

## 7. 개발 단계

### Phase 1: 데이터 준비 (Week 1)

**목표**: 벡터스토어 구축

**작업**:
1. 근로기준법 전문 수집
2. 고용노동부 FAQ 크롤링
3. 문서 전처리 및 청킹
4. Ollama 임베딩 생성
5. Weaviate 벡터스토어 구축

**산출물**:
- `data/processed/` 폴더
- Weaviate 컬렉션 생성 완료

---

### Phase 2: Agent 개발 (Week 2)

**목표**: 4개 Agent 구현

**작업**:
1. 질문 분류 Agent
2. 문서 검색 Agent (Weaviate + Ollama)
3. 답변 생성 Agent (vLLM)
4. 검증 Agent

**산출물**:
- `agents/` 폴더 완성
- 각 Agent 단위 테스트

---

### Phase 3: 워크플로우 통합 (Week 3)

**목표**: LangGraph 파이프라인 완성

**작업**:
1. StateGraph 구성
2. 조건부 라우팅 구현
3. 엔드-투-엔드 테스트
4. 성능 최적화

**산출물**:
- `workflow.py` 완성
- 테스트 케이스 통과

---

### Phase 4: 인터페이스 & 배포 (Week 4)

**목표**: 사용 가능한 형태 완성

**작업**:
1. CLI 인터페이스 구현
2. FastAPI + Gradio/Streamlit 웹서비스 구현
3. 문서화
4. 데모 준비

**산출물**:
- `main.py` CLI
- `README.md` 작성
- 데모 영상/자료

---

## 8. 성능 목표

### 8.1 응답 품질

```
정확도: >85% (법조문 인용 정확도)
재현율: >80% (관련 문서 검색률)
F1 Score: >0.8
```

### 8.2 시스템 성능

```
응답 시간: <5초 (평균)
메모리 사용: <6GB VRAM
처리량: >10 req/min (단일 사용자)
```

### 8.3 사용성

```
Confidence >0.8: 즉시 답변
Confidence 0.5-0.8: 답변 + 경고
Confidence <0.5: 전문가 상담 안내
```

---

## 9. 평가 방법

### 9.1 테스트 데이터셋

```
질문 카테고리별 10개씩 (총 50개)
- 임금 관련: 10개
- 근로시간: 10개
- 휴가/휴일: 10개
- 해고/징계: 10개
- 기타: 10개
```

### 9.2 평가 지표

**자동 평가**:
- BLEU Score (참조 답변과 비교)
- Retrieval Accuracy (관련 문서 포함 여부)

**수동 평가**:
- 법적 정확성 (3점 척도)
- 답변 명확성 (3점 척도)
- 출처 적절성 (3점 척도)

---

## 10. 리스크 관리

### 10.1 기술적 리스크

| 리스크 | 영향 | 완화 방안 |
|--------|------|-----------|
| VRAM 부족 | 높음 | 3B 모델 사용, 배치 크기 축소 |
| 검색 정확도 낮음 | 중간 | 하이브리드 검색, 필터링 강화 |
| LLM 환각 | 높음 | 출처 검증, Confidence 체크 |

### 10.2 법률적 리스크

**면책 조항**:
```
본 챗봇은 일반적인 정보 제공 목적으로,
법률 자문을 대체하지 않습니다.
구체적 사안은 전문가와 상담하세요.
```

---

## 11. 향후 계획

### 11.1 단기 (3개월)

- [ ] 판례 데이터 추가 (100건)
- [ ] 웹 UI 개발 (Gradio/Streamlit)
- [ ] 사용자 피드백 수집

### 11.2 중기 (6개월)

- [ ] 실시간 법률 업데이트 자동화
- [ ] 대화형 컨텍스트 관리

### 11.3 장기 (1년)

- [ ] 다국어 지원 (영어)
- [ ] 음성 인터페이스
- [ ] 모바일 앱 개발

---

## 12. 참고 자료

### 12.1 데이터 출처

- [국가법령정보센터](https://www.law.go.kr)
- [고용노동부](https://www.moel.go.kr)
- [대법원 종합법률정보](https://glaw.scourt.go.kr)

### 12.2 기술 문서

- [LangChain 공식 문서](https://python.langchain.com)
- [LangGraph 가이드](https://langchain-ai.github.io/langgraph)
- [Weaviate 문서](https://weaviate.io/developers/weaviate)
- [vLLM 문서](https://docs.vllm.ai)

---

## 13. 라이선스

```
본 프로젝트는 교육 및 연구 목적으로 개발되었습니다.
상업적 사용 시 법률 전문가의 검토를 권장합니다.
```

---

## 14. 문의

**개발자**: 정종혁  
**이메일**: devna0111@gmail.com  
**GitHub**: [github.com/devna0111]

---

**최종 업데이트**: 2025-10-04