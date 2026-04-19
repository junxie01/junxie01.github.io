---
title: Fedora中安装FreshRSS
tags:
  - Linux
categories:
  - Linux
abbrlink: 751a68a
date: 2025-10-06 22:31:32
---
&emsp;&emsp;Fedora中Apache环境下如何安装FreshRSS
<!--less-->
&emsp;&emsp;之前总是蹭一个小伙子自己建的[RSS](https://rss.othing.xyz/)，白嫖，怕哪天人家不搞了，还是自己建一个吧。详细脚本安装请查看其[github](https://github.com/FreshRSS/FreshRSS/blob/edge/cli/README.md)。废话不多说，具体如下：
# 一、安装依赖
FreshRSS是基于PHP的自建RSS聚合器，需要Apache+PHP环境：
```
sudo dnf install httpd php php-cli php-common php-json php-gd php-mbstring php-intl php-xml php-pdo php-mysqlnd unzip git -y
```

启用并启动 Apache：
```
sudo systemctl enable --now httpd
```

确认端口 80 正在监听：
```
sudo ss -tulnp | grep :80
```
# 二、下载并安装 FreshRSS

推荐安装到 /usr/share/FreshRSS：
```
cd /usr/share
sudo git clone https://github.com/FreshRSS/FreshRSS.git
cd FreshRSS
sudo git checkout stable   # 或 edge 分支（开发版）
```

设置权限（Fedora 的 Apache 用户是 apache）：
```
sudo chown -R apache:apache /usr/share/FreshRSS
sudo chmod -R 755 /usr/share/FreshRSS
```
# 三、配置 Apache

新建配置文件：
```
sudo vim /etc/httpd/conf.d/freshrss.conf
```
写入以下内容：
```
Alias /FreshRSS /usr/share/FreshRSS

<Directory /usr/share/FreshRSS>
    AllowOverride All
    Options Indexes FollowSymLinks
    Require all granted
</Directory>
```
保存退出后，重启 Apache：
```
sudo systemctl restart httpd
```
# 四、处理 SELinux 限制（Fedora 特有）
Fedora 默认启用了 SELinux，会阻止 Apache 访问 /usr/share 下的应用。
执行以下命令放行：
```
sudo chcon -R -t httpd_sys_rw_content_t /usr/share/FreshRSS
sudo setsebool -P httpd_can_network_connect on
```
（若仍被拒绝，可临时关闭测试：sudo setenforce 0）

# 五、访问 Web 界面

打开浏览器访问：
```
http://localhost/FreshRSS
```
你应看到 FreshRSS 的安装页面。
根据提示创建管理员账号、数据库配置（SQLite/MySQL 都可）。

如果提示 “You don’t have permission to access this resource”，请确认：

Apache 配置文件中包含 Require all granted

SELinux 权限已放行（执行了 chcon）

# 六、命令行工具（可选）

FreshRSS 提供强大的 CLI 管理工具，位于 cli/ 目录。
例如列出用户：
```
cd /usr/share/FreshRSS
sudo -u apache php cli/list-users.php
```
Fedora 用的是 apache 用户，而不是 Debian/Ubuntu 的 www-data。

# 七、日志与排错

查看 Apache 错误日志：
```
sudo tail -n 30 /var/log/httpd/error_log
```

查看 SELinux 拒绝记录：
```
sudo ausearch -m AVC,USER_AVC -ts recent
```
# 八、（可选）设置自动更新任务

添加一个定时任务更新 RSS 源：
```
sudo -u apache php /usr/share/FreshRSS/app/actualize_script.php > /dev/null 2>&1
```
在 /etc/cron.d/freshrss 中添加：
```
*/20 * * * * apache php /usr/share/FreshRSS/app/actualize_script.php > /dev/null 2>&1
```
表示每20分钟更新一次。
