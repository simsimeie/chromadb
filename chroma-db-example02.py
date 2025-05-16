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

import os
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

from chromadb.utils import embedding_functions
import chromadb

# Chroma DB에 연결
client = chromadb.HttpClient(host="localhost", port=8000)
# 연결 확인
print(f"heart beat : {client.heartbeat()}")

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small")

# 4. 컬렉션 생성 또는 가져오기
# 임베딩 함수를 지정하여 컬렉션을 가져오거나 생성합니다.
# 이렇게 하면 Chroma DB가 이 컬렉션에서 임베딩이 필요한 작업을 할 때 이 함수를 사용합니다.
collection_name = "my_openai_embeddings_collection"
collection = client.get_or_create_collection(
    name=collection_name,
    embedding_function=embedding_function # <-- 설정한 임베딩 함수 연결
)
print(f"'{collection_name}' 컬렉션 가져오거나 생성 완료.")

# 5. 임베딩할 텍스트 데이터 준비
documents = [
    "서울은 대한민국의 수도이며 활기찬 도시입니다.",
    "Chroma DB는 오픈 소스 임베딩 데이터베이스입니다.",
    "오늘 날씨가 매우 좋습니다.",
    "인공지능 기술은 빠르게 발전하고 있습니다.",
    "저는 벡터 데이터베이스에 대해 배우고 있습니다."
]
metadatas = [
    {"source": "city", "language": "ko"},
    {"source": "database", "language": "ko"},
    {"source": "weather", "language": "ko"},
    {"source": "AI", "language": "ko"},
    {"source": "database", "language": "ko"}
]
ids = [f"doc{i+1}" for i in range(len(documents))]


# 6. 데이터 추가 (Chroma가 임베딩 함수 사용하여 임베딩 자동 생성 및 저장)
print(f"'{collection_name}' 컬렉션에 데이터 추가 중...")

# embeddings=... 를 따로 제공하지 않습니다. 설정된 embedding_function이 자동으로 처리합니다.
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
print(f"'{collection_name}' 컬렉션에 데이터 {len(documents)}개 추가 완료.")
print("현재 컬렉션 아이템 수:", collection.count())


# 7. 유사도 검색 실행
# 검색 텍스트에 대한 임베딩도 설정된 embedding_function이 자동으로 생성합니다.
query_text = "한국의 수도에 대해 알려줘"

print(f"\n검색 텍스트: '{query_text}'")
# query() 메소드 호출 시 임베딩 함수가 검색 텍스트를 임베딩합니다.
results = collection.query(
    query_texts=[query_text],
    n_results=2, # 가장 유사한 결과 2개 요청
    include=['documents', 'metadatas', 'distances'] # 반환할 정보 지정
)

print("\n검색 결과:")
# 결과는 리스트 내 리스트 형태로 반환될 수 있습니다.
# 예시: ids, documents, metadatas, distances 등 키로 접근
print("IDs:", results.get('ids'))
print("Documents:", results.get('documents'))
print("Metadatas:", results.get('metadatas'))
print("Distances:", results.get('distances'))
