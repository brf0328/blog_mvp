from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.core.security import get_password_hash, verify_password
from app.models.models import User
from tortoise.transactions import atomic
# 创建路由器
router = APIRouter()

# 注册请求模型
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    
# 登录响应模型
class UserLogin(BaseModel):
    username: str
    email: str
    access_token: str
    
# 用户信息响应模型
class UserInfo(BaseModel):
    username: str
    email: str

# 注册接口
@atomic
@router.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    用户注册接口
    
    1. 验证用户名和邮箱是否已存在
    2. 对密码进行哈希处理
    3. 创建新用户
    """
    # 检查用户名是否已存在
    existing_user = await User.filter(username=user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被使用"
        )
    
    # 检查邮箱是否已存在
    existing_email = await User.filter(email=user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 对密码进行哈希处理
    hashed_password = get_password_hash(user_data.password)
    
    # 创建新用户
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    
    return {"username": user.username, "email": user.email}

# 登录接口
@atomic
@router.post("/login", response_model=UserLogin)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),grant_type:str="password"):#自动获取表单数据
    """
    用户登录接口
    
    1. 验证用户是否存在
    2. 验证密码是否正确
    3. 创建会话并设置Cookie
    """
    # 查询用户
    user = await User.filter(username=form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证密码
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建简单的会话Token (在实际应用中应使用JWT或其他安全方式)
    # 这里简单使用用户ID作为会话标识
    session_id = f"session_{user.id}"
    
    # 设置Cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,#cookie只允许被http协议访问
        max_age=1800,  # 30分钟过期
        samesite="lax"#防止跨站攻击
    )
    
    # 返回登录成功的信息和访问令牌
    return {
        "username": user.username,
        "email": user.email,
        "access_token": session_id
    }

# 获取当前用户信息
@router.get("/me", response_model=UserInfo)
async def get_current_user(session_id: Optional[str] = None):
    """获取当前登录用户信息"""
    # 这里应该根据会话ID获取用户信息
    # 在实际应用中，需要使用JWT或其他会话管理方式
    
    # 示例逻辑，实际应用中需要替换成真实的会话验证逻辑
    if not session_id or not session_id.startswith("session_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或会话已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = int(session_id.replace("session_", ""))
        user = await User.get(id=user_id)
        return {"username": user.username, "email": user.email}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或会话已过期",
            headers={"WWW-Authenticate": "Bearer"},
        ) 