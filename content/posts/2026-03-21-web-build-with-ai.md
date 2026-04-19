---
title: 用AI做网页
categories:
  - ai
tags:
  - web
abbrlink: 8cd95a7c
date: 2026-03-21 10:36:31
---
  我又试着做了两个网页，一个是[论文周报](https://www.seis-jun.xyz/paper_weekly/frontend/)，另一个是[每周地震](https://www.seis-jun.xyz/earthquake_weekly/)。
<!--less-->
&emsp;&emsp;这次用的是[Andriod Studio](https://developer.android.com/studio)。套路明白了，大概现在的一些IDE平台都嵌入了大预言模型，可以对话然后让AI帮你做事。这应该跟openclaw差不太多，只是相比起来openclaw给的权限太高，可以操纵你的电脑所有内容，而这些IDE只能操作当前目录。
&emsp;&emsp;好了分别介绍一下我的两个网页。首先是论文周报：

# 📚 地震学多专题论文周报 (paper_weekly)

一个自动追踪 arXiv和主要滴血期刊地震学相关研究（DAS、面波、成像、冰川地震等）并自动翻译、生成 PDF 报告并集成至 Hexo 博客的自动化系统。

## 🌐 站点集成说明

### 部署为子站点 
1. 在本仓库的 **Settings > Pages** 中开启部署，选择 `main` 分支。
2. 您的论文页面将自动出现在：`https://www.seis-jun.xyz/paper_weekly/`
3. 在Hexo中的next主题下的 `_config.yml` 菜单中添加该链接即可。

### 自动化流程
- **定时触发**：每周日北京时间上午 8:00 自动运行。
- **手动触发**：在 GitHub Actions 页面点击 "Run workflow"。
- **包含专题**：冰川地震、分布式光纤传感、面波研究、地震成像、地震研究。

## 🛠️ 必须完成的配置 (Secrets)

在 GitHub 仓库 **Settings > Secrets and variables > Actions** 中添加：
- `MAIL_USERNAME`: Gmail 地址 (如 `xxx@gmail.com`)。
- `MAIL_PASSWORD`: Google 账号生成的 **16 位应用专用密码** (删除空格)。
- `MAIL_TO`: 接收邮箱。

## 🔍 故障排查 (邮件发送失败)

如果 GitHub Actions 报 `535 Login fail`：
1. **两步验证**：确保 Google 账号已开启 2-Step Verification。
2. **应用密码**：必须使用 16 位 App Password，填入 Secret 时删除所有空格。
3. **YAML 配置**：确保 `.github/workflows/update.yml` 中 `server_port: 465` 且 `secure: true`。

## 📂 仓库结构
- `update_papers.py`: 核心脚本（多专题抓取、翻译、PDF 生成）。
- `frontend/`: 网页展示端（支持多专题切换）。
- `.github/workflows/update.yml`: GitHub Actions 配置文件。

可以到我的侧边栏点击[论文周报](https://www.seis-jun.xyz/paper_weekly/frontend/)查看。每周日它会自动检索文章然后生成pdf发邮件给我，另外也会更新网页。目前版本并没有集成AI，不能总结论文内容，只有翻译。有机会再集成AI吧。

&emsp;&emsp;另一个网页是每周地震。以前参加组会每周都会有的内容。

# Weekly Earthquake Report (USGS Insights)

这是一个基于 USGS 数据实时生成的地震周报系统。它会自动抓取过去一周全球发生的地震，挑选震级最大的三个事件进行深度分析，包括局部历史地震对比、地质构造总结以及来自 USGS 和 Google News 的多源报道。

## 🌟 功能特点

- **全球地震图**：实时展示过去 7 天全球地震分布，震级越大圆圈越大。
- **板块边界展示**：在地图上叠加全球地质板块边界（Tectonic Plates）。
- **重大地震深度分析**：
    - **局部地图**：自动定位震中，展示 10 度范围内的地理细节。
    - **历史对比**：自动调取 1970 年以来该区域所有 M5.0+ 的历史地震（蓝色圆圈）。
    - **视觉化报告**：直接嵌入 USGS 官方生成的 **Shakemap (烈度图)**、**Moment Tensor (震源球)**、**PAGER (损失预估)** 等专业图表。
    - **多源新闻**：集成 USGS 内部报告链接和 **Google News** 实时搜索结果。
- **全自动更新**：利用 GitHub Actions 每周日凌晨（UTC）自动运行抓取脚本并更新网页。

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (Leaflet.js)
- **后端**: Python 3 (Requests, Regex)
- **数据源**: [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/)
- **自动化**: GitHub Actions

## 🚀 本地运行

1. **安装依赖**:
   ```bash
   pip3 install requests
   ```

2. **抓取最新数据**:
   ```bash
   python3 fetch_data.py
   ```

3. **启动预览服务器**:
   ```bash
   python3 -m http.server 8000
   ```
   访问 `http://localhost:8000` 即可查看。

## 🤖 自动化部署 (GitHub Actions)

项目已配置 `.github/workflows/update_earthquakes.yml`。
- **定时运行**: 每周日 00:00 UTC。
- **手动触发**: 在 GitHub 仓库的 `Actions` 页面选择 "Update Earthquake Data" 并运行。

## 🔗 部署为子站点
1. 在本仓库的 **Settings > Pages** 中开启部署，选择 `main` 分支。
2. 您的论文页面将自动出现在：`https://www.seis-jun.xyz/earthquake_weekly`
3. 在 Hexo 的 `_config.yml` 菜单中添加该链接即可。

也可以到我的侧边栏点击[每周地震](https://www.seis-jun.xyz/earthquake_weekly/)查看。每周日会重新抓取数据，更新网页。目前版本比较简单，欢迎提意见。
