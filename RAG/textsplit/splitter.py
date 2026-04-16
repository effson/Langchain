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
