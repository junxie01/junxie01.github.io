---
title: 如何发布你自己的脚本
tags:
  - python
categories:
  - python
abbrlink: c743ea3e
date: 2025-07-01 11:07:47
---
&emsp;&emsp;你是不是也想让自己的程序像obspy一样，叫全世界的人pip install就可以用？
<!--less-->
&emsp;&emsp;这里以一个简单的例子来说明如何创建自己的程序、打包并发布到PyPI。
# 创建自己的项目
首先创建一个目录mypkg_project，结构如下：
```
mypkg_project/
├── mypkg/
│   ├── __init__.py
│   └── utils.py
├── README.md
├── setup.py
├── pyproject.toml
```
# 编写包的内容
在mypkg/utils.py内写入：
```
def add(a, b):
    return a + b
```
在mypkg/__init__.py内写入：
```
from .utils import add
```
# 添加元数据文件README.md
在README.md中写入：
```
# mypkg
A simple Python package with an add function.
```
在setup.py中写入：
```
from setuptools import setup, find_packages
setup(
    name='mypkg',
    version='0.1',
    author='Your Name',
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
```
在pyproject.toml中写入：
```
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```
# 项目打包
在根目录mypkg_project/中运行：
```
python3 -m pip install --upgrade build
python3 -m build
```
会生成：
```
dist/
├── mypkg-0.1-py3-none-any.whl
└── mypkg-0.1.tar.gz
```
# 本地安装
用pip就可以本地安装：
```
pip install dist/mypkg-0.1-py3-none-any.whl
```
利用python就可以调用：
```
from mypkg import add
add(2, 3)
```
# 上传到PyPI（公开发布）
首先安装twine：
```
pip install twine
```
发布：
```
twine upload dist/*
```
这里会提示你输入PyPI的用户名和密码。这一步需要首先到[PyPI](https://pypi.org/account/register/)注册账号，发布的时候需要用token
```
twine upload --repository pypi dist/* -u __token__ -p pypi-<your_token>
```
上传成功之后可以在https://pypi.org/project/mypkg/访问。
然后任何人都可以安装你的脚本了：
```
pip install mypkg
```

