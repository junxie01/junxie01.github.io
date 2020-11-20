---
title: 为啥要这样安装FileZilla
categories:
  - Linux
tags:
  - filezilla
abbrlink: dea40c8a
date: 2020-11-20 23:27:46
---
&emsp;&emsp;为了要传输数据到服务器需要安装FileZilla程序，那还不易热儿，那就安装呗。然而安装过程让人难忘，不得不记录一下。遗憾的是，到现在仍然还没有搞定。
<!-- more -->
&emsp;&emsp;首先在<https://filezilla-project.org/>下载了个可执行程序---显然是运行不了的。仔细看发现是在debian10.0下编译的。我的系统是Fedora和Elementary OS5，两个都运行不了。然后下载了源程序FileZilla_3.51.0_src.tar.bz2。
&emsp;&emsp;解压，安装filezilla-3.51.0，编译过程出错，显示没有安装libfilezilla。
&emsp;&emsp;于是下载libfilezilla-0.25.0.tar.bz2，解压，安装libfilezilla-0.25.0，编译过程出错，显示没有安装有nettle。
&emsp;&emsp;于是下载nettle-3.6.tar.gz，解压编译安装nettle-3.6一次通过。
&emsp;&emsp;然后在libfilezilla-0.25.0下预编译，出错，显示：
``` bash
configure: error: hogweed 3.3 greater was not found. You can get it from https://www.lysator.liu.se/~nisse/nettle/
```
&emsp;&emsp;于是重装nettle-3.6
```bash
./configure --enable-mini-gmp
make
make check
make install
```
&emsp;&emsp;安装成功，然后在libfilezilla-0.25.0下预编译，出错，显示：
```bash
configure: error: GnuTLS 3.5.8 or greater was not found. You can get it from https://gnutls.org/
```
&emsp;&emsp;然后下载gnutls-3.6.15.tar.xz，解压gnutls-3.6.15编译出错，显示：
``` bash
configure: error: 
***
*** gmp was not found.
```
&emsp;&emsp;然后下载gmp-6.1.0.tar.bz2，解压gmp-6.1.0，编译安装完成。回到gnutls-3.6.15再次编译出错，显示：
``` bash
configure: error: 
  ***
  *** Libtasn1 4.9 was not found. To use the included one, use --with-included-libtasn1
```
&emsp;&emsp;然后下载libtasn1-4.9.tar.gz，解压libtasn1-4.9，编译出错，显示：
``` bash
ASN1.c: In function '_asn1_yyparse':
ASN1.y:152:47: error: '__builtin___snprintf_chk' output may be truncated before the last format character [-Werror=format-truncation=]
 neg_num : '-' NUM     {snprintf($$,sizeof($$),"-%s",$2);}
                                               ^~~~~
In file included from /usr/include/stdio.h:862:0,
                 from ./int.h:31,
                 from ASN1.y:30:
/usr/include/x86_64-linux-gnu/bits/stdio2.h:64:10: note: '__builtin___snprintf_chk' output between 2 and 66 bytes into a destination of size 65
   return __builtin___snprintf_chk (__s, __n, __USE_FORTIFY_LEVEL - 1,
          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        __bos (__s), __fmt, __va_arg_pack ());
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ASN1.y:164:47: error: '__builtin___snprintf_chk' output may be truncated before the last format character [-Werror=format-truncation=]
                 | '-' NUM        {snprintf($$,sizeof($$),"-%s",$2);}
                                               ^~~~~
In file included from /usr/include/stdio.h:862:0,
                 from ./int.h:31,
                 from ASN1.y:30:
/usr/include/x86_64-linux-gnu/bits/stdio2.h:64:10: note: '__builtin___snprintf_chk' output between 2 and 66 bytes into a destination of size 65
   return __builtin___snprintf_chk (__s, __n, __USE_FORTIFY_LEVEL - 1,
          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        __bos (__s), __fmt, __va_arg_pack ());
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cc1: all warnings being treated as errors
Makefile:1112: recipe for target 'ASN1.lo' failed
make[2]: *** [ASN1.lo] Error 1
make[2]: Leaving directory '/home/junxie/Downloads/libtasn1-4.9/lib'
Makefile:1176: recipe for target 'check-recursive' failed
make[1]: *** [check-recursive] Error 1
make[1]: Leaving directory '/home/junxie/Downloads/libtasn1-4.9/lib'
Makefile:1009: recipe for target 'check-recursive' failed
make: *** [check-recursive] Error 1
```
&emsp;&emsp;至此，我已快崩溃，已经不知道自己在哪儿，是要干啥。网上已经几乎找不到相关问题词条，估计还没有人遇到过这些问题。
&emsp;&emsp;很想吐槽一下Linux。虽然用户可以随心所欲DIY，但是起点似乎有点太高。所谓的DIY也不过是把好多人写的代码集合在自己电脑上编译，源代码长什么样我虽然比较关心，但哪有时间闲情和精力去看？
&emsp;&emsp;像我这种需要用到Linux处理大量数据且编译程序的便利，又需要用到现成较为成熟程序包编译而不可得的情况，还真是尴尬。这又让我想到了Python。似乎厉害透顶，几乎所有人都在学，都在用，都在把以前用fortran，c写的代码转成python或者用python穿身衣服塑个金身。可结果用起来，某些只能用python2，另一些又只能用python3。有些程序首次用还总告诉你某某module找不到。安装起来还常常不成功。使用起来十分不友好。真是让人头疼恼火啊。也不知大家是怎么喜欢上的。只能怪自己太菜，还没对python开窍吧。
&emsp;&emsp;谁能指条明路？
