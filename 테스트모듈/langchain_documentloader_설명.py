"""
LangChain의 다양한 Loader 완벽 가이드
"""

from pathlib import Path

print("=" * 70)
print("LangChain Loader 종류와 사용법")
print("=" * 70)

# ============================================================
# 1. 주요 Loader 목록
# ============================================================

print("\n[1] 파일 형식별 Loader")
print("-" * 70)

loaders_table = """
파일 형식      | Loader 클래스                  | import 경로
-------------|-------------------------------|------------------------------------------
.txt         | TextLoader                    | langchain_community.document_loaders
.md          | TextLoader                    | langchain_community.document_loaders
.pdf         | PyPDFLoader                   | langchain_community.document_loaders
.docx        | Docx2txtLoader                | langchain_community.document_loaders
.csv         | CSVLoader                     | langchain_community.document_loaders
.json        | JSONLoader                    | langchain_community.document_loaders
.html        | UnstructuredHTMLLoader        | langchain_community.document_loaders
.xlsx        | UnstructuredExcelLoader       | langchain_community.document_loaders
.pptx        | UnstructuredPowerPointLoader  | langchain_community.document_loaders
"""

print(loaders_table)


# ============================================================
# 2. 실제 사용 예시
# ============================================================

print("\n[2] 각 Loader 사용 예시")
print("-" * 70)

# 2-1. TextLoader (.txt, .md)
print("\n📄 TextLoader - 텍스트 파일")
print("-" * 50)

text_example = '''
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "data/raw/laws/근로기준법.txt",
    encoding="utf-8"
)
docs = loader.load()

# DirectoryLoader와 함께 사용
from langchain_community.document_loaders import DirectoryLoader

dir_loader = DirectoryLoader(
    "data/raw/laws",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)
'''
print(text_example)


# 2-2. PyPDFLoader (.pdf)
print("\n📕 PyPDFLoader - PDF 파일")
print("-" * 50)

pdf_example = '''
from langchain_community.document_loaders import PyPDFLoader

# 단일 PDF 파일
loader = PyPDFLoader("data/raw/laws/근로기준법.pdf")
docs = loader.load()  # 페이지별로 Document 생성됨

# DirectoryLoader와 함께
from langchain_community.document_loaders import DirectoryLoader

dir_loader = DirectoryLoader(
    "data/raw/laws",
    glob="*.pdf",
    loader_cls=PyPDFLoader
)
docs = dir_loader.load()

# 설치 필요: pip install pypdf
'''
print(pdf_example)


# 2-3. Docx2txtLoader (.docx)
print("\n📘 Docx2txtLoader - Word 파일")
print("-" * 50)

docx_example = '''
from langchain_community.document_loaders import Docx2txtLoader

# 단일 Word 파일
loader = Docx2txtLoader("data/raw/laws/근로기준법.docx")
docs = loader.load()

# DirectoryLoader와 함께
dir_loader = DirectoryLoader(
    "data/raw/laws",
    glob="*.docx",
    loader_cls=Docx2txtLoader
)
docs = dir_loader.load()

# 설치 필요: pip install docx2txt
'''
print(docx_example)


# 2-4. CSVLoader (.csv)
print("\n📊 CSVLoader - CSV 파일")
print("-" * 50)

csv_example = '''
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    "data/raw/faqs/질문답변.csv",
    encoding="utf-8",
    csv_args={
        'delimiter': ',',
        'quotechar': '"'
    }
)
docs = loader.load()  # 각 행이 하나의 Document

# DirectoryLoader와 함께
dir_loader = DirectoryLoader(
    "data/raw/faqs",
    glob="*.csv",
    loader_cls=CSVLoader,
    loader_kwargs={
        'encoding': 'utf-8',
        'csv_args': {'delimiter': ','}
    }
)
'''
print(csv_example)


# 2-5. JSONLoader (.json)
print("\n🗂️  JSONLoader - JSON 파일")
print("-" * 50)

json_example = '''
from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    "data/raw/faqs/질문답변.json",
    jq_schema='.[]',  # JSON 구조에 따라 변경
    text_content=False
)
docs = loader.load()

# 설치 필요: pip install jq
'''
print(json_example)


# ============================================================
# 3. 우리 프로젝트에 적용하기
# ============================================================

print("\n[3] 우리 프로젝트에 적용 - 여러 형식 지원")
print("-" * 70)

multi_format_code = '''
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader
)

class MultiFormatDocumentLoader:
    """여러 파일 형식을 지원하는 로더"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
    
    def load_laws(self):
        """법령 문서 로드 - 여러 형식 지원"""
        laws_dir = self.data_dir / "laws"
        
        all_docs = []
        
        # 1. .txt 파일
        txt_loader = DirectoryLoader(
            str(laws_dir),
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        all_docs.extend(txt_loader.load())
        
        # 2. .pdf 파일
        pdf_loader = DirectoryLoader(
            str(laws_dir),
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        all_docs.extend(pdf_loader.load())
        
        # 3. .docx 파일
        docx_loader = DirectoryLoader(
            str(laws_dir),
            glob="*.docx",
            loader_cls=Docx2txtLoader
        )
        all_docs.extend(docx_loader.load())
        
        return all_docs

# 사용
loader = MultiFormatDocumentLoader()
docs = loader.load_laws()  # txt, pdf, docx 모두 로드!
'''
print(multi_format_code)


