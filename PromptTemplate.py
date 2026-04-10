import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from datetime import datetime
import time

# =======  方式1：使用构造方法实例化提示词模板
# 创建一个PromptTemplate对象，用于生成格式化的提示词模板，该模板包含两个变量：role（角色）和question（问题）

template1 = PromptTemplate(
    template="你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}",
    input_variables=['role', 'question']
)

prompt1 = template1.format(role="你希望的角色",question="你想问的问题")




# =======  方式2：使用 from_template 方法实例化提示词模板
template2 = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
# 使用指定的角色和问题参数来格式化模板，生成最终的提示词字符串
prompt2 = template2.format(role="python开发",question="快速排序怎么写？")




# =======  方式3：部分提示词模板(partial_variables),实例化过程中指定 partial_variables 参数

# -->  1 实例化过程中指定 partial_variables 参数
# 创建一个包含时间变量的模板，时间变量使用partial_variables预设为当前时间
template3 = PromptTemplate.from_template(
    "时间：{time},请对我的问题给出答案，我的问题是：{question}",
    partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
)
prompt3 = template3.format(question="今天是几号？")

# -->  2 使用 partial 方法指定默认值
template4 = PromptTemplate.from_template("现在时间是：{time},请对我的问题给出答案，我的问题是：{question}")
# 使用 partial 方法指定默认值
partial = template4.partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
prompt4 = partial.format(question="今天是几号？")

template3 = PromptTemplate(
    template="{foo} {bar}",
    input_variables=["foo", "bar"],
    partial_variables={"foo": "hello"},  # 预先定义部分变量foo值为hello
)

prompt = template3.format(foo="li4",bar="world")
print(prompt)  # li4 world

prompt = template3.format(bar="world")
print(prompt)  # hello world
