"""
Each document loader may define its own parameters, but they share a common API:
- load() – Loads all documents at once.
- lazy_load() – Streams documents lazily, useful for large datasets.
"""
from langchain_community.document_loaders import TextLoader

file_path = "assets/sample.txt"  # 文件路径
encoding = "utf-8"  # 文件编码方式

docs = TextLoader(file_path, encoding).load()
print(docs) # [Document(metadata={'source': 'assets/sample.txt'}, page_content='LangChain 是一个用于构建...')]
