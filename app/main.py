import time

import ddddocr
import onnxruntime
import uvicorn
from fastapi import FastAPI, Header, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Pillow==9.5.0 依赖问题
# from PIL import Image
# if not hasattr(Image, 'ANTIALIAS'):
#     setattr(Image, 'ANTIALIAS', Image.LANCZOS)
# 抑制警告信息
onnxruntime.set_default_logger_severity(3)


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='/static/js/swagger-ui-bundle.js',
        # swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='/static/css/swagger-ui.css'
        # swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch


async def sleep(x_sleep: int | None = Header(default=None, description="设置延迟响应时间(秒)")):
    if x_sleep:
        time.sleep(x_sleep)


# app = FastAPI(dependencies=[Depends(sleep)])
app = FastAPI(dependencies=[], docs_url=None, redoc_url=None)

# 将静态文件路径映射到指定的目录
app.mount("/static", StaticFiles(directory="app/static"), name="static")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,

    # 允许跨域请求的源列表
    allow_origins=origins,

    # 跨域请求支持 cookies
    allow_credentials=False,

    # 跨域请求的 HTTP 方法列表
    allow_methods=["*"],

    # 跨域请求允许使用的 HTTP 请求头列表
    allow_headers=["*"],
)


@app.get("/", tags=['FastAPI'])
async def main():
    return "Hello World!"


class RqCaptchaModel(BaseModel):
    """验证码请求模型"""
    img: str
    length: int | None = None


class RpCaptchaModel(BaseModel):
    """验证码响应模型"""
    code: str | None = None
    length: int | None = None
    result: bool = True
    message: str | None = None


@app.post("/ocr", response_model=RpCaptchaModel, name='识别验证码')
async def ocr(body: RqCaptchaModel):
    """
    对验证码图像进行光学字符识别（OCR）。

    Args：
        img：要进行OCR的验证码图像。
        length: 预期验证码的长度。

    Returns：
        包含OCR结果代码、结果长度和表示OCR过程状态的消息的字典。

    Examples：

    ```js
        /**
        * 对图像进行光学字符识别（OCR）。
        * @async
        * @param {string} img - 要进行OCR的图像。
        * @param {number} len - 预期验证码的长度，如果有就校验。
        * @param {function} f - 处理OCR结果的回调函数。
        * @returns {Promise} - 一个解析为OCR结果的Promise。
        * @throws {Error} - 如果网络请求失败或OCR结果不成功。
        */
        async function ocr(img, len, f) {
            let response = await fetch("https://localhost/ocr", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    "img": img,
                    "length": len
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error('网络请求失败');
                }
                return response.json();
            }).then(data => {
                if (data.result) {
                    return data
                } else {
                    throw new Error(data.message);
                };
            })
                .catch(error => { return error });

            let json = await response;
            console.log(json);
            // f(json);
        }

    ```

    ```python
    data = {"img": data,"length": 4}
    rp = requests.post(url="https://localhost/ocr", json=data, verify=False)
    print(rp.json())
    ```

    ```python
    import base64
    import json
    import urllib.request

    def parse(img: bytes, show: bool = False):
        url = "http://10.121.111.124:8000/ocr"
        data = {"img": base64.b64encode(img).decode('utf-8')}
        data_encoded = json.dumps(data).encode('utf-8')

        req = urllib.request.Request(url, data=data_encoded, method="POST")
        req.add_header("Content-Type", "application/json")

        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')  # 读取响应内容并解码为字符串

        json_data = json.loads(response_data)
        if show:
            print(json_data)
        return json_data["code"]

    ```

    """
    return ocr(body)


def check_data(data: str):
    if data.startswith("data:image/"):
        return data.split(',')[1]
    return data


def ocr(body: RqCaptchaModel):
    ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
    try:
        base64_data = check_data(body.img)
        resp = ocr.classification(base64_data)
    except Exception as err:
        error = {"code": None, "length": None,
                 "result": False, "message": f"识别出现问题！{err}"}
        print(error)
        return error
    if body.length and len(resp) != body.length:
        error = {"code": None, "length": None,
                 "result": False, "message": "验证码长度不匹配！"}
        print(error)
        return error
    return {"code": resp, "length": len(resp), "message": "验证码已识别！"}


if __name__ == '__main__':
    # uvicorn app.main:app --reload --host 0.0.0.0 --port 20000
    uvicorn.run(app='main:app', host='0.0.0.0', port=20000, reload=True)
