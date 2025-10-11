"""
DirectoryLoader 완벽 설명
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from pathlib import Path

print("=" * 70)
print("DirectoryLoader 완벽 가이드")
print("=" * 70)

# ============================================================
# 1. DirectoryLoader 기본 사용법
# ============================================================

print("\n[1] 기본 사용법")
print("-" * 70)

"""
DirectoryLoader(
    path,              # 폴더 경로
    glob,              # 파일 패턴 (예: "*.txt", "**/*.md")
    loader_cls,        # 파일을 어떻게 읽을지 (TextLoader, PDFLoader 등)
    loader_kwargs      # loader에 전달할 추가 옵션
)
"""

# 예시 1: .txt 파일만 읽기
loader_txt = DirectoryLoader(
    path="data/raw/laws",
    glob="*.txt",                    # laws 폴더의 .txt만
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)

print("설정:")
print(f"  경로: data/raw/laws")
print(f"  패턴: *.txt")
print(f"  결과: laws 폴더의 모든 .txt 파일을 읽음")


# ============================================================
# 2. glob 패턴 설명
# ============================================================

print("\n[2] glob 패턴 이해하기")
print("-" * 70)

patterns = {
    "*.txt": "현재 폴더의 .txt 파일만",
    "**/*.txt": "현재 폴더 + 하위 폴더의 모든 .txt 파일",
    "*.md": ".md 파일만",
    "*": "모든 파일 (확장자 무관)",
    "sample_*.txt": "sample_로 시작하는 .txt 파일"
}

for pattern, desc in patterns.items():
    print(f"  {pattern:15s} → {desc}")

print("\n💡 우리 프로젝트에서는 '*.txt' 또는 '*.md'를 주로 사용")


# ============================================================
# 3. loader_cls 옵션들
# ============================================================

print("\n[3] loader_cls 종류")
print("-" * 70)

loaders = """
TextLoader          → 일반 텍스트 파일 (.txt, .md)
PDFLoader           → PDF 파일
CSVLoader           → CSV 파일
JSONLoader          → JSON 파일
UnstructuredLoader  → 여러 형식 자동 감지
"""

print(loaders)
print("💡 우리는 TextLoader만 사용 (텍스트 파일만 다루므로)")


# ============================================================
# 4. 실제 동작 시연
# ============================================================

print("\n[4] 실제 동작 확인")
print("-" * 70)

# laws 폴더가 있다고 가정
if Path("data/raw/laws").exists():
    loader = DirectoryLoader(
        path="data/raw/laws",
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    
    # 로드 실행
    documents = loader.load()
    
    print(f"✓ 발견된 문서: {len(documents)}개")
    
    if documents:
        first_doc = documents[0]
        print(f"\n첫 번째 문서:")
        print(f"  파일: {first_doc.metadata.get('source')}")
        print(f"  크기: {len(first_doc.page_content)} 글자")
        print(f"  내용 미리보기: {first_doc.page_content[:100]}...")
else:
    print("⚠️  data/raw/laws 폴더가 없습니다")
    print("(실제 환경에서는 문서들을 자동으로 읽어옵니다)")


# ============================================================
# 5. DirectoryLoader가 하는 일 (내부 동작)
# ============================================================

print("\n[5] DirectoryLoader 내부 동작 순서")
print("-" * 70)

steps = """
1. 지정된 폴더 탐색
   └─ path="data/raw/laws"

2. glob 패턴에 맞는 파일 찾기
   └─ glob="*.txt" → 근로기준법_샘플.txt 발견

3. 각 파일마다 loader_cls로 읽기
   └─ TextLoader로 파일 내용 읽기

4. Document 객체 생성
   └─ page_content에 파일 내용
   └─ metadata에 파일 경로 저장

5. 모든 Document를 리스트로 반환
   └─ [Document1, Document2, ...]
