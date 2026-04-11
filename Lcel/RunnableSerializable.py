"""
RunnableSerializable-串行链
子链叠加串行，假如我们需要多次调用大模型，将多个步骤串联起来实现功能
"""
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="deepseek-chat", # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
    api_key=os.getenv("deepseek-api"),
    base_url='https://api.deepseek.com'
)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])

parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

result1 = chain1.invoke({"topic": "langchain"})
logger.info(result1)


prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，将用户输入内容翻译成英文"),
    ("human", "{input}")
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2


# 组合成一个复合 Chain，使用 lambda 函数将chain1执行结果content内容添加input键作为参数传递给chain2
full_chain = chain1 | (lambda content: {"input": content}) | chain2

result = full_chain.invoke({"topic": "langchain"})
logger.info(result)

"""
2026-04-11 15:43:18.327 | INFO     | __main__:<module>:30 - LangChain是一个用于开发基于大型语言模型（LLM）应用程序的开源框架。它通过提供模块化组件和链式调用，简化了LLM与外部数据源、工具和记忆系统的集成，使开发者能够高效构建复杂的AI应用，如智能问答、文档分析和对话系统。
2026-04-11 15:43:24.094 | INFO     | __main__:<module>:45 - LangChain is a framework designed for developing applications powered by language models. It simplifies the process of integrating large language models (such as GPT-4) with external data sources, tools, and memory systems by offering modular components and chain-based calls, thereby enabling the creation of more powerful and complex applications.
"""
