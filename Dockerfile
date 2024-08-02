FROM python:3.10

# 設定工作目錄
WORKDIR /threatter

# 複製 requirements.txt 到容器中
COPY requirements.txt .

# 升級 pip 並安裝依賴
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install cryptography

# 安裝 Vim
RUN apt-get update \
    && apt-get install -y vim

# 複製當前目錄下的所有文件到容器中的工作目錄
COPY . /threatter

# 容器啟動時執行的命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


