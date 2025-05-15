from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from typing import List, Optional
import markdown2
import logging
from app.schemas import PostCreate, PostRead, PostUpdate
from app.models.models import Post, Category, Tag, User
from app.api.auth import get_current_user
from tortoise.expressions import Q

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    """创建新文章"""
    logger.info(f"创建文章: {post.title}, 分类IDs: {post.category_ids}, 标签IDs: {post.tag_ids}")
    
    # 将 Markdown 转换为 HTML
    content_html = markdown2.markdown(post.content_markdown, extras=["fenced-code-blocks", "tables"])
    
    # 创建文章
    post_obj = await Post.create(
        title=post.title,
        content_markdown=post.content_markdown,
        content_html=content_html,
        is_published=post.is_published,
        author_id=current_user.id
    )
    logger.info(f"文章创建成功, ID: {post_obj.id}")
    
    # 添加分类
    if post.category_ids:
        for cat_id in post.category_ids:
            category = await Category.get_or_none(id=cat_id)
            if category:
                await post_obj.categories.add(category)
                logger.info(f"添加分类: {category.id} - {category.name}")
            else:
                logger.warning(f"分类ID {cat_id} 不存在")
    else:
        logger.info("没有提供分类ID")
    
    # 添加标签
    if post.tag_ids:
        for tag_id in post.tag_ids:
            tag = await Tag.get_or_none(id=tag_id)
            if tag:
                await post_obj.tags.add(tag)
                logger.info(f"添加标签: {tag.id} - {tag.name}")
            else:
                logger.warning(f"标签ID {tag_id} 不存在")
    else:
        logger.info("没有提供标签ID")
    
    # 获取完整的文章数据，包括关联的分类和标签
    await post_obj.fetch_related("categories", "tags")
    
    # 验证是否成功关联
    categories = await post_obj.categories.all()
    tags = await post_obj.tags.all()
    logger.info(f"关联成功的分类数量: {len(categories)}, 标签数量: {len(tags)}")
    
    return {
        **post_obj.__dict__,
        "author_id": post_obj.author_id,
        "categories": categories,
        "tags": tags
    }

@router.get("/", response_model=List[PostRead])
async def get_posts(
    skip: int = 0, 
    limit: int = 10, 
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    published_only: bool = True
):
    """获取文章列表，支持分页、搜索和筛选"""
    # 构建查询条件
    query = Post.all()
    
    # 只展示已发布的文章
    if published_only:
        query = query.filter(is_published=True)
    
    # 标题搜索
    if search:
        query = query.filter(title__icontains=search)
    
    # 按分类筛选
    if category_id:
        query = query.filter(categories__id=category_id)
    
    # 按标签筛选
    if tag_id:
        query = query.filter(tags__id=tag_id)
    
    # 获取总数
    total = await query.count()
    
    # 分页查询
    posts = await query.offset(skip).limit(limit).prefetch_related("author", "categories", "tags")
    
    # 构造结果
    result = []
    for post in posts:
        post_dict = post.__dict__
        post_dict["author_id"] = post.author_id
        post_dict["categories"] = await post.categories.all()
        post_dict["tags"] = await post.tags.all()
        result.append(post_dict)
    
    return result

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int):
    """获取单篇文章详情"""
    post = await Post.get_or_none(id=post_id).prefetch_related("author", "categories", "tags")
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    if not post.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="文章未发布"
        )
    
    post_dict = post.__dict__
    post_dict["author_id"] = post.author_id
    post_dict["categories"] = await post.categories.all()
    post_dict["tags"] = await post.tags.all()
    
    return post_dict

@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新文章"""
    post = await Post.get_or_none(id=post_id, author_id=current_user.id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在或您无权编辑"
        )
    
    update_data = {}
    
    # 更新文章内容
    if post_update.title is not None:
        update_data["title"] = post_update.title
    
    if post_update.content_markdown is not None:
        update_data["content_markdown"] = post_update.content_markdown
        update_data["content_html"] = markdown2.markdown(
            post_update.content_markdown,
            extras=["fenced-code-blocks", "tables"]
        )
    
    if post_update.is_published is not None:
        update_data["is_published"] = post_update.is_published
    
    # 应用更新
    if update_data:
        await post.update_from_dict(update_data).save()
    
    # 更新分类
    if post_update.category_ids is not None:
        # 清除现有分类
        await post.categories.clear()
        # 添加新分类
        for cat_id in post_update.category_ids:
            category = await Category.get_or_none(id=cat_id)
            if category:
                await post.categories.add(category)
    
    # 更新标签
    if post_update.tag_ids is not None:
        # 清除现有标签
        await post.tags.clear()
        # 添加新标签
        for tag_id in post_update.tag_ids:
            tag = await Tag.get_or_none(id=tag_id)
            if tag:
                await post.tags.add(tag)
    
    # 获取更新后的完整数据
    await post.fetch_related("categories", "tags")
    
    post_dict = post.__dict__
    post_dict["author_id"] = post.author_id
    post_dict["categories"] = await post.categories.all()
    post_dict["tags"] = await post.tags.all()
    
    return post_dict

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    """删除文章"""
    post = await Post.get_or_none(id=post_id, author_id=current_user.id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在或您无权删除"
        )
    
    await post.delete()
    return None 