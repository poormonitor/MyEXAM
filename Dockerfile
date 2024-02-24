FROM python:3.11-slim

COPY requirements.txt .
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources
RUN apt update && apt install -y patch build-essential swig
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app
VOLUME /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "2", "--port", "8000"]
