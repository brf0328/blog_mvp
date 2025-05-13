from passlib.context import CryptContext
from typing import Optional

# 创建密码上下文，使用bcrypt算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    使用bcrypt对密码进行哈希
    
    Args:
        password: 原始密码
        
    Returns:
        哈希后的密码字符串
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    Args:
        plain_password: 用户提供的明文密码
        hashed_password: 数据库中存储的哈希密码
        
    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password) 