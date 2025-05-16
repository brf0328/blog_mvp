import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from config.settings import TORTOISE_ORM
from app.api import router as api_router
from app.views import router as views_router
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置Jinja2Templates
templates = Jinja2Templates(directory="templates")

# 注册API路由
app.include_router(api_router, prefix="/api")

# 注册视图路由
app.include_router(views_router)

# 注册Tortoise ORM
register_tortoise(
    app = app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='info', workers=1)