---
title: hexo 如何给文章设密码
categories:
  - web
tags: 
  - web
  - hexo
abbrlink: 7c8ba603
date: 2024-05-28 14:15:34
---
有些文章写了，但不想要给别人看，那就设一个密码。
<!-- less -->
# 安装插件
命令：
```
npm install hexo-blog-encrypt
```
# 修改配置
在本目录配置文件_config.yml加入：
```
encrypt:
   enable: true
```
# 博客文章加密
写新的文章时加入：
```
password: xxxxx
message: 输入密码的提示。
```
高级设置：
```
password: xxxx
abstract: here is something encrypted
message: 请输入密码。
wrong_pass_message: Oh, wrong password, please try again.
```
