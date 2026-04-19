---
title: 文献阅读(39)
abbrlink: 10f5007b
date: 2025-12-11 14:24:43
categories:
  - work
tags:
  - paper
---
&emsp;&emsp;[Lellouch et al. (2019), JGR](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019JB017533)
<!--less-->

## 题目
Seismic Velocity Estimation Using Passive Downhole Distributed Acoustic Sensing Records: Examples From the San Andreas Fault Observatory at Depth
## 第一作者与通讯作者
- 第一作者：A. Lellouch（斯坦福地球物理系，当时为博士后，现以色列本·古里安大学）  
- 通讯作者：A. Lellouch（ ariellel@stanford.edu）  

## 一作同期另外三篇代表性著作
1. Lellouch, A., & Reshef, M. (2019). Velocity analysis and micro-seismic location improvement using moveout-corrected gathers. *Geophysics*, 84(3), KS119-KS131.  
2. Lellouch, A., Yuan, S., Spica, Z., Biondi, B., & Ellsworth, W. L. (2019). Seismic velocity estimation using passive downhole distributed acoustic sensing records: Examples from the San Andreas Fault Observatory at Depth. *Journal of Geophysical Research: Solid Earth*, 124, 6931-6948.（即本文）  
3. Lellouch, A., et al. (2018). *Stanford DAS Array earthquake analysis*. SEG Annual Meeting, Expanded Abstracts.  

## 摘要
准确的地震波速度剖面对于结构成像与震源定位至关重要，但传统主动源 VSP 昂贵且耗时。本文利用安装在圣安德烈亚斯断层深部观测孔（SAFOD）中的井下分布式光纤声波传感（DAS）阵列，仅依靠被动记录的天然地震与背景噪声，提取了 P 波与 S 波速度模型。我们首先用两次近垂直入射的微震（M1.33 与 M2.46）进行初至拾取与局部 slant-stack 扫描，获得 50–750 m 深度范围内 1-m 间隔的 VP 与 VS 剖面；其次用 1 天连续背景噪声做井中干涉测量，仅提取 VP。  
&gt; 结果显示：① 地震法得到的 VP 与 2005 年常规检波器 VSP 相差 &lt;3%，但分辨率显著提高；② 首次给出了该段 VS 剖面；③ 发现 50–100 m、300–500 m、500–750 m 三个速度段及 500–520 m 处 VP/VS 局部异常；④ 在 500 m 处识别出强 SP 转换事件，佐证了该异常。  
&gt; 背景噪声干涉法 VP 结果介于区域模型与地震法之间，但无法获得 VS。研究表明，永久井下 DAS 可利用微震与噪声实现低成本、高分辨率、可重复的速度表征，为断层区浅层结构监测提供了新途径。  

## 相关研究的重要性
| 序号 | 重要性 | 前人具体工作 | 存在的不足 |
|---|---|---|---|
| 1 | 断层区浅层速度是震源精确定位、地震灾害评估的基础 | Thurber et al. (2006, 2018) 用井中检波器 VSP 获得 SAFOD 附近 VP | 成本高、无法长期重复；S 波难以激发 |
| 2 | 浅层低速带误差会向下传播，影响深部成像与储层描述 | Armstrong et al. (2001); Blias (2009) | 传统表面地震缺乏 10–100 m 尺度分辨率 |
| 3 | 需要一种可永久布设、耐高温高压、兼顾 P/S 波的速度监测手段 | Daley et al. (2013, 2016) 首次现场验证 DAS 可记录地震波 | 仅展示记录能力，未系统提取速度模型；未给出 VS |
| 4 | 微震被动速度建模可避免主动源环保与成本问题 | Miyazawa et al. (2008) 用井中检波器噪声干涉得 VP | 未使用 DAS；未给出 VS；未与 VSP 对比 |
| 5 | 光纤应变-速率转换与角度敏感性导致 S 波成像困难 | Dean et al. (2017); Martin (2018) | 理论上 DAS 对平行传播 S 波不敏感，实际处理策略缺失 |

