"""
Each document loader may define its own parameters, but they share a common API:
- load() – Loads all documents at once.
- lazy_load() – Streams documents lazily, useful for large datasets.
"""
# pip install langchain_community pypdf
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader

file_path = "assets/sample.txt"  # 文件路径
encoding = "utf-8"  # 文件编码方式

txtdocs = TextLoader(file_path, encoding).load()
print(txtdocs) # [Document(metadata={'source': 'assets/sample.txt'}, page_content='LangChain 是一个用于构建...')]



pdfdocs = PyPDFLoader(
    # 文件路径，本地文件或在线文件链接，如"https://arxiv.org/pdf/alg-geom/9202012"
    file_path="assets/sample.pdf", 
    #  提取模式: plain 提取文本 layout 按布局提取
    extraction_mode="plain",
).load()
print(pdfdocs)

