from fastmcp import Client
import asyncio

client = Client("http://127.0.0.1:9000/mcp")

async def main():
    tools = await client.list_tools()
    print(tools)

# 运行异步函数
asyncio.run(main())
