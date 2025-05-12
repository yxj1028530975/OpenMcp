# OpenMCP Docker 部署指南

这个目录包含了部署OpenMCP应用的Docker配置文件。

## 目录结构

- `Dockerfile.backend` - 后端API服务的Docker镜像构建文件
- `docker-compose.yml` - 使用Docker Compose管理多容器应用
- `setup-mirror.sh` - 配置国内镜像源的脚本（可选）

## 快速开始

1. 确保已安装Docker和Docker Compose
2. 在项目根目录创建`.env`文件（可选，用于自定义环境变量）
3. 执行以下命令启动服务:

```bash
cd docker
docker-compose up -d
```

## 环境变量

您可以通过创建`.env`文件或在执行`docker-compose`命令时设置以下环境变量：

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| BACKEND_PORT | 9000 | 后端API服务的对外端口 |
| DAILYHOT_API_PORT | 6688 | 热榜API服务的对外端口 |
| DAILYHOT_API_URL | http://dailyhot-api:6688 | 热榜API服务的URL |
| BACKEND_CORS_ORIGINS | ["http://localhost","http://localhost:80"] | 允许跨域访问的源 |
| TIMEZONE | Asia/Shanghai | 容器的时区设置 |

## 服务访问

启动成功后，可通过以下URL访问相应服务：

- 后端API服务: `http://localhost:9000`
- 热榜API服务: `http://localhost:6688`

## 使用uv包管理

本项目使用了uv包管理工具替代传统的pip。如果需要更新依赖，可以：

1. 在本地使用uv更新依赖：
```bash
# 安装uv
curl -sSf https://astral.sh/uv/install.sh | sh

# 导出依赖到requirements.txt
uv pip freeze > requirements.txt
```

2. 重新构建Docker镜像：
```bash
docker-compose build --no-cache backend
docker-compose up -d
```

## 开发模式

如果您想在开发模式下使用Docker：

1. 修改`docker-compose.yml`中的volumes部分移除`:ro`（只读）标志，允许容器内写入文件：
```yaml
volumes:
  - ../apps:/app/apps
```

2. 可以添加开发工具（如调试器）到Dockerfile中：
```dockerfile
RUN pip install debugpy
```

## 故障排除

如果您遇到问题：

1. 检查容器日志：
```bash
docker-compose logs -f backend
```

2. 进入容器内部检查：
```bash
docker-compose exec backend /bin/sh
```

3. 检查网络连接：
```bash
docker network inspect openmcp-network
```

4. 常见问题：
   - 如果热榜API无法访问，检查`DAILYHOT_API_URL`环境变量是否正确设置
   - 如果端口冲突，修改`.env`文件中的相应端口配置

## Docker Compose命令参考

```bash
# 启动所有服务
docker-compose up -d

# 仅启动后端服务
docker-compose up -d backend

# 重新构建并启动服务
docker-compose up -d --build

# 停止所有服务
docker-compose down

# 停止并删除所有容器和网络
docker-compose down -v

# 查看服务状态
docker-compose ps

# 进入容器内部(例如进入后端容器)
docker-compose exec backend bash
```

## 进阶配置

### 性能优化

- **后端服务**: 可以调整uvicorn的工作进程数和线程数
```yaml
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

- **Nginx配置**: 可以调整工作进程数和连接数，在nginx.conf中添加
```
worker_processes auto;
worker_connections 1024;
```

### 使用外部数据源

如果您需要将热榜API服务替换为外部数据源，请修改`.env`文件中的`DAILYHOT_API_URL`变量，并删除`docker-compose.yml`中的`dailyhot-api`服务部分。

### 生产环境部署建议

对于生产环境，建议额外配置：

1. **HTTPS支持**: 更新Nginx配置，添加SSL证书
2. **环境隔离**: 为开发、测试和生产环境使用不同的docker-compose文件
3. **资源限制**: 在docker-compose.yml中添加资源限制
```yaml
services:
  backend:
    # ...
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```
4. **监控和日志**: 集成Prometheus、Grafana和ELK等工具
5. **数据持久化**: 配置适当的卷挂载，保存重要数据 