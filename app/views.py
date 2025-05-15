from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models.models import Post, Category, Tag
from app.api.auth import get_current_user_optional, get_current_user
from app.models.models import User
import math

router = APIRouter()
templates = Jinja2Templates(directory="templates")
# 首页
@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    category_id: int = None,
    tag_id: int = None,
    current_user: User = Depends(get_current_user_optional)
):
    """首页，显示文章列表"""
    # 构建查询
    query = Post.filter(is_published=True)
    
    # 按分类筛选
    if category_id:
        query = query.filter(categories__id=category_id)
    
    # 按标签筛选
    if tag_id:
        query = query.filter(tags__id=tag_id)
    
    # 计算分页
    total = await query.count()
    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page
    
    # 获取文章列表
    posts = await query.order_by("-created_at").offset(offset).limit(per_page).prefetch_related(
        "author", "categories", "tags"
    )
    
    # 获取所有分类和标签（用于侧边栏）
    categories = await Category.all()
    tags = await Tag.all()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "posts": posts,
            "page": page,
            "total_pages": total_pages,
            "categories": categories,
            "tags": tags,
            "current_category_id": category_id,
            "current_tag_id": tag_id,
            "user": current_user
        }
    )

@router.get("/manage-categories-tags", response_class=HTMLResponse)
async def manage_categories_tags(
    request: Request,
    current_user: User = Depends(get_current_user)  # 必须登录
):
    """管理分类和标签页面"""
    # 获取所有分类和标签
    categories = await Category.all()
    tags = await Tag.all()
    
    return templates.TemplateResponse(
        "manage_categories_tags.html",
        {
            "request": request,
            "user": current_user,
            "categories": categories,
            "tags": tags
        }
    )

@router.get("/posts/new", response_class=HTMLResponse)
async def create_post_form(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """创建文章表单"""
    # 获取所有分类和标签
    categories = await Category.all()
    tags = await Tag.all()
    
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "post": None,
            "categories": categories,
            "tags": tags,
            "user": current_user
        }
    )

@router.get("/posts/edit/{post_id}", response_class=HTMLResponse)
async def edit_post_form(
    request: Request,
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    """编辑文章表单"""
    # 获取文章，并检查权限
    post = await Post.get_or_none(id=post_id).prefetch_related("categories", "tags")
    
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=404, detail="文章不存在或您无权编辑")
    
    # 获取所有分类和标签
    categories = await Category.all()
    tags = await Tag.all()
    
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "post": post,
            "categories": categories,
            "tags": tags,
            "user": current_user
        }
    )

@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def post_detail(
    request: Request,
    post_id: int,
    current_user: User = Depends(get_current_user_optional)
):
    """文章详情页"""
    post = await Post.get_or_none(id=post_id).prefetch_related(
        "author", "categories", "tags"
    )
    
    if not post or (not post.is_published and (not current_user or current_user.id != post.author_id)):
        raise HTTPException(status_code=404, detail="文章不存在或未发布")
    
    # 获取所有分类和标签（用于侧边栏）
    categories = await Category.all()
    tags = await Tag.all()
    
    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "post": post,
            "categories": categories,
            "tags": tags,
            "user": current_user
        }
    )

@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    page: int = 1,
    per_page: int = 5,
    current_user: User = Depends(get_current_user)  # 必须登录
):
    """用户个人主页"""
    # 构建查询 - 获取当前用户的所有文章，包括草稿
    query = Post.filter(author_id=current_user.id)
    
    # 计算分页
    total = await query.count()
    total_pages = math.ceil(total / per_page)
    offset = (page - 1) * per_page
    
    # 获取文章列表
    posts = await query.order_by("-created_at").offset(offset).limit(per_page).prefetch_related(
        "categories", "tags"
    )
    
    # 获取用户的所有分类和标签
    user_categories = set()
    user_tags = set()
    
    for post in await Post.filter(author_id=current_user.id).prefetch_related("categories", "tags"):
        for category in await post.categories.all():
            user_categories.add(category)
        for tag in await post.tags.all():
            user_tags.add(tag)
    
    # 获取所有分类和标签（用于侧边栏）
    all_categories = await Category.all()
    all_tags = await Tag.all()
    
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": current_user,
            "posts": posts,
            "posts_count": total,
            "page": page,
            "total_pages": total_pages,
            "user_categories": list(user_categories),
            "user_tags": list(user_tags),
            # 侧边栏数据
            "categories": all_categories,
            "tags": all_tags,
        }
    )

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, current_user: User = Depends(get_current_user_optional)):
    """登录页面"""
    # 如果用户已登录，重定向到首页
    if current_user:
        return RedirectResponse(url="/")
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "user": None, "categories": [], "tags": []}
    )

@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request, current_user: User = Depends(get_current_user_optional)):
    """注册页面"""
    # 如果用户已登录，重定向到首页
    if current_user:
        return RedirectResponse(url="/")
    
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "user": None, "categories": [], "tags": []}
    )

@router.get("/logout")
async def logout(request: Request):
    """登出处理"""
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_id")
    return response 