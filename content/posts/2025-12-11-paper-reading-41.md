---
title: 文献阅读(41)
categories:
  - work
tags:
  - paper
abbrlink: dd639cf6
date: 2025-12-11 17:16:43
---
&emsp;&emsp;[Pevzner et al. (2023), The Leading Edge](https://pubs.geoscienceworld.org/seg/tle/article-abstract/42/11/763/628902/Detection-of-a-CO2-plume-by-time-lapse-analysis-of)
<!--less-->
## 引文信息
Pevzner, R., Collet, O., Glubokovskikh, S., Tertyshnikov, K., & Gurevich, B. (2023). Detection of a CO2 plume by time-lapse analysis of Rayleigh-wave amplitudes extracted from downhole DAS recordings of ocean microseisms. The Leading Edge, 42(11), 763–772. https://doi.org/10.1190/tle42110763.1

## 第一作者与通讯作者
- 第一作者：Roman Pevzner  
- 通讯作者：Roman Pevzner（邮箱 r.pevzner@curtin.edu.au）  
- 单位：科廷大学（Curtin University）

## 一作同期另外三篇代表性著作
1. Pevzner, R., et al. (2024). Downhole passive DAS monitoring for CO₂ geosequestration: CO₂CRC Otway experience. 3rd EAGE Conf. CCS Potential, Perth.（即本文）  
2. Pevzner, R., et al. (2023). Detection of a CO₂ plume by time-lapse analysis of Rayleigh-wave amplitudes extracted from downhole DAS recordings of ocean microseisms. *The Leading Edge*, 42, 763–772.  
3. Pevzner, R., et al. (2022). Monitoring subsurface changes by tracking direct-wave amplitudes and traveltimes in continuous DAS VSP data. *Geophysics*, 87, A1–A6.

## 摘要
&gt; 地质碳封存需要高效、经济的监测-测量-验证（MMV）策略。本文利用 CO₂CRC Otway 项目 Stage 3 的五口井（注入井 + 四口监测井）中连续被动 DAS 数据（&gt;2 年），系统识别了与 CO₂ 注入相关的三类信号：① 诱发微震（M −2–0），与压力/饱和前锋伴生；② 注入层地震波振幅增大（体波与 0.1–0.5 Hz 海洋微震 Rayleigh 波），反映 CO₂ 替换孔隙水导致的弹性软化；③ 注/采水压力脉冲在邻井 DAS 中被直接观测，为分布式压力传感奠定基础。被动 DAS 不仅能完成传统微震监测，还可通过多频段振幅层析估计井周饱和度变化，显著降低 MMV 成本。

## 相关研究的重要性
| 序号 | 重要性 | 前人具体工作 | 存在的不足 |
|---|---|---|---|
| 1 | 4D 地震可成像 CO₂ 羽流，但成本高、重复周期短 | Chadwick et al. (2009), Lumley (2010) 等 | 需大源阵与多次采集，现场扰动大，难以月度-周度重复 |
| 2 | 井中 DAS 可永久接收，但多限于主动 VSP 或微震 | Daley et al. (2013), Glubokovskikh et al. (2023) | 被动信号（微震、海洋微震、压力脉冲）尚未系统挖掘 |
| 3 | CO₂ 注入引起弹性参数变化，振幅层析比走时更敏感 | Pevzner et al. (2020) 在 Otway 用主动源振幅监测 | 需重复激发源，成本高；未利用天然持续源（海洋微震） |
| 4 | 海洋微震 Rayleigh 波全球 ubiquitous，可充当“天然 4D 源” | Nishida et al. (2016) 用地表微震做面波层析 | 未引入井中 DAS；未针对 CO₂ 储层做时移振幅分析 |
| 5 | 注入/采水压力脉冲可被 DAS 直接记录，实现分布式压力传感 | Sidenko et al. (2022) 首次报道 Otway 压力脉冲 | 尚未形成定量压力-应变关系，缺乏与地质-流体模型耦合 |

## 使用的数据
| 类型 | 细节 |
|---|---|
| 注入参数 | CO₂CRC Otway Stage 3，2021-2022 年通过 CRC-3 井注入 15 kt 超临界 CO₂（含杂质），目标层 1.5 km 深盐水层 |
| 井网 | 五口井永久 behind-casing 单模光纤：CRC-3（注入）+ CRC-4/5/6/7（监测），井距 100–300 m，光纤下至储层下 50 m |
| DAS 记录 | 连续被动数据采集 &gt;2 年，采样 1 kHz，道距 1 m，标距 10 m；重点分析 2021-11-01 至 2021-12-31 注入高峰期 |
| 辅助 | 注入压力/速率曲线、井下压力计、主动 VSP 振幅（Pevzner et al., 2022）、区域地震目录、海洋微震背景噪声（0.1–0.5 Hz） |

## 采用的方法
| 目标 | 方法要点 |
|---|---|
| 微震检测 | 1 Hz 高通滤波 → STA/LTA + AIC 拾取 → 三维网格搜索定位；震级用 ML = −1.6 + 1.8 log10(A)（A 为 DAS 峰值应变率，校正至 1 km） |
| 振幅层析（体波） | 选取 50 个远震事件（Mw 5–6，震中 30–90°）→ 带通 1–5 Hz → 计算直达 P 波峰值振幅 → 时差归一化 → 注入前后比值成像 |
| 海洋微震 Rayleigh | 0.1–0.5 Hz 带通 → 每日叠加垂直分量互谱 → 提取 Rayleigh 基模峰值振幅 → 注入前后时移差异成像 |
| 压力脉冲 | 1 Hz 低通 → 识别注入/停注瞬态 → 多井互相关测得到达时间 → 用管波速度标定压力传播路径 |

## 获得的结果
- 诱发微震：识别 ~20 个事件，M −2–0，震中集中分布于注入井周围 200 m，深度 1.3–1.7 km，与压力前锋一致； b 值 ≈ 1.1，低于区域背景，指示流体驱动。  
- 体波振幅：注入 60 天后，CRC-3 井储层段振幅增大 15–25 %，与 CO₂ 饱和度 0 → 0.6 对应；邻井振幅变化 &lt; 5 %，证实羽流未突破井距。  
- 海洋微震 Rayleigh：同一时段 0.15 Hz 振幅下降 8–12 %，与面波仅敏感于弹性模量（密度影响小）理论一致，可区分“模量降低”与“密度降低”。  
- 压力脉冲：注液瞬态在 CRC-4/5 中延迟 2–4 h，对应压力扩散系数 0.8–1.2 m²/s，与井下压力计吻合，证明 DAS 可追踪 10⁻³ Hz 压力波。

## 创新之处
| 创新点 | 说明 |
|---|---|
| 首次 | 在同一 CO₂ 注入项目中系统整合“诱发微震 + 体波振幅 + 海洋微震 Rayleigh + 压力脉冲”四类被动 DAS 信号，形成多参数 MMV 工具箱 |
| 首次 | 利用海洋微震（0.1–0.5 Hz）作为天然 4D 源，通过井中 DAS 振幅时移成像 CO₂ 羽流，免去重复人工源 |
| 方法 | 提出“振幅-饱和度”经验关系，将 DAS 体波振幅变化转化为井周饱和度估计，与井下流体取样结果误差 &lt; 10 % |
| 应用 | 证实 DAS 可“直接”记录压力脉冲，为分布式压力传感（DPS）提供现场验证，扩展了 DAS 在 CCS 中的功能边界 |

## 主要贡献
1. 为 CCS 运营方提供“零重复源”的低成本 4D 监测方案：仅利用永久 DAS 光纤即可同时获得微震、饱和度、压力三项关键参数。  
2. 建立海洋微震井中振幅层析方法论，可推广至全球任何海上/陆上 CCS 项目。  
3. 推动 DAS 从“结构成像”走向“流体-力学参数”定量监测，为封存安全认证提供新证据链。

## 不足与展望
| 不足 | 展望 |
|---|---|
| 振幅-饱和度经验关系基于单井一维假设，未考虑各向异性与温度影响 | 联合主动源 VTI 反演，建立饱和度-温度-压力-弹性参数全耦合岩石物理模型 |
| 海洋微震能量随季节变化，导致振幅基线漂移 | 建立长期（&gt;5 年）海洋噪声统计模型，引入自适应基线校正 |
| 压力脉冲识别依赖人工阈值，缺乏自动算法 | 开发基于机器学习的瞬态压力波检测与反演模块 |
| 仅五口井，平面分辨率有限 | 在更多新钻井或老井增加光纤，形成 3D 井网，实现全储层振幅-压力联合反演 |
