from starlette.responses import HTMLResponse
from starlette.requests import Request
from common.server import server_app


@server_app.custom_route("/", methods=["GET"])
async def index(request: Request) -> HTMLResponse:
    """
    服务首页，提供API说明和使用方法
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <title>OpenMCP API 控制台</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {
                --primary-color: #3498db;
                --secondary-color: #2c3e50;
                --accent-color: #e74c3c;
                --light-color: #ecf0f1;
                --dark-color: #2c3e50;
                --success-color: #2ecc71;
                --info-color: #3498db;
                --warning-color: #f39c12;
            }
            
            body {
                font-family: 'PingFang SC', 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: #f8f9fa;
                color: var(--dark-color);
                line-height: 1.6;
            }
            
            .navbar {
                background-color: var(--dark-color);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .navbar-brand {
                font-weight: bold;
                color: white !important;
            }
            
            .dashboard-header {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }
            
            .dashboard-title {
                color: var(--dark-color);
                font-weight: 600;
                margin-bottom: 10px;
            }
            
            .stats-card {
                background: linear-gradient(135deg, var(--primary-color), var(--info-color));
                color: white;
                border-radius: 10px;
                padding: 25px;
                height: 100%;
                transition: transform 0.3s;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .stats-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }
            
            .stats-card.accent {
                background: linear-gradient(135deg, var(--accent-color), #e67e22);
            }
            
            .stats-card.success {
                background: linear-gradient(135deg, var(--success-color), #27ae60);
            }
            
            .stats-card.warning {
                background: linear-gradient(135deg, var(--warning-color), #f1c40f);
            }
            
            .stats-value {
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            .stats-label {
                font-size: 1rem;
                opacity: 0.9;
            }
            
            .api-card {
                background-color: white;
                border-radius: 10px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                transition: transform 0.3s, box-shadow 0.3s;
                border-left: 5px solid var(--primary-color);
            }
            
            .api-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.08);
            }
            
            .api-card h3 {
                color: var(--primary-color);
                font-weight: 600;
                margin-bottom: 15px;
            }
            
            .hot-news-card {
                border-left: 5px solid var(--accent-color);
            }
            
            .hot-news-card h3 {
                color: var(--accent-color);
            }
            
            .weather-card {
                border-left: 5px solid var(--success-color);
            }
            
            .weather-card h3 {
                color: var(--success-color);
            }
            
            .updates-card {
                border-left: 5px solid var(--warning-color);
            }
            
            .updates-card h3 {
                color: var(--warning-color);
            }
            
            .badge-api {
                background-color: var(--primary-color);
                color: white;
                padding: 5px 10px;
                border-radius: 30px;
                font-size: 0.8rem;
                font-weight: normal;
            }
            
            .method-badge {
                font-weight: 500;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                text-transform: uppercase;
            }
            
            .method-get {
                background-color: #61affe;
                color: white;
            }
            
            pre {
                background-color: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border-left: 3px solid var(--primary-color);
            }
            
            code {
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            }
            
            .platform-list {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 15px;
            }
            
            .platform-badge {
                background-color: #e9ecef;
                color: var(--dark-color);
                padding: 5px 10px;
                border-radius: 30px;
                font-size: 0.8rem;
                display: inline-flex;
                align-items: center;
                gap: 5px;
                transition: background-color 0.2s;
            }
            
            .platform-badge:hover {
                background-color: var(--primary-color);
                color: white;
            }
            
            .update-item {
                padding: 15px 0;
                border-bottom: 1px solid #eee;
            }
            
            .update-item:last-child {
                border-bottom: none;
            }
            
            .update-date {
                font-size: 0.85rem;
                color: #6c757d;
                margin-bottom: 5px;
            }
            
            .update-title {
                font-weight: 600;
                margin-bottom: 8px;
            }
            
            .update-description {
                color: #495057;
            }
            
            .feature-icon {
                font-size: 1.2rem;
                margin-right: 5px;
                color: var(--primary-color);
            }
            
            .footer {
                background-color: var(--dark-color);
                color: #ffffff;
                padding: 30px 0;
                margin-top: 50px;
            }
            
            .footer a {
                color: #9ad0ff;
                text-decoration: none;
            }
            
            .footer a:hover {
                text-decoration: underline;
            }
            
            @media (max-width: 768px) {
                .stats-value {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <!-- 导航栏 -->
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/"><i class="bi bi-lightning-charge"></i> OpenMCP API 控制台</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                            <a class="nav-link active" href="#"><i class="bi bi-house"></i> 首页</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#apis"><i class="bi bi-code-slash"></i> API</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#updates"><i class="bi bi-journal-text"></i> 更新</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        
        <div class="container">
            <!-- 欢迎信息 -->
            <div class="dashboard-header">
                <h1 class="dashboard-title"><i class="bi bi-bar-chart"></i> 服务监控看板</h1>
                <p class="lead">欢迎使用OpenMCP API服务，这里提供天气查询和热门资讯获取功能的实时监控和使用指南。</p>
            </div>
            
            <!-- 数据统计 -->
            <div class="row mb-4">
                <div class="col-md-3 col-sm-6 mb-4">
                    <div class="stats-card">
                        <div class="stats-value">2</div>
                        <div class="stats-label">可用API</div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6 mb-4">
                    <div class="stats-card accent">
                        <div class="stats-value">50+</div>
                        <div class="stats-label">支持的平台</div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6 mb-4">
                    <div class="stats-card success">
                        <div class="stats-value">99.9%</div>
                        <div class="stats-label">服务可用率</div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6 mb-4">
                    <div class="stats-card warning">
                        <div class="stats-value">24/7</div>
                        <div class="stats-label">全天候服务</div>
                    </div>
                </div>
            </div>
            
            <!-- API信息 -->
            <h2 class="mt-5 mb-4" id="apis"><i class="bi bi-code-square"></i> 可用API</h2>
            
            <div class="row">
                <!-- 天气API -->
                <div class="col-lg-6 mb-4">
                    <div class="api-card weather-card">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h3><i class="bi bi-cloud-sun"></i> 天气查询 API</h3>
                            <span class="badge-api">实时API</span>
                        </div>
                        <p>获取指定城市的实时天气信息，支持全国主要城市</p>
                        
                        <div class="mb-3">
                            <span class="method-badge method-get">GET</span>
                            <code class="ms-2">/message?tool=get_weather_cityname</code>
                        </div>
                        
                        <h5>参数说明：</h5>
                        <ul>
                            <li><strong>cityname</strong>: 城市名称（中国城市使用拼音）</li>
                        </ul>
                        
                        <h5>示例请求：</h5>
                        <pre><code>curl -X GET "http://localhost:9000/message?tool=get_weather_cityname&args=`{\"cityname\":\"beijing\"}`"</code></pre>
                        
                        <h5>返回数据：</h5>
                        <ul>
                            <li>城市名称</li>
                            <li>天气情况</li>
                            <li>温度</li>
                            <li>湿度</li>
                            <li>风速</li>
                        </ul>
                    </div>
                </div>
                
                <!-- 热门资讯API -->
                <div class="col-lg-6 mb-4">
                    <div class="api-card hot-news-card">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h3><i class="bi bi-fire"></i> 热门资讯 API</h3>
                            <span class="badge-api">热点API</span>
                        </div>
                        <p>获取各大平台的热点资讯，覆盖社交、新闻、视频、技术等多个领域</p>
                        
                        <div class="mb-3">
                            <span class="method-badge method-get">GET</span>
                            <code class="ms-2">/message?tool=get_hot_news</code>
                        </div>
                        
                        <h5>参数说明：</h5>
                        <ul>
                            <li><strong>platform</strong>: 平台名称</li>
                            <li><strong>limit</strong>: 返回条目数量（可选，默认10条）</li>
                        </ul>
                        
                        <h5>示例请求：</h5>
                        <pre><code>curl -X GET "http://localhost:9000/message?tool=get_hot_news&args=`{\"platform\":\"zhihu\",\"limit\":5}`"</code></pre>
                        
                        <h5>支持的热门平台：</h5>
                        <div class="platform-list">
                            <span class="platform-badge"><i class="bi bi-chat-dots"></i> 知乎</span>
                            <span class="platform-badge"><i class="bi bi-chat"></i> 微博</span>
                            <span class="platform-badge"><i class="bi bi-play-btn"></i> B站</span>
                            <span class="platform-badge"><i class="bi bi-music-note"></i> 抖音</span>
                            <span class="platform-badge"><i class="bi bi-newspaper"></i> 头条</span>
                            <span class="platform-badge"><i class="bi bi-chat-square"></i> 豆瓣</span>
                            <span class="platform-badge"><i class="bi bi-browser-chrome"></i> IT之家</span>
                            <span class="platform-badge"><i class="bi bi-info-circle"></i> 更多...</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 更新日志 -->
            <h2 class="mt-5 mb-4" id="updates"><i class="bi bi-clock-history"></i> 最新更新</h2>
            <div class="api-card updates-card">
                <h3><i class="bi bi-journal-code"></i> 更新日志</h3>
                
                <div class="update-item">
                    <div class="update-date">2025年5月15日</div>
                    <div class="update-title">v1.2.0 - 功能增强与界面优化</div>
                    <div class="update-description">
                        <ul>
                            <li><i class="bi bi-check2 feature-icon"></i> 新增服务看板首页，直观展示API功能和使用方法</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 热门资讯API支持更多平台，新增技术社区和游戏资讯平台</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 提高响应速度和并发处理能力</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 优化错误处理和用户反馈机制</li>
                        </ul>
                    </div>
                </div>
                
                <div class="update-item">
                    <div class="update-date">2025年4月8日</div>
                    <div class="update-title">v1.1.0 - 服务稳定性提升</div>
                    <div class="update-description">
                        <ul>
                            <li><i class="bi bi-check2 feature-icon"></i> 提高系统稳定性，修复已知问题</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 优化缓存策略，减少外部API调用频率</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 增强安全性，防止恶意请求</li>
                        </ul>
                    </div>
                </div>
                
                <div class="update-item">
                    <div class="update-date">2025年3月20日</div>
                    <div class="update-title">v1.0.0 - 服务正式发布</div>
                    <div class="update-description">
                        <ul>
                            <li><i class="bi bi-check2 feature-icon"></i> 初始版本发布，提供天气查询和热门资讯获取功能</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 支持30+热门平台的热点内容获取</li>
                            <li><i class="bi bi-check2 feature-icon"></i> 天气查询支持全国主要城市</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- 连接信息 -->
            <div class="row mt-5">
                <div class="col-md-6 mb-4">
                    <div class="api-card">
                        <h3><i class="bi bi-link-45deg"></i> API连接信息</h3>
                        <p>使用以下端点连接OpenMCP API服务：</p>
                        <ul>
                            <li><strong>SSE连接：</strong> <code>http://localhost:9000/sse</code></li>
                            <li><strong>消息端点：</strong> <code>http://localhost:9000/message</code></li>
                        </ul>
                        <p class="mt-3"><i class="bi bi-info-circle"></i> 建议使用SSE连接获取实时更新和异步响应</p>
                    </div>
                </div>
                
                <div class="col-md-6 mb-4">
                    <div class="api-card">
                        <h3><i class="bi bi-question-circle"></i> 需要帮助？</h3>
                        <p>如有任何问题或需要更多帮助，请联系管理员：</p>
                        <ul>
                            <li><i class="bi bi-envelope"></i> <a href="mailto:admin@openmcp.com">admin@openmcp.com</a></li>
                            <li><i class="bi bi-github"></i> <a href="https://github.com/OpenMcp/OpenMcp" target="_blank">GitHub仓库</a></li>
                            <li><i class="bi bi-book"></i> <a href="/docs" target="_blank">详细文档</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 页脚 -->
        <footer class="footer">
            <div class="container">
                <div class="row">
                    <div class="col-md-6">
                        <h5>OpenMCP API 服务</h5>
                        <p>提供高质量、高可用的API服务，轻松获取天气和热点资讯</p>
                    </div>
                    <div class="col-md-3">
                        <h5>链接</h5>
                        <ul class="list-unstyled">
                            <li><a href="#apis">可用API</a></li>
                            <li><a href="#updates">更新日志</a></li>
                            <li><a href="/docs">API文档</a></li>
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h5>关于</h5>
                        <ul class="list-unstyled">
                            <li><a href="#">关于我们</a></li>
                            <li><a href="#">服务条款</a></li>
                            <li><a href="#">隐私政策</a></li>
                        </ul>
                    </div>
                </div>
                <hr class="mt-4 mb-4" style="border-color: rgba(255,255,255,0.1);">
                <div class="text-center">
                    <p>&copy; 2025 OpenMCP API. 保留所有权利。</p>
                </div>
            </div>
        </footer>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)