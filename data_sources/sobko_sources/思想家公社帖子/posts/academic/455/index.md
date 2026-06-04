---
post_id: 455
title: VASP最简单的安装方法（含全程视频演示）
url: http://sobereva.com/455
date: '2019-01-01T13:35:00+08:00'
source_categories:
- 第一性原理
primary_topic: VASP
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题直接是VASP安装方法，且强调运行演示，属于软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**VASP的最简单的安装方法**

The simplest way to install VASP

文/Sobereva@[北京科音](http://www.keinsci.com)   2019-Jan-1

目前计算化学公社论坛（<http://bbs.keinsci.com>）上的第一性原理板块里已经有多篇写得很好的关于VASP的编译方法的帖子了。笔者这里写一个初学者最易于理解的版本，不仅所需要的操作步骤是最少的，而且编译出来的VASP运行效率几乎是最高的。考虑到少数读者可能存在阅读理解能力障碍、极其不情愿看文字，本文的安装过程笔者录了完整的演示视频，见[**https://www.bilibili.com/video/av39616222/**](https://www.bilibili.com/video/av39616222/)。我相信，哪怕是对Linux、VASP、编程零基础的读者，只要严格模仿演示视频，也一定可以非常顺利地安装。也希望这些零基础VASP用户看了此视频后不会再去花钱找人装VASP或者花钱买网上乱七八糟的VASP安装视频。

本文用的软件版本和系统都是撰文时的最新版。编译的是VASP 5.4.4，操作系统是CentOS 7.6，编译器和MPI/MKL库是Intel Parallel Studio XE 2019 Update 1，其中的ifort编译器就是19.0.1版。Intel编译器目前不是免费的，但可以获取试用版。CentOS是在笔者来看最适合计算化学研究者使用的Linux操作系统，免费、稳定、设计合理、用户规模庞大、兼容性好、安装各种计算化学程序省心，不仅是最流行的计算服务器用的操作系统，初学者使用起来也没任何压力。本文安装过程用的账户是root账户，如果你用的是普通用户，本文中的安装路径需要做相应的调整。如果读者用的系统、程序、编译器版本和此文的不同，也有极大可能无法按照此文的方法安装，请随机应变。另外，使用较新系统、程序版本的读者，不要再去参考网上众多年代较早的编译VASP的文章，要么编译过程繁琐，要么根本不适合当前情况。

如果读者不会装CentOS系统，或者之前装过但是是瞎装的，强烈建议严格效仿此视频里的方式安装：《在VMware 15中安装CentOS 7.6的完整过程视频演示》（<http://sobereva.com/454>），可以很容易地装好系统，而且之后编译安装各种计算化学程序也都会比较顺利。

## 1 安装Intel编译器和相关的库

将parallel_studio_xe_2019_update1_cluster_edition.tgz包拷贝到Linux里面，通过tar -xzf [文件名]将之解压。如果当前处于图形环境，就进入此目录，在命令行下运行./install_GUI.sh启动Intel Parallel Studio XE的图形界面的安装程序。如果你是在纯文本环境下，就运行./install.sh启动文本界面的安装程序，但是在自定义组件的时候操作比较繁琐。

对于root用户，默认的安装路径是/opt/intel，这里就用默认路径。如果你想省硬盘，安装过程中可以选择自定义，对于编译计算化学程序完全用不着的组件都可以不去装。其中IA32版的组件都不装，因为我们编译程序都是编译64bit版本。要装的组件里只有以下这些是必须的  
·Intel Fortran Compiler  
·Intel C++ Compiler  
·Intel Math Kernel Library 2019 Update 1 for Fortran里的Intel MKL core libraries for Fortran、Fortran 95 interfaces for BLAS and LAPACK、Cluster support for Fortran  
·Intel Math Kernel Library 2019 Update 1 for C/C++里的Intel MKL core libraries for C/C++、Cluster support for C/C++  
·Intel MPI Library 2019 Update 1里的Intel MPI Library for applications...  
·Intel Threading Building Blocks 2019（这是Intel C++ Compiler必须依赖的）  
安装时可能会显示缺少32bit库之类，不用管，继续装即可。

装好后，使用比如gedit ~/.bashrc命令编辑当前用户目录下的.bashrc文件，这里面的内容是每次进入bash终端时自动运行的。把下面这行加入其中末尾，用来自动配置Intel Parallel Studio XE的运行环境：  
source /opt/intel/parallel_studio_xe_2019/psxevars.sh  
（如果你之前装了其它MPI库，应当把.bashrc里相应配置在开头加上#注释掉，免得造成冲突。另外，加入这语句后如果发现使用SSH的File Transfer界面以sftp方式连接失败，应当把这个.sh文件里的echo语句给注释掉或者删掉）

然后重新进入终端，运行ifort -V，如果显示出了编译器的版本，说明编译器已经可以正常使用了。

然后进入/opt/intel/compilers_and_libraries_2019.1.144/linux/mkl/interfaces/fftw3xf，运行make libintel64命令，过一会儿当前目录下会产生libfftw3xf_intel.a库文件。

## 2 编译VASP

解压VASP包，得到vasp.5.4.4目录。进入此目录，把arch/makefile.include.linux_intel拷到上一级目录下改名为makefile.include，里面的配置专门适合Intel编译器。打开此文件，把其中的OFLAG参数里加入-xhost，这样编译器会使得编译出的程序能够利用当前机子CPU能支持的最高档次的指令集以加速计算，也因此就没必要手动添加其它一些VASP编译教程里诸如-xAVX、-mSSE4.2之类的选项了。

之后运行make all命令开始编译。一般半个小时到一个小时可以编译完毕。

编译完成后，在vasp.5.4.4/bin目录下出现了vasp_gam、vasp_ncl、vasp_std三个可执行文件，分别是Gamma only版，非共线版和标准版。为了使用方便，可以把最常用的vasp_std改名为vasp。然后在~/.bashrc末尾加入以下这行，使得此目录加入到操作系统寻找可执行文件的路径中：  
export PATH=$PATH:/sob/vasp.5.4.4/bin  
之后重新进入终端，VASP就可以用了。

## 3 测试VASP

下载测试任务包<http://sobereva.com/attach/455/benchmark.Hg.tar.gz>，这是个含50个Hg原子的标准测试任务。将之解压，会看到IN-short和IN-long，分别是一个耗时较短和一个耗时较长任务的INCAR文件。这里将IN-short改名为INCAR，进入此目录，输入mpirun -np 4 vasp测试调用四个核心执行此任务，然后检查得到的OUTCAR看是否内容正常，没异常的话就说明完全装好了！

如果运行自己的任务出现异常，把ulimit -s unlimited命令加入到~/.bashrc里重新进入终端再试，此命令可以避免某些操作系统对堆栈内存可用尺寸进行过严限制的问题。
