from common.server import server_app
from application.weather.weather_api import *
from application.DailyHotApi.dailyhot_api import *
from common.main_ui import *


if __name__ == "__main__":
    server_app.run(
        transport="sse",
        host="0.0.0.0",
        port=9000,
        path="/mcp",
        log_level="debug"
    )
