"""
"placeholder" 是 ("placeholder", "{memory}") 的简写语法，
等价于 MessagesPlaceholder("memory")。

隐式使用MessagesPlaceholder
"""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 使用 ChatPromptTemplate 构建一个多角色对话提示模板
prompt1 = ChatPromptTemplate.from_messages([
    ("placeholder", "{memory}"),
    ("system", "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
    ("human", "{question}")
])

# 使用 invoke 方法传入上下文变量，生成格式化后的对话 prompt 内容
prompt1_value = prompt1.invoke({
    "memory": [
        # 用户第一轮对话
        HumanMessage("我的名字叫亮仔，是一名程序员"),
        # AI 第一轮回答
        AIMessage("好的，亮仔你好")
    ],

    "question": "请问我的名字叫什么？"
})
print(prompt1_value.to_string())



"""
如果我们不确定消息何时生成，也不确定要插入几条消息，比如在提示词中添加聊天历史记忆这种场景，
可以在ChatPromptTemplate添加MessagesPlaceholder占位符，在调用invoke时，在占位符处插入消息。

显式使用MessagesPlaceholder
"""
prompt2 = ChatPromptTemplate.from_messages([
    # 添加一条系统消息，设定 AI 的角色或行为准则
    ("system", "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
    # 插入 memory 占位符，用于填充历史对话记录（如多轮对话上下文）
    MessagesPlaceholder("memory"),
    # 添加一条用户问题消息，用变量 {question} 表示
    ("human", "{question}")
])

prompt2_value = prompt2.invoke({
    "memory": [
        HumanMessage("我的名字叫亮仔，是一名程序员111"),
        AIMessage("好的，亮仔你好222")
    ],
    "question": "请问我的名字叫什么？"
})

print(prompt2_value.to_string())