"""

print(steps)


# ============================================================
# 6. 우리가 수동으로 구현한 코드와 비교
# ============================================================

print("\n[6] 수동 구현 vs DirectoryLoader")
print("-" * 70)

print("""
수동 구현 (우리 코드):
  장점: 세밀한 제어 가능, 로깅 추가 쉬움
  단점: 코드가 길어짐, 에러 처리 직접 해야 함
  
  for file in folder.glob("*.txt"):
      with open(file) as f:
          content = f.read()
      doc = Document(content, metadata)
      docs.append(doc)

DirectoryLoader:
  장점: 코드 짧음, LangChain 표준, 안정적
  단점: 커스터마이징 제한적, 상세 로깅 어려움
  
  loader = DirectoryLoader(folder, glob="*.txt")
  docs = loader.load()
""")


# ============================================================
# 7. 실전 팁
# ============================================================

print("\n[7] 실전 사용 팁")
print("-" * 70)

tips = """
1. 여러 확장자 읽기:
   # .txt와 .md 둘 다 읽으려면
   txt_loader = DirectoryLoader(path, glob="*.txt", ...)
   md_loader = DirectoryLoader(path, glob="*.md", ...)
   all_docs = txt_loader.load() + md_loader.load()

2. 하위 폴더까지 읽기:
   DirectoryLoader(path, glob="**/*.txt", ...)
   
3. 특정 파일 제외:
   # DirectoryLoader는 exclude가 없으므로
   # 로드 후 필터링
   docs = loader.load()
   docs = [d for d in docs if "temp" not in d.metadata['source']]

4. 에러 처리:
   try:
       docs = loader.load()
   except Exception as e:
       print(f"로딩 실패: {e}")
"""

print(tips)


# ============================================================
# 8. 우리 프로젝트 추천 방식
# ============================================================

print("\n[8] 우리 프로젝트 추천")
print("-" * 70)

recommendation = """
초급자:
  → 수동 구현 (for문 + open) 사용
  → 각 단계를 이해하면서 학습
  
중급자 이상:
  → DirectoryLoader 사용
  → 코드 간결, 유지보수 쉬움
  
실무:
  → DirectoryLoader + 커스텀 로깅 조합
  → 표준 도구 사용하되 필요시 확장
"""

print(recommendation)


# ============================================================
# 9. 예제: 혼합 방식 (추천)
# ============================================================

print("\n[9] 추천 방식: DirectoryLoader + 로깅")
print("-" * 70)

example_code = '''
import logging
from langchain_community.document_loaders import DirectoryLoader, TextLoader

logger = logging.getLogger(__name__)

def load_documents(folder_path):
    """DirectoryLoader + 상세 로깅"""
    
    logger.info(f"문서 로딩 시작: {folder_path}")
    
    try:
        loader = DirectoryLoader(
            folder_path,
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        docs = loader.load()
        logger.info(f"✓ {len(docs)}개 문서 로드 완료")
        
        # 상세 정보 로깅
        for doc in docs:
            logger.debug(f"  - {doc.metadata['source']}")
        
        return docs
        
    except Exception as e:
        logger.error(f"로딩 실패: {e}")
        return []
'''

print(example_code)


# ============================================================
# 요약
# ============================================================

print("\n" + "=" * 70)
print("요약")
print("=" * 70)

summary = """
DirectoryLoader = 폴더의 파일들을 자동으로 읽어주는 도구

핵심 파라미터:
  path         → 폴더 경로
  glob         → 파일 패턴 (*.txt, *.md)
  loader_cls   → 읽는 방법 (TextLoader)
  
하는 일:
  1. 폴더 탐색
  2. 패턴에 맞는 파일 찾기
  3. 각 파일 읽기
  4. Document 객체로 변환
  5. 리스트로 반환
  
장점: 코드 간결, 안정적
단점: 상세 제어 제한적

우리 선택:
  → 학습 단계: 수동 구현 (현재)
  → 실전 단계: DirectoryLoader (나중에)
"""

print(summary)