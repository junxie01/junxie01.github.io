---
title: 文献阅读(38)
categories:
  - work
tags:
  - paper
abbrlink: 9ee313a
date: 2025-12-11 09:26:29
---
&emsp;&emsp;[Li & Jin (2024), Geophysics](https://pubs.geoscienceworld.org/seg/geophysics/article-abstract/89/2/P11/634865/Using-distributed-acoustic-sensing-to-characterize)
<!--less-->

### 题目
Using distributed acoustic sensing to characterize unconventional reservoirs via perforation-shot triggered P waves

### 第一作者与通讯作者信息
- **第一作者**：Peiyao Li
  - 单位：美国科罗拉多矿业学院（Colorado School of Mines）地球物理系  
  - 邮箱：lipeiyao@mines.edu

---

### 第一作者其他三篇代表性著作
1. Li, P., and Jin, G., 2024. *Using distributed acoustic sensing to characterize unconventional reservoirs via perforation-shot triggered P waves*. Geophysics, 89(2): P11–P19.  
2. Li, P., Jin, G., and Lellouch, A., 2023. *Guided-wave dispersion inversion for shale reservoir properties using DAS-recorded perforation shots*. SEG Technical Program Expanded Abstracts, 342–346.  
3. Li, P., Jin, G., 2022. *P-wave dispersion analysis of DAS-recorded perforation shots for lateral heterogeneity detection in horizontal wells*. Unconventional Resources Technology Conference (URTeC), 2341–2350.

---

### 摘要
非常规储层横向非均质性认识不足常对钻井、完井效率及产量产生负面影响，而现有测井与地震调查手段在刻画此类非均性方面能力有限。我们提出一种替代地球物理方法：利用分布式声波传感（DAS）记录射孔弹激发P波，以刻画非常规储层。在实测数据中，DAS记录的射孔弹产生强P波信号，其波形呈现明显频散。通过对相邻射孔弹信号进行平均，可可靠测量沿水平井的相速度变化。我们观测到一段低相速度异常区，其与测井曲线及三维地震体均方根振幅在空间上吻合。数值模拟验证了P波频散行为的合理性。与建模结果及其他测量对比表明，该方法对非常规储层刻画具有合理探测半径，并可通过对比压裂前后相速度差异推断压裂效果。数据采集可与射孔作业同步进行，成本低且适合现场推广。

---

### 相关研究的重要性
| 研究方向 | 重要性 | 前人研究 | 不足 |
|---|---|---|---|
| **非常规储层横向非均质性** | 直接影响水平井靶窗选择、压裂设计与产量 | NguyenLe & Shin (2019) 指出厚度变化影响产能；Maus et al. (2020) 提出断层导致导向失误 | 测井探测半径&lt;1 m，地震分辨率&gt;25 m，均无法匹配储层厚度（7–12 m） |
| **射孔弹信号利用** | 利用现有作业源，无需额外震源 | Zhang et al. (2019) 用井中检波器记录射孔弹研究各向异性；Lellouch et al. (2019) 用DAS记录导波 | 检波器数量稀疏（11级），空间采样不足；未定量提取相速度 |
| **DAS高频P波分析** | DAS具1 m空间采样、10 kHz采样率，可捕捉短波长 | Jin & Roy (2017) 用DAS低频应变研究裂缝；Byerley et al. (2018) 用DAS-VSP监测压裂 | 多聚焦微震或低频应变，忽视射孔弹P波频散信息 |
| **波导频散反演** | 频散曲线可反演层速度、厚度 | Luo et al. (2021) 用导波频散反演页岩属性 | 仅研究导波，未利用体波P波；缺乏现场验证 |

---

### 本文使用的数据
| 数据类型 | 来源 | 特点 |
|---|---|---|
| **DAS原始炮集** | 美国DJ盆地Codell砂岩水平井，永久光纤外置 | 76段压裂，&gt;300次射孔弹，10 kHz采样，~1 m道距，2500 m水平段 |
| **辅助资料** | 邻井声波时差测井、伽马测井、声幅成像测井 | 厚度7–12 m，速度约3800–4500 m/s |
| **三维地震** | 地表3D地震体 | 提取Codell层均方根振幅，垂向分辨率~25 m |

---

### 采用的方法
| 步骤 | 方法 | 说明 |
|---|---|---|
| **信号提取** | 带通滤波（50–1000 Hz）+ 时空软掩模 | 去除强管波，保留P波 |
| **频散分析** | 多道面波分析（MASW） | 将炮集T(t,x)→频率-相速度域D(f,V)，拾取局部最大脊线 |
| **空间平均** | 100 m滑动窗 | 每窗≥3次射孔弹测量，计算均值与标准误 |
| **数值验证** | Devito 2D 有限差分 | 建立高-低-高速波导模型，重复观测系统，复现频散与高阶模态 |
| **压裂前后对比** |  heel-ward（压裂前）vs toe-ward（压裂后） | 计算相速度差ΔVp，评估压裂诱导变化 |

---

### 获得的结果
| 评估维度 | 主要结果 |
|---|---|
| **频散特征** | P波呈明显正频散：频率↑ 相速度↓；异常区内仅基阶模态，外区出现一阶高阶模态 |
| **异常区一致性** | 低相速度区（1000–2300 m）与低伽马、高裂缝密度、低地震振幅吻合，空间范围介于测井与地震之间 |
| **数值验证** | 模拟复现频散曲线形态与高阶模态激发条件，证实波导陷阱效应 |
| **压裂前后差异** | 平均ΔVp ≈ −26 m/s（↓0.7%），局部最大↓200 m/s（↓5%），显著大于测量不确定度（±33 m/s） |

---

### 创新之处与贡献
| 类别 | 具体内容 |
|---|---|
| **理论创新** | 首次提出**“射孔弹P波频散+ DAS”**刻画非常规储层横向非均质性，填补测井与地震之间的尺度空白（探测半径~50–200 m，空间分辨率~100 m） |
| **方法创新** | 开发**“软掩模-MASW-局部脊线拾取”**流程，实现&gt;300次射孔弹自动频散提取；引入**heel/toe双向采样**策略，天然获得压裂前后对比 |
| **工程贡献** | 无需额外震源与作业停顿，**“光纤随射孔”**成本低；可实时指导后续段簇间距、液量调整 |
| **数据贡献** | 公开DJ盆地完整DAS射孔弹炮集及配套测井，为社区提供新的基准数据集 |

---

### 不足与未来方向
| 不足 | 具体描述 | 未来工作 |
|---|---|---|
| **一维速度模型** | 仅用垂直速度剖面，未考虑横向速度变化 | 2D/3D反演，联合拾取频散与振幅 |
| **高阶模态利用不足** | 仅拾取基阶，未反演厚度与高阶联合 | 多模态联合反演，提高厚度分辨率 |
| **缺乏定量岩石物理** | 仅对比伽马、裂缝计数，未直接输出孔隙度、脆性指数 | 建立**相速度-岩石物性**转换关系，耦合测井校准 |
| **永久光纤成本高** | 目前依赖永久光缆 | 推广**钢丝光缆DAS**，开发实时自动处理模块 |
| **未考虑各向异性** | 忽略页岩TI/HTI影响 | 引入各向异性频散理论，联合S波偏振分析 |
