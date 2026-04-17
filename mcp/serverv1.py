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

"""
2026-04-17 12:54:43.739 | INFO     | __main__:<module>:73 - 启动 MCP SSE 天气服务器，监听 http://0.0.0.0:8000/sse
INFO:     Started server process [28720]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:49675 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:49677 - "POST /messages/?session_id=282f822ba1d44744a19193fb72fa2555 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49679 - "POST /messages/?session_id=282f822ba1d44744a19193fb72fa2555 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49681 - "POST /messages/?session_id=282f822ba1d44744a19193fb72fa2555 HTTP/1.1" 202 Accepted
[04/17/26 12:56:26] INFO     Processing request of type           server.py:727
                             ListToolsRequest                                  
INFO:     127.0.0.1:25992 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:25994 - "POST /messages/?session_id=39cd9d663589435283e00289b23cae64 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:25996 - "POST /messages/?session_id=39cd9d663589435283e00289b23cae64 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:25998 - "POST /messages/?session_id=39cd9d663589435283e00289b23cae64 HTTP/1.1" 202 Accepted
[04/17/26 13:01:35] INFO     Processing request of type           server.py:727
                             ListToolsRequest                                  
INFO:     127.0.0.1:24840 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:24842 - "POST /messages/?session_id=c3d7265982f3424f9f3e5f931277510e HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:24844 - "POST /messages/?session_id=c3d7265982f3424f9f3e5f931277510e HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:24846 - "POST /messages/?session_id=c3d7265982f3424f9f3e5f931277510e HTTP/1.1" 202 Accepted
[04/17/26 13:03:20] INFO     Processing request of type           server.py:727
                             CallToolRequest                                   
[04/17/26 13:03:22] INFO     HTTP Request: GET                  _client.py:1025
                             https://api.openweathermap.org/dat                
                             a/2.5/weather?q=Shanghai&appid=503                
                             aa50197757eec743aefd2a7daa49d&unit                
                             s=metric&lang=zh_cn "HTTP/1.1 200                 
                             OK"                                               
2026-04-17 13:03:22.221 | INFO     | __main__:get_weather:68 - 查询 Shanghai 天气结果：{'coord': {'lon': 121.4581, 'lat': 31.2222}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': '多云', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 19.92, 'feels_like': 19.74, 'temp_min': 19.92, 'temp_max': 19.92, 'pressure': 1014, 'humidity': 68, 'sea_level': 1014, 'grnd_level': 1013}, 'visibility': 8000, 'wind': {'speed': 3, 'deg': 10}, 'clouds': {'all': 75}, 'dt': 1776402078, 'sys': {'type': 1, 'id': 9659, 'country': 'CN', 'sunrise': 1776374657, 'sunset': 1776421379}, 'timezone': 28800, 'id': 1796236, 'name': 'Shanghai', 'cod': 200}
INFO:     127.0.0.1:24856 - "POST /messages/?session_id=c3d7265982f3424f9f3e5f931277510e HTTP/1.1" 202 Accepted
                    INFO     Processing request of type           server.py:727
                             ListToolsRequest                                  

"""
