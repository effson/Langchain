from langchain.chat_models  import  init_chat_model
import os

from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

prompt_template = """
    请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，
    如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。
    文本内容：
    {context}
    问题：{question}
    回答：
    "
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3", 
    dashscope_api_key=os.getenv("aliQwen-api")
)

loader = Docx2txtLoader("java.docx")  
documents = loader.load()

# 5. 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
texts = text_splitter.split_documents(documents)

vector_store = Redis.from_documents(
    documents=texts,
    embedding=embeddings,
    redis_url="redis://localhost:16988",  # 替换为你的 Redis 地址
    index_name="java_index",  # 向量索引名称
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 8. 创建Runnable链
rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
)

# 9. 提问
# 如果没有rag，大模型是不知道答案的，或者胡乱回答
"""
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = llm.invoke("00000是什么意思")
print(response.content)
结果如下，没有解决问题：
"00000"的含义完全取决于它出现的**具体场景**。如果没有上下文，最直接的理解就是**“五个零”**。

以下是它在不同领域常见的几种含义：

### 1. 数值与逻辑含义
*   **无/空值：** 代表数量为零、什么都没有。在数学和逻辑中常作为起始点或基准线。
*   **占位符：** 在某些表格或数据录入中，如果某项暂时不知道如何填写，可能会填上 00000 作为占位。

### 2. 科技与编程
*   **默认密码/初始值：** 很多设备、路由器或软件出厂时的默认密码是 `000000` 或 `00000`（虽然为了安全现在大多已更改）。
*   **空指针/错误代码：** 在计算机编程中，有时会返回全零来表示没有数据、未分配内存或操作成功（视具体系统定义而定）。
*   **二进制补码：** 在十六进制显示中，可能代表某个特定状态的空置。

### 3. 日常通讯与身份
*   **电话号码/区号：** 极少数情况下可能是内部短号、分机号，或者是某些测试号码。但在中国，手机号开头通常不是 0，且以 5 个 0 结尾的号码极不常见（不像 66666、88888 那样被视为靓号）。
*   **验证码：** 如果你是在接收短信验证码，收到一串 00000 可能是系统生成错误，或者这是某种特殊的防抖验证码（不推荐）。
*   **地址代码：** 在某些旧的系统数据库中，有时用全零表示地址不详。

### 4. 金融与银行
*   **银行卡余额：** 账户余额为 0，显示为 0.00 或类似格式。
*   **交易代码：** 某些特定的银行内部流水号可能包含此数字，但纯 00000 较为少见，除非是初始账号。

### 5. 彩票与抽奖
*   **模拟数据：** 在一些非官方的试算工具中，可能用于模拟中奖号码。
*   **未中奖：** 有时指代没有匹配的奖项。

### 6. 网络文化
*   **沉默/无语：** 类似于“..."，有时候用一串 0 代表无话可说（但这并不通用，更多见于特定圈子）。

---

### ⚠️ 重要提醒（安全性）
如果你是在以下场景看到"00000"，请提高警惕：
1.  **索要验证码：** 如果有人说给你发"00000"做验证码让你转账或授权，**这是诈骗**，请立即拒绝。
2.  **不明链接：** 如果网页或 App 登录界面提示输入"00000"，请务必核实该软件的真实性。
3.  **短信诈骗：** 发送含有乱码或重复数字的垃圾短信也是可能的，直接拉黑即可。

**总结：**
如果只是单纯的数学或代码符号，它就是**五个零**。如果是生活中遇到的陌生代码（尤其是涉及钱财或隐私），建议不要轻信，并确认来源是否可靠。

如果您能告诉我**在哪里看到的"00000"**（例如：手机短信、电影台词、电脑屏幕报错、还是朋友发的消息？），我可以为您提供更准确的解释。
"""

question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n问题:", question)
print("\n回答:", result.content)

"""
文档个数:1

问题: 00000和A0001分别是什么意思

回答: 根据提供的文本内容：
- **00000** 的中文描述是“一切 ok”，说明是“正确执行后的返回”。
- **A0001** 的中文描述是“用户端错误”，说明是“一级宏观错误码”。


127.0.0.1:6379> keys *
1) "for_rag:01KPB9JFCD0Y1AER7RMHPY1P50"
2) "doc:java_index:52490f55b9c84c2cbf3df126ba5706fa"
3) "for_rag:01KPB9JFCD0Y1AER7RMHPY1P4Z"
4) "doc:ebindex:3a10b291d48b49ffadae05748fc36b70"
5) "message_store:user-001"
6) "doc:ebindex:8bb54c2953eb4229a6771aa9700cfe02"
7) "for_rag:01KPB9JFCD0Y1AER7RMHPY1P51"
8) "doc:ebindex:8afd559d25304255a505f2f292988519"
127.0.0.1:6379> hgetall "doc:java_index:52490f55b9c84c2cbf3df126ba5706fa"
1) "content_vector"
2) "\xb6\xcc\xb8\xbd#\xf3\xb0\xbc\xad\x9c\xc2\xbd\xaf\x12\x99\xbc\xf1#\xfe\xbc\x88\xff\xd9\xbc\x83F$=@\x9b\...
3) "source"
4) "java.docx"
5) "content"
6) "Java\xe5\xbc\x80\xe5\x8f\x91\xe6\x89\x8b\xe5\x86\x8c\xef\xbc\x88\xe9\xbb\x84\xe5\xb1\xb1\xe7\x89\x88\xef\xbc\x89 \n\n \n\nJava\xe5\xbc\x80\...
127.0.0.1:6379>
"""
