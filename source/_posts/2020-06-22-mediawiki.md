---
title: How to install and backup mediawiki
categories: Linux
tags:
  - wiki
abbrlink: 10861
date: 2020-06-22 10:18:19
---
Meidawiki is a good tool to organise the information and knowledge. I even use it to keep some notes. My first mediawiki was established like in 2012. There are some important informations in my database. Therefore I hope to keep it and run it in every Laptop. This blog keeps the steps on how to install and backup it.

<!-- more -->

## intall mediawiki 

I installed the mediawiki in Elementary OS (Ubuntu), so steps of installing mediawiki are like:

### install dependents: 
```
sudo apt-get install apache2 mysql-server php5 php5-mysql libapache2-mod-php5
```

### install mediawiki:
There are two ways to do that:

#### The systematic way:
```
 sudo apt-get install mediawiki (this will install a low version)
```

#### Manual:

step1: download an upgraded version:
```
wget https://releases.wikimedia.org/mediawiki/1.33/mediawiki-1.33.0.tar.gz
```
extract them and put them into /var/lib/mediawiki

step 2: Create a database ( in mysql )

1. Check and see if the database server is running; for example, run 
```
/usr/local/mysql/bin/mysqladmin status
```
If it is not, run mysqld\_safe to start it: 
```
sudo /usr/local/mysql/bin/mysqld\_safe &
```

2. Set a password for the "root" account on your database server. 
```
/usr/local/mysql/bin/mysqladmin -u root password yourpassword
```
3. Run the MySQL command-line client: 
```
/usr/local/mysql/bin/mysql -u root -p
```
4. Run command in the mysql command-line:

```
create database wikidb;
GRANT ALL ON my\_wiki.* TO 'new_mysql_user'@'localhost';
grant index, create, select, insert, update, delete, alter, lock tables on wikidb.* to 'wikiuser'@'localhost' identified by 'password’;
```
problem? sometimes this message may show up: 

```
connection error: Access denied for user 'root'@'localhost' (localhost)
```

In my case, I found a solvation:
```
sudo mysql -u root
use mysql;
update user set plugin='mysql\_native\_password' where User='root';
flush privileges;
quit
reboot
```

step3: go to 127.0.0.1/mediawiki, follow the steps.

## Back up wikidb:
All information are restored in mySQL database, so backup it with command:
```
mysqldump -u[user] -p[password] [databasename] > [dump\_name]
```
In my case, it goes like:
```
mysqldump -u root -p wikidb >wikidb.mysql
```
My database is in wikidb.mysql. And I do not want to do this by typing them in the terminal. In replacement, I use crontab, edit crontab:
```
crontab -e
```
with a new task:
```
0 12 * * 1 mysqldump -u root -p wikidb >/home/junxie/work/wikidb.mysql
```
This means to run backup command in the noon every Monday.

## Restore a wikidb in a new computer:
If you move in to another computer, after installing the mediawiki, run the following commend to restore the backup one.
```
mysql -u[user] -p[password] [database_name] < [dump\_name]
```
In my case, it is:
```
mysql -u root -p wikidb <wikidb.mysql
```
Have fun ^_^
