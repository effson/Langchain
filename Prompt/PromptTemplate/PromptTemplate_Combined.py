from langchain_core.prompts import PromptTemplate

# 组合方式 1:
template1 = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n") + "内容不超过{length}个字"
prompt1 = template1.format(topic="LangChain", length=100)

# 组合方式 2:
prompt_a = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n")
prompt_b = PromptTemplate.from_template("内容不超过{length}个字")

prompt_all = prompt_a + prompt_b
prompt2 = prompt_all.format(topic="LangChain", length=200)
