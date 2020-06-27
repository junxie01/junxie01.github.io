---
title: hexo免密发布
tags:
  - hexo
  - web
abbrlink: 55505
date: 2020-05-31 03:23:55
---
每次发布都得输入用户名和密码，挺麻烦费事。网上[大神](https://blog.csdn.net/hhgggggg/article/details/77853665)可真多，搜搜就能解决。和ssh登录服务器类似，步骤如下：

<!-- more -->
## 生成SSH密钥


使用ssh-kergen生成密钥：
``` bash
$ssh-keygen -t rsa -C "junxie01@gmail.com"
```

一路enter就行了。生成的秘钥在主目录的.ssh/id_rsa.pub中。复制一下。

## 添加Github项目的Deploy keys

在项目junxie01.github.io点击settings-->Deploy keys-->Add deploy key.把拷贝好的秘钥粘贴在这里。然后勾选可写。

测试是否配置成功。
``` bash
$ssh -T git@github.com
```
如果出现如下内容则表示配置成功。
```
Hi junxie01/junxie01.github.io! You've successfully authenticated, but GitHub does not provide shell access.
```

## 网站设置文件设置

在网站设置文件deploy字段设置：
```
deploy:
  type: git
  repository: git@github.com:junxie01/junxie01.github.io.git
  branch: master
```
好了，发布网站时hexo d就不用输入用户名和密码了。大功告成。

## Git自带配置文件

这个方法是针对github的，配置好了推送克隆什么的都万事大吉了。是这位大神[博文](https://www.jianshu.com/p/28efda0555bb)里看到的。里面介绍了两种方法，我用的是第一种，因为它看起来更简单。

``` bash
$ git config --global credential.helper store  
```
如果有多个账号什么的去掉--global就好了。为安全性着想还要给store设置一个时限。

``` bash
git config --global credential.helper 'cache --timeout=3600'
```
这个我就没有管了。问题不大吧。

