from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.models import Category, User
from app.schemas import CategoryCreate, CategoryRead
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CategoryRead)
async def create_category(category: CategoryCreate, current_user: User = Depends(get_current_user)):
    """创建新分类"""
    # 检查分类是否已存在
    existing = await Category.filter(name=category.name).first()
    if existing:
        # 如果分类已存在，直接返回
        return existing
    
    # 创建分类
    cat_obj = await Category.create(name=category.name)
    return cat_obj

@router.get("/", response_model=List[CategoryRead])
async def get_categories():
    """获取所有分类"""
    return await Category.all()

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, current_user: User = Depends(get_current_user)):
    """删除分类"""
    category = await Category.get_or_none(id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    await category.delete()
    return None 