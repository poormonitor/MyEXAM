FROM python:3.11-slim

ARG CN="N"
ARG CN_MIRROR="mirrors.bfsu.edu.cn"

COPY requirements.txt .

RUN [ "$CN" != "N" ] && \
    sed -i "s/deb.debian.org/${CN_MIRROR}/g" /etc/apt/sources.list.d/debian.sources || true
RUN apt-get -y update  && \
    apt-get -y upgrade && \
    apt install -y patch build-essential swig git

RUN [ "$CN" != "N" ] &&  \
    pip config set global.index-url "https://${CN_MIRROR}/pypi/web/simple" || true
RUN pip install -r requirements.txt --no-cache-dir

RUN git config --global --add safe.directory /app

WORKDIR /app
VOLUME /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "2", "--port", "8000"]
