# 基础镜像（精简 Python 环境）
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 关键1：安装 git（解决 git-python 依赖）
# 更新包索引 + 安装 git + 清理缓存（减少镜像体积）
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 关键2：设置 Python 搜索路径，确保能找到 app 模块
ENV PYTHONPATH=/app

# 复制依赖文件并安装 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有项目文件
COPY . .

# 容器启动命令（用模块方式运行，确保路径正确）
CMD ["python", "-m", "app.main"]