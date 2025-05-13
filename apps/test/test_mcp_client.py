from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
import asyncio

headers = {"Authorization": "Bearer mytoken"}
transport = StreamableHttpTransport(url="http://82.156.47.117:9000/mcp", headers=headers)
client = Client(transport)

async def main():
    async with client:  # 使用上下文管理器连接客户端
        tools = await client.list_tools()
        print(tools)

if __name__ == "__main__":
    asyncio.run(main())