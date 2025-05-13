from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.core.security import get_password_hash, verify_password
from app.models.models import User
from tortoise.transactions import atomic
router = APIRouter()
@atomic
@router.delete("/users/{username}", status_code=status.HTTP_200_OK)
async def delete_user(username: str):
    user = await User.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await user.delete()
    return {"detail": "用户已删除"}