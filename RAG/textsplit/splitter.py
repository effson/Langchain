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

chunk_size = 100
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap, 
        length_function=len
)
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

# splitter_documents = [Document(page_content=text) for text in splitter_texts]
# for idx, splitter_document in enumerate(splitter_documents, 1):
#     print(f"第{idx}个文档 - 大小：{len(splitter_document.page_content)}, 内容：{splitter_document.page_content}\n")
full_content = ""
for text in splitter_texts:
    if full_content:
        full_content += text[30:]  # 剔除重叠的30个字符后拼接
    else:
        full_content += text

print(f"拼接后文本大小：{len(full_content)}")
print(f"是否与原始文本完全一致：{full_content == content}")
print(f"拼接后完整内容：\n{full_content}")

"""
拼接后文本大小：225
是否与原始文本完全一致：True
拼接后完整内容：
大模型RAG（检索增强生成）是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，辅助生成模型以提升回答的准确性和相关性。其核心流程包括用
户输入查询、系统检索相关知识、生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区，提供更准确、实时和可解释的输出，广泛应用于
问答系统、内容生成、客服、教育和企业领域。然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。
"""


print("==========================================================================================")

# RecursiveCharacterTextSplitter不仅可以分割纯文本，还可以直接分割Document对象

loader = UnstructuredLoader("rag.txt")
documents = loader.load()

doc_text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30, length_function=len)
splitter_documents = doc_text_splitter.split_documents(documents)

print(f"分割文档数量：{len(splitter_documents)}")

for splitter_document in splitter_documents:
    print(f"文档片段：{splitter_document.page_content}")
    print(f"文档片段大小：{len(splitter_document.page_content)}, 文档元数据：{splitter_document.metadata}")

"""
分割文档数量：14
文档片段：《倚天屠龙记》是金庸“射雕三部曲”的终章，以元末乱世为背景，谱写了一曲江湖侠义与家国情怀交织的传奇。
文档片段大小：50, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': '2089ea66f6635c149a4ea8fda049b579'}
文档片段：小说核心围绕张无忌的成长轨迹展开，他本是武当弟子张翠山与天鹰教殷素素之子，自幼身中玄冥神掌，历经磨难却得奇遇，
文档片段大小：55, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': '391f965ee98ac9ace2fac0a7c04ce062'}
文档片段：先后习得九阳神功、乾坤大挪移、太极拳剑等绝世武功，从懵懂少年蜕变为号令群雄的明教教主。
文档片段大小：43, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': '6cb0cd75cba7ef7dcfa0f719eebdf5f0'}
文档片段：故事开篇以张三丰创立的武当派为引，张翠山与殷素素因屠龙刀相遇相知，却因正邪之分被迫自尽，年幼的张无忌流落江湖，
文档片段大小：55, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'a8598e5eba3b218cca5787c32571bdca'}
文档片段：尝尽人情冷暖。机缘巧合下，他在冰火岛长大，后重返中原，于昆仑山洞中习得九阳神功，化解寒毒，又在明教光明顶密室练就乾坤大挪移，
文档片段大小：62, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'eb6582fe294124a83a59424b531e93ad'}
文档片段：凭一己之力化解六大门派对明教的围剿，一战成名。
文档片段大小：23, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'aca752b6aa10b3d967d4e89b91c21f71'}
文档片段：书中最动人的，莫过于张无忌与赵敏、周芷若、小昭、蛛儿四位女子的情感纠葛。赵敏敢爱敢恨，为他舍弃郡主之位；
文档片段大小：52, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'd0c7326298fb54f5352eaba528dbf86f'}
文档片段：周芷若温柔隐忍，却因师门使命陷入挣扎；小昭乖巧忠诚，最终为救他远赴波斯。情与义的抉择，贯穿张无忌的江湖之路，也让人物更显鲜活。
文档片段大小：63, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': '2ad1eba5cb3c9475ac89f22547d6831d'}
文档片段：倚天剑与屠龙刀是贯穿全书的线索，“武林至尊，宝刀屠龙；号令天下，莫敢不从；倚天不出，谁与争锋”的传说，
文档片段大小：51, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'd861f8c83a4f27e2489d87a5859c4a71'}
文档片段：引发江湖数十年纷争。实则两柄兵器暗藏《武穆遗书》与《九阴真经》，承载着驱除元廷、还我河山的家国大义。
文档片段大小：50, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'b51294065f06fb70c51c440bf61af356'}
文档片段：张无忌最终揭开谜底，却不愿贪恋权势，将秘籍赠予有识之士，携手赵敏归隐江湖。
文档片段大小：37, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'bf004430752ebc89093b8a3ee64b412f'}
文档片段：小说既刻画了六大门派的恩怨情仇、明教内部的权力博弈，也折射出元末农民起义的动荡格局。
文档片段大小：42, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': 'e915bc9cc0484440aaac0c3886b183f3'}
文档片段：张三丰的道骨仙风、赵敏的飒爽果敢、周芷若的复杂人性，皆成为经典形象。金庸以细腻笔触，
文档片段大小：42, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': '493742297954f855ab8018f7305536c9'}
文档片段：在江湖侠义中融入对人性善恶、权力欲望的思考，让《倚天屠龙记》超越普通武侠小说的范畴，成为几代人心中的经典。
文档片段大小：53, 文档元数据：{'source': 'rag.txt', 'last_modified': '2026-04-16T15:18:25', 'languages': ['zho'], 'filename': 'rag.txt', 'filetype': 'text/plain', 'category': 'Title', 'element_id': '6b06e3b525cf73fbcad89d6b21b2c063'}
"""
