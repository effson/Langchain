import os
import json
import httpx
from typing import TypedDict

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 1.Tool 定义
@tool
def get_weather(loc: str) -> dict:
    """
    查询即时天气函数

    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
                则 loc 参数需要输入 'Beijing'/'shanghai'。
    :return: OpenWeather API 查询即时天气的结果。
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
        "lang": "zh_cn"
    }
    response = httpx.get(url, params=params, timeout=30)
    data = response.json()
    #print(json.dumps(data, ensure_ascii=False, indent=2))
    return json.dumps(data, ensure_ascii=False)



# 2 结构化输出（推荐）
class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str


# 3 模型（OpenAI Compatible）
model = ChatOpenAI(
    model="qwen-plus",
    # 配置进环境变量
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 4 创建Agent
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=(
        "你是天气助手。"
        "当用户询问多个城市天气时，"
        "你需要分别调用工具获取数据，并进行比较分析。"
    ),
    response_format=WeatherCompareOutput,
)

# 5 调用Agent
result = agent.invoke(
    {"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"}
)
print(result)

print()

print(json.dumps(result["structured_response"], ensure_ascii=False, indent=2))

"""
{'messages': [AIMessage(content='', additional_kwargs={'refusal': None}, 
response_metadata={'token_usage': {'completion_tokens': 38, 'prompt_tokens': 339, 'total_tokens': 377, 'completion_tokens_details': None,
'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'qwen-plus', 
'system_fingerprint': None, 'id': 'chatcmpl-4de72acc-9ef9-96be-b03a-37712554a920', 'finish_reason': 'tool_calls', 'logprobs': None}, 
id='lc_run--019d9bb6-dd81-72e3-ae3a-e49305e094f0-0', 
tool_calls=[
  {'name': 'get_weather', 'args': {'loc': 'Beijing'}, 'id': 'call_60b227ead9ef498abbeefa', 'type': 'tool_call'}, 
  {'name': 'get_weather', 'args': {'loc': 'Shanghai'}, 'id': 'call_dd88f5bfed2f49c99a3d24', 'type': 'tool_call'}], 
invalid_tool_calls=[], usage_metadata={'input_tokens': 339, 'output_tokens': 38, 'total_tokens': 377, 'input_token_details': {'cache_read': 0}, 
'output_token_details': {}}), ToolMessage(content='{"coord": {"lon": 116.3972, "lat": 39.9075}, 
"weather": [
  {"id": 800, "main": "Clear", "description": "晴", "icon": "01n"}
  ], 
"base": "stations", "main": {"temp": 15.94, "feels_like": 14.87, "temp_min": 15.94, "temp_max": 15.94, "pressure": 1011, "humidity": 49, "sea_level": 1011, "grnd_level": 1006}, 
"visibility": 10000, "wind": {"speed": 2.18, "deg": 168, "gust": 4.48}, "clouds": {"all": 6}, "dt": 1776433194, 
"sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1776375259, "sunset": 1776423205}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}', 
name='get_weather', id='7d45a082-3ade-419b-854d-b243e53f7db9', tool_call_id='call_60b227ead9ef498abbeefa'), ToolMessage(content='{"coord": {"lon": 121.4581, "lat": 31.2222}, 
"weather": [{"id": 802, "main": "Clouds", "description": "多云", "icon": "03n"}], "base": "stations", 
"main": {"temp": 17.92, "feels_like": 17.78, "temp_min": 17.92, "temp_max": 17.92, "pressure": 1016, "humidity": 77, 
"sea_level": 1016, "grnd_level": 1015}, "visibility": 10000, "wind": {"speed": 4, "deg": 30}, "clouds": {"all": 40}, "dt": 1776433921, 
"sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1776374657, "sunset": 1776421379}, "timezone": 28800, "id": 1796236, 
"name": "Shanghai", "cod": 200}', name='get_weather', id='811e8910-d05c-4dc3-a9ca-1f4409c9ae5f', tool_call_id='call_dd88f5bfed2f49c99a3d24'), 
AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 70, 'prompt_tokens': 1002, 
'total_tokens': 1072, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 
'model_provider': 'openai', 'model_name': 'qwen-plus', 'system_fingerprint': None, 'id': 'chatcmpl-a3e972e4-131d-99ac-a0af-b714ce0c0872', 
'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--019d9bb6-eb8c-7cf2-999c-bf1604170fb4-0', 
tool_calls=[{'name': 'WeatherCompareOutput', 'args': {'beijing_temp': 15.94, 'shanghai_temp': 17.92, 'hotter_city': 'Shanghai', 
'summary': '上海比北京温度高约1.98°C，北京天气晴朗，上海多云。'}, 'id': 'call_7857ec7fc9324aeba46115', 'type': 'tool_call'}], 
invalid_tool_calls=[], usage_metadata={'input_tokens': 1002, 'output_tokens': 70, 'total_tokens': 1072, 'input_token_details': {'cache_read': 0}, 
'output_token_details': {}}), ToolMessage(content="Returning structured response: {'beijing_temp': 15.94, 'shanghai_temp': 17.92, 
'hotter_city': 'Shanghai', 'summary': '上海比北京温度高约1.98°C，北京天气晴朗，上海多云。'}", name='WeatherCompareOutput', 
id='d6f802c1-8931-46d8-873d-e08fdbe8b41e', tool_call_id='call_7857ec7fc9324aeba46115')], 
'structured_response': {'beijing_temp': 15.94, 'shanghai_temp': 17.92, 'hotter_city': 'Shanghai', 
'summary': '上海比北京温度高约1.98°C，北京天气晴朗，上海多云。'}}

{
  "beijing_temp": 15.94,
  "shanghai_temp": 17.92,
  "hotter_city": "Shanghai",
  "summary": "上海比北京温度高约1.98°C，北京天气晴朗，上海多云。"
}
"""
