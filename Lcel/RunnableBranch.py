"""
分支链
LangChain提供类RunnableBranch完成LCEL条件分支判断，根据输入的不同采用不同的处理逻辑，
会根据用户输入选择对应的提示词进行处理。根据判断结果执行不同的逻辑分支
"""
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
from langchain_core.runnables import RunnableBranch
import os
from dotenv import load_dotenv

load_dotenv()

english_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个英语翻译专家，你叫小英"),
    ("human", "{query}")
])

japanese_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个日语翻译专家，你叫小日"),
    ("human", "{query}")
])

korean_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个韩语翻译专家，你叫小韩"),
    ("human", "{query}")
])

def determine_language(inputs):
    """判断语言种类"""
    query = inputs["query"]
    if "日语" in query:
        return "japanese"
    elif "韩语" in query:
        return "korean"
    else:
        return "english"

model = init_chat_model(
    model="deepseek-chat", # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
    api_key=os.getenv("deepseek-api"),
    base_url='https://api.deepseek.com'
)

# 创建字符串输出解析器
parser = StrOutputParser()

chain = RunnableBranch(
    (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
    (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
    (english_prompt | model | parser)
)

test_queries = [
    {'query': '请你用韩语翻译这句话:"见到你很高兴"'},
    {'query': '请你用日语翻译这句话:"见到你很高兴"'},
    {'query': '请你用英语翻译这句话:"见到你很高兴"'}
]

for query_input in test_queries:

    lang = determine_language(query_input)
    logger.info(f"检测到语言类型: {lang}")

    if lang == "japanese":
        chatPromptTemplate = japanese_prompt
    elif lang == "korean":
        chatPromptTemplate = korean_prompt
    else:
        chatPromptTemplate = english_prompt

    formatted_messages = chatPromptTemplate.format_messages(**query_input)
    logger.info("格式化后的提示词:")
    for msg in formatted_messages:
        logger.info(f"[{msg.type}]: {msg.content}")

    result = chain.invoke(query_input)
    logger.info(f"输出结果: {result}\n")
    
"""
2026-04-11 15:24:02.606 | INFO     | __main__:<module>:73 - 检测到语言类型: korean
2026-04-11 15:24:02.606 | INFO     | __main__:<module>:87 - 格式化后的提示词:
2026-04-11 15:24:02.606 | INFO     | __main__:<module>:89 - [system]: 你是一个韩语翻译专家，你叫小韩
2026-04-11 15:24:02.606 | INFO     | __main__:<module>:89 - [human]: 请你用韩语翻译这句话:"见到你很高兴"
2026-04-11 15:24:04.176 | INFO     | __main__:<module>:93 - 输出结果: "만나서 반갑습니다"

2026-04-11 15:24:04.176 | INFO     | __main__:<module>:73 - 检测到语言类型: japanese
2026-04-11 15:24:04.176 | INFO     | __main__:<module>:87 - 格式化后的提示词:
2026-04-11 15:24:04.176 | INFO     | __main__:<module>:89 - [system]: 你是一个日语翻译专家，你叫小日
2026-04-11 15:24:04.176 | INFO     | __main__:<module>:89 - [human]: 请你用日语翻译这句话:"见到你很高兴"
2026-04-11 15:24:05.897 | INFO     | __main__:<module>:93 - 输出结果: 「お会いできて嬉しいです。」

2026-04-11 15:24:05.897 | INFO     | __main__:<module>:73 - 检测到语言类型: english
2026-04-11 15:24:05.898 | INFO     | __main__:<module>:87 - 格式化后的提示词:
2026-04-11 15:24:05.898 | INFO     | __main__:<module>:89 - [system]: 你是一个英语翻译专家，你叫小英
2026-04-11 15:24:05.898 | INFO     | __main__:<module>:89 - [human]: 请你用英语翻译这句话:"见到你很高兴"
2026-04-11 15:24:07.355 | INFO     | __main__:<module>:93 - 输出结果: Nice to meet you.
"""
