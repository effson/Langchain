import os

from langchain.chat_models  import  init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector

from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
COLLECTION_NAME = "java_index"

llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

prompt_template = """
    请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，
    如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。
    文本内容：
    {context}
    问题：{question}
    回答：
    "
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("aliQwen-api")
)

vector_store = PGVector(
    connection=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
    embeddings=embeddingsModel,  # embeddings给查询使用
)

retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2})
rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
)

question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n问题:", question)
print("\n回答:", result.content)
"""
问题: 00000和A0001分别是什么意思

回答: 根据提供的文本信息：

*   **00000**：中文描述为“一切 ok”，说明为“正确执行后的返回”。
*   **A0001**：中文描述为“用户端错误”，说明为“一级宏观错误码”。
"""
