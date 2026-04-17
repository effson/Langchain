import json
import os
import httpx
from loguru import logger
from mcp.server import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("WeatherServerSSE", host="0.0.0.0", port=8000)

@mcp.tool()  # 保留原装饰器写法，无任何修改
def get_weather(city: str) -> str:
    """
    查询指定城市的即时天气信息。
    参数 city: 城市英文名，如 Beijing
    返回: OpenWeather API 的 JSON 字符串
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }
    resp = httpx.get(url, params=params, timeout=10)
    data = resp.json()
    logger.info(f"查询 {city} 天气结果：{data}")
    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    logger.info("启动 MCP SSE 天气服务器，监听 http://0.0.0.0:8000/sse")
    # 运行 MCP 服务，保留原 transport="sse" 参数，无任何修改
    mcp.run(transport="sse")
