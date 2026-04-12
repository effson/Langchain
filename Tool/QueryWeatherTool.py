from langchain_core.tools import tool
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

@tool
def get_weather(loc):
    """
    查询即时天气函数
    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
                则 loc 参数需要输入 'Beijing'/'shanghai'。
    :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
             https://home.openweathermap.org/users/sign_in。
             返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式进行表示，
             其中包含了全部重要的天气信息。
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    response = httpx.get(url, params=params, timeout=30)

    data = response.json()
    #print(json.dumps(data))
    return json.dumps(data)

# result = get_weather.invoke("shanghai")
result = get_weather.invoke("beijing")
print(result)

"""
{
  "coord": {
    "lon": 116.3972,   // 经度
    "lat": 39.9075     // 纬度
  },
  "weather": [
    {
      "id": 804,       // 天气状况代码 (804 代表阴天)
      "main": "Clouds", 
      "description": "阴，多云", 
      "icon": "04d"    // 天气图标 ID
    }
  ],
  "base": "stations",
  "main": {
    "temp": 26.94,        // 当前温度 (摄氏度)
    "feels_like": 26.05,  // 体感温度
    "temp_min": 26.94,    // 最低温度
    "temp_max": 26.94,    // 最高温度
    "pressure": 1009,     // 气压 (hPa)
    "humidity": 20,       // 湿度 (%)
    "sea_level": 1009,    // 海平面气压
    "grnd_level": 1004    // 地面气压
  },
  "visibility": 10000,    // 能见度 (米)
  "wind": {
    "speed": 2.15,        // 风速 (米/秒)
    "deg": 60,            // 风向 (角度)
    "gust": 3.49          // 阵风风速
  },
  "clouds": {
    "all": 99             // 云量 (%)
  },
  "dt": 1775981488,       // 数据计算时间 (Unix 时间戳)
  "sys": {
    "type": 1,
    "id": 9609,
    "country": "CN",      // 国家代码
    "sunrise": 1775943710,// 日出时间 (Unix 时间戳)
    "sunset": 1775990902  // 日落时间 (Unix 时间戳)
  },
  "timezone": 28800,      // 时区偏移量 (秒)，28800/3600 = 东八区
  "id": 1816670,          // 城市 ID (北京)
  "name": "Beijing",      // 城市名称
  "cod": 200              // 状态码：成功
}
"""
