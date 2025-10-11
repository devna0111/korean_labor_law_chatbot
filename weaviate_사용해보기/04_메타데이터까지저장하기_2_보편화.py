from langchain.schema import Document
from langchain_community.vectorstores import Weaviate
from langchain_ollama import OllamaEmbeddings
import weaviate

client = weaviate.Client("http://localhost:8080")

embedding = OllamaEmbeddings(model="bona/bge-m3-korean:latest")

if client.schema.exists("MyLangchainCollection_2"):
    client.schema.delete_class("MyLangchainCollection_2")

client.schema.create_class({
    "class": "MyLangchainCollection_2",
    "vectorizer": "text2vec-ollama",
    "properties": [
        {
            "name": "text",
            "dataType": ["text"]
        },
        {
            "name": "source",
            "dataType": ["text"]
        },
        {
            "name": "author",
            "dataType": ["text"]
        }
    ]
})

vectorstore = Weaviate(
    client=client,
    index_name="MyLangchainCollection_2",
    text_key="text",
    embedding=embedding,
)

# Document 리스트 생성 (텍스트 + 메타데이터 포함)
docs = [
    Document(page_content="Weaviate is a vector database", metadata={"source": "Wikipedia", "author": "Alice"}),
    Document(page_content="놀라운 Weaviate", metadata={"source": "Naver", "author": "정종혁"}),
    Document(page_content="LangChain supports Weaviate", metadata={"source": "Docs", "author": "Bob"}),
]

# add_documents 메서드로 삽입
vectorstore.add_documents(docs)

test = "What is the Weaviate?"
answer = vectorstore.similarity_search_by_vector(embedding.embed_query(test), k=3)

# print(answer)
# print([i.page_content for i in answer])
# print()

def get_metadata_for_texts(client, class_name, texts:list):
    """
    texts: 유사도 검색 결과로 나온 텍스트 리스트
    """
    docs = []
    for text in texts:
        # Weaviate에서 text 필드가 일치하는 객체 쿼리 (단순 예시)
        result = (
            client.query
            .get(class_name, ["text", "source", "author"])
            .with_where({
                "path": ["text"],
                "operator": "Equal",
                "valueText": text
            })
            .do()
        )
        
        objs = result.get("data", {}).get("Get", {}).get(class_name, [])
        if objs:
            obj = objs[0]  # 보통 text가 unique 하다고 가정
            metadata = {
                "source": obj.get("source", ""),
                "author": obj.get("author", "")
            }
        else:
            metadata = {}
        docs.append(Document(page_content=text, metadata=metadata))
    return docs

# 사용 예시
# 1) 유사도 검색 수행 (메타데이터는 없음)
results = vectorstore.similarity_search_by_vector(embedding.embed_query("Weaviate가 뭔가요?"), k=3)
# print(results)

# 2) 텍스트 리스트 추출
texts = [doc.page_content for doc in results]
# print(texts)

# 3) 텍스트 기반으로 메타데이터 포함 문서 재구성
docs_with_metadata = get_metadata_for_texts(client, "MyLangchainCollection_2", texts)

for doc in docs_with_metadata:
    print("본문 :", doc.page_content,"\t 메타데이터 :", doc.metadata)
    
# result = client.query.get("MyLangchainCollection_2", ["text", "source", "author"]).do()
# print(result.get('data'))