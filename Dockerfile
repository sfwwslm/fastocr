FROM python:3.10-slim

LABEL maintainer="sfwwslm@gmail.com"

WORKDIR /usr/local/fastocr

COPY app /usr/local/fastocr/app

# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \ # 2024年8月5日 阿里源变得很慢
RUN pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/ \
    && pip install --no-cache-dir -r app/requirements.txt

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "20000"]
