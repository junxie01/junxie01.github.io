---
title: 如何备份hexo
categories: web
tags:
  - web
abbrlink: 61239
date: 2020-05-31 13:52:53
---
要是换了电脑网站怎么办？那当然是需要备份的了。u盘什么的，网盘什么的也不错。不过搜到大神的[博文](https://notes.doublemine.me/2015-04-06-%E5%A4%87%E4%BB%BDHexo%E5%8D%9A%E5%AE%A2%E6%BA%90%E6%96%87%E4%BB%B6.html)介绍说放到githup的repo里面就可以了。于是试了一下，果然可以啊。步骤如下：
## 创建github的repository

创建一个和你的hexo目录一样的repo。我的就是hexo。在hexo主目录下执行如下命令：
<!-- more -->

``` bash
$echo "# hexo" >>README.md
$git init
$git commit -m ""
$git add README.md 
$git commit -m "README"
$git remote add origin https://github.com/junxie01/hexo.git
$git push -u origin master
```

## 备份/推送

每次完成hexo的更新或者新博文的建立就可以运行如下命令进行推送/备份。

``` bash
$git add .
$git commit -m "hexo备份"
$git push origin master
```

## 新电脑网站移植

需要在新电脑写博客需要安装npm，node.js，hexo。然后把github的repo克隆到本地就好了。

```bash
$git clone git@github.com:junxie01/hexo.git
```

## 同步本地网站

当github中的repo有更新时，执行一下命令可以同步到本地。
``` bash
$git pull origin master
```

## 自动推送/备份

那位牛人博主还有一篇博文[利用nodejs脚本自动备份](https://notes.doublemine.me/2015-07-06-%E8%87%AA%E5%8A%A8%E5%A4%87%E4%BB%BDHexo%E5%8D%9A%E5%AE%A2%E6%BA%90%E6%96%87%E4%BB%B6.html)。我不太懂，省得麻烦。干脆写一个bash脚本(例如do_deploy_push.bash)就可以解决这些问题。脚本如下:
``` bash
hexo cl && hexo g && hexo d
git add .
git commit -m "backup hexo at `date` "
git push origin master
```
在hexo主目录下面运行 bash do_deploy_push.bash就大功告成了。

