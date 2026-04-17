import json
import os
import httpx
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
'''
多工具并行调用,一次性发起了同一个外部函数的两次调用请求并将最后结果聚合
一次问题 → 多工具调用 → 聚合回答
'''


@tool
def get_weather(loc):
    """
    查询即时天气函数

    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
                则 loc 参数需要输入 'Beijing'/'shanghai'。
    :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
             https://api.openweathermap.org/data/2.5/weather。
             返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式进行表示，
             其中包含了全部重要的天气信息。
    """
    # Step 1. 构建请求 URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3. 发送 GET 请求获取天气数据
    response = httpx.get(url, params=params,timeout=30)

    # Step 4. 解析响应内容为 JSON 并序列化为字符串返回
    data = response.json()
    print(json.dumps(data))
    return json.dumps(data)


llm = ChatOpenAI(
    model="qwen3.5-flash",
    # 配置进环境变量
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# 创建聊天提示模板，定义agent的对话结构和角色
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是天气助手，请根据用户的问题，给出相应的天气信息"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 定义可用工具列表，包含获取天气信息的工具函数
tools = [get_weather]

# 创建工具调用agent，整合语言模型、工具和提示模板。该agent能够根据用户问题调用相应工具获取天气信息
agent = create_tool_calling_agent(llm, tools, prompt)

# 创建agent执行器，负责协调agent和工具的执行流程
# agent:指定要执行的agent实例 tools:提供agent可调用的工具列表 verbose:设置为True，启用详细输出模式便于调试
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行agent，处理用户关于北京和上海天气的查询请求
result = agent_executor.invoke({"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"})

# 输出执行结果
print(result)

"""


> Entering new AgentExecutor chain...

Invoking: `get_weather` with `{'loc': 'Beijing'}`


{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 800, "main": "Clear", "description": "\u6674", "icon": "01n"}], "base": "stations", "main": {"temp": 17.94, "feels_like": 16.81, "temp_min": 17.94, "temp_max": 17.94, "pressure": 1009, "humidity": 39, "sea_level": 1009, "grnd_level": 1006}, "visibility": 10000, "wind": {"speed": 3.09, "deg": 183, "gust": 7.08}, "clouds": {"all": 0}, "dt": 1776426001, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1776375259, "sunset": 1776423205}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}
{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 800, "main": "Clear", "description": "\u6674", "icon": "01n"}], "base": "stations", "main": {"temp": 17.94, "feels_like": 16.81, "temp_min": 17.94, "temp_max": 17.94, "pressure": 1009, "humidity": 39, "sea_level": 1009, "grnd_level": 1006}, "visibility": 10000, "wind": {"speed": 3.09, "deg": 183, "gust": 7.08}, "clouds": {"all": 0}, "dt": 1776426001, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1776375259, "sunset": 1776423205}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}
Invoking: `get_weather` with `{'loc': 'Shanghai'}`


{"coord": {"lon": 121.4581, "lat": 31.2222}, "weather": [{"id": 804, "main": "Clouds", "description": "\u9634\uff0c\u591a\u4e91", "icon": "04n"}], "base": "stations", "main": {"temp": 18.92, "feels_like": 18.75, "temp_min": 18.92, "temp_max": 18.92, "pressure": 1015, "humidity": 72, "sea_level": 1015, "grnd_level": 1014}, "visibility": 8000, "wind": {"speed": 3, "deg": 30}, "clouds": {"all": 100}, "dt": 1776426275, "sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1776374657, "sunset": 1776421379}, "timezone": 28800, "id": 1796236, "name": "Shanghai", "cod": 200}
{"coord": {"lon": 121.4581, "lat": 31.2222}, "weather": [{"id": 804, "main": "Clouds", "description": "\u9634\uff0c\u591a\u4e91", "icon": "04n"}], "base": "stations", "main": {"temp": 18.92, "feels_like": 18.75, "temp_min": 18.92, "temp_max": 18.92, "pressure": 1015, "humidity": 72, "sea_level": 1015, "grnd_level": 1014}, "visibility": 8000, "wind": {"speed": 3, "deg": 30}, "clouds": {"all": 100}, "dt": 1776426275, "sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1776374657, "sunset": 1776421379}, "timezone": 28800, "id": 1796236, "name": "Shanghai", "cod": 200}根据您查询的结果：

*   **北京**：天气晴朗，气温约为 **17.94°C**。
*   **上海**：多云，气温约为 **18.92°C**。

比较这两个城市，今天的 **上海比北京稍微更热一些**（相差约1°C）。

> Finished chain.
{'input': '请问今天北京和上海的天气怎么样，哪个城市更热？', 'output': '根据您查询的结果：\n\n*   **北京**：天气晴朗，气温约为 **17.94°C**。\n*   **上海**：多云，气温约为 **18.92°C**。\n\n比较这两个城市，今天的 **上海比北京稍微更热一些**（相差约1°C）。'}

"""
