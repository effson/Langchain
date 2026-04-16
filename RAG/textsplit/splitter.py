# pip install -U langchain-text-splitters langchain_unstructured python-magic-bin
"""
LangChain提供多种文本分割器（Text Splitters）：将长文本拆分为块（Chunks） -> 合并相邻块直到达到目标大小 -> 保持一定的重叠（Overlap）以防止上下文丢失
1. 递归字符分割器 (RecursiveCharacterTextSplitter): 最推荐的通用分割器。
- 策略：有一组默认的分隔符列表 ["\n\n", "\n", " ", ""],尝试按顺序拆分，直到块的大小合适
- 优点：尽可能保持段落、句子和单词的完整性。语义保留效果最好
- 适用场景：绝大多数通用文本、README、普通报告

2. Token 分割器 (TokenTextSplitter): 按 LLM 实际看到的 Token 数量切分

3. 字符分割器 CharacterTextSplitter ： 按指定字符切分
"""


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document

"""
split_text()方法进行文本分割
RecursiveCharacterTextSplitter中指定：
- chunk_size=100,块大小为100，
- chunk_overlap=30, 片段重叠字符数为30，
- length_function=len，计算长度的函数使用len，# 可选：默认为字符串长度，可自定义函数来实现按 token 数切分
"""
# 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30, length_function=len)
content = (
    "大模型RAG（检索增强生成）是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，"
    "辅助生成模型以提升回答的准确性和相关性。其核心流程包括用户输入查询、系统检索相关知识、"
    "生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区，"
    "提供更准确、实时和可解释的输出，广泛应用于问答系统、内容生成、客服、教育和企业领域。"
    "然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。")

splitter_texts = text_splitter.split_text(content)
# 将分割后的文本块转换为文档对象列表
splitter_documents = text_splitter.create_documents(splitter_texts)
print(f"原始文本大小：{len(content)}, 分割文档数量：{len(splitter_documents)}")
for splitter_document in splitter_documents:
    print(f"文档片段大小：{len(splitter_document.page_content)},文档内容：{splitter_document.page_content}")
"""
原始文本大小：225, 分割文档数量：3
文档片段大小：100,文档内容：大模型RAG（检索增强生成）是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，辅助生成模型以提升回答的准确性和相关性。其核心流程包括用户输入查询、系统检索相关知识、生成模
文档片段大小：100,文档内容：相关性。其核心流程包括用户输入查询、系统检索相关知识、生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区，提供更准确、实时和可解释的输出，广泛应用于问答系统、内容
文档片段大小：85,文档内容：区，提供更准确、实时和可解释的输出，广泛应用于问答系统、内容生成、客服、教育和企业领域。然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。
"""

# RecursiveCharacterTextSplitter不仅可以分割纯文本，还可以直接分割Document对象
