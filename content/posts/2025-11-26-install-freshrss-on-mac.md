---
title: Mac中安装FreshRSS
tags:
  - FreshRSS
categories:
  - mac
abbrlink: 8f5ea8f8
date: 2025-11-26 10:01:14
---
&emsp;&emsp;Mac中如何安装FreshRSS
<!--less-->
&emsp;&emsp;参考FreshRSS的github[主页](https://github.com/FreshRSS/FreshRSS/tree/edge)。不过还是麻烦，请[千问](https://www.qianwen.com/)帮忙，简直不要太简单。步骤如下：
## 依赖安装（PHP + Composer）
用以下命令安装:
```
brew install php
brew install composer
```
## 安装FreshRSS
命令如下：
```
git clone https://github.com/FreshRSS/FreshRSS.git
cd FreshRSS
# 如果想参与开发可切入edge分支：git checkout edge
php -S localhost:8080 -t .
```
接下来访问 http://localhost:8080 进行安装。
## 迁移和更新
数据都在data下面，拷贝他就可以进行迁移。更新的话运行如下脚本。
```
git pull origin main
```
## 下次登录
运行以下脚本
```
echo 'alias freshrss="cd ~/FreshRSS && php -S localhost:8080 -t ."' >> ~/.zshrc
source ~/.zshrc
```
然后每次运行freshrss，然后在浏览器访问 http://localhost:8080 就好。
大功告成。
