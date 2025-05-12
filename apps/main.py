from common.server import server_app
from application.weather.weather_api import *
from application.DailyHotApi.dailyhot_api import *
from common.main_ui import *
import argparse
import os


if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='OpenMCP API服务')
    parser.add_argument('--host', type=str, default=os.environ.get('HOST', '127.0.0.1'),
                        help='主机地址 (默认: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', 9000)),
                        help='端口号 (默认: 9000)')
    args = parser.parse_args()
    
    # 在Docker中运行时，需要绑定到0.0.0.0才能从容器外访问
    print(f"启动服务: host={args.host}, port={args.port}")
    server_app.run(transport="sse", host=args.host, port=args.port)
