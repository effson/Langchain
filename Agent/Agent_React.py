import os

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()
# 模拟产品数据库
PRODUCT_DATABASE = {
    "无线耳机": [
        {"id": "WH-1000XM5", "name": "索尼 WH-1000XM5", "popularity": 95, "price": 299},
        {"id": "QC45", "name": "Bose QuietComfort 45", "popularity": 88, "price": 329},
        {"id": "AIRMAX", "name": "苹果 AirPods Max", "popularity": 92, "price": 549},
        {"id": "PXC550", "name": "森海塞尔 PXC 550", "popularity": 76, "price": 299},
        {"id": "HT450", "name": "JBL Tune 760NC", "popularity": 82, "price": 99}
    ],
    "游戏鼠标": [
        {"id": "GPW", "name": "罗技 G Pro 无线", "popularity": 90, "price": 129},
        {"id": "VIPER", "name": "雷蛇 Viper V2 Pro", "popularity": 87, "price": 149},
        {"id": "DAV3", "name": "雷蛇 DeathAdder V3", "popularity": 85, "price": 119}
    ],
    "笔记本电脑": [
        {"id": "MBP14", "name": "MacBook Pro 14英寸", "popularity": 94, "price": 1999},
        {"id": "XPS13", "name": "戴尔 XPS 13", "popularity": 89, "price": 1299},
        {"id": "TPX1", "name": "ThinkPad X1 Carbon", "popularity": 86, "price": 1499}
    ]
}

# 模拟库存数据库
INVENTORY_DATABASE = {
    "WH-1000XM5": {"stock": 10, "location": "仓库-A"},
    "QC45": {"stock": 0, "location": "仓库-B"},
    "AIRMAX": {"stock": 5, "location": "仓库-C"},
    "PXC550": {"stock": 15, "location": "仓库-A"},
    "HT450": {"stock": 25, "location": "仓库-B"},
    "GPW": {"stock": 8, "location": "仓库-C"},
    "VIPER": {"stock": 12, "location": "仓库-A"},
    "DAV3": {"stock": 3, "location": "仓库-B"},
    "MBP14": {"stock": 7, "location": "仓库-C"},
    "XPS13": {"stock": 0, "location": "仓库-A"},
    "TPX1": {"stock": 4, "location": "仓库-B"}
}


# 工具1：搜索产品
@tool
def search_products(query: str) -> str:
    """搜索产品并返回按受欢迎度排序的结果"""
    print(f"🔍 [工具调用] search_products('{query}')")

    # 关键词映射，支持多种中文表达方式
    keyword_mapping = {
        "无线耳机": ["无线耳机", "蓝牙耳机", "头戴式耳机", "耳机"],
        "游戏鼠标": ["游戏鼠标", "电竞鼠标", "鼠标"],
        "笔记本电脑": ["笔记本电脑", "笔记本", "手提电脑", "电脑"]
    }

    # 查找匹配的类别
    matched_category = None
    for category, keywords in keyword_mapping.items():
        if any(keyword in query for keyword in keywords):
            matched_category = category
            break

    if matched_category and matched_category in PRODUCT_DATABASE:
        products = PRODUCT_DATABASE[matched_category]
        # 按受欢迎度排序
        sorted_products = sorted(products, key=lambda x: x['popularity'], reverse=True)
        result = f"找到 {len(sorted_products)} 个匹配 '{query}' 的产品:\n"

        for i, product in enumerate(sorted_products, 1):
            result += f"{i}. {product['name']} (ID: {product['id']}) - 受欢迎度: {product['popularity']}% - ￥{product['price']}\n"

        return result


# 工具2：检查库存
@tool
def check_inventory(product_id: str) -> str:
    """检查特定产品的库存状态"""
    print(f"📦 [工具调用] check_inventory('{product_id}')")

    if product_id in INVENTORY_DATABASE:
        stock_info = INVENTORY_DATABASE[product_id]
        status = "有库存" if stock_info['stock'] > 0 else "缺货"
        return f"产品 {product_id}: {status} ({stock_info['stock']} 件库存) - 位置: {stock_info['location']}"
    else:
        return f"未找到产品ID: {product_id}"


