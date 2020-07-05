---
title: 如何调用fftw进行Fast Fourier Transform
abbrlink: '7866e538'
date: 2020-07-05 18:21:16
categories:
tags:
---
&emsp;&emsp;我们常常要看信号的振幅谱来进行分析，那傅里叶变换就必不可少。如果水平不错你可以试着自己写。当然有很多已经写好的包，非常方便，例如这里要讲到的fft[^1]。
<!-- more -->

&emsp;&emsp;他的用法其实人家[主页](http://www.fftw.org/)说明文档讲的很清楚。我这里就记录一下怎么用之来对sac文件进行读取并计算fft。程序是用fortran写的，C的话可以参考fftw说明文档。
首先把主程序贴出来：
```
program main
use globe_data  // 全局变量
use sacio       // sac 头变量
implicit none
integer i,nerr,itest
character (180) :: sacfile,tmp
type(sac_head) :: sachead
complex(8),allocatable,dimension(:) :: s1,s2
if (iargc().ne.2)stop 'Usage: fft sacfile '
call getarg(1,sacfile)    // 读参数到sacfile，即sac 文件
call read_sachead(trim(sacfile),sachead,nerr) //读sac文件头变量
npts=sachead%npts
dt=sachead%delta
nn=2
npow=1
do while(nn.le.npts)
   nn=nn*2
   npow=npow+1
enddo
nk=nn/2+1
halfn=20
dom=dble(1.0/nn/dt)
allocate(sig(nn,3))
call read_sac(trim(sacfile), sig(:,1),sachead,nerr) //读sac文件数据到sig(:,1)
allocate(s1(nn),s2(nn))
s1=czero
s1(1:npts)=dcmplx(dble(sig(1:npts,1)),0.0d0)
call dfftw_plan_dft_1d(plan,nn,s1,s2,FFTW_FORWARD, FFTW_ESTIMATE)
call dfftw_execute(plan)
call dfftw_destroy_plan(plan)
sachead%npts=nk
sig(:,1)=real(dreal(s2))
call write_sac(trim(sacfile)//'_fft',sig(:,1),sachead,nerr) ! problem with nerr=-1
deallocate(sig,s1,s2)
end program
```
这里sig(:,:)是个二维数组，其实用一维的就够了哈。
sacio.f90 是一个module，定义了sac文件的头，并含有sac读写程序。需要的话给我发信息，或者邮件^_^。
globe_data.f90也是一个module，定义了全局变量：
```
module globe_data
integer,parameter :: nmax=2000000,nstmax=1000
real(4),dimension(4,2):: fre
real(4),allocatable,dimension(:,:):: sig,sigo
real(4),allocatable,dimension(:) :: sigt
real :: dt
real(8) :: dom
integer :: halfn
integer :: ncom,comb,npts
integer :: nn,npow,nk,nf
complex(8),allocatable,dimension(:,:):: seisout
complex(8),parameter:: czero=(0.0d0,0.0d0)
integer,parameter :: FFTW_ESTIMATE=64,FFTW_MEASURE=1
integer,parameter :: FFTW_FORWARD=-1,FFTW_BACKWARD=1
integer(8) :: plan,plan1,plan2,plan3
end module
```
编译需要一个makefile：
```
FC=gfortran
FFLAG=-lfftw3 -I /usr/include -L /usr/lib64 -fbounds-check
objects=call_fft.o sacio.o globe_data.o
all:sacio.mod globe_data.mod call_fft
.f.o:
	$(FC) $(FFLAG) $< -c
%.o:%.f90
	$(FC) $(FFLAG) $< -c 
sacio.mod:sacio.f90
	$(FC) $< -c
globe_data.mod:globe_data.f90
	$(FC) $< -c
call_fft:$(objects)
	$(FC) $^ -o $@ $(FFLAG) -lm
clean:
	-rm *.o *.mod 
```
注意这里要加上-lfftw3表示调用fftw，-I给定fftw头的路径，-L给定fftw的lib。如果是按照默认路径安装的fftw，那一般都不用指定-I和-L，因为默认路径一般已经包含在编译环境里了。
好了大功告成了。



[^1]: http://www.fftw.org/
