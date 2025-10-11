"""
텍스트 청킹 모듈 (LangChain ChatOllama 버전)
- 조항 단위 분할
- ChatOllama 기반 메타데이터 자동 생성 (제목, 키워드)
"""
import re
import json
from typing import List, Dict

from start import path_extend
path_extend() # 모든 디렉토리 임포트 가능하게 경로 추가

from langchain.schema import Document
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from config.logging_config import setup_logger

logger = setup_logger("text_splitter")
logger.info(f"text_splitter.py 활성화")

# 메타데이터 생성기
class MetadataGenerator:
    """
    LangChain ChatOllama를 사용한 메타데이터 생성기
    조항 텍스트 → 제목 + 키워드 5개
    """
    
    def __init__(self, model: str = "qwen2.5:1.5b"):
        """
        Args:
            model: Ollama 모델명
        """
        self.llm = ChatOllama(
            model=model,
            temperature=0.3
        )
        
        logger.info(f"ChatOllama 초기화: {model}")
    
    def generate(self, text: str) -> Dict[str, any]:
        """
        텍스트 분석하여 제목과 키워드 생성
        
        Args:
            text: 분석할 조항 텍스트
            
        Returns:
            {"title": "제목", "keywords": ["키워드1", ...]}
        """
        
        # 텍스트가 너무 길면 앞부분만
        text_preview = text[:300] if len(text) > 300 else text
        
        prompt = f"""다음 법률 조항을 분석하여 제목과 주요 키워드 5개를 추출하세요.

법률 조항:
{text_preview}

출력 형식 (JSON):
{{
    "title": "이 조항의 핵심 내용을 한 문장으로",
    "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
}}

JSON만 출력:"""
        
        try:
            # LangChain ChatOllama 사용
            response = self.llm.invoke([HumanMessage(content=prompt)])
            result_text = response.content
            
            # JSON 추출
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = result_text[json_start:json_end]
                metadata = json.loads(json_str)
                
                logger.debug(f"✓ 메타데이터: {metadata.get('title', '')[:50]}")
                return metadata
            else:
                logger.warning("JSON 추출 실패")
                return {"title": "파싱 실패", "keywords": []}
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 에러: {e}")
            return {"title": "파싱 에러", "keywords": []}
        
        except Exception as e:
            logger.error(f"메타데이터 생성 실패: {e}")
            return {"title": "생성 실패", "keywords": []}

