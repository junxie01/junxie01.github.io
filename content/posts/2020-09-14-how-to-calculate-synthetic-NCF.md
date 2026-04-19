---
title: 怎么计算理论的NCF？
abbrlink: ce006a34
date: 2020-09-14 15:55:31
categories:
  - work
tags:
  - sem
  - NCF
---
![Distribution of ambient noise sources (100-300 s) (Ermert et al., 2017 )](source_dis.png)
<!-- less -->
&emsp;&emsp;好久没有更新博客了。原因是上个月文章修改意见下来了，第二轮大修，这酸爽，难以言表。
&emsp;&emsp;不知道啥时候开始（大概是Fichter和Ermert的文章发表之后），做噪声互相关工作总会被审稿人问：噪声源影响有多大啊？难为人啊。要是能像Ermert他们把源和结构一块儿做了不就结了。但那是人家的手艺，捡起来难啊。
&emsp;&emsp;另一个方法就是做模拟。给定源，计算两点波形，做胡相关，叠加。一维，近距离还好做，全球的三维的咋办？
&emsp;&emsp;还好有大神啊。人家Tromp et al. (2010)早都弄出来了。就是用Specfem3d_globe就可以了。
&emsp;&emsp;其实specfem3d_globe的说明文档已经讲的很清楚了，我这里就简单说一下。一般，波形的正演模拟只需要一步，而ensemble average的NCF需要两步，要计算敏感核函数需要三步。需要注意的点主要有：
&emsp;&emsp;1，NCF的模拟不需要CMTSOLUTION，需将其六分量设置为0。
&emsp;&emsp;2，There are other parameters in DATA/Par_file which should be given specific values. For instance, NUMBER_OF_RUNS and NUMBER_OF_THIS_RUN must be 1; ROTATE_SEISMOGRAMS_RT, SAVE_ALL_SEISMOGRAMS_IN_ONE_FILES, USE_BINARY_FOR_LARGE_FILE and MOVIE_COARSE should be .false.. Moreover, since the first two steps for calculating noise cross-correlation kernels correspond to forward simulations, SIMULATION_TYPE must be 1 when NOISE_TOMOGRAPHY equals 1 or 2. Also, we have to reconstruct the ensemble forward wavefields in adjoint simulations, therefore we need to set SAVE_FORWARD to .true. for the second step, i.e., when NOISE_TOMOGRAPHY equals 2. The third step is for kernel constructions. Hence SIMULATION_TYPE should be 3, whereas SAVE_FORWARD must be .false.. （从使用手册抄的，关于Par_file的设置)
&emsp;&emsp;3，利用EXAMPLES/noise_examples/NOISE_TOMOGRAPHY.m (main program)和EXAMPLES/noise_examples/PetersonNoiseModel.m两个matlab程序获得S_squared。运行该程序需要提供NSTEP和dt。这两个参数在编译之后运行xcreate_header_file会显示。
&emsp;&emsp;4，Create a file called NOISE_TOMOGRAPHY/irec_master_noise. Note that this file should be put in directory NOISE_TOMOGRAPHY as well. This file contains only one integer, which is the ID of the 'maste' receiver. For example, if in this file shows 5, it means that the fifth receiver listed in DATA/STATIONS becomes the ‘master’. That’s why we mentioned previously that the order of receivers in DATA/STATIONS important. （该文件定义了是哪个台与其他台的互相关）
&emsp;&emsp;5，Create a file called NOISE_TOMOGRAPHY/nu_master. This file holds three numbers, forming a (unit) vector. It describes which component we are cross-correlating at the ‘master’ receiv. （该文件定义了哪些分量做胡相关）
&emsp;&emsp;6，Describe the noise direction and distributions in src/specfem3d/noise_tomography.f90. Search for a subroutine called noise_distribution_direction in noise_tomography.f90. It is actually located at the very beginning of noise_tomography.f90. The default assumes vertical noises and a uniform distribution across the whole physical domain. It should be quite self-explanatory for modifications. Should you modify this part, you have to re-compile the source code. (again, that’s why we recommend that you alwaysre-compile the code before you run simulations)（这里根据需要自己给定噪声源的分布。）
&emsp;&emsp;接下来就可以运行了。要得到NCF需要运行要两步，在修改参数运行第二步的时候一定要重新编译一下。
&emsp;&emsp;然后就可以跑了。结果我老是跑不通，老是出错。多番检查发现错误出在子程序print_stf_file()，即输出震源时间函数的子程序。但没有弄明白为什么会出错。这个程序没有产生后续需要调用的参数。大胆的将其注释掉了。然后程序就跑通了。其实在Par_file里面将PRINT_SOURCE_TIME_FUNCTION改为false应该就可以了。在噪声源均匀的情况下，跑出来的NCF与single force差了pi/4，以及一些微小的差异。移动pi/4之后基本能够对上，应该是正确的了。Hooray!
&emsp;&emsp;第三步我是没跑通，估计是因为空间不足，因为我看到中间数据就已经接近900G。不过我要的是synthetic NCF，足够了，有空再试sensitivity kernel吧。
&emsp;&emsp;封面图是我用来做模拟的噪声源分布。结果表明源的影响不大啊。乐。
