from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=os.getenv("aliQwen-api")  # 从环境变量读取
)

vector_store = RedisVectorStore(embeddingsModel, config=RedisConfig(index_name="for_rag",redis_url="redis://localhost:16988"))

query = "我喜欢用什么手机"

results = vector_store.similarity_search_with_score(query, k=3) # top 3

print("=== 查询结果 ===")
for i, (doc, score) in enumerate(results, 1):
    similarity = 1 - score  #  score 是距离，可以转成相似度
    print(f"结果 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"相似度: {similarity:.4f}")
"""
=== 查询结果 ===
结果 1:
内容: 我喜欢用苹果手机
元数据: {'segment_id': '3'}
相似度: 0.8594
结果 2:
内容: 我喜欢吃苹果
元数据: {'segment_id': '1'}
相似度: 0.6610
结果 3:
内容: 苹果是我最喜欢吃的水果
元数据: {'segment_id': '2'}
相似度: 0.6227
"""