# 创建代理
model = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

agent = create_agent(
    model,
    tools=[search_products, check_inventory],
    system_prompt="""你是电商助手，遵循ReAct模式：
    1. 先推理用户需求
    2. 选择合适的工具执行操作
    3. 基于工具结果进行下一步推理
    4. 重复直到获得完整答案

    保持推理步骤简洁明了。"""
)

# 测试案例1：无线耳机搜索
result1 = agent.invoke({
    "messages": [{"role": "user", "content": "查找当前最受欢迎的无线耳机并检查是否有库存"}]
})

print("\n" + "=" * 40)
print("📊 最终结果:")
for msg in result1['messages']:
    if hasattr(msg, 'content'):
        print(f"{msg.__class__.__name__}: {msg.content}")
print("=" * 40)

print()
print()

# # 详细追踪ReAct循环过程
def track_react_cycle(messages):
    print("ReAct循环步骤分析:")
    step = 1
    for i, msg in enumerate(messages):
        msg_type = msg.__class__.__name__
        if msg_type == "AIMessage" and hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"\n🔄 步骤{step}: Reasoning + Acting")
            for tool_call in msg.tool_calls:
                print(f"   🛠️  工具调用: {tool_call['name']}({tool_call['args']})")
            step += 1
        elif msg_type == "ToolMessage":
            print(f"   📋  观察结果: {msg.content[:80]}...")
        elif msg_type == "AIMessage" and not (hasattr(msg, 'tool_calls') and msg.tool_calls):
            print(f"\n✅ 最终回答: {msg.content}")

# 追踪案例1的ReAct循环
track_react_cycle(result1['messages'])

"""
🔍 [工具调用] search_products('无线耳机')
📦 [工具调用] check_inventory('WH-1000XM5')

========================================
📊 最终结果:
HumanMessage: 查找当前最受欢迎的无线耳机并检查是否有库存
AIMessage: 1. 首先，我需要搜索当前最受欢迎的无线耳机。
2. 然后，从搜索结果中获取最受欢迎的产品ID，并检查其库存状态。


ToolMessage: 找到 5 个匹配 '无线耳机' 的产品:
1. 索尼 WH-1000XM5 (ID: WH-1000XM5) - 受欢迎度: 95% - ￥299
2. 苹果 AirPods Max (ID: AIRMAX) - 受欢迎度: 92% - ￥549
3. Bose QuietComfort 45 (ID: QC45) - 受欢迎度: 88% - ￥329
4. JBL Tune 760NC (ID: HT450) - 受欢迎度: 82% - ￥99
5. 森海塞尔 PXC 550 (ID: PXC550) - 受欢迎度: 76% - ￥299

AIMessage: 最受欢迎的无线耳机是索尼 WH-1000XM5（ID: WH-1000XM5），接下来我将检查它的库存状态。



ToolMessage: 产品 WH-1000XM5: 有库存 (10 件库存) - 位置: 仓库-A
AIMessage: 索尼 WH-1000XM5 是当前最受欢迎的无线耳机，且有库存（10件），存放于仓库-A。
========================================


ReAct循环步骤分析:

🔄 步骤1: Reasoning + Acting
   🛠️  工具调用: search_products({'query': '无线耳机'})
   📋  观察结果: 找到 5 个匹配 '无线耳机' 的产品:
1. 索尼 WH-1000XM5 (ID: WH-1000XM5) - 受欢迎度: 95% - ￥299
2. 苹果 ...

🔄 步骤2: Reasoning + Acting
   🛠️  工具调用: check_inventory({'product_id': 'WH-1000XM5'})
   📋  观察结果: 产品 WH-1000XM5: 有库存 (10 件库存) - 位置: 仓库-A...

✅ 最终回答: 索尼 WH-1000XM5 是当前最受欢迎的无线耳机，且有库存（10件），存放于仓库-A。
"""
