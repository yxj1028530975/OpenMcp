from pydantic import Field
from typing import Annotated
from .utils import format_alert, get_weather_from_cityname
from common.server import server_app
from dataclasses import dataclass

@dataclass
class Weather:
    cityname: Annotated[str, Field(description="城市名称")]
    weather: Annotated[str, Field(description="天气情况")]
    temperature: Annotated[str, Field(description="温度")]
    humidity: Annotated[str, Field(description="湿度")]
    wind_speed: Annotated[str, Field(description="风速")]

@server_app.tool()
async def get_weather_cityname(cityname: str):
    """
    通过城市名称（中国城市使用拼音）获取天气信息

    Args:
        cityname: 城市名称（中国城市使用拼音）
    
    Returns:
        code: 0 成功 -1 失败
        weather: 天气信息
        msg: 成功或失败信息
    """
    weather_data = await get_weather_from_cityname(cityname)
    if not weather_data:
        return {"code": -1, "msg": "Failed to fetch weather data"}
    weather_info = format_alert(weather_data)
    if "error" in weather_info:
        return {"code": -1, "msg": weather_info.get("error", "Failed to fetch weather data")}
    return {"code": 0, "weather": Weather(**weather_info), "msg": "success"}
