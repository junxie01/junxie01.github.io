---
title: 如何在自己电脑中部署deepseek
categories:
  - Linux
tags:
  - Linux
abbrlink: 869ca85c
date: 2025-02-05 16:00:13
---
&emsp;&emsp;deepseek很火，我也来凑热闹。之前发布的一些LLM都没关注本地部署，因为似乎要钱，而deepseek是免费的（贫穷限制了我的想象）。
<!--less-->
# Windows下deepseek部署
&emsp;&emsp;首先是在windows下下载[ollama](https://ollama.com/download)并安装。然后在cmd下运行:
```bash
ollama run deepseek-r1:7b
```
其实安装时输入deepseek-r1默认就是7b，大小有4.7G。当然还有其他的版本，自己去搜索并根据自己的GPU大小进行安装。
安装完之后出现了

">>>"

就可以对话了。下次要调用就在cmd中重新运行命令:
```
ollama run deepseek-r1
```

# Linux下deepseek部署
&emsp;&emsp;在Linux下面则这样安装ollama，命令:
```
curl -fsSL https://ollama.com/install.sh | sh
```
这个命令是从github下载ollama进行安装。得保证你能连接到github。接下来安装deepseek:
```
ollama run deepseek-r1:7b
```

# deepseek与zotero结合
deepseek可以和zotero结合进行本地的文献阅读。
这个时候就要安装awsome GPT，位置在[zotero中文社区](https://zotero-chinese.com/plugins/)。配置可以参考[这里](https://zhuanlan.zhihu.com/p/20850142386)。我尝试了一下，没有搞定。有机会再整。


# 图像生成大模型Janus-Pro-7B本地部署
&emsp;&emsp;另外DeepSeek发布的多模态大模型Janus-Pro-7B支持图像生成，也可以[本地部署](https://www.upx8.com/4681)，超厉害。
## 安装Git和conda
## 创建环境：
```
conda create -n mp python=3.10 -y
conda activate mp
```
## 克隆Janus
```
git clone https://github.com/deepseek-ai/Janus.git
cd Janus
```
## 安装依赖
```
pip install -e .
```
## 安装Graio(UI)
```
pip install gradio
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
## 运行
```
python demo/app_januspro.py
```
调用gpu运行
```
python demo/app_januspro.py --device cuda
```
打开本地链接[http://127.0.0.1:7860](http://127.0.0.1:7860)就可以使用。

理想很丰满，现实很骨感，还是没搞定，有时间再整。
