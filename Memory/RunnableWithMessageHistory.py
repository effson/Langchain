"""
可持续记忆（RunnableWithMessageHistory）
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()
llm = init_chat_model(
    model="deepseek-chat", # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
    api_key=os.getenv("deepseek-api"),
    base_url='https://api.deepseek.com'
)

prompt = ChatPromptTemplate.from_messages([
    # 用于插入历史消息
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
parser = StrOutputParser()
chain = prompt | llm | parser


history = InMemoryChatMessageHistory()
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,
    input_messages_key="input",  # 指定输入键
    history_messages_key="history"  # 指定历史消息键
)
history.clear()
config = RunnableConfig(configurable={"session_id": "user-001"})

logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))

"""
2026-04-11 22:30:28.112 | INFO     | __main__:<module>:46 - 张三你好！很高兴认识你！热爱学习是一个非常棒的习惯，它能不断为你打开新的世界，带来成长和乐趣。😊

不知道你最近在学习什么领域的内容呢？或者有什么特别感兴趣的方向？无论是学科知识、技能提升，还是兴趣爱好相关的学习，都可以和我分享哦～ 如果你有任何问题或需要学习资源推荐，我也很乐意帮忙！一起加油吧！ 📚✨
2026-04-11 22:30:30.272 | INFO     | __main__:<module>:47 - 你叫**张三**，你的爱好是**学习**。 😊  
"""
