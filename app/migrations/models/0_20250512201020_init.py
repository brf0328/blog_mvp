from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `category` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称'
) CHARACTER SET utf8mb4 COMMENT='文章分类表';
CREATE TABLE IF NOT EXISTS `tag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '标签名称'
) CHARACTER SET utf8mb4 COMMENT='标签表';
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password_hash` VARCHAR(100) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `post` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(200) NOT NULL,
    `content_markdown` LONGTEXT NOT NULL COMMENT 'markdown格式内容',
    `content_html` LONGTEXT NOT NULL COMMENT 'html格式内容',
    `is_published` BOOL NOT NULL COMMENT '是否发布' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `author_id` INT NOT NULL,
    CONSTRAINT `fk_post_user_4fc8b4bc` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='博客文章表';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `post_tag` (
    `post_id` INT NOT NULL,
    `tag_id` INT NOT NULL,
    FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_post_tag_post_id_4edf8d` (`post_id`, `tag_id`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `post_category` (
    `post_id` INT NOT NULL,
    `category_id` INT NOT NULL,
    FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_post_catego_post_id_0d8446` (`post_id`, `category_id`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
