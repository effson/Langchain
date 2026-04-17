"""
powershell -ExecutionPolicy ByPass -c "Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression"
PS C:\Users\Mechrev> uv --version
uv 0.11.7 (9d177269e 2026-04-15 x86_64-pc-windows-msvc)
PS C:\Users\Mechrev> where.exe uvx
C:\Users\Mechrev\.local\bin\uvx.exe
PS C:\Users\Mechrev>
"""
# https://docs.langchain.com/oss/python/langchain/mcp
import asyncio
import json
import os
from typing import Any, Dict

from langchain_classic.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from loguru import logger

from McpServer import mcp
from dotenv import load_dotenv

# .env文件读取
load_dotenv()

def load_servers(file_path : str = "mcp.json") -> Dict[str, Any]:
    """
    从指定json文件中加载MCP服务器配置
    :param file_path(str): 配置文件路径。默认为"mcp.json"
    :return:Dict[str, any]:包含MCP服务器配置的字典，若文件中没有”mcpServers“键则返回空字典
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("mcpServers", {})

async def run_chat_loop() -> None:
    """
    启动一个基于MCP工具的聊天代理循环
    :param
    :return:None
    """
    server_cfg = load_servers()

    mcp_client = MultiServerMCPClient(server_cfg)
    tools = await mcp_client.get_tools()
    logger.info(f"已加载{len(tools)}个MCP工具: {[t.name for t in tools]}")

    llm = init_chat_model(
        model="deepseek-chat",  # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
        model_provider="deepseek",
        api_key=os.getenv("deepseek-api"),
        base_url='https://api.deepseek.com'
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有用的助手，需要使用提供的工具来完成用户的请求。"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors="解析用户指令失败，请重新输入清晰的指令"
    )

    logger.info("\n MCP Agent 已启动，请先输入提问给LLM+MCP,输入Quit退出")

    while True:
        user_input = input("\n 你:").strip()
        if user_input.lower() == "quit":
            break
        try:
            result = await agent_executor.ainvoke({"input": user_input})
            print(f"\nAI: {result['output']}")
        except Exception as exc:
            logger.info(f"\n Error: {exc}")

    logger.info("会话结束，Bye！")

if __name__ == "__main__":
    asyncio.run(run_chat_loop())

"""
[04/17/26 13:01:35] INFO     HTTP Request: GET                  _client.py:1740
                             http://127.0.0.1:8000/sse                         
                             "HTTP/1.1 200 OK"                                 
                    INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=39cd9d663589435283e00289b                
                             23cae64 "HTTP/1.1 202 Accepted"                   
                    INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=39cd9d663589435283e00289b                
                             23cae64 "HTTP/1.1 202 Accepted"                   
                    INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=39cd9d663589435283e00289b                
                             23cae64 "HTTP/1.1 202 Accepted"                   
2026-04-17 13:01:35.321 | INFO     | __main__:run_chat_loop:95 - 已加载1个MCP工具: ['get_weather']

 你:2026-04-17 13:01:37.866 | INFO     | __main__:run_chat_loop:118 - 
 MCP Agent 已启动，请先输入提问给LLM+MCP,输入Quit退出
你好


> Entering new AgentExecutor chain...
[04/17/26 13:02:37] INFO     HTTP Request: POST                 _client.py:1740
                             https://api.deepseek.com/v1/chat/c                
                             ompletions "HTTP/1.1 200 OK"                      
你好！我可以帮您查询天气信息。如果您想知道某个城市的天气情况，请告诉我城市名称（英文名，比如 Beijing、Shanghai、New York 等），我就可以为您查询即时天气信息。

> Finished chain.

AI: 你好！我可以帮您查询天气信息。如果您想知道某个城市的天气情况，请告诉我城市名称（英文名，比如 Beijing、Shanghai、New York 等），我就可以为您查询即时天气信息。

 你:Shanghai的天气怎么样


> Entering new AgentExecutor chain...
[04/17/26 13:03:17] INFO     HTTP Request: POST                 _client.py:1740
                             https://api.deepseek.com/v1/chat/c                
                             ompletions "HTTP/1.1 200 OK"                      

Invoking: `get_weather` with `{'city': 'Shanghai'}`
responded: 我来帮您查询上海的天气情况。

[04/17/26 13:03:20] INFO     HTTP Request: GET                  _client.py:1740
                             http://127.0.0.1:8000/sse                         
                             "HTTP/1.1 200 OK"                                 
                    INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=c3d7265982f3424f9f3e5f931                
                             277510e "HTTP/1.1 202 Accepted"                   
                    INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=c3d7265982f3424f9f3e5f931                
                             277510e "HTTP/1.1 202 Accepted"                   
                    INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=c3d7265982f3424f9f3e5f931                
                             277510e "HTTP/1.1 202 Accepted"                   
[04/17/26 13:03:22] INFO     HTTP Request: POST                 _client.py:1740
                             http://127.0.0.1:8000/messages/?se                
                             ssion_id=c3d7265982f3424f9f3e5f931                
                             277510e "HTTP/1.1 202 Accepted"                   
[{'type': 'text', 'text': '{"coord": {"lon": 121.4581, "lat": 31.2222}, "weather": [{"id": 803, "main": "Clouds", "description": "多云", "icon": "04d"}], "base": "stations", "main": {"temp": 19.92, "feels_like": 19.74, "temp_min": 19.92, "temp_max": 19.92, "pressure": 1014, "humidity": 68, "sea_level": 1014, "grnd_level": 1013}, "visibility": 8000, "wind": {"speed": 3, "deg": 10}, "clouds": {"all": 75}, "dt": 1776402078, "sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1776374657, "sunset": 1776421379}, "timezone": 28800, "id": 1796236, "name": "Shanghai", "cod": 200}', 'id': 'lc_153678e5-6591-4c38-b3ad-7fa1240b4e4c'}]                    INFO     HTTP Request: POST                 _client.py:1740
                             https://api.deepseek.com/v1/chat/c                
                             ompletions "HTTP/1.1 200 OK"                      
根据查询结果，上海当前的天气情况如下：

**天气状况：** 多云
**温度：** 19.92°C（体感温度19.74°C）
**湿度：** 68%
**气压：** 1014 hPa
**风速：** 3 m/s，风向10度
**能见度：** 8000米
**云量：** 75%

总体来说，上海现在是多云天气，温度约20°C，比较舒适，湿度适中，风力较小。

> Finished chain.

AI: 根据查询结果，上海当前的天气情况如下：

**天气状况：** 多云
**温度：** 19.92°C（体感温度19.74°C）
**湿度：** 68%
**气压：** 1014 hPa
**风速：** 3 m/s，风向10度
**能见度：** 8000米
**云量：** 75%

总体来说，上海现在是多云天气，温度约20°C，比较舒适，湿度适中，风力较小。

你:quit
2026-04-17 13:08:29.452 | INFO     | __main__:run_chat_loop:130 - 会话结束，Bye！
"""
