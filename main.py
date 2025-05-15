import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from config.settings import TORTOISE_ORM
from app.api import router as api_router
from app.views import router as views_router
import os
import logging
from pathlib import Path

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

# 该方法会在fastapi启动时触发，内部通过传递进去的app对象，监听服务启动和终止事件
# 当检测到启动事件时，会初始化Tortoise对象，如果generate_schemas为True则还会进行数据库迁移
# 当检测到终止事件时，会关闭连接
register_tortoise(
    app = app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 开发环境中启用自动生成模式
    add_exception_handlers=True,  # 开发环境中启用异常处理
)

@app.on_event("startup")
async def startup_event():
    logger.info("应用启动")
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("应用关闭")

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level='info', workers=1)