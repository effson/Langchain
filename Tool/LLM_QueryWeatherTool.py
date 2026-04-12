import os
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputKeyToolsParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from loguru import logger
from dotenv import load_dotenv

from QueryWeatherTool import get_weather

load_dotenv()
# 初始化大语言模型实例
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

llm_with_tools = llm.bind_tools([get_weather])
tool_parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)
weather_query_chain = llm_with_tools | tool_parser | get_weather

output_prompt = PromptTemplate.from_template(
    """你是一个专业的天气播报员。请将下面这段 JSON 格式的天气原始数据转述成一段亲切、自然且详细的中文播报。    
    原始数据：{weather_json}
    
    要求：
    1. 包含城市名、天气描述、温度、感官温度和湿度。
    2. 给出简洁的穿衣或出行建议。
    3. 不要提及 JSON、接口等技术术语。
    """
)
output_parser = StrOutputParser()
output_chain = output_prompt | llm | output_parser

# 构建完整的处理链：天气查询链 ->将天气数据包装为字典格式 -> 输出链
full_chain = weather_query_chain | (lambda x: {"weather_json": x}) | output_chain

result = full_chain.invoke("请问北京今天的天气如何？")
logger.info(result)

# if __name__ == "__main__":
#     while True:
#         user_input = input("\n请输入你想查询的城市（输入 'exit' 退出）：")
#         if user_input.lower() in ['exit', 'quit', 'q']:
#             break
#
#         try:
#             # 运行链路
#             # 用户输入 "北京天气怎么样" -> llm_with_tools 识别出 loc="Beijing" -> get_weather 执行
#             print("正在查询，请稍候...")
#             result = full_chain.invoke(user_input)
#             logger.success(f"\nAI 播报结果：\n{result}")
#         except Exception as e:
#             logger.error(f"查询出错：{e}")

"""
{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 804, "main": "Clouds", "description": "\u9634\uff0c\u591a\u4e91", "icon": "04d"}], "base": "stations", "main": {"temp": 25.94, "feels_like": 25.09, "temp_min": 25.94, "temp_max": 25.94, "pressure": 1009, "humidity": 19, "sea_level": 1009, "grnd_level": 1005}, "visibility": 10000, "wind": {"speed": 2.41, "deg": 72, "gust": 3.63}, "clouds": {"all": 98}, "dt": 1775985007, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1775943710, "sunset": 1775990902}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}
2026-04-12 17:21:06.798 | INFO     | __main__:<module>:41 - 大家好，欢迎收听今天的天气播报。此刻我们关注的城市是北京。

受高空云层影响，今天北京的天空显得格外沉稳，整体呈现出阴天伴随多云的状况，阳光暂时有些害羞躲了起来。目前的气温记录在 26 摄氏度左右，体感温度大约是 25 度，让人感觉十分凉爽舒适，没有明显的燥热感。

不过，我要特别提醒一下，今天的空气湿度仅为 19%，这属于相当干燥的状态。虽然此时吹着轻柔的微风，风速大概每秒 2 米多，但也可能会加速水分蒸发，所以保湿工作很重要。

针对这种情况，我给大家两点温馨的小建议：
第一，在穿衣方面，26 度的气温非常适合穿着轻薄的单衣、短袖 T 恤或是透气的衬衫，无需穿得太厚重。
第二，在出行和健康方面，由于空气较为干燥，建议外出的朋友们多补充水分，随时携带水杯。另外，皮肤敏感的朋友也可以适当使用一些润肤露。虽然今日云量很大，但能见度依然良好，完全不影响您正常的外出活动和行程安排。

以上就是北京的最新天气情况，祝大家今天心情愉快，一切顺利！
"""
