import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()
# 1. 初始化阿里千问 Embedding 模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=os.getenv("aliQwen-api")  # 从环境变量读取
)

texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis 是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。"
]
documents = [Document(page_content=text, metadata={"source": "manual"}) for text in texts]

# 3. 连接到 Redis 并存入向量（自动调用 embeddings 嵌入）
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url="redis://localhost:16988",
    index_name="ebindex",          # 向量索引名称
)

# 4. （可选）后续可直接用于检索
retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # 从Redis中找出 与提出的问题在语义上最接近的前2条记录
results = retriever.invoke("LangChain 和 Redis 怎么结合？")
for res in results:
    print(res.page_content)

"""
127.0.0.1:6379> keys *
1) "doc:ebindex:3a10b291d48b49ffadae05748fc36b70"
2) "doc:ebindex:8bb54c2953eb4229a6771aa9700cfe02"
3) "doc:ebindex:8afd559d25304255a505f2f292988519"
4) "message_store:user-001"
127.0.0.1:6379> type "doc:ebindex:3a10b291d48b49ffadae05748fc36b70"
hash
127.0.0.1:6379> hgetall "doc:ebindex:3a10b291d48b49ffadae05748fc36b70"
1) "content_vector"
2) "f\xae\xad\xbd\xb54\xd8<\xeb\x8c\xaf\xbd...
3) "source"
4) "manual"
5) "content"
6) "Redis \xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe9\xab\x98\xe6\x80\xa7\xe8\x83\xbd\xe7
\x9a\x84\xe9\x94\xae\xe5\x80\xbc\xe5\xad\x98\xe5\x82\xa8\xe7\xb3\xbb\xe7\xbb\x9f\xef\xbc
\x8c\xe6\x94\xaf\xe6\x8c\x81\xe5\x90\x91\xe9\x87\x8f\xe6\xa3\x80\xe7\xb4\xa2\xe3\x80\x82"
(Redis 是一个高性能的键值存储系统，支持向量检索。)
"""
