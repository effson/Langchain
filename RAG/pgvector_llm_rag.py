import os

from langchain.chat_models  import  init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector

from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
COLLECTION_NAME = "java_index" # 与Redis的index_name一样

"""
docker run --name pgvector-container `
-e POSTGRES_USER=langchain `
-e POSTGRES_PASSWORD=langchain `
-e POSTGRES_DB=langchain `
-p 6024:5432 `
-d pgvector/pgvector:0.8.2-pg16-trixie
892991beab094d45ca26dd405ef4f9e17907b11bfe189b2ad6227ed318d649c8
"""

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

loader = Docx2txtLoader("java.docx")
documents = loader.load()

# 5. 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
texts = text_splitter.split_documents(documents)

vector_store = PGVector.from_documents(
    documents=texts,
    embedding=embeddingsModel,
    connection=CONNECTION_STRING,
    collection_name=COLLECTION_NAME,
    collection_metadata="java_errcode 参考",
    use_jsonb=True, # 建议开启，这样 metadata 会以 jsonb 格式存储，查询更快
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

# 9. 提问
question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n问题:", question)
print("\n回答:", result.content)

"""
问题: 00000和A0001分别是什么意思

回答: 根据提供的文本内容：

*   **00000**：中文描述为“一切 ok”，说明为“正确执行后的返回”。
*   **A0001**：中文描述为“用户端错误”，说明为“一级宏观错误码”。

# psql -U langchain -d langchain
psql (16.13 (Debian 16.13-1.pgdg13+1))
Type "help" for help.

langchain=# \dt
                  List of relations
 Schema |          Name           | Type  |   Owner   
--------+-------------------------+-------+-----------
 public | langchain_pg_collection | table | langchain
 public | langchain_pg_embedding  | table | langchain
(2 rows)

langchain=# SELECT document, cmetadata FROM langchain_pg_embedding LIMIT 5;
langchain=# \d langchain_pg_embedding
               Table "public.langchain_pg_embedding"
    Column     |       Type        | Collation | Nullable | Default 
---------------+-------------------+-----------+----------+---------
 id            | character varying |           | not null | 
 collection_id | uuid              |           |          | 
 embedding     | vector            |           |          | 
 document      | character varying |           |          | 
 cmetadata     | jsonb             |           |          | 
Indexes:
    "langchain_pg_embedding_pkey" PRIMARY KEY, btree (id)
    "ix_cmetadata_gin" gin (cmetadata jsonb_path_ops)
Foreign-key constraints:
    "langchain_pg_embedding_collection_id_fkey" FOREIGN KEY (collection_id) REFERENCES langchain_pg_collection(uuid) ON DELETE CASCADE

langchain=# SELECT count(*) FROM langchain_pg_embedding;
 count 
-------
     1
(1 row)

langchain=# SELECT * FROM langchain_pg_collection;
                 uuid                 |    name    |          cmetadata          
--------------------------------------+------------+-----------------------------
 86e215ba-fdce-4724-b3f0-48ea21b3cfa5 | java_index | "java_errcode \u53c2\u8003"
(1 row)
"""
