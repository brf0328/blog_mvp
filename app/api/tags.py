from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.models import Tag, User
from app.schemas import TagCreate, TagRead
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TagRead)
async def create_tag(tag: TagCreate, current_user: User = Depends(get_current_user)):
    """创建新标签"""
    # 检查标签是否已存在
    existing = await Tag.filter(name=tag.name).first()
    if existing:
        # 如果标签已存在，直接返回
        return existing
    
    # 创建标签
    tag_obj = await Tag.create(name=tag.name)
    return tag_obj

@router.get("/", response_model=List[TagRead])
async def get_tags():
    """获取所有标签"""
    return await Tag.all()

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, current_user: User = Depends(get_current_user)):
    """删除标签"""
    tag = await Tag.get_or_none(id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    await tag.delete()
    return None 