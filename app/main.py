import ddddocr
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from pydantic import BaseModel


app = FastAPI(dependencies=[], docs_url=None, redoc_url=None)

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


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    # 添加判断确保 openapi_url 存在
    if app.openapi_url is None:
        raise Exception("OpenAPI schema URL is not available")
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="使用说明",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )


class ReqModel(BaseModel):
    """验证码请求模型"""

    img: str
    length: int | None = None


class ResModel(BaseModel):
    """验证码响应模型"""

    code: str | None = None
    length: int | None = None
    result: bool = True
    message: str | None = None


@app.post("/ocr", response_model=ResModel, name="识别验证码")
async def main(body: ReqModel):
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
    """
    return ocr(body)


@app.get("/", name="测试ocr是否正常", tags=["FastAPI"], response_class=HTMLResponse)
async def test():
    with TestClient(app) as client:
        b64 = "data:image/jpeg;base64,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"
        response = client.post("/ocr", json={"img": b64, "length": 4}).json()
        if response["code"] == "ACVD":
            return "<h1>基于 FastAPI 和 ddddocr 的 OCR API 服务</h1>"
        return "<h1>验证码识别失败</h1>"


def check_data(data: str):
    if data.startswith("data:image/"):
        return data.split(",")[1]
    return data


def ocr(body: ReqModel):
    ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
    try:
        base64_data = check_data(body.img)
        resp = ocr.classification(base64_data)
    except Exception as err:
        error = {
            "code": None,
            "length": None,
            "result": False,
            "message": f"识别出现问题！{err}",
        }
        print(error)
        return error
    if body.length and len(resp) != body.length:
        error = {
            "code": None,
            "length": None,
            "result": False,
            "message": "验证码长度不匹配！",
        }
        print(error)
        return error
    return {
        "code": resp,
        "length": len(resp),
        "message": "验证码已识别！",
    }


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=20001, reload=True)
