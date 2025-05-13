from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.delete import router as delete_router
# 创建主路由
router = APIRouter()

# 注册认证路由
router.include_router(auth_router, prefix="/auth", tags=["认证"]) 
router.include_router(delete_router, prefix="/delete", tags=["删除"])