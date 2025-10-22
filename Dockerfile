FROM python:3.12-slim  # 基础镜像：Python 3.12 轻量版
WORKDIR /app           # 设置容器内工作目录
COPY requirements.txt . # 复制依赖清单到工作目录
RUN pip install -r requirements.txt  # 安装 Python 依赖
COPY . .               # 复制项目所有文件到工作目录
CMD ["python", "app.py"]  # 容器启动命令：运行主程序