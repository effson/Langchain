"""
Each document loader may define its own parameters, but they share a common API:
- load() – Loads all documents at once.
- lazy_load() – Streams documents lazily, useful for large datasets.
"""
# pip install langchain_community pypdf unstructured markdown
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# TextLoader
file_path = "assets/sample.txt"  # 文件路径
encoding = "utf-8"  # 文件编码方式

txtdocs = TextLoader(file_path, encoding).load()
print(txtdocs) # [Document(metadata={'source': 'assets/sample.txt'}, page_content='LangChain 是一个用于构建...')]


# PyPDFLoader
pdfdocs = PyPDFLoader(
    # 文件路径，本地文件或在线文件链接，如"https://arxiv.org/pdf/alg-geom/9202012"
    file_path="assets/sample.pdf", 
    #  提取模式: plain 提取文本 layout 按布局提取
    extraction_mode="plain",
).load()
print(pdfdocs) 
"""
[
    Document(metadata={'producer': 'Microsoft® Word 2019', 'creator': 'Microsoft® Word 2019', 'creationdate': '2023-07-24T17:46:07+08:00', 'title': '中国科学院国家天文台2023年度部门预算', 'author': 'MC SYSTEM', 'moddate': '2023-07-24T17:46:07+08:00', 'source': 'assets/sample.pdf', 'total_pages': 36, 'page': 0, 'page_label': '1'}, 
             page_content='中国科学院国家天文台 \n2023 年部门预算'), 
    Document(metadata={'producer': 'Microsoft® Word 2019', 'creator': 'Microsoft® Word 2019', 'creationdate': '2023-07-24T17:46:07+08:00', 'title': '中国科学院国家天文台2023年度部门预算', 'author': 'MC SYSTEM', 'moddate': '2023-07-24T17:46:07+08:00', 'source': 'assets/sample.pdf', 'total_pages': 36, 'page': 1, 'page_label': '2'}, 
             page_content='目    录 \n一、中国科学院国家天文台基本情况 ..................................... 1 \n（一）单位职...'), 
    Document(metadata={'producer': 'Microsoft® Word 2019', 'creator': 'Microsoft® Word 2019', 'creationdate': '2023-07-24T17:46:07+08:00', 'title': '中国科学院国家天文台2023年度部门预算', 'author': 'MC SYSTEM', 'moddate': '2023-07-24T17:46:07+08:00', 'source': 'assets/sample.pdf', 'total_pages': 36, 'page': 2, 'page_label': '3'}, 
             page_content='（一）政府采购情况说明 .................................................. 21 \n（二）国有资产占有使用情...'), 
    ...
    
    Document(metadata={'producer': 'Microsoft® Word 2019', 'creator': 'Microsoft® Word 2019', 'creationdate': '2023-07-24T17:46:07+08:00', 'title': '中国科学院国家天文台2023年度部门预算', 'author': 'MC SYSTEM', 'moddate': '2023-07-24T17:46:07+08:00', 'source': 'assets/sample.pdf', 'total_pages': 36, 'page': 35, 'page_label': '36'}, 
             page_content='33 \n项目绩效目标表 \n \n(2023 年度)  \n项目名称 国家天文科学数据中心 \n主管部门及代码 [173]中国科学院 实施单...')
]
"""

mddocs = UnstructuredMarkdownLoader(
    file_path="assets/sample.md",
    # 加载模式: single 返回单个Document对象，  elements 按标题等元素切分文档
    mode="elements",
).load()
print(mddocs)
