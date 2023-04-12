import base64
import json

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise

from utils.administrator import check_admin, build_token, check_token
from utils.reference import response_result, try_to_do
from utils.settings import *
from utils.whitelist import check_whitelist

from service import api_router, page_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# 增加Session
app.add_middleware(SessionMiddleware, secret_key=Env.SECRET_KEY)

app.include_router(api_router.router)
app.include_router(page_router.router)


async def _response(request, call_next):
    try:
        response = await call_next(request)
    except Exception as e1:
        response = Response(f"请求失败: {e1}")
        response.headers.update({
            "access-control-allow-methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
            "access-control-allow-credentials": "true",
            "access-control-allow-allow-origin": "*"
        })

    return response


@try_to_do
def has_token(request: Request):
    if token := request.headers.get("Authorization"):
        t = token.replace("Bearer ", "")
        return t

    if session := request.cookies.get("session"):
        t = base64.b64decode(session.split(".")[0])
        return json.loads(t)["token"]


# http 拦截器
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.url.path == "/":
        return RedirectResponse(url="/service/index")
    if check_whitelist(request.url.path):
        return await _response(request, call_next)

    status, token = has_token(request)
    if not status or token is None or not check_token(token):
        return RedirectResponse(url="/service/login", headers={"Context-Type": "text/html"})

    return await _response(request, call_next)


# 所有应用的model注册到数据库
register_tortoise(
    app,
    config={
        "connections": DATABASE,
        "apps": {"models": {"models": DATABASE_MODELS}},
        "use_tz": True,
        "timezone": "Asia/Shanghai",
    },
    generate_schemas=True,
)


@app.get("/health")
async def health():
    return "Health"


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    assert check_admin(body["username"], body["password"]) is True
    request.session["token"] = (token := build_token())
    return response_result(1, token)
