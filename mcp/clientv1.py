"""
"fetch": {
      "command": "uvx",
      "args": [
        "custom-value"
      ],
      "transport": "stdio"
    }
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
from sqlalchemy import exc

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
        except:
            logger.info(f"\n Error: {exc}")

    logger.info("会话结束，Bye！")

if __name__ == "__main__":
    asyncio.run(run_chat_loop())
