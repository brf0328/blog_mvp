# Blog MVP

一个基于FastAPI和Tortoise ORM开发的简洁高效的博客系统，支持文章发布、分类管理和标签功能。

## 项目功能

- **用户管理**: 
  - 用户注册与账户创建
  - 安全登录与身份验证
  - 个人资料管理
  - 会话控制与安全登出

- **文章管理**: 
  - 创建、编辑、删除文章
  - 草稿保存功能
  - 文章预览
  - 富文本编辑

- **分类系统**: 
  - 创建和管理文章分类
  - 分类层级关联
  - 按分类筛选文章

- **标签系统**: 
  - 灵活添加文章标签
  - 标签云展示
  - 按标签快速筛选内容

- **Markdown支持**: 
  - 集成SimpleMDE编辑器
  - 实时Markdown预览
  - 支持常用Markdown语法
  - 代码高亮显示

- **响应式设计**: 
  - 自适应桌面、平板和手机屏幕
  - 优化的移动端阅读体验
  - 触控友好的操作界面

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

- **User**: 用户表，存储用户信息（用户名、邮箱、密码哈希等）
- **Post**: 博客文章表，包含标题、内容、发布状态、创建时间等
- **Category**: 文章分类表，包含分类名称和描述
- **Tag**: 文章标签表，包含标签名称
- **post_category**: 文章与分类的多对多关联表（自动创建）
- **post_tag**: 文章与标签的多对多关联表（自动创建）

## 安装与启动

1. 克隆仓库:
   ```bash
   git clone https://github.com/yourusername/blog_mvp.git
   cd blog_mvp
   ```

2. 创建虚拟环境并激活:
   ```bash
   # 使用conda
   conda create -n blog-mvp python=3.10 -y
   conda activate blog-mvp
   
   # 或使用venv
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

4. 配置数据库:
   - 在`config/settings.py`中修改数据库连接配置
   ```python
   # 示例配置
   TORTOISE_ORM = {
       "connections": {
           "default": "mysql://username:password@localhost:3306/blog_db"
       },
       # 其他配置...
   }
   ```

5. 初始化数据库:
   ```bash
   aerich init-db
   ```

6. 启动服务器:
   ```bash
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

### 用户管理
1. **注册账户**：访问注册页面，填写用户名、邮箱和密码
2. **登录系统**：使用注册的账户信息登录
3. **个人主页**：登录后可以访问个人主页，查看自己发布的文章统计和列表

### 文章管理
1. **创建文章**：点击导航栏的"写文章"按钮
2. **编辑内容**：使用Markdown编辑器撰写文章内容
3. **设置分类和标签**：为文章选择适当的分类和标签
4. **保存草稿**：可以暂存为草稿，稍后继续编辑
5. **发布文章**：完成编辑后发布文章
6. **编辑已有文章**：在个人主页或文章详情页面可以编辑自己的文章
7. **删除文章**：在编辑页面可以删除不需要的文章

### 分类和标签管理
1. **访问管理页面**：点击"管理分类和标签"进入管理界面
2. **创建分类**：添加新的文章分类
3. **创建标签**：添加新的文章标签
4. **删除操作**：可以删除不再使用的分类或标签

### 浏览和阅读
1. **首页浏览**：在首页可以看到最新发布的文章列表
2. **分类筛选**：通过点击分类名称筛选特定分类的文章
3. **标签筛选**：通过点击标签名称查看相关标签的文章
4. **阅读文章**：点击文章标题进入详情页阅读全文

## 高级功能

### Markdown支持
- 支持标准Markdown语法，包括标题、列表、链接、图片等
- 代码块支持语法高亮
- 实时预览编辑效果

### 响应式设计
- 自动适应不同尺寸的屏幕设备
- 在手机和平板上也能获得良好的阅读和操作体验

## 注意事项

- 本项目使用MySQL数据库，请确保已安装并正确配置数据库
- 开发环境中启用了自动生成数据库模式(generate_schemas=True)，生产环境请改为False并使用Aerich管理数据库迁移
- 首次使用时，请先创建分类和标签，再创建文章
- 文章内容支持Markdown格式，可以使用Markdown语法丰富文章表现形式

## 技术栈

- **后端框架**：FastAPI
- **ORM**：Tortoise ORM
- **数据库**：MySQL
- **前端**：HTML、CSS、JavaScript
- **模板引擎**：Jinja2
- **Markdown编辑器**：SimpleMDE
- **认证**：JWT Token