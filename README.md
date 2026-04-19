# SEISAMUSE

一个为地球科学研究者设计的个人学术网站，使用 Python + Jinja2 + Markdown 构建。

## 项目概述

SEISAMUSE 是一个静态网站生成器，专为地震学家和地球物理学家设计，提供以下功能：

- 博客文章管理（从 Hexo 迁移了 196 篇文章）
- 分页功能（每页 20 篇文章）
- 标签过滤系统
- 响应式设计，适配不同设备
- 捐赠功能（支付宝/微信）
- 脚本下载功能

## 技术栈

- **后端**：Python 3
- **模板引擎**：Jinja2
- **内容格式**：Markdown
- **样式**：Tailwind CSS
- **图标**：Font Awesome

## 快速开始

### 环境要求

- Python 3.7+
- 依赖包：
  - jinja2
  - markdown
  - pygments
  - pillow

### 安装依赖

```bash
pip install jinja2 markdown pygments pillow
```

### 构建网站

```bash
python3 build.py
```

构建完成后，网站文件会生成在 `site/` 目录中。

### 本地测试

```bash
cd site
python3 -m http.server 8080
```

然后在浏览器中访问：`http://localhost:8080`

## 部署

### 使用 GitHub Pages

1. 构建网站：`python3 build.py`
2. 移动网站文件到根目录：`mv site/* . && rm -rf site`
3. 推送到 GitHub 仓库：`git add . && git commit -m "Update website" && git push`
4. 在 GitHub 仓库设置中启用 Pages：
   - 分支：main
   - 文件夹：/(root)
5. 网站会自动部署到 `https://www.seis-jun.xyz/`

### 自动部署

使用提供的 `do_deploy.bash` 脚本自动构建和部署：

```bash
./do_deploy.bash
```

## 目录结构

```
seisamuse/
├── build.py          # 构建脚本
├── content/          # 内容目录
│   ├── posts/        # 博客文章（Markdown格式）
│   ├── about.md      # 关于页面
│   ├── links.md      # 链接页面
│   ├── images/       # 图片资源
│   └── scripts/      # 可下载脚本
├── templates/        # Jinja2 模板
├── do_deploy.bash    # 部署脚本
├── index.html        # 首页（构建生成）
├── blog/             # 博客页面（构建生成）
├── css/              # 样式文件（构建生成）
├── images/           # 图片（构建生成）
├── links/            # 链接页面（构建生成）
└── scripts/          # 脚本（构建生成）
```

## 添加新文章

1. 在 `content/posts/` 目录中创建新的 Markdown 文件
2. 文件名格式：`YYYY-MM-DD-title.md`
3. 添加文章头部信息：

```markdown
---
title: 文章标题
date: 2024-06-15
tags: [tag1, tag2]
---

文章内容...
```

4. 运行 `python3 build.py` 重新构建网站

## 自定义

### 修改网站配置

编辑 `build.py` 文件中的配置变量：

- `site_name`：网站名称
- `site_url`：网站 URL
- `author`：作者信息
- `description`：网站描述

### 修改模板

- `templates/base.html`：基础模板
- `templates/index.html`：首页模板
- `templates/blog.html`：博客列表模板
- `templates/post.html`：文章详情模板
- `templates/about.html`：关于页面模板
- `templates/links.html`：链接页面模板

## 功能特性

✅ 从 Hexo 迁移了 196 篇文章
✅ 分页功能（每页 20 篇文章）
✅ 标签过滤系统
✅ 响应式设计
✅ 捐赠功能
✅ 脚本下载功能
✅ Markdown 支持
✅ 代码高亮

## 联系方式

- 作者：Jun Xie
- 邮箱：your.email@example.com
- 网站：https://www.seis-jun.xyz

## 许可证

MIT License