# 텍스트 분할기
class LawTextSplitter:
    """
    법률 문서 전용 텍스트 분할기
    - 조항 단위로 분할
    - ChatOllama로 메타데이터 자동 생성
    """
    
    def __init__(self, use_llm: bool = True, ollama_model: str = "qwen2.5:1.5b"):
        """
        Args:
            use_llm: LLM 메타데이터 생성 사용 여부
            ollama_model: Ollama 모델명
        """
        self.use_llm = use_llm
        
        if self.use_llm:
            self.metadata_gen = MetadataGenerator(model=ollama_model)
            logger.info("LLM 메타데이터 생성 활성화")
        else:
            self.metadata_gen = None
            logger.info("LLM 메타데이터 생성 비활성화")
    
    def split_by_article(self, text: str) -> List[str]:
        """
        조항 단위로 텍스트 분할
        
        Args:
            text: 원본 법률 문서
            
        Returns:
            조항별로 나눈 텍스트 리스트
        """
        logger.info("조항 단위 분할 시작")
        
        # 정규식: 제N조, 제N조의N
        pattern = r'(제\s*\d+\s*조(?:의\s*\d+)?)'
        
        # 분할
        chunks = re.split(pattern, text)
        
        # 조항 번호 + 내용 합치기
        articles = []
        for i in range(1, len(chunks), 2):
            if i + 1 < len(chunks):
                article_num = chunks[i].strip()
                article_content = chunks[i + 1].strip()
                
                # 너무 짧으면 제외
                if len(article_content) < 50:
                    logger.debug(f"건너뜀: {article_num} (내용 부족)")
                    continue
                
                full_article = f"{article_num}\n{article_content}"
                articles.append(full_article)
        
        logger.info(f"✓ {len(articles)}개 조항으로 분할")
        return articles
    
    def split_document(self, document: Document) -> List[Document]:
        """
        Document 객체를 조항 단위로 분할 + 메타데이터 생성
        
        Args:
            document: 원본 Document
            
        Returns:
            조항별 Document 리스트
        """
        logger.info(f"문서 분할: {document.metadata.get('filename', 'unknown')}")
        
        # 1. 조항 분할
        articles = self.split_by_article(document.page_content)
        
        if not articles:
            logger.warning("분할된 조항이 없음")
            return []
        
        # 2. 각 조항을 Document로
        chunked_docs = []
        
        for idx, article_text in enumerate(articles, 1):
            # 조항 번호 추출
            article_match = re.match(r'(제\s*\d+\s*조(?:의\s*\d+)?)', article_text)
            article_num = article_match.group(1) if article_match else f"청크{idx}"
            
            # 메타데이터 복사
            metadata = document.metadata.copy()
            metadata['chunk_id'] = idx
            metadata['article_num'] = article_num
            
            # LLM으로 제목/키워드 생성
            if self.use_llm and self.metadata_gen:
                try:
                    logger.info(f"메타데이터 생성: {article_num}")
                    
                    llm_metadata = self.metadata_gen.generate(article_text)
                    
                    metadata['title'] = llm_metadata.get('title', article_num)
                    metadata['keywords'] = llm_metadata.get('keywords', [])
                    
                    logger.info(f"✓ {article_num}: {metadata['title']}")
                    
                except Exception as e:
                    logger.warning(f"메타데이터 실패: {article_num} - {e}")
                    metadata['title'] = article_num
                    metadata['keywords'] = []
            else:
                metadata['title'] = article_num
                metadata['keywords'] = []
            
            # Document 생성
            chunk_doc = Document(
                page_content=article_text,
                metadata=metadata
            )
            
            chunked_docs.append(chunk_doc)
        
        logger.info(f"✓ {len(chunked_docs)}개 청크 생성")
        return chunked_docs
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        여러 Document 한꺼번에 분할
        
        Args:
            documents: Document 리스트
            
        Returns:
            분할된 Document 리스트
        """
        logger.info("=" * 50)
        logger.info(f"전체 문서 분할: {len(documents)}개")
        logger.info("=" * 50)
        
        all_chunks = []
        
        for doc in documents:
            chunks = self.split_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"✅ 전체 분할 완료: {len(all_chunks)}개")
        return all_chunks

# FAQ/판례용 분할기
class SimpleSplitter:
    """
    FAQ, 판례 등을 위한 단순 분할기
    고정 크기로 분할
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Args:
            chunk_size: 청크 크기 (글자)
            chunk_overlap: 중복 크기 (글자)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(f"SimpleSplitter: size={chunk_size}, overlap={chunk_overlap}")
    
    def split_document(self, document: Document) -> List[Document]:
        """
        고정 크기로 분할
        
        Args:
            document: 원본 Document
            
        Returns:
            분할된 Document 리스트
        """
        text = document.page_content
        chunks = []
        
        start = 0
        chunk_id = 1
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            metadata = document.metadata.copy()
            metadata['chunk_id'] = chunk_id
            
            chunks.append(Document(
                page_content=chunk_text,
                metadata=metadata
            ))
            
            start = end - self.chunk_overlap
            chunk_id += 1
        
        logger.debug(f"분할 완료: {len(chunks)}개")
        return chunks
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """여러 문서 분할"""
        all_chunks = []
        for doc in documents:
            all_chunks.extend(self.split_document(doc))
        
        logger.info(f"✓ {len(all_chunks)}개 청크")
        return all_chunks

