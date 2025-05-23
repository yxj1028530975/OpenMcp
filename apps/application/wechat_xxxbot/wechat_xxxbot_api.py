from pydantic import Field
from typing import List, Optional, Dict, Any, Union, Annotated
import httpx
from common.server import server_app
from dataclasses import dataclass
import tomllib


with open("apps/application/odoo_data/config.toml", "rb") as f:
    plugin_config = tomllib.load(f)

base_url = plugin_config["xxx_bot"]["base_url"]

@server_app.tool()
async def wechat_msg_send_txt(
    at: Annotated[str, Field(description="@的wxid，多个wxid用,隔开")],
    content: Annotated[str, Field(description="消息内容")],
    ToWxid: Annotated[str, Field(description="发送给的wxid")],
    type: Annotated[int, Field(description="消息类型")],
    wxid: Annotated[str, Field(description="发送者的wxid")],
):
    
    """
    发送微信文本消息，支持@群成员功能。判断需不需要他艾特群成员，如果需要艾特群成员，则调用 wechat_group_getChatRoomMemberDetail 接口获取群成员详情，然后通过名称找到最相似的那个人，再传参给这个接口
    
    参数说明:
    - wxid: 发送者的微信ID
    - ToWxid: 接收者的微信ID，群聊ID通常以@chatroom结尾 
    - content: 消息内容，@人时需在消息前加上@对方昵称
    - type: 消息类型，文本消息固定为1
    - at: 要@的成员wxid，多个成员用逗号分隔
    
    使用提示:
    - 如需@群成员但不知道其wxid，请先调用wechat_group_getChatRoomMemberDetail获取群成员信息
    - @格式示例: "@昵称 消息内容"
    
    示例:
    {
        "wxid": "wxid_tjlscvvc60a022",
        "ToWxid": "51740029844@chatroom",
        "content": "@木不易成楊！ 北京欢迎你",
        "type": 1,
        "at": "LoVe10285309"
    }
    """
    url = f"{base_url}/api/Msg/SendTxt"
    async with httpx.AsyncClient() as client:
        body = {
            "at": at,
            "content": content,
            "ToWxid": ToWxid,
            "type": 1,
            "wxid": wxid
        }
        response = await client.post(url, json=body)
        return response.json()

@server_app.tool()
async def wechat_group_getChatRoomMemberDetail(
    QID: Annotated[str, Field(description="群ID")],
    wxid: Annotated[str, Field(description="发送者的wxid")],
):
    """
    获取微信群成员详细信息，返回成员列表包含wxid和昵称。
    
    参数说明:
    - QID: 群聊ID，通常以@chatroom结尾
    - wxid: 调用者的微信ID
    
    返回数据:
    - 返回包含群成员信息的列表，每个成员包含UserName(wxid)和NickName(昵称)
    
    使用场景:
    - 在需要@特定群成员但不知道其wxid时使用
    - 可通过昵称匹配找到对应成员的wxid
    
    示例返回:
    [
        {
            "UserName": "LoVe10285309",  # 群成员的wxid
            "NickName": "木不易成楊！"   # 群成员的昵称
        },
        ...
    ]
    """
    url = f"{base_url}/api/Group/GetChatRoomMemberDetail"
    async with httpx.AsyncClient() as client:
        body = {
            "QID": QID,
            "wxid": wxid
        }
        response = await client.post(url, json=body)
        if response.json()["Code"] != 0:
            return []
        return [{"UserName": item["UserName"], "NickName": item["NickName"]} 
                for item in response.json()["Data"]["NewChatroomData"]["ChatRoomMember"]]
