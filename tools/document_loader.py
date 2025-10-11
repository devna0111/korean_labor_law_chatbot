"""
문서 로더 모듈
LangChain의 Document와 DirectoryLoader 활용
"""
from pathlib import Path
from typing import List, Dict

from start import path_extend
path_extend() # 모든 디렉토리 임포트 가능하게 경로 추가

# LangChain 임포트
from langchain.schema import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)
from config.logging_config import setup_logger

logger = setup_logger("document_loader")
logger.info(f"document_loader.py 활성화")

# DocumentLoader 클래스
class DocumentLoader:
    """
    문서 로더 클래스 (LangChain 활용)
    
    - 파일 '내용 전체'를 읽어서 Document로
    """
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Args:
            data_dir: 데이터 폴더 경로
        """
        self.data_dir = Path(data_dir)
        
        logger.info(f"DocumentLoader 초기화: {self.data_dir}")
        
        if not self.data_dir.exists():
            logger.error(f"데이터 폴더를 찾을 수 없습니다: {self.data_dir}")
            raise FileNotFoundError(f"데이터 폴더를 찾을 수 없습니다: {self.data_dir}")
        
        logger.debug(f"데이터 폴더 확인 완료: {self.data_dir}")
    
    def load_laws(self) -> List[Document]:
        """
        법령 문서들 로드 (LangChain DirectoryLoader 사용)
        
        Returns:
            Document 리스트 (LangChain Document)
        """
        logger.info("법령 문서 로딩 시작")
        laws_dir = self.data_dir / "laws"
        return self._load_from_directory(laws_dir, doc_type="law")
    
    def load_faqs(self) -> List[Document]:
        """FAQ 문서들 로드"""
        logger.info("FAQ 문서 로딩 시작")
        faqs_dir = self.data_dir / "faqs"
        return self._load_from_directory(faqs_dir, doc_type="faq")
    
    def load_cases(self) -> List[Document]:
        """판례 문서들 로드"""
        logger.info("판례 문서 로딩 시작")
        cases_dir = self.data_dir / "cases"
        return self._load_from_directory(cases_dir, doc_type="case")
    
    def _load_from_directory(self, directory: Path, doc_type: str) -> List[Document]:
        """
        특정 폴더의 모든 파일 로드 (LangChain 활용)
        
        Args:
            directory: 폴더 경로
            doc_type: 문서 타입 (law/faq/case)
            
        Returns:
            Document 리스트
        """
        if not directory.exists():
            logger.warning(f"폴더가 없습니다: {directory}")
            return []
        
        logger.debug(f"폴더 탐색: {directory}")
        
        documents = []
        
        try:
            # LangChain의 DirectoryLoader 사용
            # glob="**/*.txt" : 모든 .txt 파일
            # loader_cls=TextLoader : 텍스트 파일 로더
            txt_loader = DirectoryLoader(
                str(directory),
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            txt_docs = txt_loader.load()
            
            # .md 파일도 로드
            md_loader = DirectoryLoader(
                str(directory),
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            md_docs = md_loader.load()
            
            # 합치기
            all_docs = txt_docs + md_docs
            
            # 메타데이터에 타입 추가
            for doc in all_docs:
                doc.metadata['type'] = doc_type
                doc.metadata['size'] = len(doc.page_content)
                logger.debug(f"문서 로드: {doc.metadata.get('source')} ({doc.metadata['size']} 글자)")
            
            documents = all_docs
            logger.info(f"✓ {directory.name}에서 {len(documents)}개 문서 로드 완료")
            
        except Exception as e:
            logger.error(f"폴더 로딩 중 에러: {directory}")
            logger.error(f"에러 내용: {str(e)}")
        
        return documents
    
    def load_all(self) -> Dict[str, List[Document]]:
        """
        모든 문서 로드
        
        Returns:
            카테고리별 Document 딕셔너리
        """
        logger.info("=" * 50)
        logger.info("전체 문서 로딩 시작")
        logger.info("=" * 50)
        
        all_docs = {
            "laws": self.load_laws(),
            "faqs": self.load_faqs(),
            "cases": self.load_cases()
        }
        
        # 통계
        total = sum(len(docs) for docs in all_docs.values())
        logger.info(f"✅ 총 {total}개 문서 로드 완료")
        
        for category, docs in all_docs.items():
            logger.info(f"  - {category}: {len(docs)}개")
        
        return all_docs


# ============================================================
# 질문 2에 대한 설명 코드
# ============================================================

def demonstrate_what_document_contains():
    """
    Document가 '이름만' 담는 게 아니라 '내용 전체'를 담는다는 것을 보여주는 예시
    """
    print("\n" + "=" * 60)
    print("Document가 담고 있는 내용 확인")
    print("=" * 60)
    
    loader = DocumentLoader()
    all_docs = loader.load_all()
    
    # 첫 번째 문서 자세히 보기
    if all_docs['laws']:
        first_doc = all_docs['laws'][0]
        
        print(f"\n📄 파일명: {first_doc.metadata.get('source')}")
        print(f"📏 크기: {first_doc.metadata.get('size')} 글자")
        print(f"📦 타입: {first_doc.metadata.get('type')}")
        print(f"\n📝 내용 (처음 500자):")
        print("-" * 60)
        print(first_doc.page_content[:500])
        print("-" * 60)
        print("\n👆 보시다시피 '파일 내용 전체'가 page_content에 들어있습니다!")


# ============================================================
# 테스트
# ============================================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("document_loader.py 테스트 시작")
    logger.info("=" * 60)
    
    try:
        # 기본 로딩 테스트
        loader = DocumentLoader()
        all_documents = loader.load_all()
        
        # 간단한 요약
        print("\n" + "=" * 50)
        print("로드된 문서 요약")
        print("=" * 50)
        
        for category, docs in all_documents.items():
            print(f"\n📁 {category.upper()}: {len(docs)}개")
            
            for i, doc in enumerate(docs, 1):
                filename = Path(doc.metadata.get('source', 'unknown')).name
                print(f"  [{i}] {filename} - {doc.metadata.get('size', 0)} 글자")
        
        # 질문 2에 대한 상세 설명
        demonstrate_what_document_contains()
        
        logger.info("=" * 60)
        logger.info("테스트 완료!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.critical(f"치명적 에러: {str(e)}")
        logger.exception("전체 에러 추적:")
        raise