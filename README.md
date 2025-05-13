# Blog MVP

一个基于FastAPI和Tortoise ORM的简单博客系统。

## 项目结构

```
blog_mvp/
│
├── app/                  # 应用目录
│   ├── api/              # API路由
│   │   ├── __init__.py
│   │   ├── posts.py      # 文章API
│   │   └── users.py      # 用户API
│   │
│   ├── models.py         # 数据模型定义
│   └── settings.py       # 项目配置
│
├── migrations/           # 数据库迁移文件
│   └── models/
│
├── static/               # 静态资源
├── templates/            # 模板文件
├── main.py               # 应用入口
└── requirements.txt      # 项目依赖
```

## 数据模型

- User: 用户表
- Post: 博客文章表
- Category: 文章分类表
- Tag: 标签表

## 启动项目

1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

2. 初始化数据库:
   ```
   aerich init-db
   ```

3. 启动服务器:
   ```
   uvicorn main:app --reload
   ```

4. 访问API文档:
   ```
   http://localhost:8000/docs
   ```