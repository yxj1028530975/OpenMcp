from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="127.0.0.1",  # optional, default
        port=9000,         # optional, default
        path="/mcp",       # optional, default
        log_level="debug"  # optional
    )