from fastapi import APIRouter
from app.api import posts, auth, categories, tags

# 创建主路由
router = APIRouter()

# 注册子路由
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
router.include_router(categories.router, prefix="/categories", tags=["categories"])
router.include_router(tags.router, prefix="/tags", tags=["tags"])

# 这里缺少分类和标签的路由注册