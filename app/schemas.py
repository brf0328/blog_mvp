from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class PostBase(BaseModel):
    title: str
    content_markdown: str


class PostCreate(PostBase):
    is_published: bool = False
    category_ids: Optional[List[int]] = []
    tag_ids: Optional[List[int]] = []


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content_markdown: Optional[str] = None
    is_published: Optional[bool] = None
    category_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None


class PostRead(PostBase):
    id: int
    content_html: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    categories: Optional[List[CategoryRead]] = []
    tags: Optional[List[TagRead]] = [] 