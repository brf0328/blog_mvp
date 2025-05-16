from fastapi import APIRouter
from typing import List
from app.models.models import Category
from app.schemas import CategoryRead

router = APIRouter()

@router.get("/", response_model=List[CategoryRead])
async def get_categories():
    """获取所有分类"""
    return await Category.all() 