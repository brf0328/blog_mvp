TORTOISE_ORM = {
    'connections': {
        'default': {
            # PostgreSQL 引擎配置
            # 'engine': 'tortoise.backends.asyncpg',
            
            # MySQL 或 MariaDB 引擎配置
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': 'brfdsg66',
                'database': 'blog_mvp',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                # 仅在需要查看SQL语句时设为True
                "echo": False
            }
        },
    },
    'apps': {
        'models': {
            'models': ['app.models.models', "aerich.models"],
            'default_connection': 'default',
        }
    },
    'use_tz': False,
    'timezone': "UTC"
}