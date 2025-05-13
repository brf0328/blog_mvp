import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.settings import TORTOISE_ORM
from app.api import router as api_router

app = FastAPI()
app.include_router(api_router)

# 该方法会在fastapi启动时触发，内部通过传递进去的app对象，监听服务启动和终止事件
# 当检测到启动事件时，会初始化Tortoise对象，如果generate_schemas为True则还会进行数据库迁移
# 当检测到终止事件时，会关闭连接
register_tortoise(
    app = app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 开发环境中启用自动生成模式
    add_exception_handlers=True,  # 开发环境中启用异常处理
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, log_level= 'debug', workers=1)