## 本文使用的数据
| 类型 | 细节 |
|---|---|
| 地震事件 | 2017-06 美国地质调查局目录中 M1.33（Z=11.16 km，Δ=1.87 km）与 M2.46（Z=11.43 km，Δ=2.49 km） |
| DAS 记录 | SAFOD 主孔 0–800 m， SMF-28 单模光纤，10 m  gauge length，1 m 道距，2 500 Hz 采样，22 天连续 |
| 背景噪声 | 上述光纤 1 天连续数据（去除地震段） |
| 对比数据 | 2005 年同一孔眼 3-C 检波器 VSP（炮点偏移 40 m，15 m 间隔，55 Hz 主频）与 Hole et al. (2006) 区域表面地震 VP 模型 |

## 采用的方法
| 步骤 | 方法要点 |
|---|---|
| 1 | 地震选取与质量控制：USGS 目录匹配，信噪比筛选 |
| 2 | 初至拾取：线性规划最大化振幅，零交叉校正，50 m 平滑 |
| 3 | 局部 slant-stack：150 m 高斯窗，30 m/s 速度扫描，semblance 最大，自动拾取 VP 与 VS |
| 4 | 背景噪声干涉：井中相邻道 50 m 间隔互相关，1 天叠加，二次插值得走时，反演 VP |
| 5 | VS 提取专用流程：P 波 moveout→f-k 滤波→残余 S  moveout→自动拾取 |
| 6 | 误差分析：拾取加 Gaussian 误差（P 4 ms，S 20 ms）+  bootstrap 10 000 次；slant-stack 用 0.95/0.8 峰值 semblance 宽度 |

## 获得的结果
- 0–800 m 高分辨率 VP、VS 剖面（1 m 间隔），与检波器 VSP 平均差异 &lt;3%。  
- 发现三段速度结构：0–100 m 未固结冲积层（VP/VS≈3），100–300 m 压实沉积，300–500 m 低速稳定层，500–750 m 再次压实。  
- 500–520 m 处 VP/VS 局部峰值（≈2.4）与强 SP 转换事件吻合，解释为局部流体/裂隙带。  
- 背景噪声 1 天即可得中等分辨率 VP，但频率低（5–20 Hz），无 VS。  

## 本文创新之处
| 创新点 | 说明 |
|---|---|
| 首次 | 将井下 DAS 被动地震记录用于同时提取 P 与 S 波速度剖面 |
| 首次 | 把背景噪声井中干涉法应用于 DAS 数据提取体波 VP |
| 方法 | 提出针对 DAS 角度敏感性的 S 波 f-k + 双 moveout 滤波拾取流程 |
| 验证 | 与同一井眼常规 VSP 检波器结果定量对比，误差 &lt;3%，分辨率提升 15 倍（1 m vs 15 m） |
| 发现 | 揭示 SAFOD 上 800 m 三段速度结构及 500 m 处 VP/VS 异常，被独立 SP 转换事件佐证 |

## 主要贡献
1. 证明永久井下 DAS 可替代/补充昂贵 VSP，实现零成本重复速度监测。  
2. 提供一套可移植的被动源 VP/VS 建模流程（拾取 + slant-stack + 干涉）。  
3. 为圣安德烈亚斯断层近地表精细结构、流体分布与应力场研究提供新的高分辨率模型。  

## 不足与展望
| 不足 | 可能的改进 |
|---|---|
| 仅两件可用地震，M2.46 因文件头缺失未用于 VS | 延长记录期，联合区域台网目录增加事件数 |
| S 波拾取仍受 P 尾波、转换波干扰，误差大 | 引入极化分析、多分量 DAS 或 3-C 检波器联合 |
| 背景噪声法无 VS | 尝试利用微震尾波或旋转噪声提取 Rayleigh 波 |
| 光纤深度-空间映射假定电缆无松弛 | 采用主动脉冲标定或分布式温度传感补偿 |
| 未考虑 3-D 射线弯曲与各向异性 | 结合走时层析或全波形反演进一步提高精度 |
