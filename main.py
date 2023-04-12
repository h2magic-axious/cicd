import base64
import importlib
import json

from fastapi import FastAPI, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from tortoise.contrib.fastapi import register_tortoise

from utils.reference import response_result, try_to_do
from utils.settings import *
from utils.whitelist import check_whitelist
from utils.administrator import administrator

app = FastAPI(default_response_class=ORJSONResponse)
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

for app_name in BASE_DIR.joinpath("apps").iterdir():
    name = app_name.name
    if app_name.is_dir() and name != "__pycache__":
        print("导入应用: ", name)
        # 导入 Router
        try:
            r = importlib.import_module(f"apps.{name}.router")
            app.include_router(r.router)
        except Exception as e:
            print(f"未找到路由表: apps.{name}.router: {e}")

        # 导入 Signals
        if app_name.joinpath("signals.py").exists():
            importlib.import_module(f"apps.{name}.signals")


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
def check_token(request: Request):
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
        return RedirectResponse(url=app.url_path_for("service_index"))
    if check_whitelist(request.url.path):
        return await _response(request, call_next)

    status, token = check_token(request)
    if not status or token is None:
        return RedirectResponse(url=app.url_path_for("service_login"), headers={"Context-Type": "text/html"})

    try:
        if administrator.parse(token) != administrator:
            return Response("Invalid Token", status_code=400)
    except Exception as e:
        print("Token解析错误: {e}")
        return RedirectResponse(url=app.url_path_for("service_login"), headers={"Context-Type": "text/html"})

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
    assert administrator.check(body["username"], body["password"]) is True
    request.session["token"] = administrator.token
    return response_result(1, request.session["token"])
