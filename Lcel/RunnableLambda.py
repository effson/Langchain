"""
RunnableLambda-函数链
将普通Python函数融入Runnable流程.
"""
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()
model = init_chat_model(
    model="deepseek-chat", # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
    api_key=os.getenv("deepseek-api"),
    temperature=0.0,
    base_url='https://api.deepseek.com'
)

def debug_print(x):
    logger.info(f"中间结果:{x}")
    return {"input": x}

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
parser1 = StrOutputParser()
# 子链1：生成内容
chain1 = prompt1 | model | parser1

# 子链2提示词
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，将用户输入内容翻译成英文"),
    ("human", "{input}")
])
parser2 = StrOutputParser()


chain2 = prompt2 | model | parser2
debug_node = RunnableLambda(debug_print)

full_chain = chain1 | debug_print | chain2

# 调用复合链
result1 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果111:{result1}")

full_chain = chain1 | debug_node | chain2

result2 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果222:{result2}")

"""
2026-04-11 17:35:33.822 | INFO     | __main__:debug_print:23 - 中间结果:LangChain是一个用于开发由大型语言模型驱动的应用程序的框架。它通过提供模块化组件和链式调用，简化了构建复杂应用（如问答系统、聊天机器人等）的过程，并支持与外部数据源和工具集成。
2026-04-11 17:35:36.660 | INFO     | __main__:<module>:49 - 最终结果111:LangChain is a framework designed for developing applications powered by large language models. It simplifies the process of building complex applications, such as question-answering systems and chatbots, by offering modular components and chain-based calls. Additionally, it supports integration with external data sources and tools.
2026-04-11 17:35:39.517 | INFO     | __main__:debug_print:23 - 中间结果:LangChain是一个用于开发由大型语言模型驱动的应用程序的框架。它通过提供模块化组件和链式调用，简化了构建复杂应用（如问答系统、聊天机器人等）的过程，并支持与外部数据源和工具集成。
2026-04-11 17:35:42.233 | INFO     | __main__:<module>:54 - 最终结果222:LangChain is a framework designed for developing applications powered by large language models. It simplifies the process of building complex applications, such as question-answering systems and chatbots, by offering modular components and chain-based calls. Additionally, it supports integration with external data sources and tools.
"""
