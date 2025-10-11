from langchain_community.vectorstores import Weaviate
from langchain_ollama import OllamaEmbeddings
import weaviate

# 클라이언트 생성 (v3)
client = weaviate.Client("http://localhost:8080")

embedding = OllamaEmbeddings(model="bona/bge-m3-korean:latest")

vectorstore = Weaviate(
    client=client,
    index_name="MyLangchainCollection",
    text_key="text",
    embedding=embedding,
)

# 텍스트 + 메타데이터 리스트
texts = [
    "Weaviate is a vector database",
    "LangChain supports Weaviate",
]
metadatas = [
    {"source": "Wikipedia", "author": "Alice"},
    {"source": "Docs", "author": "Bob"},
]

# 추가
vectorstore.add_texts(texts=texts, metadatas=metadatas)
