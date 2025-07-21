# 使用官方 Python 映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 暴露端口
EXPOSE 5000

# 設定環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 啟動應用程式
CMD ["python", "app.py"]
