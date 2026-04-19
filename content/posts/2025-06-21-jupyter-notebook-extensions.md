---
title: 有趣的jupyter-notebook插件
tags:
  - python
categories:
  - python
abbrlink: 69c8d283
date: 2025-06-21 19:45:32
---

&emsp;&emsp;收集了一些有趣的jupyter notebook插件。
<!--less-->

| **插件名称**               | **简介**                                                                 | **官方链接**                                                                 |
|----------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------|
| **Jupyter Contrib NBe**    | 核心扩展包，集成50+插件（代码补全、变量监控、执行时间显示等）             | [GitHub](https://github.com/ipython-contrib/jupyter_contrib_nbextensions)  |
| **Hinterland**             | 实时代码补全工具，支持 Python/R/Julia，减少拼写错误                      | [文档](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/hinterland/README.html) |
| **Table of Contents (2)** | 动态生成目录，支持标题跳转，适合长文档导航                               | [配置页](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/toc2/README.html) |
| **Variable Inspector**    | 侧边栏实时显示变量类型/大小/值，替代频繁 `print(type)` 操作              | [说明](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/varInspector/README.html) |
| **ExecuteTime**            | 记录每个 Cell 的执行时间和完成时间，优化性能分析                         | [详情](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/execute_time/README.html) |
| **Autopep8**               | 一键格式化代码为 PEP8 标准，提升可读性                                   | [PyPI](https://pypi.org/project/autopep8/)                                |
| **jupyterthemes**          | 界面主题美化，支持暗黑模式/护眼配色（如 `monokai`, `solarized`）          | [GitHub](https://github.com/dunovank/jupyter-themes)                      |
| **Notify**                 | 内核空闲时发送浏览器通知，适合长时间任务（如模型训练）                   | [文档](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/notify/README.html) |
| **jupyter Widgets**        | 创建交互控件（滑块/下拉菜单），将静态图表转为动态仪表盘                  | [官网](https://ipywidgets.readthedocs.io/en/latest/)                      |
| **Voilà**                  | 将 Notebook 转为独立 Web 应用，隐藏代码仅保留交互结果                    | [文档](https://voila.readthedocs.io/en/stable/)                           |
| **RISE**                   | 实时代码幻灯片工具，用 Markdown 标题分页，支持演示中修改参数             | [GitHub](https://github.com/damianavila/RISE)                            |

安装：
```
pip install jupyter_contrib_nbextensions jupyterthemes voila rise
jupyter contrib nbextension install
jupyter nbextension enable [插件名]  # 启用具体插件
```
