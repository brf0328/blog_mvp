# Blog MVP

一个基于FastAPI和Tortoise ORM开发的简单博客系统，支持文章发布、分类管理和标签功能。

## 项目功能

- **用户管理**: 注册、登录、登出
- **文章管理**: 创建、编辑、删除文章
- **分类系统**: 文章分类的创建、删除和关联
- **标签系统**: 文章标签的创建、删除和关联
- **Markdown支持**: 使用SimpleMDE编辑器，支持Markdown格式内容编写和预览
- **响应式设计**: 适配不同尺寸的屏幕

## 项目结构

```
blog_mvp/
│
├── app/                          # 应用目录
│   ├── api/                      # API路由
│   │   ├── __init__.py           # API路由注册
│   │   ├── auth.py               # 认证相关API
│   │   ├── categories.py         # 分类管理API
│   │   ├── posts.py              # 文章管理API
│   │   └── tags.py               # 标签管理API
│   │
│   ├── core/                     # 核心功能
│   │   └── security.py           # 安全相关功能（密码哈希等）
│   │
│   ├── models/                   # 数据模型目录
│   │   └── models.py             # 数据库模型定义
│   │
│   ├── migrations/               # 数据库迁移文件
│   │
│   ├── schemas.py                # Pydantic模型定义
│   └── views.py                  # 视图路由（网页路由）
│
├── config/                       # 配置目录
│   └── settings.py               # 数据库连接配置
│
├── static/                       # 静态资源目录
├── templates/                    # HTML模板目录
│   ├── base.html                 # 基础模板
│   ├── detail.html               # 文章详情页
│   ├── edit.html                 # 文章编辑页
│   ├── index.html                # 首页
│   ├── login.html                # 登录页面
│   ├── manage_categories_tags.html # 分类和标签管理页面
│   ├── profile.html              # 用户个人主页
│   └── register.html             # 注册页面
│
├── main.py                       # 应用入口
└── requirements.txt              # 项目依赖
```

## 数据库模型

- **User**: 用户表，存储用户信息
- **Post**: 博客文章表，包含标题、内容等
- **Category**: 文章分类表
- **Tag**: 文章标签表
- **post_category**: 文章与分类的多对多关联表（自动创建）
- **post_tag**: 文章与标签的多对多关联表（自动创建）

## 安装与启动

1. 克隆仓库:
   ```
   git clone https://github.com/yourusername/blog_mvp.git
   cd blog_mvp
   ```

2. 创建虚拟环境并激活:
   ```
   conda create -n blog-mvp python=3.10 -y
   conda activate blog-mvp
   ```

3. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

4. 配置数据库:
   - 在`config/settings.py`中修改数据库连接配置

5. 初始化数据库:
   ```
   aerich init-db
   ```

6. 启动服务器:
   ```
   uvicorn main:app --reload
   ```

7. 访问网站:
   ```
   http://localhost:8000/
   ```

8. 访问API文档:
   ```
   http://localhost:8000/docs
   ```

## 使用指南

1. 首先注册一个账户并登录
2. 在"管理分类和标签"页面创建分类和标签
3. 点击"写文章"创建新文章，可以选择分类和标签
4. 在个人主页可以查看和管理自己的所有文章
5. 在首页可以浏览已发布的文章，可按分类或标签筛选

## 注意事项

- 本项目使用MySQL数据库，请确保已安装并正确配置数据库
- 开发环境中启用了自动生成数据库模式(generate_schemas=True)，生产环境请改为False并使用Aerich管理数据库迁移