# OpenMCP Docker 部署指南

这个目录包含了部署OpenMCP应用的Docker配置文件。本项目使用uv包管理工具和现代化Python项目结构，依赖通过`pyproject.toml`和`uv.lock`文件管理。

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

## 依赖管理 (使用 uv)

本项目使用uv包管理工具替代传统的pip和requirements.txt。uv是一个现代化的Python包管理器，具有更快的安装速度、更可靠的依赖解析和更好的缓存机制。

### 为什么使用uv而不是requirements.txt

- **更快的安装速度**: uv安装依赖比pip快5-10倍
- **确定性构建**: 使用uv.lock文件确保依赖版本一致
- **更好的缓存**: 使用持久化缓存卷提高重复构建速度
- **现代化项目结构**: 通过pyproject.toml集中管理项目配置

### 如何使用uv管理依赖

1. **安装uv**:
```bash
# 在Linux/macOS上安装
curl -sSf https://astral.sh/uv/install.sh | sh

# 在Windows上安装
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. **添加新依赖**:
```bash
cd apps
uv pip install package_name
```
这会自动更新pyproject.toml和uv.lock文件。

3. **从现有配置安装依赖**:
```bash
cd apps
uv pip sync
```

4. **导出为requirements.txt** (如果需要):
```bash
cd apps
uv pip freeze > requirements.txt
```

### 在Docker中使用uv

我们的Dockerfile已配置为使用uv:
- 先复制pyproject.toml和uv.lock文件
- 使用uv安装依赖
- 使用持久化缓存卷加速重复构建

如果更新了依赖，重新构建Docker镜像即可:
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

2. 使用uv的开发模式安装依赖:
```dockerfile
RUN uv pip install --dev --system -i https://mirrors.aliyun.com/pypi/simple/ .
```

3. 对于本地开发，您可以创建一个独立的虚拟环境:
```bash
cd apps
uv venv .venv
uv pip sync
source .venv/bin/activate  # 在Linux/macOS上
# 或者
.venv\Scripts\activate     # 在Windows上
```

## 故障排除

如果您遇到依赖相关问题：

1. **检查uv.lock文件是否存在并最新**:
```bash
ls -la apps/uv.lock
```

2. **重新生成uv.lock文件**:
```bash
cd apps
uv pip sync --upgrade
```

3. **检查容器内的依赖**:
```bash
docker-compose exec backend python -m pip list
```

4. **uv缓存问题**:
```bash
# 清除uv缓存
docker-compose down
docker volume rm openmcp-uv-cache
docker-compose up -d
```

5. **其他常见问题**:
   - 如果热榜API无法访问，检查`DAILYHOT_API_URL`环境变量是否正确设置
   - 如果端口冲突，修改`.env`文件中的相应端口配置
   - 如果依赖安装失败，检查`pyproject.toml`中的依赖配置

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
docker-compose exec backend /bin/sh
```

## 进阶配置

### 优化Docker构建

- **多阶段构建**: 对于复杂项目可以考虑使用多阶段构建减小最终镜像大小
```dockerfile
FROM python:3.12-alpine AS builder
# 安装uv和依赖
RUN curl -sSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"
COPY apps/pyproject.toml apps/uv.lock /app/
WORKDIR /app
RUN uv pip install --system --no-deps .

FROM python:3.12-alpine
# 只复制已安装的依赖和必要文件
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY apps /app/apps
```

### 使用外部数据源

如果您需要将热榜API服务替换为外部数据源，请修改`.env`文件中的`DAILYHOT_API_URL`变量，并删除`docker-compose.yml`中的`dailyhot-api`服务部分。

### 生产环境部署建议

对于生产环境，建议额外配置：

1. **HTTPS支持**: 配置反向代理如Nginx或Traefik，处理SSL终结
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