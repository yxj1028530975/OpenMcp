from fastmcp import FastMCP
import httpx
import aiohttp
import yaml
# Create a basic server instance

def yaml_serializer(data):
    return yaml.dump(data, sort_keys=False)

mcp = FastMCP(name="天气助手", tool_serializer=yaml_serializer)

# Create a server with the custom serializer
mcp = FastMCP(name="MyServer")
# You can also add instructions for how to interact with the server
mcp_with_instructions = FastMCP(
    name="天气助手",
    instructions="""
        This server provides data analysis tools.
        Call get_average() to analyze numerical data.
        """
)

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b

@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by ID."""
    # The {user_id} in the URI is extracted and passed to this function
    return {"id": user_id, "name": f"User {user_id}", "status": "active"}

# Asynchronous tool (ideal for I/O-bound operations)
@mcp.tool()
async def fetch_weather(city: str) -> dict:
    """Retrieve current weather conditions for a city."""
    # Use 'async def' for operations involving network calls, file I/O, etc.
    # This prevents blocking the server while waiting for external operations.
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/weather/{city}") as response:
            # Check response status before returning
            response.raise_for_status()
            return await response.json()