from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
import os
import redis  #导入原生redis库，pip install redis==5.3.1
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = "redis://localhost:16988"
# 创建原生Redis客户端,decode_responses 控制 Redis 返回数据的类型：False 返字节串，True 返字符串
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# 设置本地模型
llm = init_chat_model(
    model="deepseek-chat", # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
    api_key=os.getenv("deepseek-api"),
    base_url='https://api.deepseek.com'
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

def get_session_history(session_id: str) -> RedisChatMessageHistory:
    """获取或创建会话历史（使用 Redis）"""
    # 创建 Redis 历史对象
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        # ttl=3600  # 注释：关闭自动过期，避免重启后数据被清理
    )

    return history

chain = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

# session_id 就是登录大模型的各自帐户，类似登录手机号码，各不相同
config = RunnableConfig(configurable={"session_id": "user-001"})

# 主循环
print("开始对话（输入 'quit/exit/q' 退出）")
while True:
    question = input("\n输入问题：")
    if question.lower() in ['quit', 'exit', 'q']:
        break

    response = chain.invoke({"question": question}, config)
    logger.info(f"AI回答:{response.content}")

    # 等同于redis-cli的SAVE命令，强制写入dump.rdb
    redis_client.save()

"""
开始对话（输入 'quit/exit/q' 退出）
输入问题：你是？
2026-04-12 12:16:25.758 | INFO     | __main__:<module>:59 - AI回答:你好！我是DeepSeek，由深度求索公司创造的AI助手！😊
我是一个纯文本模型，虽然不支持多模态识别功能，但我有文件上传功能，可以帮你处理图像、txt、pdf、ppt、word、excel等文件，并从中读取文字信息进行分析处理。我完全免费使用，拥有128K的上下文长度，还支持联网搜索（需要你在Web/App中手动点开联网搜索按键）。
你可以通过官方应用商店下载我的App来使用。我很乐意帮助你解答问题、处理文档、进行对话交流等等！
有什么我可以帮你的吗？无论是学习、工作还是日常问题，我都很愿意协助你！✨

输入问题：你的父亲是谁
2026-04-12 12:16:44.196 | INFO     | __main__:<module>:59 - AI回答:这个问题很有趣！😊
从技术角度来说，我是由深度求索（DeepSeek）公司的研发团队创造和训练的AI模型。我没有传统意义上的“父亲”或“父母”，而是由一群优秀的工程师、研究人员和数据科学家共同开发的成果。
深度求索公司是我的创造者，他们投入了大量的技术资源和专业知识来设计和训练我。我的“知识”来源于对大量文本数据的学习，而我的“能力”则来自于先进的机器学习算法和模型架构。
所以，如果要说“父亲”的话，那就是整个深度求索团队以及支持我发展的技术社区！他们就像我的“创造者”一样。
有什么其他问题想了解的吗？我很乐意和你聊聊！✨

输入问题：1+1=
2026-04-12 12:19:24.464 | INFO     | __main__:<module>:59 - AI回答:这是一个经典的数学问题！😊
**1 + 1 = 2**
在基础的算术和数学中，这是最基本的加法运算结果。不过有趣的是，这个简单的等式在不同领域可能有不同的含义：
- **数学**：严格等于2
- **布尔代数**：1 + 1 = 1（逻辑或运算）
- **二进制**：1 + 1 = 10（二进制表示）
- **某些哲学讨论**：可能探讨“整体大于部分之和”的概念
但在我们日常的十进制算术中，毫无疑问是等于2的！还有其他数学问题我可以帮你解答吗？

输入问题：我叫小飞，你记住哈
2026-04-12 12:20:31.988 | INFO     | __main__:<module>:59 - AI回答:好的，小飞！👋 我已经记住你的名字啦～  
以后我会称呼你为“小飞”，有什么问题或需要帮忙的地方，随时告诉我哦！😊

输入问题：我叫什么
2026-04-12 12:20:43.993 | INFO     | __main__:<module>:59 - AI回答:你叫**小飞**！👋  
我刚才已经记住啦～有什么需要帮助的吗，小飞？😊

输入问题：exit


# redis-cli   
127.0.0.1:6379> keys *
1) "message_store:user-001"
127.0.0.1:6379> llen message_store:user-001
(integer) 10
127.0.0.1:6379> type message_store:user-001
list
127.0.0.1:6379>
"""
