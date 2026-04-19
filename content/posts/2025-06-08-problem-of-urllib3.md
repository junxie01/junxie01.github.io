---
title: urllib3的问题
tags:
  - python
categories:
  - work
abbrlink: 4cf90829
date: 2025-06-08 14:12:26
---
&emsp;&emsp;安装了seisman的[HinetPy](https://github.com/seisman/HinetPy)，运行脚本数据下载脚本的时候就遇到这个问题：
```
from HinetPy import Client, win32
  File "/home/junxie/work/Snet/HinetPy-main/HinetPy/__init__.py", line 23, in <module>
    from .client import Client
  File "/home/junxie/work/Snet/HinetPy-main/HinetPy/client.py", line 22, in <module>
    from urllib3.util import create_urllib3_context
ImportError: cannot import name 'create_urllib3_context' from 'urllib3.util' (/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/__init__.py)
```
怎么整？
<!--less-->
&emsp;&emsp;遇到问题不要歪，凡事都来找AI。
&emsp;&emsp;于是我把问题贴给了chatGPT，它说：
   * 方法1 给urllib3降级，降到1.26.x，可我的就是1.26.16，pass
   * 方法2 更新HinetPy到最新版本，可人家都就是最新版本啊，pass
   * 方法3 手动patch，具体是将client.py中的
```
from urllib3.util import create_urllib3_context
```
&emsp;&emsp;替换为
```
from ssl import create_default_context as create_urllib3_context
```
&emsp;&emsp;看起来挺靠谱的。于是出现了这个问题
```
  File "/home/junxie/work/Snet/HinetPy-main/HinetPy/client.py", line 139, in __init__
    self.login(user, password)
  File "/home/junxie/work/Snet/HinetPy-main/HinetPy/client.py", line 188, in login
    self.session.mount(self._HINET, AddedCipherAdapter())
  File "/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/requests/adapters.py", line 155, in __init__
    self.init_poolmanager(pool_connections, pool_maxsize, block=pool_block)
  File "/home/junxie/work/Snet/HinetPy-main/HinetPy/client.py", line 47, in init_poolmanager
    ctx = create_urllib3_context(ciphers=":HIGH:!DH:!aNULL")
TypeError: create_default_context() got an unexpected keyword argument 'ciphers'
```
&emsp;&emsp;然后，各种折腾一翻，删除，重装还是不行，看看模块create_urllib3_context
```
grep create_urllib3_context /home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/*.py
```
&emsp;&emsp;长这样：
```
/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/proxy.py:from .ssl_ import create_urllib3_context, resolve_cert_reqs, resolve_ssl_version
/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/proxy.py:    ssl_context = create_urllib3_context(
/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/ssl_.py:def create_urllib3_context(
/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/ssl_.py:        context = ssl_.create_urllib3_context()
/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/ssl_.py:        be created using :func:create_urllib3_context.
/home/junxie/.conda/envs/py3/lib/python3.9/site-packages/urllib3/util/ssl_.py:        context = create_urllib3_context(ssl_version, cert_reqs, ciphers=ciphers)
```
&emsp;&emsp;表明urllib3安装是正确的。所以在client.py中，将这一句：
```
from urllib3.util import create_urllib3_context
```
&emsp;&emsp;改为：
```
from urllib3.util.ssl_ import create_urllib3_context
```
&emsp;&emsp;然后就万事大吉了。总结：不懂就问AI吧，但不好好学习和思考，到头来还是不懂。然而这又有什么关系，只要有AI在，会问AI问题就行了。没AI的话，那就拜拜了。
