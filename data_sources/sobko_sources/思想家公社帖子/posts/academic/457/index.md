---
post_id: 457
title: GROMACS的安装方法（含全程视频演示）
url: http://sobereva.com/457
date: '2019-01-02T18:11:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章是GROMACS在Linux下的安装方法，属于标准软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**注**：GROMACS通常在Linux下运行，本文只讲在Linux下的编译和安装方法。GROMACS在Windows下也照样可以完美编译和运行，参见《GROMACS的原生Windows版的编译和安装方法》（<http://sobereva.com/458>），里面还提供了笔者编译好的Windows版。

**GROMACS的安装方法**

Installation method of GROMACS

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2019-Jan-2  Last update: 2025-Feb-15

本文对最流行的分子动力学GROMACS程序在Linux下的安装方法进行详细说明。当新出的GROMACS版本的安装方法和本文所述出现较大差异时，本文也会做相应的更新。PS：之前笔者也写过老版本GROMACS安装方法，见《Gromacs 5.1.1与4.6.7编译方法》（<http://sobereva.com/247>）和《Gromacs 4.0.4、4.5.5版安装方法》（<http://sobereva.com/29>），但这俩文章对于目前版本来说已经没有意义了。

下面介绍的是GROMACS 2018系列最后一个版本2018.8版的安装，对GROMACS 2018及之后的各个版本经测试也完全适用（一直到2025.x版我都测试过）。本文最初是针对当时计算化学工作者最常用的CentOS 7操作系统写的，实测对CentOS/RockyLinux 8、9也完全适用。对于其它Linux系统的用户，安装方法可能与本文有异。本文的CentOS 7.6是按照《在VMware 15中安装CentOS 7.6的完整过程视频演示》（<http://sobereva.com/454>）演示的方式完全新装的。本文假定读者是root用户，程序将被安装到/sob目录下。如果你是普通用户，请随机应变，恰当设置路径。本文所示的安装过程中主机全程都能访问Internet。本文编译用的C++编译器是操作系统自带的gcc，虽然用Intel C++编译器也可以，但编译出的程序的速度没有显著差别。

从GROMACS 2020开始，要求gcc编译器版本>=5，而CentOS 7.x的gcc版本是4.8.5，因此2020版没法直接在CentOS 7.x下装。要么升级gcc版本（有一定风险，方法自行google），要么用老一点的GROMACS，要么用CentOS/RockyLinux >=8.0版。  
从GROMACS 2021开始，还要求cmake版本必须>=3.17，而CentOS/RockyLinux 8的软件源里的cmake版本偏老，因此必须按照下文所述手动安装cmake。  
从GROMACS 2025开始，还要求gcc 11，CentOS/RockyLinux 8的gcc太老而无法安装。还要求cmake版本必须>=3.28，RockyLinux 9的软件源里的cmake版本偏老，因此必须按照下文所述手动安装cmake。

另外值得一提的是，如果你的gcc较新而GROMACS版本较老，也可能编译不过去，比如我发现Rocky Linux 9自带的gcc 11.2.1编译GROMACS 2018.8就无法编译通过。

下面安装的是纯CPU运算、单精度、能单机并行但不能跨节点并行的版本。如果需要GPU加速或跨节点或双精度运算，看文末的附注。**本文用make的时候使用了-j选项以通过并行编译降低编译耗时，但个别情况下可能导致编译出错，在虚拟机下编译还有卡住的可能，届时请去掉-j再试**。下文的安装过程有全程视频演示，初学者不熟悉Linux的话请严格效仿着安装：**https://www.bilibili.com/video/av39749252/**。

