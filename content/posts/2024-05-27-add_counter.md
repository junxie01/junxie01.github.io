---
title: Hexo添加字数统计
abbrlink: '986e5406'
categories: 
   - web
date: 2024-05-27 16:50:09
tags:
    - hexo
    - web
---
1. 修改根目录下的_config.yml. 找到busuanzi_count:
enable: true

2. 修改themes下的_config.yml. 找到footer：
counter: true

3. 修改themes/next/layout/_partials/footer.njk，添加:
```
{% if theme.footer.counter %}
    <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
{% endif %}
```
