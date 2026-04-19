---
title: 文献阅读(37)
categories:
  - work
tags:
  - paper
abbrlink: 8e762df5
date: 2025-12-10 19:31:10
---
&emsp;&emsp;[Ma et al. (2024), Geophysics](https://pubs.geoscienceworld.org/seg/geophysics/article-abstract/89/4/D183/643890/Distributed-acoustic-sensing-microseismic)
<!--less-->

### 引文信息
Ma, Y., Ajo-Franklin, J., Nayak, A., Zhu, X., Correa, J., & Kerr, E. (2024). Distributed acoustic sensing microseismic reflection imaging for hydraulic fracture and fault lineament characterization. Geophysics, 89(4), D183–D192. https://doi.org/10.1190/geo2023-0582.1

### 一作与通讯作者信息
- **第一作者 & 通讯作者**：Yuanyuan Ma  
  **单位**：Rice University, Department of Earth, Environmental & Planetary Sciences, Houston, Texas, USA  
  **邮箱**：ym50@rice.edu

---

### 一作近三年三篇代表性著作
1. Ma, Y., Eaton, D. W., Wang, C., & Aklilu, A. (2023). *Characterizing hydraulic fracture growth using DAS-recorded microseismic reflections*. Geophysics, 88(6), WC47–WC57.  
   → 首次现场验证 DAS 微地震反射波可成像远端裂缝，与 LF-DAS 联合解释。

2. Ma, Y., Ajo-Franklin, J., Nayak, A., Zhu, X., & Correa, J. (2023). *DAS microseismic reflection imaging for hydraulic fracture and fault zones mapping*. SEG IMAGE Expanded Abstracts.  
   → 提出 3D 预堆 Kirchhoff 迁移流程，不再假设裂缝平面。

3. Staněk, F., Jin, G., & Ma, Y. (2022). *Fracture imaging using DAS-recorded microseismic events*. Frontiers in Earth Science, 10, 907749.  
   → 构建射线追踪 2D 成像框架，为本文 3D 升级奠定理论基础。

---

### 摘要

&gt; 本研究提出一套全新流程，对井下分布式声波传感（DAS）记录的微地震反射 S 波进行三维偏移，以刻画水力压裂裂缝网络。与现有常假设裂缝为平面或预设走向的方法不同，本技术无需任何几何先验。DAS 公里级光纤提供大孔径与 &lt;1 m 空间采样，可捕获远超传统井中检波器的强反射信号。我们将每个微地震事件视为高频点源，对分离后的反射波场逐源执行预堆 Kirchhoff 偏移，并将多源结果聚类叠加，生成 3D 反射率体。高分辨率图像照亮了储层核心刺激带——这一区域传统地面阵列或主动源难以触及。为验证流程，本文使用美国南德克萨斯 Eagle Ford 页岩与 Austin 白垩层多井拉链压裂 DAS 数据，将反射成像与微地震云及低频 DAS 应变测量联合解释。结果提升了对裂缝几何的认识，可直接估算缝长与缝高，并指示远端含液先存断层。该框架具备实时监测与动态追踪裂缝演化的潜力。

---

### 相关研究的重要性

1. **微地震云≠裂缝面**  
   事件点集无法显示未激活断层或远端裂缝，且定位误差 30–50 m，难以支撑“分段-分簇”优化。

2. **DAS 高密度优势待挖掘**  
   千米光纤 1 m 道距、&gt;200 Hz 频率，可记录丰富反射波，但业界多聚焦直达波定位，大量反射信息被丢弃。

3. **主动源高频受限**  
   地面震源主频 30–60 Hz，难以分辨 &lt;10 m 裂缝；微地震事件在储层内部，频率 200–600 Hz，分辨率潜力高。

4. **2D 反射成像不足以指导工程**  
   现有 DAS 反射研究仅限“事件-光纤”平面，无法给出缝高、走向变化，工程决策仍需 3D 裂缝体。

---

### 前人研究及不足

| 研究 | 内容 | 不足 |
|------|------|------|
| **Lin & Zhang (2016)** | 井中 3C 检波器微地震逆时偏移 | 检波器稀疏（10 级），反射波识别难；未用 DAS |
| **Grechka et al. (2017)** | 3C 检波器反射成像 | 假设裂缝平面，2D 成像，未给出缝高 |
| **Staněk et al. (2022)** | DAS 射线追踪 2D 成像 | 仅单事件平面，无 3D 体，无多源叠加 |
| **Ma et al. (2023a)** | DAS 反射波 2D 成像 + LF-DAS 验证 | 仍假设垂直裂缝，未拓展到 3D，无聚类叠加 |
| **Reshetnikov et al. (2023)** | 照明分析与 AVO | 聚焦振幅解释，未解决 3D 几何与聚类权重 |

---

### 本文数据

| 数据 | 说明 |
|------|------|
| **DAS 微地震原始记录** | 南德州 Eagle Ford + Austin 白垩，两口水平拉链压裂井（well 3 & 5）；well 3 光纤 3.1 km，1 m 道距，10 m gauge，1 kHz 采样 |
| **微地震目录** | 地面 2653 事件，Mw −2.5–0.5；人工筛选 232 个含清晰反射 S 波事件 |
| **速度模型** | 1D 横向各向同性（VTI）Vp 模型，Vp/Vs=1.81，拟合直达 P/S 走时 |
| **LF-DAS 应变数据** | 同一光纤 &lt;0.1 Hz，独立拾取跨井 frac-hit，用于裂缝撞击验证 |

---

### 本文方法

1. **预处理与事件优选**  
   空间 median + 带通 10–200 Hz；保留 Mw ≥ −1.5 且反射 S/N &gt; 阈值事件（100 个）

2. **波场分离**  
   f-k 滤波分 heel/toe 向 → 手动 mute 直达 S 波，提取纯反射

3. **3D 预堆 Kirchhoff 偏移**  
   逐源计算 S 波走时表（eikonal 求解器），双支成像后取绝对值叠加，消除震源极性差异

4. **空间聚类叠加**  
   - 将 100 事件按震源位置聚为 8 簇  
   - 簇内等权叠加 → 簇间等权叠加，避免高密度簇产生伪影  
   - 3 × 3 中值滤波去噪，输出 10 m³ 网格 3D 反射率体

5. **多数据联合验证**  
   与微地震云、LF-DAS frac-hit、最大水平应力方向（SHmax）对比，估算缝长、缝高、走向

---

### 本文结果

1. **3D 高分辨率裂缝体**  
   - 缝长半长 ≥400 m，缝高 300 m，走向 42.5° 与 SHmax 一致  
   - 空间分辨率 ≈3.5 m（中心频率 150 Hz，Vs≈2.5 km/s）

2. **与微地震云高度一致**  
   反射像延伸方向、范围与事件云吻合，但给出更远端细节（图 8）

3. **与 LF-DAS 交叉验证**  
   stage 13 frac-hit 与反射像位置误差 &lt;20 m；stage 8 弱反射对应早期压裂连通先存断层（图 10）

4. **揭示先存断层含液路径**  
   远场高反射能量带与微地震云不重合，推测为含液断层，提供潜在流体通道（图 7e–h）

---

### 创新点与贡献

| 创新 | 贡献 |
|------|------|
| **首次实现“无几何假设”3D DAS 微地震反射裂缝成像** | 摒弃平面/垂直假设，直接输出 10 m³ 网格裂缝体，工程上可直接读取缝长、缝高 |
| **提出“空间聚类-等权叠加”策略** | 解决微地震源分布极不均、极性相反导致伪影问题，为行业提供可复制的叠加范式 |
| **给出 3.5 m 分辨率量化指标** | 明确中心频率-速度-采样关系，为后续场地提供参数设计依据 |
| **联合微地震云+LF-DAS 三重验证** | 形成“事件定位-应变撞击-反射成像”闭环，提升解释可信度 |

---

### 不足与未来方向

| 不足 | 说明 |
|------|------|
| **事件选手动干预大** | 目前人工挑选高 S/N 事件，未来需机器学习自动识别反射波 |
| **近光纤 40 m 成像盲区**  
