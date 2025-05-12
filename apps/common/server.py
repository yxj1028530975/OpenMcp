from fastmcp import FastMCP, Context
import yaml

def yaml_serializer(data):
    return yaml.dump(data, sort_keys=False)

server_app = FastMCP(name="ContextDemo", tool_serializer=yaml_serializer)