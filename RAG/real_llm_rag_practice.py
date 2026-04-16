from langchain.chat_models  import  init_chat_model
import os

from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
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

loader = Docx2txtLoader("java.docx")  
documents = loader.load()

# 5. 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
texts = text_splitter.split_documents(documents)

vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url="redis://localhost:16988",  # 替换为你的 Redis 地址
    index_name="java_index",  # 向量索引名称
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 8. 创建Runnable链
rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
)

# 9. 提问
# 如果没有rag，大模型是不知道答案的，或者胡乱回答
question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n问题:", question)
print("\n回答:", result.content)

"""
文档个数:1

问题: 00000和A0001分别是什么意思

回答: 根据提供的文本内容：
- **00000** 的中文描述是“一切 ok”，说明是“正确执行后的返回”。
- **A0001** 的中文描述是“用户端错误”，说明是“一级宏观错误码”。


127.0.0.1:6379> keys *
1) "for_rag:01KPB9JFCD0Y1AER7RMHPY1P50"
2) "doc:java_index:52490f55b9c84c2cbf3df126ba5706fa"
3) "for_rag:01KPB9JFCD0Y1AER7RMHPY1P4Z"
4) "doc:ebindex:3a10b291d48b49ffadae05748fc36b70"
5) "message_store:user-001"
6) "doc:ebindex:8bb54c2953eb4229a6771aa9700cfe02"
7) "for_rag:01KPB9JFCD0Y1AER7RMHPY1P51"
8) "doc:ebindex:8afd559d25304255a505f2f292988519"
127.0.0.1:6379> hgetall "doc:java_index:52490f55b9c84c2cbf3df126ba5706fa"
1) "content_vector"
2) "\xb6\xcc\xb8\xbd#\xf3\xb0\xbc\xad\x9c\xc2\xbd\xaf\x12\x99\xbc\xf1#\xfe\xbc\x88\xff\xd9\xbc\x83F$=@\x9b\...
3) "source"
4) "java.docx"
5) "content"
6) "Java\xe5\xbc\x80\xe5\x8f\x91\xe6\x89\x8b\xe5\x86\x8c\xef\xbc\x88\xe9\xbb\x84\xe5\xb1\xb1\xe7\x89\x88\xef\xbc\x89 \n\n \n\nJava\xe5\xbc\x80\...
127.0.0.1:6379>
"""
