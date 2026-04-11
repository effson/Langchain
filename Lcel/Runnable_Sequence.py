"""
顺序链
LangChain 的一个典型链条由Prompt、Model、OutputParser （可没有）组成，
然后可以通过 链（Chain） 把它们顺序组合起来，让一个任务的输出成为下一个任务的输入
"""
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

# 创建聊天提示模板，包含系统角色设定和用户问题输入
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我提出的问题"),
    ("human", "请回答:{question}")
])

prompt = chat_prompt.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
logger.info(prompt)

model = init_chat_model(
    model="deepseek-chat", # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
    api_key=os.getenv("deepseek-api"),
    base_url='https://api.deepseek.com'
)

result = model.invoke(prompt)
logger.info(f"********>模型原始输出:\n{result}")

# 字符串输出解析器
parser = StrOutputParser ()

# 解析模型输出为结构化结果并记录日志
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
# 记录解析结果的数据类型
logger.info(f"结果类型: {type(response)}")
print("*" * 60)


# 构建处理链：提示模板 -> 模型 -> 输出解析器
chain = chat_prompt | model | parser

# 执行处理链并记录最终结果及数据类型
result_chain = chain.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答200字以内"})
logger.info(f"Chain执行结果:\n {result_chain}")
logger.info(f"Chain执行结果类型: {type(result_chain)}")

print(type(chain))
