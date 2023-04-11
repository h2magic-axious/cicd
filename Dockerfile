FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install git -y &&  \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install -r requirements.txt

ENV GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

EXPOSE 80

CMD ["./start.sh"]