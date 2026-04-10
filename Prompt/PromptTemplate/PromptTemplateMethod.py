from langchain_core.prompts import PromptTemplate

# =============== 1.format函数 ===============
template1 = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
prompt1 = template1.format(role="python开发",question="二分查找算法怎么写？")

# 输出生成的提示词
print(prompt1) # 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：二分查找算法怎么写？
print(type(prompt1))  # <class 'str'>



# =============== 2.invoke函数 ===============
"""
invoke() 是 LangChain Expression Language（LCEL 的统一执行入口，用于执行任意可运行对象（Runnable ）。返回的是一个 PromptValue 对象，
可以用 .to_string() 或 .to_messages() 查看内容
"""
template2 = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")

# 使用invoke方法填充模板中的占位符，生成具体的提示词， 参数：字典类型，包含role和question两个键值对
# 返回值：PromptValue对象，包含了格式化后的提示词
prompt2 = template2.invoke({"role": "python开发", "question": "冒泡排序怎么写？"})
print(prompt2) # text='你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？'
print(type(prompt2)) # <class 'langchain_core.prompt_values.StringPromptValue'>

# to_string()方法将PromptValue转换为可读的字符串格式
print(prompt2.to_string()) # 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？
print(type(prompt2.to_string())) # <class 'str'>

print(prompt2.to_messages()) 
# [HumanMessage(content='你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？', additional_kwargs={}, response_metadata={})]
print(type(prompt2.to_messages())) # <class 'list'>



# =============== 3.partial函数 ===============
"""
partial()方法可以格式化部分变量，并且继续返回一个模板，通常在部分提示词模板场景下使用
"""
# 创建模板对象，定义提示词模板格式
# 模板包含两个占位符：role（角色）和 question（问题）
template3 = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")
partial = template3.partial(role="python开发")

print(partial) 
# input_variables=['question'] input_types={} partial_variables={'role': 'python开发'} template='你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}'
print(type(partial)) # <class 'langchain_core.prompts.prompt.PromptTemplate'>

prompt3 = partial.format(question="冒泡排序怎么写？")
print(prompt3) # 你是一个专业的python开发工程师，请回答我的问题给出回答，我的问题是：冒泡排序怎么写？
print(type(prompt3)) # <class 'str'>
