---
title: Hexo next 使用utterances评论
categories:
  - web
tags:
  - web
  - hexo
abbrlink: 8d4b165c
date: 2024-05-28 19:25:39
---
之前next里用的是valine评论区，谁知这次怎么弄都配置不上，搜索之下发现新版next已经不支持valine了。好像是因为其安全问题。因此我准备用utterances。
<!--less-->
根据官网介绍步骤如下：
1. 在github中新建一个仓库，例如较utt_comment.
2. 点击https://github.com/apps/utterances安装Github App 关联的仓库要选刚刚建立的那个，例如：utt_comment.
3. 在主题配置文件_config.yml中设置：
```
# Utterances
# For more information: https://utteranc.es
utterances:
  enable: true
  repo: your-name/your-repo # Github repository owner and name
  # Available values: pathname | url | title | og:title
  issue_term: pathname
  # Available values: github-light | github-dark | preferred-color-scheme | github-dark-orange | icy-dark | dark-blue | photon-dark | boxy-light
  theme: github-light
```
