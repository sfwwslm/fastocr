FROM python:3.10-slim

LABEL maintainer="sfwwslm@gmail.com"

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /usr/local/fastocr

COPY ./requirements.txt /usr/local/fastocr/requirements.txt

# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \ # 2024年8月5日 阿里源变得很慢
RUN pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/ \
&& pip install --no-cache-dir -r requirements.txt

COPY app /usr/local/fastocr/app

EXPOSE 20000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "20000"]