# ============================================================
# 4. 필요한 패키지 설치
# ============================================================

print("\n[4] 각 Loader별 필요 패키지")
print("-" * 70)

requirements = """
# 기본 (이미 설치됨)
langchain
langchain-community

# PDF 지원
pip install pypdf

# Word 지원
pip install docx2txt

# JSON 고급 기능
pip install jq

# Excel 지원
pip install openpyxl unstructured

# HTML 지원
pip install unstructured

# 전부 한 번에 설치
pip install pypdf docx2txt openpyxl
"""
print(requirements)


# ============================================================
# 5. Loader 선택 가이드
# ============================================================

print("\n[5] 어떤 Loader를 써야 할까?")
print("-" * 70)

guide = """
프로젝트 상황별 추천:

1. 법령 문서가 PDF로 제공되는 경우
   → PyPDFLoader 사용
   → 국가법령정보센터는 PDF 다운로드 지원
   
2. 법령 문서를 직접 복사한 경우
   → TextLoader 사용 (현재 우리)
   
3. 고용노동부 FAQ가 Excel인 경우
   → UnstructuredExcelLoader 또는 CSVLoader
   
4. 판례가 Word 파일인 경우
   → Docx2txtLoader 사용
   
5. 여러 형식이 섞여 있는 경우
   → 위 MultiFormatDocumentLoader 패턴 사용
"""
print(guide)


# ============================================================
# 6. 실전 팁
# ============================================================

print("\n[6] 실전 사용 팁")
print("-" * 70)

tips = """
1. PDF 로딩 시 주의사항
   - 페이지당 하나의 Document 생성됨
   - 긴 법령은 수백 개의 Document가 될 수 있음
   - → 나중에 청킹(chunking) 시 고려 필요

2. Word 파일 주의사항
   - 표, 이미지는 제대로 안 읽힐 수 있음
   - 가능하면 텍스트로 변환 후 사용 권장

3. 성능 비교
   속도: TextLoader > Docx2txtLoader > PyPDFLoader
   정확도: 원본 텍스트 > Word > PDF

4. 에러 처리
   try:
       docs = pdf_loader.load()
   except Exception as e:
       print(f"PDF 로딩 실패: {e}")
       # TextLoader로 폴백

5. 메타데이터 확인
   PDF: page 번호가 metadata에 포함됨
   Word: page 번호 없음
   Text: source만 있음
"""
print(tips)


# ============================================================
# 7. 우리 프로젝트 권장사항
# ============================================================

print("\n[7] 우리 프로젝트 권장")
print("-" * 70)

recommendation = """
현재 단계 (학습):
  → TextLoader만 사용
  → .txt, .md 파일로 샘플 데이터 관리
  → 단순하고 명확함

나중 단계 (실전):
  → PyPDFLoader 추가
  → 국가법령정보센터 PDF 직접 사용
  → 더 많은 데이터 확보 가능

최종 단계 (배포):
  → MultiFormatDocumentLoader
  → PDF, Word, Text 모두 지원
  → 유연한 데이터 관리
"""
print(recommendation)


# ============================================================
# 8. 코드 예시: PDF 추가 지원
# ============================================================

print("\n[8] 빠른 확장 예시")
print("-" * 70)

quick_example = '''
# 기존 코드에 PDF 지원 추가하는 법

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader  # 👈 추가
)

class DocumentLoader:
    def load_laws(self):
        laws_dir = self.data_dir / "laws"
        all_docs = []
        
        # 기존: .txt 파일
        txt_loader = DirectoryLoader(
            str(laws_dir),
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        all_docs.extend(txt_loader.load())
        
        # 추가: .pdf 파일  👈 이 부분만 추가하면 됨!
        pdf_loader = DirectoryLoader(
            str(laws_dir),
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        all_docs.extend(pdf_loader.load())
        
        return all_docs

# 이제 .txt와 .pdf 둘 다 읽을 수 있음!
'''
print(quick_example)


# ============================================================
# 요약
# ============================================================

print("\n" + "=" * 70)
print("요약")
print("=" * 70)

summary = """
loader_cls에 다른 Loader를 넣으면:
  → 다양한 파일 형식 지원 가능!

주요 Loader:
  TextLoader      → .txt, .md
  PyPDFLoader     → .pdf ✅ 많이 사용
  Docx2txtLoader  → .docx ✅ 많이 사용
  CSVLoader       → .csv
  JSONLoader      → .json

우리 프로젝트:
  현재: TextLoader만 (충분)
  나중: PyPDFLoader 추가 권장 (법령 PDF)
  
추가 설치:
  pip install pypdf docx2txt
  
확장 방법:
  DirectoryLoader에 glob만 바꿔서 여러 번 호출
  → 모든 형식의 파일을 읽을 수 있음!
"""
print(summary)

print("\n💡 질문: PDF나 Word 파일도 다뤄보고 싶으신가요?")
print("   아니면 지금은 TextLoader만으로 진행할까요?")