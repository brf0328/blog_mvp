from tortoise.models import Model
from tortoise import fields



class User(Model):
    """用户表"""
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # 反向关系 可以通过 posts 访问所有关联的 Post
    posts = fields.ReverseRelation["Post"]
    
    class Meta:
        table = "user"
        table_description = "用户表"

class Post(Model):
    """博客文章表"""
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content_markdown = fields.TextField(description="markdown格式内容")
    content_html = fields.TextField(description="html格式内容")
    is_published = fields.BooleanField(default=False,description="是否发布")
    created_at = fields.DatetimeField(auto_now_add=True,description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True,description="更新时间")
    
    # 外键关系
    author = fields.ForeignKeyField("models.User", related_name="posts")
    
    # 多对多关系 - 会自动创建中间表
    categories = fields.ManyToManyField("models.Category", related_name="posts", through="post_category")
    tags = fields.ManyToManyField("models.Tag", related_name="posts", through="post_tag")
    
    class Meta:
        table = "post"#定义表名
        table_description = "博客文章表"

class Category(Model):
    """文章分类表"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True,description="分类名称")
    
    class Meta:
        table = "category"
        table_description = "文章分类表"


class Tag(Model):
    """标签表"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True,description="标签名称")
    creator_id = fields.IntField(null=True, description="创建者ID")
    
    class Meta:
        table = "tag"
        table_description = "标签表"
