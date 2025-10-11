import weaviate
from langchain_community.vectorstores import Weaviate
from langchain_ollama import OllamaEmbeddings

# Weaviate 클라이언트 (v3)
client = weaviate.Client("http://localhost:8080")

embedding = OllamaEmbeddings(model="bona/bge-m3-korean:latest")
if client.schema.exists("MyLangchainCollection"):
    client.schema.delete_class("MyLangchainCollection")

# LangChain Vectorstore
vectorstore = Weaviate(
    client=client,
    index_name="MyLangchainCollection",
    text_key="text",
    embedding=embedding,
)

# 문서 추가
texts = ["Weaviate is a vector database", "LangChain supports Weaviate", "Weaviate is Awesome!"]
vectorstore.add_texts(texts)

# 유사 검색 (near_vector 방식)
query_vector = embedding.embed_query("What is Weaviate?")
results = vectorstore.similarity_search_by_vector(query_vector, k=3)

for r in results:
    print(r.page_content)

# 클라이언트 종료 필요 없음 (v3)
