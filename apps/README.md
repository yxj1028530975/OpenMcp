# OpenMCP 应用

这个目录包含OpenMCP应用的核心代码。本项目使用uv包管理工具代替传统的pip和requirements.txt。

## 快速开始

### 使用uv安装依赖

1. 安装uv：
```bash
# Linux/macOS
curl -sSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. 创建虚拟环境并安装依赖：
```bash
uv venv .venv
uv pip sync
```

3. 激活虚拟环境：
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. 运行应用：
```bash
python main.py
```

## 开发指南

### 添加新依赖

使用uv添加新依赖会自动更新pyproject.toml和uv.lock文件：
```bash
uv pip install package_name
```

### 更新依赖

更新所有依赖：
```bash
uv pip sync --upgrade
```

更新特定依赖：
```bash
uv pip install --upgrade package_name
```

### 项目结构

- `main.py` - 应用入口点
- `common/` - 通用工具和辅助函数
- `application/` - 应用核心逻辑
- `test/` - 测试代码
- `pyproject.toml` - 项目配置和依赖定义
- `uv.lock` - 依赖锁定文件，确保依赖版本一致

## Docker部署

有关Docker部署的详细信息，请参阅`/docker/README.md`。
