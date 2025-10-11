"""
통합 문서 로더 (Load + Split 동시 처리)
파일을 읽으면서 바로 청킹까지 완료
"""

import re
import json

from start import path_extend
path_extend() # 모든 디렉토리 임포트 가능하게 경로 추가

from config.logging_config import setup_logger
logger = setup_logger(__name__)
logger.info(f"document_load_and_split.py 활성화")

from pathlib import Path
from typing import List, Dict

from langchain.schema import Document
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage


# 통합 문서 로더

class UnifiedDocumentLoader:
    """
    파일 읽기 + 청킹을 한 번에 처리하는 로더
    """
    
    def __init__(
        self,
        data_dir: str = "data/raw",
        use_llm: bool = True,
        ollama_model: str = "qwen2.5:1.5b"
    ):
        """
        Args:
            data_dir: 데이터 폴더
            use_llm: 메타데이터 생성 여부
            ollama_model: Ollama 모델
        """
        self.data_dir = Path(data_dir)
        self.use_llm = use_llm
        
        if not self.data_dir.exists():
            raise FileNotFoundError(f"폴더 없음: {self.data_dir}")
        
        # LLM 초기화
        if self.use_llm:
            self.llm = ChatOllama(model=ollama_model, temperature=0.3)
            logger.info(f"LLM 활성화: {ollama_model}")
        else:
            self.llm = None
            logger.info("LLM 비활성화")
    
    def _generate_metadata(self, text: str) -> Dict:
        """LLM으로 메타데이터 생성"""
        if not self.use_llm or not self.llm:
            return {"title": "", "keywords": []}
        
        text_preview = text[:300]
        
        prompt = f"""다음 법률 조항을 분석하여 제목과 키워드 5개를 추출하세요.

{text_preview}

JSON 형식으로 출력:
{{"title": "제목", "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]}}"""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            result = response.content
            
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                return json.loads(result[json_start:json_end])
            
        except Exception as e:
            logger.debug(f"메타데이터 생성 실패: {e}")
        
        return {"title": "", "keywords": []}
    
    def _split_law_text(self, text: str, source_path: str) -> List[Document]:
        """
        법령 텍스트를 조항 단위로 분할하면서 Document 생성
        """
        # 조항 패턴
        pattern = r'(제\s*\d+\s*조(?:의\s*\d+)?)'
        chunks = re.split(pattern, text)
        
        documents = []
        
        for i in range(1, len(chunks), 2):
            if i + 1 < len(chunks):
                article_num = chunks[i].strip()
                article_content = chunks[i + 1].strip()
                
                if len(article_content) < 50:
                    continue
                
                full_text = f"{article_num}\n{article_content}"
                
                # 메타데이터 생성
                llm_meta = self._generate_metadata(full_text)
                
                # Document 생성 (바로!)
                doc = Document(
                    page_content=full_text,
                    metadata={
                        "source": source_path,
                        "type": "law",
                        "chunk_id": len(documents) + 1,
                        "article_num": article_num,
                        "title": llm_meta.get("title", article_num),
                        "keywords": llm_meta.get("keywords", [])
                    }
                )
                
                documents.append(doc)
                logger.info(f"✓ {article_num}: {doc.metadata['title']}")
        
        return documents
    
    def _split_simple_text(self, text: str, source_path: str, doc_type: str) -> List[Document]:
        """
        FAQ/판례를 단순 분할하면서 Document 생성
        """
        chunk_size = 1000
        chunk_overlap = 100
        
        documents = []
        start = 0
        chunk_id = 1
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            doc = Document(
                page_content=chunk_text,
                metadata={
                    "source": source_path,
                    "type": doc_type,
                    "chunk_id": chunk_id
                }
            )
            
            documents.append(doc)
            
            start = end - chunk_overlap
            chunk_id += 1
        
        return documents
    
    def load_laws(self) -> List[Document]:
        """법령 로드 + 청킹"""
        laws_dir = self.data_dir / "laws"
        
        if not laws_dir.exists():
            logger.warning(f"폴더 없음: {laws_dir}")
            return []
        
        logger.info("=" * 50)
        logger.info("법령 로드 + 청킹")
        logger.info("=" * 50)
        
        all_chunks = []
        
        # .txt 파일들
        for file_path in laws_dir.glob("*.txt"):
            logger.info(f"\n파일: {file_path.name}")
            
            # 파일 읽기
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            # 읽으면서 바로 청킹
            chunks = self._split_law_text(text, str(file_path))
            all_chunks.extend(chunks)
            
            logger.info(f"→ {len(chunks)}개 청크")
        
        logger.info(f"\n✅ 법령 총 {len(all_chunks)}개 청크")
        return all_chunks
    
    def load_faqs(self) -> List[Document]:
        """FAQ 로드 + 청킹"""
        faqs_dir = self.data_dir / "faqs"
        
        if not faqs_dir.exists():
            return []
        
        logger.info("\nFAQ 로드 + 청킹")
        
        all_chunks = []
        
        for file_path in list(faqs_dir.glob("*.txt")) + list(faqs_dir.glob("*.md")):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            chunks = self._split_simple_text(text, str(file_path), "faq")
            all_chunks.extend(chunks)
        
        logger.info(f"✓ FAQ {len(all_chunks)}개 청크")
        return all_chunks
    
    def load_cases(self) -> List[Document]:
        """판례 로드 + 청킹"""
        cases_dir = self.data_dir / "cases"
        
        if not cases_dir.exists():
            return []
        
        logger.info("\n판례 로드 + 청킹")
        
        all_chunks = []
        
        for file_path in cases_dir.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            chunks = self._split_simple_text(text, str(file_path), "case")
            all_chunks.extend(chunks)
        
        logger.info(f"✓ 판례 {len(all_chunks)}개 청크")
        return all_chunks
    
    def load_all(self) -> List[Document]:
        """
        모든 문서 로드 + 청킹 (한 번에!)
        
        Returns:
            청크된 Document 리스트
        """
        logger.info("=" * 60)
        logger.info("전체 문서 로드 + 청킹 시작")
        logger.info("=" * 60)
        
        all_chunks = []
        
        # 법령
        law_chunks = self.load_laws()
        all_chunks.extend(law_chunks)
        
        # FAQ
        faq_chunks = self.load_faqs()
        all_chunks.extend(faq_chunks)
        
        # 판례
        case_chunks = self.load_cases()
        all_chunks.extend(case_chunks)
        
        logger.info("=" * 60)
        logger.info(f"✅ 전체 완료: {len(all_chunks)}개 청크")
        logger.info("=" * 60)
        
        return all_chunks

