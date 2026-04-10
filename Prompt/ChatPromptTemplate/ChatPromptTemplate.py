"""
函数 ：from_messages
模板变量替换后，直接生成消息列表（List[BaseMessage]），
包含：SystemMessage``HumanMessage``AIMessage
常用场景：用于手动查看或调试 Prompt 的最终“消息结构”或者自己拼接进 Chain。

实例化需传入 ---> messages: Sequence[MessageLikeRepresentation]

messages 参数支持如下格式：
->	tuple 构成的列表，格式为[(role, content)]
template = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}。"),
        ("human", "你能帮我做什么?"),
        ("ai", "我能开发很多{thing}。"),
        ("human", "{user_input}"),
    ]
)
->	dict 构成的列表，格式为[{“role”:... , “content”:...}]
chat_prompt = ChatPromptTemplate(
    [
        {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
        {"role": "user", "content": "请问：{question}"}
    ]
)
->	Message 类构成的列表
"""

import os
from typing import List

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate


chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，请回答我提出的问题"),
        ("human", "请回答:{question}")
    ]
)

# -- 返回值: 格式化后的消息列表
# -- prompt_value = chat_prompt.format_messages(role="python开发工程师", question="冒泡排序怎么写")
prompt_value = chat_prompt.format_messages(**{"role": "python开发工程师", "question": "堆排序怎么写"})
print(prompt_value)
"""
[
      SystemMessage(content='你是一个python开发工程师，请回答我提出的问题', additional_kwargs={}, response_metadata={}), 
      HumanMessage(content='请回答:堆排序怎么写', additional_kwargs={}, response_metadata={})
]
"""

prompt_value2 = chat_prompt.invoke({"role": "python开发工程师", "question": "堆排序怎么写"})
print(prompt_value2.to_string())
"""
System: 你是一个python开发工程师，请回答我提出的问题
Human: 请回答:堆排序怎么写
"""


prompt_value3 = chat_prompt.format(**{"role": "python开发工程师", "question": "快速排序怎么写"})
"""
System: 你是一个python开发工程师，请回答我提出的问题
Human: 请回答:堆排序怎么写
"""
