# 使用 Python 3.12 slim 作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝代码
COPY server server
COPY frontend frontend

# 启动命令（根据你的项目实际情况修改）
CMD ["python", "server/start_server.py"]