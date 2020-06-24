---
title: 这个网站是怎么来的
categories: web
tags:
  - web
  - next
abbrlink: 25921
date: 2020-05-26 01:21:16
---
目的：心血来潮，漫无目的。
方法：利用Hexo+Github构建。
花费：1块钱用于腾讯云买域名+6块用于阿里云买域名+宝宝睡了之后的晚上。
用途：好记性不如烂笔头。用手敲敲还可锻炼一下。
时间：2020年5月26日晚。
步骤：参见[这里](https://cloud.tencent.com/developer/article/1423783)，具体如下：
<!-- more -->
## 一、建立repo

建一个和自己的github用户名一样的repo。

## 二、安装必要的程序

需要安装的程序有Git，node.js，hexo

### 1，安装Git

``` bash
$ sudo apt install git
```
### 2，安装node.js

``` bash
$ sudo apt install nodejs 
```
### 3，安装hexo&&初始化

``` bash
$ npm install -g hexo
$ hexo init [dir] #当前目录或新建[dir]
```
## 三、设置

### 1，设置文件为_config.yml，自行修改例如

title 博客名字
subtitle 副标题
author 作者
等等。遇到问题多看看[hexo的官方文档](https://hexo.io/zh-cn/docs)。
### 2，主题配置

想要自己的博客好看那就需要配置主题theme,我用的是Next。
具体设置可以到google搜索关键字hexo+next。
## 四、部署网站到github

### 1，在_config.yml中添加

deploy:
  type: git
  repository: https://github.com/你的名字/你的名字.github.io.git
  branch: master 
### 2，安装部署工具

``` bash
$ npm install hexo-deployer-git  --save
```
### 3，发布

``` bash
$ hexo cl && hexo g && hexo d
```
现在可以打开网址：你的名字.github.io访问。

## 五、绑定域名
### 1，购买域名

### 2，域名解析

找到域名解析选项添加两条记录:
CNAME www 你的名字.github.io
CNAME @ 你的名字.github.io
### 3，添加CNAME文件

在hexo文件夹的source目录中新建CNAME文件，将你的域名写入。然后就大功告成。
完结撒花。

