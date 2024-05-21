FROM python:3.10-slim

WORKDIR /usr/local/fastocr

COPY app /usr/local/fastocr/app

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --no-cache-dir -r app/requirements.txt

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "20000"]
