"""
RunnableParallel-并行链

在 Langchain 中，创建并行链（Parallel Chains），是指同时运行多个子链（Chain），并在它们都完成后汇总结果。
**作用**：同时执行多个 Runnable，合并结果
"""
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
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

# 并行链1提示词
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
# 并行链1解析器
parser1 = StrOutputParser()
# 并行链1：生成中文结果
chain1 = prompt1 | model | parser1

# 并行链2提示词
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
# 并行链2解析器
parser2 = StrOutputParser()

# 并行链2：生成英文结果
chain2 = prompt2 | model | parser2

# 创建并行链,用于同时执行多个语言处理链
parallel_chain = RunnableParallel({
    "chinese": chain1,
    "english": chain2
})

# 调用复合链
result = parallel_chain.invoke({"topic": "langchain"})
logger.info(result)

# 打印并行链的ASCII图形表示，LangGraph提前预告，不是本节知识点
parallel_chain.get_graph().print_ascii()


"""
2026-04-11 17:27:44.823 | INFO     | __main__:<module>:52 - {'chinese': 'LangChain是一个用于开发由大型语言模型驱动的应用程序的框架。它通过提供模块化组件和链式调用，简化了将LLM与外部数据源、工具和记忆系统集成的过程，从而构建更强大、可定制的AI应用。', 'english': 'LangChain is a framework for developing applications powered by language models. It simplifies the process of chaining together different components (like prompts, models, and data sources) to create complex, context-aware applications such as chatbots, agents, and retrieval-augmented generation (RAG) systems.'}
             +--------------------------------+              
             | Parallel<chinese,english>Input |              
             +--------------------------------+              
                   ****               ****                   
                ***                       ***                
              **                             **              
+--------------------+                +--------------------+ 
| ChatPromptTemplate |                | ChatPromptTemplate | 
+--------------------+                +--------------------+ 
           *                                     *           
           *                                     *           
           *                                     *           
   +--------------+                      +--------------+    
   | ChatDeepSeek |                      | ChatDeepSeek |    
   +--------------+                      +--------------+    
           *                                     *           
           *                                     *           
           *                                     *           
  +-----------------+                   +-----------------+  
  | StrOutputParser |                   | StrOutputParser |  
  +-----------------+                   +-----------------+  
                   ****               ****                   
                       ***         ***                       
                          **     **                          
            +---------------------------------+              
            | Parallel<chinese,english>Output |              
            +---------------------------------+  
"""
