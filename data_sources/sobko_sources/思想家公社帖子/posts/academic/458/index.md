---
post_id: 458
title: GROMACS的原生Windows版的编译和安装方法（支持GPU加速）
url: http://sobereva.com/458
date: '2019-01-04T21:05:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题就是GROMACS在Windows下的编译和安装教程，软件主题明确。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**GROMACS的原生Windows版的编译和安装方法（支持GPU加速）**

Compilation and installation methods of the native Windows version of GROMACS (supporting GPU acceleration)

文/Sobereva@[北京科音](http://www.keinsci.com)    
First release: 2019-Jun-4  Last update: 2021-Jul-10

注1：本文拿2019.1版作为例子进行说明编译过程。本文的纯CPU版的编译方法经测试对于GROMACS 2018、2019各版本都适用，其它版本只要不是太老的应当都可以用，但未经实际测试。本文的编译CUDA GPU加速版的方法经测试对GROMACS 2019.1及之后的2019.x版、2020.x版都适用，不适用于2019.1之前的版本。本文的编译方法对于未来的GROMACS版本以及其它Visual Studio版本是否适用笔者不保证，请自行尝试，如果发现不行，请举一反三试图解决。

注2：如果大家对编译过程不感兴趣，只想立刻直接用笔者编译好的Windows版的GROMACS，请直接看本文第5节，里面有下载地址和安装方法。

## 1 前言：关于在Windows下使用GROMACS

GROMACS一般都是在Linux下运行，其Linux下的安装方法我在《GROMACS的安装方法》（<http://sobereva.com/457>）中已经详细交代了，还特意录了视频演示编译过程。在Windows下使用GROMACS有多种方式：

• 使用VMware装Linux虚拟机，并照常以Linux方式编译。装Linux虚拟机十分简单，过程见《在VMware 15中安装CentOS 7.6的完整过程视频演示》（<http://sobereva.com/454>）。Linux下的所有程序都可以以这种方式使用，而且直接有图形环境。但局限性是VMware客户机支持的CPU核数有限，比如VMware 16最多支持32个核。总的来说笔者极度青睐VMware。

• 在Cygwin下编译。Cygwin提供了类似Linux系统的命令行环境，也提供了程序包管理器和源，相对于使用VMware更轻量级，而且编译出的程序只要提供一些Cygwin的dll文件就可以直接挪到其它Windows机子下用。对于大多数程序Cygwin下编译方式和Linux下一样（gcc、make、cmake等都有），但也有很多情况需要额外折腾，有时编译过程特别迟钝，而且有时候有一些特殊情况，比如笔者在Cygwin下编译GROMACS时必须要求不利用AVX指令集，否则编译会失败。

• Win10的Linux子系统（WSL）。笔者个人不怎么喜欢这东西，用着别扭，这里不多提，和Cygwin在形式上有很大相似之处，鉴于是Windows自带的，以后必然会吞掉Cygwin很大的生存空间。

以上三种方法在原理上都会使得计算性能打一些折扣，但一般也就10~15%左右，这不是重点，共同的严重缺点是不能支持GPU加速（WSL2倒是号称支持，不过我没试过）。在Windows下最完美的运行GROMACS的方法莫过于直接编译原生的Windows版GROMACS，编译出的程序可以拿到任何其它Windows机子上直接用，不需要装额外运行环境，不会像上述三种方法那样会对CPU性能打折扣，而且还能像Linux下一样在跑GROMACS的时候使用GPU加速。

本文目的是详细介绍一下怎么编译原生的Windows版GROMACS，其实过程一点也不复杂（网上有些教别人编译Windows版GROMACS的文章写得很不好，过程十分繁琐，写得不明不白，而且对较新版本还不适用）。

首先提一下，GROMACS需要利用FFT（快速傅立叶变换）库，有三种选择  
(1)FFTW库：这是最佳选择，一般都用这个，效率高。在Linux下编译GROMACS可以自动下载FFTW库并安装，但是在Windows下没法实现这点  
(2)MKL库：效率和FFTW差不多，需要额外安装，较麻烦，而且占不少硬盘  
(3)fftpack库：这是GROMACS自带的，图省事用这个就行了，但是经实测效率比基于FFTW库低百分之十几

下面按照编译过程由简到繁，分为三部分依次说：  
(1)编译基于fftpack的纯CPU版  
(2)编译基于fftw的纯CPU版  
(3)编译基于fftw且支持CUDA加速的版本  
本文只涉及编译最常用的单精度版、只能单节点并行的情况。本文编译的都是64bit版本。

## 2 编译基于fftpack的纯CPU版

如果你对计算效率没什么要求，只需要以尽量简单的方式编译出一个能在Windows下跑的GROMACS，那么只看这一节就够了。下面我们来编译基于fftpack库的GROMACS。

首先安装Visual Studio，这里用的是Visual Studio 2019。Visual Studio最低级的是community（社区）版，是完全免费的。大家在<https://visualstudio.microsoft.com/zh-hans/downloads/>就可以下载到最新版。下载到的是一个非常小的安装器，启动它就可以在线安装（目前的Visual Studio是没有镜像文件的。虽然也有办法把其组件全部下载后再离线安装，但是会占几十GB硬盘，因此不要考虑离线方式安装）。虽然看起来在线安装好像很耗时，但其实以现在的网速来说总耗时也不算很高。安装Visual Studio的时候应选择“使用C++的桌面开发”，确认“安装详细信息”中“用于CMake的Visual C++工具”是已选中的状态。

将gromacs-2019.1.tar.gz源代码包解压到比如C:\gromacs-2019.1。

在开始菜单里选Visual Studio 2019 - Visual Studio Tools - Developer PowerShell for VS 2019，由此进入编译环境都配置好的命令行窗口。然后依次输入  
cd C:\gromacs-2019.1  
mkdir build  
cd build  
cmake .. -DCMAKE_INSTALL_PREFIX=C:/gmx2019.1 -DGMX_FFT_LIBRARY=fftpack -G "Visual Studio 16 2019"  
cmake --build . --target INSTALL --config Release

耐心地等待编译好后，会看到出现了C:\gmx2019.1目录，里面就是编译好的可执行文件以及相关文件了，内容和Linux版一样。按照本文第5节的做法将C:\gmx2019.1\bin添加到Path环境变量后，程序就可以用了，用法和Linux版没有任何区别。

当前机子的CPU最高支持什么指令集，默认情况下编译出的GROMACS就是基于什么指令集的。如果比如你的机子的CPU支持AVX2指令集，那么编译出的GROMACS拿到只支持到AVX指令集的CPU上就没法跑，比如mdrun运行时会崩溃。

有几点值得额外说明，有兴趣可以了解一下：

cmake的-G选项代表设置Generator，相当于指定编译环境，可以运行cmake -G查看有哪些Generator可选。"Visual Studio 15 2017 Win64"代表产生出对应于VS2017的64bit平台的解决方案，之后进而编译出的程序就是适合Windows 64bit的版本了。

Visual Studio自带了cmake（因为我们安装VS时选上了），实际上也可以直接去cmake官网上下载独立的cmake程序，里面还带有cmake-gui.exe，提供了cmake的图形界面。网上某些编译Windows版GROMACS的文章用了这个东西，实际上完全多此一举，直接按照上面的做法用命令行输入省事得多。

如果读者打开build目录下的Gromacs.sln解决方案文件，会看到里面有很多不同的工程，其中名为ALL_BUILD的工程对应于编译出最终的可执行文件，而INSTALL的工程对应于不仅编译可执行文件（因为其引用了ALL_BUILD），还将程序安装到CMAKE_INSTALL_PREFIX设的目录，因此上文的语句里用了--target INSTALL。

上面的--config后面跟的是编译时用的配置。名为Release的配置是适合用于发布的，会对代码充分进行优化。

在cmake --build ...的那一步后面再接上比如-j 4代表使用4核并行编译，但是实测发现对编译耗时没有可查觉的影响，和Linux下的情况完全不同。

## 3 编译基于fftw的纯CPU版

先在此下载FFTW 3.3.8库：<http://www.fftw.org/fftw-3.3.8.tar.gz>。将之随便解压到某个地方，然后开启Developer PowerShell for VS 2019，进入FFTW库解压的目录（此目录下会看到CMakeLists.txt），运行以下命令  
cmake . -DCMAKE_INSTALL_PREFIX=C:\fftw338 -DENABLE_SSE2=ON -DENABLE_AVX=ON -DENABLE_FLOAT=ON -DBUILD_SHARED_LIBS=ON -G "Visual Studio 16 2019"  
cmake --build . --target INSTALL --config Release

这样，FFTW库就被装到C:\fftw338目录下了，里面有库文件、头文件等。如果你的CPU支持AVX2指令集，建议把上面命令里-DENABLE_AVX=ON改为-DENABLE_AVX2=ON以获得更好的性能。

接下来的编译过程类似上一节，区别是指定的FFT库不同：  
cd C:\gromacs-2019.1  
mkdir build  
cd build  
cmake .. -DCMAKE_INSTALL_PREFIX=C:/gmx2019.1 -DGMX_FFT_LIBRARY=fftw3 -DCMAKE_PREFIX_PATH=C:/fftw338 -G "Visual Studio 16 2019"  
cmake --build . --target INSTALL --config Release

编译完成后，手动将C:\fftw338\bin里的fftw3f.dll拷到C:\gmx2019.1\bin目录下，之后将这个目录加入Path环境变量后就可以用了。

## 4 编译基于fftw且支持CUDA加速的版本

去<https://developer.nvidia.com/cuda-toolkit>下载CUDA toolkit，里面提供了编译CUDA加速程序所需要的库、头文件、编译器等等。为了节约硬盘空间，装CUDA toolkit时只需要选择安装CUDA分类里的Development、Runtime和Visual Studio Integration即可。这里假定装到了自定义的D:\CUDA_toolkit目录下。值得一提的是，编译CUDA版GROMACS的机子并不需要非得有可以实现CUDA加速的GPU，只要装了CUDA toolkit，在什么机子上都可以编译。

按照上一节的做法把FFTW库编译好，然后输入  
cd C:\gromacs-2019.1  
mkdir build  
cd build  
cmake .. -DCMAKE_INSTALL_PREFIX=C:/gmx2019.1_GPU -DGMX_FFT_LIBRARY=fftw3 -DCMAKE_PREFIX_PATH=C:/fftw338 -G "Visual Studio 16 2019" -DGMX_GPU=ON -DCUDA_TOOLKIT_ROOT_DIR=D:/CUDA_toolkit  
cmake --build . --target INSTALL --config Release

然后和上一节一样把fftw3f.dll拷到新产生的C:\gmx2019.1_GPU\bin目录下，之后将这个目录加入Path环境变量后就可以用了。

如果你编译出的GROMACS要拿到其它没有装CUDA toolkit的机子上用，或者那台机子装的CUDA toolkit是老版本，那么你应当先把D:\CUDA_toolkit\bin\cufft64_10.dll（_后面的数字视CUDA toolkit版本而定）也拷到C:\gmx2019.1_GPU\bin目录下，然后再把这个gmx2019.1_GPU目录拷到其它机子上用。

如果当前机子里有支持CUDA加速的GPU，而且GPU驱动的版本号足够新，满足当前CUDA toolkit版本的要求，那么运行CUDA版GROMACS的时候就会自动识别出兼容的GPU，并提示利用GPU进行运算。如果你的GPU不满足要求或者驱动版本太老，那么CUDA版GROMACS也能运行，只不过是纯粹用CPU来跑。在<https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html>页面里可以查到各个CUDA toolkit所需要的GPU驱动最低版本号，如果你的GPU能装上满足要求版本的驱动（较新版本的驱动不支持很老的GPU），那么你的GPU就能加速GROMACS运算。

PS：对于用GPU加速的情况，用fftpack还是fftw对计算耗时影响很小，图省事的话基于fftpack编译GPU版也可以。

## 5 笔者预编译的原生Windows版的安装方法

这里提供笔者编译好的GROMACS Windows 64bit版，在Win7、Win10、Win11下经测试都可以用，都可以单机并行，FFT库都是用的FFTW。

2018.8 CPU版，AVX指令集（15 MB）：<http://sobereva.com/soft/gmx/gmx2018.8_AVX_win64.rar>  
2019.6 CUDA GPU加速版，AVX指令集（93 MB）：<http://sobereva.com/soft/gmx/gmx2019.6_AVX_CUDA_win64.rar>  
2020.3 CUDA GPU加速版，AVX指令集（93 MB）：<http://sobereva.com/soft/gmx/gmx2020.3_AVX_CUDA_win64.rar>  
2020.6 CUDA GPU加速版，AVX2指令集（88 MB）：<http://sobereva.com/soft/gmx/gmx2020.6_AVX2_CUDA_win64.rar>（nVidia显卡驱动需>=471.11版）

使用前必须先设置环境变量，将程序的bin目录加入到Path环境变量里。对于Win7来说，过程是：假设预编译版GROMACS压缩包解压到了C:\gmx2019.6，应当进入“控制面板”-“系统”，选择“高级系统设置”，在“高级”标签页里选择“环境变量”，在“xxx的用户变量”下面选择Path变量，点击“编辑”，在“变量值”文本框最后加上一个分号，然后再写上GROMACS目录的bin子目录的路径，比如;C:\gmx2019.6\bin\。之后进入Windows的命令行窗口，输入gmx命令的时候就应该出现相关提示信息了，此时就可以像Linux版一样照常使用了。  
注：如果你的计算机水平十分糟糕，甚至差到难以按照上面的说明正确设置环境变量，一定要参考演示视频：<https://www.bilibili.com/video/av39914815/>。

如果你的机子里没有装Visual Studio，或者装了但是版本比2019老，应先去<https://aka.ms/vs/16/release/VC_redist.x64.exe>下载并安装Visual C++ Redistributable，这提供了必备的运行环境，否则启动时会提示缺少dll。

对于上面提供的CUDA GPU加速版，使用者并不需要在机子里安装CUDA toolkit，只要确保nVidia显卡驱动足够新就可以直接使用。如果你的驱动太老导致无法使用，应当先去nVidia官网<https://www.nvidia.com/Download/index.aspx>下载最新版本驱动并安装。

不要问我怎么双击gmx.exe之后程序闪退（老有人问），因为GROMACS根本就不是靠双击图标来使用的！GROMACS是通过命令行使用的程序，稍微有点最基本GROMACS常识的人都知道不应该双击gmx.exe图标来使用。如果想从0开始系统性学习GROMACS，强烈建议参加北京科音分子动力学与GROMACS培训班，一次性彻底学明白，详见：<http://www.keinsci.com/workshop/KGMX_content.html>。

如果你对Windows下命令行的操作一丁点都没概念，连查看目录下有什么文件（dir命令）、怎么切换路径（cd命令）都不会的话，我强烈建议你先花一点点看这套视频学一遍这些基础：<https://www.youtube.com/watch?v=MBBWVgE0ewk&list=PL6gx4Cwl9DGDV6SnbINlVUd0o2xT4JbMu&index=1>。没有这些最基本常识的话，什么命令行程序你都没法顺利使用（不限于GROMACS）。

经笔者在2*E5 2696v3（36核）机子上对一个三万多原子的蛋白质+水盒子的测试发现，Windows下纯CPU版的计算速度只有按照《GROMACS的安装方法》（<http://sobereva.com/457>）方法编译出来的Linux版的60%，估计是微软的编译器没有gcc那么给力所致。GPU版我没有对比测试，但应该速度相差不会这么显著。所以，如果你只用CPU来跑计算，建议还是用Linux系统。
