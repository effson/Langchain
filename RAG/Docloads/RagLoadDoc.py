"""
Each document loader may define its own parameters, but they share a common API:
- load() – Loads all documents at once.
- lazy_load() – Streams documents lazily, useful for large datasets.
"""
# pip install langchain_community pypdf unstructured markdown jq docx python-docx regex
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import JSONLoader

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



# UnstructuredMarkdownLoader
mddocs = UnstructuredMarkdownLoader(
    file_path="assets/sample.md",
    # 加载模式: single 返回单个Document对象，  elements 按标题等元素切分文档
    mode="elements",
).load()
print(mddocs)
"""
[
    Document(metadata={'source': 'assets/sample.md', 'category_depth': 0, 'languages': ['ron'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-04-16T15:18:25', 'category': 'Title', 'element_id': 'e6a3b421f39f298fffbc3cf1b3b95817'}, 
             page_content='投机解码（Speculative Decoding）介绍'), 
    Document(metadata={'source': 'assets/sample.md', 'category_depth': 1, 'languages': ['kor'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-04-16T15:18:25', 'parent_id': 'e6a3b421f39f298fffbc3cf1b3b95817', 'category': 'Title', 'element_id': '3a77bcc407e48690734a4701557ffdb6'}, 
             page_content='引言'), 
    Document(metadata={'source': 'assets/sample.md', 'languages': ['nor', 'vie', 'zho'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-04-16T15:18:25', 'parent_id': '3a77bcc407e48690734a4701557ffdb6', 'category': 'UncategorizedText', 'element_id': '5a9685df7e44c7f338356ef37bc09149'}, 
             page_content='投机解码（Speculative Decoding）是一种先进的推理优化技术，用于加速大型语言模型（Large Language Mode...'), 
    ...
    
    Document(metadata={'source': 'assets/sample.md', 'category_depth': 1, 'emphasized_text_contents': ['批处理限制'], 'emphasized_text_tags': ['b'], 'languages': ['zho', 'kor'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-04-16T15:18:25', 'parent_id': 'd72ff07d51983a0a0ea519205c1e657f', 'category': 'ListItem', 'element_id': '3b15777bd1bb8982f45716a676152789'}, 
             page_content='批处理限制：标准实现不支持高吞吐批处理。'), 
    Document(metadata={'source': 'assets/sample.md', 'category_depth': 1, 'emphasized_text_contents': ['不适合短序列'], 'emphasized_text_tags': ['b'], 'languages': ['zho'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-04-16T15:18:25', 'parent_id': 'd72ff07d51983a0a0ea519205c1e657f', 'category': 'ListItem', 'element_id': '329bfa4b74a6503d7c42d33f55a6d16c'}, 
             page_content='不适合短序列：在极短生成中收益有限。')
]
"""



# JSONLoader
jsondocs = JSONLoader(
    file_path="assets/sample.json",  # 文件路径
    jq_schema=".",  # 提取所有字段
    text_content=False,  # 提取内容是否为字符串格式
).load()
print(jsondocs)
"""
[
    Document(metadata={'source': 'C:\\Users\\Mechrev\\Desktop\\Langchain\\rag\\docloads\\assets\\sample.json', 'seq_num': 1}, 
             page_content='{"status": "success", "data": {"page": 2, "per_page": 3, "total_pa...')
]
"""



# UnstructuredWordDocumentLoader
worddocs = UnstructuredWordDocumentLoader(
    file_path="assets/alibaba-more.docx",
    # 加载模式: single 返回单个Document对象, elements 按标题等元素切分文档
    mode="single",
).load()
print(worddocs)
"""
[
    Document(metadata={'source': 'assets/alibaba-more.docx'}, 
             page_content='Java开发手册（黄山版）\n\nJava开发手册（黄山版）\n\n前言 \n\n《Java 开发手册》是阿里巴...')
]
"""
