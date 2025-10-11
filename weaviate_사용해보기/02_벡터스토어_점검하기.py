import weaviate

# v3 클라이언트 사용 (LangChain 호환 목적)
client = weaviate.Client("http://localhost:8080")

# class 점검하기
print([i.get('class') for i in client.schema.get()['classes']])
if client.schema.exists("Question"):
    client.schema.delete_class("Question")

# 클래스 이름에 저장된 데이터 확인 (예: "MyLangchainCollection")    
results = client.data_object.get(class_name="MyLangchainCollection", limit=10)

# 내용 출력
for obj in results['objects']:
    print(obj['properties'])