# 통합 분할 관리자
class TextSplitterManager:
    """
    문서 타입별 적절한 분할기 선택
    """
    
    def __init__(self, use_llm: bool = True, ollama_model: str = "qwen2.5:1.5b"):
        """
        Args:
            use_llm: LLM 메타데이터 생성 여부
            ollama_model: Ollama 모델명
        """
        self.law_splitter = LawTextSplitter(
            use_llm=use_llm,
            ollama_model=ollama_model
        )
        self.simple_splitter = SimpleSplitter()
        
        logger.info("TextSplitterManager 초기화")
    
    def split_all(self, documents_dict: Dict[str, List[Document]]) -> List[Document]:
        """
        모든 문서를 타입에 맞게 분할
        
        Args:
            documents_dict: {
                "laws": [Document, ...],
                "faqs": [Document, ...],
                "cases": [Document, ...]
            }
            
        Returns:
            분할된 모든 Document 리스트
        """
        logger.info("=" * 60)
        logger.info("전체 문서 분할 시작")
        logger.info("=" * 60)
        
        all_chunks = []
        
        # 법령: 조항 분할 + LLM
        if "laws" in documents_dict and documents_dict["laws"]:
            logger.info("\n[1] 법령 (조항 + LLM)")
            law_chunks = self.law_splitter.split_documents(documents_dict["laws"])
            all_chunks.extend(law_chunks)
        
        # FAQ: 단순 분할
        if "faqs" in documents_dict and documents_dict["faqs"]:
            logger.info("\n[2] FAQ (단순)")
            faq_chunks = self.simple_splitter.split_documents(documents_dict["faqs"])
            all_chunks.extend(faq_chunks)
        
        # 판례: 단순 분할
        if "cases" in documents_dict and documents_dict["cases"]:
            logger.info("\n[3] 판례 (단순)")
            case_chunks = self.simple_splitter.split_documents(documents_dict["cases"])
            all_chunks.extend(case_chunks)
        
        logger.info("=" * 60)
        logger.info(f"✅ 전체: {len(all_chunks)}개 청크")
        logger.info("=" * 60)
        
        return all_chunks

# 테스트

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("text_splitter.py 테스트")
    logger.info("=" * 60)
    
    # 샘플 텍스트
    sample_text = """# 근로기준법 (샘플)

제1조(목적)
이 법은 헌법에 따라 근로조건의 기준을 정함으로써 근로자의 기본적 생활을 보장, 향상시키며 균형있는 국민경제의 발전을 꾀하는 것을 목적으로 한다.

제2조(정의)
① 이 법에서 사용하는 용어의 뜻은 다음과 같다.
1. "근로자"란 직업의 종류와 관계없이 임금을 목적으로 사업이나 사업장에 근로를 제공하는 사람을 말한다.
2. "사용자"란 사업주 또는 사업 경영 담당자를 말한다.

제50조(근로시간)
① 1주 간의 근로시간은 휴게시간을 제외하고 40시간을 초과할 수 없다.
② 1일의 근로시간은 휴게시간을 제외하고 8시간을 초과할 수 없다.
"""
    
    sample_doc = Document(
        page_content=sample_text,
        metadata={"source": "test.txt", "type": "law"}
    )
    
    # 테스트 1: LLM 없이
    print("\n[테스트 1] LLM 없이 조항 분할")
    print("-" * 60)
    
    splitter_no_llm = LawTextSplitter(use_llm=False)
    chunks = splitter_no_llm.split_document(sample_doc)
    
    print(f"\n✓ {len(chunks)}개 청크\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"[청크 {i}]")
        print(f"  조항: {chunk.metadata.get('article_num')}")
        print(f"  내용: {chunk.page_content[:80]}...")
        print()
    
    # 테스트 2: ChatOllama 사용
    print("\n[테스트 2] ChatOllama로 메타데이터 생성")
    print("-" * 60)
    print("Ollama 실행 필요:")
    print("   → ollama serve")
    print("   → ollama pull qwen2.5:1.5b\n")
    
    try:
        splitter_with_llm = LawTextSplitter(use_llm=True)
        chunks_with_meta = splitter_with_llm.split_document(sample_doc)
        
        print(f"\n✓ {len(chunks_with_meta)}개 청크 (메타데이터)\n")
        
        for i, chunk in enumerate(chunks_with_meta, 1):
            print(f"[청크 {i}]")
            print(f"  조항: {chunk.metadata.get('article_num')}")
            print(f"  제목: {chunk.metadata.get('title')}")
            print(f"  키워드: {chunk.metadata.get('keywords')}")
            print()
        
    except Exception as e:
        print(f"❌ 실패: {e}")
        print("→ Ollama 서버 확인")
    
    print("=" * 60)
    print("완료!")
    print("=" * 60)