顺带一提，如果你刚接触GROMACS，想一次性完整系统学习分子动力学模拟知识和GROMACS程序的使用和实际应用的话，**非常推荐参加北京科音分子动力学与GROMACS培训班（**[**http://www.keinsci.com/workshop/KGMX_content.html**](http://www.keinsci.com/workshop/KGMX_content.html)**）**。

## 1 安装cmake 3.x

GROMACS 2018需要系统里有cmake 3.x才能编译。CentOS 7.6自带的cmake版本太老，因此需要先装cmake 3.x。

首先运行以下命令，添加EPEL源  
yum install epel-release

然后在终端里输入yum install cmake3即可下载和安装cmake包，遇到提示的时候都输入y。之后输入cmake3 /V命令，如果显示出了3.x的版本号就说明没问题了。

注1：如果用yum的时候出现乱七八糟的提示安装不了，把操作系统重启一下往往就好了。

注2：如果你没有管理员权限或者不方便用yum安装cmake，或者当前系统对应的软件源里的cmake版本太老（如果已经装了cmake可以运行cmake -V命令查看版本），可以去<http://www.cmake.org/cmake/resources/software.html>下载cmake包（下载Source distributions的，别下载成binary的），然后解压，进入其目录，运行  
./bootstrap --prefix=/sob/cmake3 -- -DCMAKE_USE_OPENSSL=OFF  
make -j  
make install  
就新产生了/sob/cmake3目录。然后删掉cmake解压的目录。之后在~/.bashrc里加入export PATH=/sob/cmake3/bin:$PATH。重新进入终端后，cmake命令就可以用了。

## 2 安装FFTW库

GROMACS 2018依赖于快速傅立叶变换库FFTW 3.3.8，可以在<http://www.fftw.org/fftw-3.3.8.tar.gz>下载。将其压缩包解压，进入此目录后运行  
./configure --prefix=/sob/fftw338 --enable-sse2 --enable-avx --enable-float --enable-shared   
以上语句代表FFTW将被安装到/sob/fftw338目录。如果你的CPU相对较新，支持AVX2指令集，可再加上--enable-avx2选项以获得更好性能。

然后运行make -j install开始编译，过一会儿编译完毕后，就出现了/sob/fftw338目录。然后可以把FFTW的解压目录和压缩包删掉了。

## 3 安装GROMACS

下载GROMACS 2018.8压缩包，地址为<http://ftp.gromacs.org/pub/gromacs/gromacs-2018.8.tar.gz>。然后将之拷到/sob目录下解压。进入解压后的目录，在终端里依次运行  
mkdir build  
cd build  
export CMAKE_PREFIX_PATH=/sob/fftw338  
cmake3 .. -DCMAKE_INSTALL_PREFIX=/sob/gmx2018.8（如果你是用的CentOS 8或更新的系统，或者手动编译的cmake，这里cmake3改为cmake。另外，这一步运行后也仔细看看屏幕上的提示，了解当前CPU支持的最佳的SIMD指令集有没有正确判断对。如果你的CPU较新却用较老的GROMACS，可能支持的SIMD根本没识别出来，此时GROMACS的mdrun运行速度会非常慢）  
make install -j  
在Intel四核机子下不到10分钟就能编译完毕（对2024.1版，我在双路EPYC 7R32 96个物理核心的机子上只花了1分钟左右就编译完毕）。

此时程序就被编译和安装到了/sob/gmx2018.8目录下。修改用户目录下的.bashrc文件（比如运行gedit ~/.bashrc），在末尾加入source /sob/gmx2018.8/bin/GMXRC，然后保存。

之后关闭终端窗口，再次打开终端，输入gmx -version，看看是否输出了GROMACS的相关信息，是的话就说明安装成功了。之后可以把GROMACS压缩包和解压出来的目录删掉。

注意，在使用gmx mdrun跑任务时，如果一开始提示WARNING: Using the slow plain C kernels. This should not happen during routine usage on supported platforms，说明编译时没有利用CPU的SIMD指令集（正常情况理应自动检测并利用），这样编译出来的mdrun的运行速度往往比理想情况慢N倍。此时需要重新编译，在使用cmake3的时候明确指定要用的指令集，比如如果你的CPU支持AVX2指令集（XEON v3系列及之后都支持）就加上-DGMX_SIMD=AVX2_256。

### 注1：在安装GROMACS过程中自动安装FFTW库

实际上，FFTW库可以不必手动安装，因为可以在安装GROMACS时自动下载并安装FFTW库。但由于国内链接FFTW官网服务器往往比较慢，自动下载FFTW库可能中途卡住或者过程巨慢，因此还是建议手动方式安装FFTW库。如果你确实打算自动安装FFTW库的话，将上文第2节直接忽略掉，也不必设export CMAKE_PREFIX_PATH=/sob/fftw338，把第3节的cmake3那一步额外加上-DGMX_BUILD_OWN_FFTW=ON选项即可，这样编译GROMACS时就会自动在FFTW官网上下载FFTW包并自动编译之。

### 注2：编译支持CUDA GPU加速的版本

GROMACS目前支持对nVidia的GPU通过CUDA方式的加速，也支持以OpenCL方式对其它厂商的GPU实现GPU加速（但功能有局限性）。对于用CUDA方式加速，先去<https://developer.nvidia.com/cuda-downloads>下载CUDA toolkit并安装到默认路径，之后编译GROMACS方法同前，区别仅是cmake3这一步额外加上-DGMX_GPU=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda选项（以实际CUDA tookit安装路径为准）。如果你装的是GROMACS >= 2021版，-DGMX_GPU=ON应改为-DGMX_GPU=CUDA。

之后运行gmx mdrun运算时，会自动使用机子里的GPU进行加速。如果又不想使用GPU加速了，那得按照上文方式编译一个只支持CPU运算的版本并放到不同的路径，并且把.bashrc改成source那个版本的GMXRC（如果编译时你没写-DGMX_GPU但也自动检测出CUDA toolkit并编译出了GPU版本，加上-DGMX_GPU=OFF强制避免编译成GPU版）。

### 注3：编译双精度版本

一般计算只需要按照前述编译单精度版本就够了，但如果模拟刚开始就崩溃，有时候用双精度版本可解决，但计算比单精度版慢将近一倍、trr/edr等文件体积大一倍。另外，做正则振动分析时在能量极小化和对角化Hessian矩阵的时候一般也需要用双精度版以确保数值精度。注意，编译双精度版本时不支持GPU加速。

要编译双精度版本的话，先按照前文方式编译一遍单精度版本，毕竟这之后在研究中肯定也得用。然后再重复一遍编译过程，但是在编译FFTW时去掉--enable-float，并且在使用cmake3命令时额外加上-DGMX_DOUBLE=ON选项。双精度版本的GROMACS可执行文件是gmx_d，而单精度是gmx，因此单精度和双精度的可执行文件可以同时存在于同一目录，互不冲突。

### 注4：编译GROMACS的MPI版本

GROMACS跨节点并行计算需要MPI库，支持OpenMPI>=1.6、MPICH>=1.4.1。在编译这种GROMACS之前首先要安装MPI库，这里用OpenMPI。去<http://www.open-mpi.org>下载OpenMPI最新版本，解压并进入此目录后运行以下命令，就会编译并安装OpenMPI到/sob/openmpi目录：  
./configure --prefix=/sob/openmpi  
make all install -j  
之后在用户目录下的.bashrc末尾加入以下两行  
export PATH=$PATH:/sob/openmpi/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/openmpi/lib  
然后重新进入终端使以上语句生效。之后编译GROMACS的方法同前，但在cmake3那一步额外加上-DGMX_MPI=ON选项。编译出来的可执行文件是gmx_mpi，比单机版本的可执行文件多了_mpi后缀。运行时候使用比如这样的命令：mpirun -np 16 gmx_mpi mdrun。  
注：对于root用户，OpenMPI要求每次执行mpirun命令都得带着-allow-run-as-root选项才行，这很烦人，但可以通过在编译OpenMPI之前修改OpenMPI的源代码来避免，见《root用户在用openmpi并行计算时避免加--allow-run-as-root的方法》（<http://sobereva.com/409>）。

顺带一提，笔者在答疑时经常看到有人明明用的是单机并行，却非要装个MPI版GROMACS，这需要批评。因为这不仅需要多做一步，而且比起用默认方式基于thread-MPI和OpenMP的并行方式效率还更低，因此**单机并行装MPI版完全是自取其辱**。

### 注5：关于AVX512指令集

编译GROMACS时，如果你的CPU相对较新，支持AVX512指令集的话，程序可能会自动基于AVX512指令集进行编译。但如果你的机子上的gcc版本太老，不支持AVX512的话就会报错。如果根据屏幕上的提示确认是由于gcc不支持AVX512指令集而无法进行编译，可以按照<http://bbs.keinsci.com/thread-12687-1-1.html>中的做法更新gcc，或者索性不用AVX512指令集，即cmake3那一步加上-DGMX_SIMD=AVX2_256来使用AVX2指令集。
