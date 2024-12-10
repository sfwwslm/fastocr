FROM python:3.12-slim

LABEL maintainer="sfwwslm@gmail.com"

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

WORKDIR /fastocr

COPY ./pyproject.toml ./README.md /fastocr/

# RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
RUN pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/ \
&& pip install --no-cache-dir .

COPY app /fastocr/app

EXPOSE 20000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "20000"]