# 테스트

if __name__ == "__main__":
    print("\n[통합 로더 테스트]\n")
    
    # LLM 없이 테스트
    print("1. LLM 없이 실행")
    loader_no_llm = UnifiedDocumentLoader(use_llm=False)
    chunks_no_llm = loader_no_llm.load_all()
    
    print(f"\n→ 총 {len(chunks_no_llm)}개 청크")
    
    if chunks_no_llm:
        print("\n첫 번째 청크:")
        print(f"  조항: {chunks_no_llm[0].metadata.get('article_num')}")
        print(f"  내용: {chunks_no_llm[0].page_content[:100]}...")
    
    print("\n" + "=" * 70)
    
    # LLM 포함 (Ollama 필요)
    print("\n2. LLM 포함 실행 (Ollama 필요)")
    print("⚠️  ollama serve + ollama pull qwen2.5:1.5b\n")
    
    try:
        loader_with_llm = UnifiedDocumentLoader(use_llm=True)
        chunks_with_llm = loader_with_llm.load_all()
        
        print(f"\n→ 총 {len(chunks_with_llm)}개 청크")
        
        if chunks_with_llm:
            print("\n첫 번째 청크:")
            chunk = chunks_with_llm[0]
            print(f"  조항: {chunk.metadata.get('article_num')}")
            print(f"  제목: {chunk.metadata.get('title')}")
            print(f"  키워드: {chunk.metadata.get('keywords')}")
    
    except Exception as e:
        print(f"❌ 실패: {e}")
    
    print("\n" + "=" * 70)
    
    # 비교
    compare_approaches()
    
    print(f"\n로그: {log_filename}")