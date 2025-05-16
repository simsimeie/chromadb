# chromadb sqllite3 버전 이슈
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    print("pysqlite3-binary not found, falling back to standard sqlite3")
    # pysqlite3-binary가 없으면 표준 sqlite3를 그대로 사용합니다.
    # 이 경우 시스템 sqlite3 버전이 낮으면 오류가 계속 발생할 수 있습니다.
    pass

import sqlite3

print(sqlite3.sqlite_version)


import chromadb

# Chroma DB에 연결
client = chromadb.HttpClient(host="localhost", port=8000)
# 연결 확인
print(f"heart beat : {client.heartbeat()}")

# collection 생성
# collection = client.create_collection(name="my_collection")

# collection에 데이터 추가
# collection.add(
#     documents=["This is a document", "This is another document"],
#     metadatas=[{"source": "doc1"}, {"source": "doc2"}],
#     ids=["doc1", "doc2"]
# )

# DB에 저장된 collection list 출력
collection_list = client.list_collections()
print(collection_list[0].name)
print(collection_list[0].metadata)

# collection 가져오기
collection = client.get_collection(name="my_collection")


# 데이터 쿼리
result = collection.get(ids=["doc1"])
print(result)

# 유사도 기반 쿼리
result = collection.query(
    query_texts=["This is a query"],
    n_results=1,
)
print(result)
