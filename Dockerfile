FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN chmod ugo+x start.sh && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install -r requirements.txt


EXPOSE 80

CMD ["./start.sh"]