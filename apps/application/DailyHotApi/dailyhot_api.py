from pydantic import Field
from typing import List, Optional, Dict, Any, Union, Annotated
import httpx
import asyncio
import os
from common.server import server_app
from dataclasses import dataclass

# 基本URL，优先使用环境变量配置
BASE_URL = os.environ.get("DAILYHOT_API_URL", "http://localhost:6688")

@dataclass
class HotItem:
    title: Annotated[str, Field(description="标题")]
    url: Annotated[Optional[str], Field(description="链接")] = None
    hot: Annotated[Optional[Union[str, int]], Field(description="热度")] = None
    img: Annotated[Optional[str], Field(description="图片链接")] = None
    mobileUrl: Annotated[Optional[str], Field(description="移动端链接")] = None
    desc: Annotated[Optional[str], Field(description="描述")] = None


# 平台与描述的映射，用于文档展示和验证支持的平台
PLATFORM_DESCRIPTIONS = {
    # 社交媒体
    "zhihu": "知乎热榜",
    "weibo": "微博热搜",
    "zhihu-daily": "知乎日报推荐榜",
    "douban-group": "豆瓣讨论小组讨论精选",
    "tieba": "百度贴吧热议榜",
    "hupu": "虎扑步行街热帖",
    
    # 视频平台
    "bilibili": "B站热榜",
    "douyin": "抖音热点榜",
    "kuaishou": "快手热点榜",
    "acfun": "AcFun排行榜",
    
    # 搜索引擎
    "baidu": "百度热搜榜",
    
    # 新闻资讯
    "toutiao": "今日头条热榜",
    "qq-news": "腾讯新闻热点榜",
    "sina-news": "新浪新闻热点榜",
    "netease-news": "网易新闻热点榜",
    "thepaper": "澎湃新闻热榜",
    "sina": "新浪网热榜",
    
    # 科技数码
    "36kr": "36氪热榜",
    "ithome": "IT之家热榜",
    "ithome-xijiayi": "IT之家「喜加一」最新动态",
    "sspai": "少数派热榜",
    "huxiu": "虎嗅24小时",
    "coolapk": "酷安热榜",
    "ifanr": "爱范儿快讯",
    
    # 技术开发
    "csdn": "CSDN排行榜",
    "juejin": "稀土掘金热榜",
    "v2ex": "V2EX主题榜",
    "52pojie": "吾爱破解榜单",
    "hostloc": "全球主机交流榜单",
    "nodeseek": "NodeSeek最新动态",
    "hellogithub": "HelloGitHub Trending",
    "51cto": "51CTO推荐榜",
    
    # 内容平台
    "weread": "微信读书飙升榜",
    "jianshu": "简书热门推荐",
    "guokr": "果壳热门文章",
    
    # 游戏动漫
    "lol": "英雄联盟更新公告",
    "miyoushe": "米游社最新消息",
    "genshin": "原神最新消息",
    "honkai": "崩坏3最新动态",
    "starrail": "崩坏：星穹铁道最新动态",
    "ngabbs": "NGA热帖",
    "douban-movie": "豆瓣电影新片榜",
    
    # 生活服务
    "weatheralarm": "中央气象台全国气象预警",
    "earthquake": "中国地震台地震速报",
    "history": "历史上的今天"
}

@server_app.tool()
async def get_hot_news(
    platform: Annotated[str, Field(description="平台名称，如zhihu(知乎)、weibo(微博)等")],
    limit: Annotated[int, Field(description="返回条目数量，默认10条")] = 10
):
    """
    支持的平台列表：
    
    - 社交媒体:
      - zhihu: 知乎热榜
      - weibo: 微博热搜
      - zhihu-daily: 知乎日报推荐榜
      - douban-group: 豆瓣讨论小组讨论精选
      - tieba: 百度贴吧热议榜
      - hupu: 虎扑步行街热帖
      
    - 视频平台:
      - bilibili: B站热榜
      - douyin: 抖音热点榜
      - kuaishou: 快手热点榜
      - acfun: AcFun排行榜
      
    - 搜索引擎:
      - baidu: 百度热搜榜
      
    - 新闻资讯:
      - toutiao: 今日头条热榜
      - qq-news: 腾讯新闻热点榜
      - sina-news: 新浪新闻热点榜
      - netease-news: 网易新闻热点榜
      - thepaper: 澎湃新闻热榜
      - sina: 新浪网热榜
      
    - 科技数码:
      - 36kr: 36氪热榜
      - ithome: IT之家热榜
      - ithome-xijiayi: IT之家「喜加一」最新动态
      - sspai: 少数派热榜
      - huxiu: 虎嗅24小时
      - coolapk: 酷安热榜
      - ifanr: 爱范儿快讯
      
    - 技术开发:
      - csdn: CSDN排行榜
      - juejin: 稀土掘金热榜
      - v2ex: V2EX主题榜
      - 52pojie: 吾爱破解榜单
      - hostloc: 全球主机交流榜单
      - nodeseek: NodeSeek最新动态
      - hellogithub: HelloGitHub Trending
      - 51cto: 51CTO推荐榜
      
    - 内容平台:
      - weread: 微信读书飙升榜
      - jianshu: 简书热门推荐
      - guokr: 果壳热门文章
      
    - 游戏动漫:
      - lol: 英雄联盟更新公告
      - miyoushe: 米游社最新消息
      - genshin: 原神最新消息
      - honkai: 崩坏3最新动态
      - starrail: 崩坏：星穹铁道最新动态
      - ngabbs: NGA热帖
      - douban-movie: 豆瓣电影新片榜
      
    - 生活服务:
      - weatheralarm: 中央气象台全国气象预警
      - earthquake: 中国地震台地震速报
      - history: 历史上的今天
    
    Args:
        platform: 平台名称，如zhihu、weibo、bilibili、baidu等
        limit: 返回条目数量限制，默认10条
    
    Returns:
        code: 0 成功 -1 失败
        news: 热榜信息，包含标题、副标题和热门数据列表
        msg: 成功或失败信息
    """
    # 检查平台是否支持
    if platform not in PLATFORM_DESCRIPTIONS:
        supported_platforms = ", ".join(PLATFORM_DESCRIPTIONS.keys())
        return {"code": -1, "msg": f"不支持的平台: {platform}。支持的平台有: {supported_platforms}"}
    
    try:
        result = await fetch_data(f"{BASE_URL}/{platform}?limit={limit}")
        if "code" in result and result["code"] == -1:
            return result
        return {"code": 0, "news": result, "msg": "success"}
    except Exception as e:
        return {"code": -1, "msg": f"获取数据失败: {str(e)}"}


async def fetch_data(url: str) -> Dict[str, Any]:
    """从原始API获取数据"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"code": -1, "msg": f"获取数据失败: {str(e)}"}