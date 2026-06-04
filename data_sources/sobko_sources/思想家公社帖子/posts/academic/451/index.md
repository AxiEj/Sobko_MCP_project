---
post_id: 451
title: 量子化学程序ORCA的安装方法
url: http://sobereva.com/451
date: '2018-12-21T04:45:00+08:00'
source_categories:
- 量子化学
- ORCA
primary_topic: ORCA
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章直接介绍ORCA安装方法，属于软件安装教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**量子化学程序ORCA的安装方法**

Installation method of ORCA quantum chemistry program

文/Sobereva@[北京科音](http://www.keinsci.com)  
First release 2018-Dec-21  Last update: 2023-Oct-19

## 0 前言

ORCA是一款对学术用户免费但不开源的量子化学程序，发展迅猛，流行程度越来越高，用户越来越多。虽然ORCA的安装很简单，都不需要编译源代码，但还是有不少量子化学初学者经常问怎么安装，这里就统一说一下。当随着ORCA程序更新，导致最新版安装方法与本文存在较大差异时，本文也将同步更新。目前本文对应的是ORCA 6。ORCA虽然有也有Mac版，但由于极其小众，安装方法这里就不提了。顺带一提，如果你想一次性快速上手&系统学习ORCA的使用，同时掌握各种重要的经验技巧、尽可能少踩坑，特别推荐参加笔者讲授的**北京科音高级量子化学培训班（**[**http://www.keinsci.com/KAQC**](http://www.keinsci.com/KAQC)**）**，里面专门有一节对ORCA的使用及相关的各种背景知识有极其全面、详细的讲解，并给出了十分丰富的精心设计的例子，通过此培训学员将能把ORCA用得十分游刃有余，比自己啃手册学习在效果和效率上都强太多了！

ORCA官网是<https://orcaforum.kofo.mpg.de>，和ORCA论坛是在一起的。进去之后注册个新用户，登陆后就可以进入论坛，页面上方有Download按钮，进去就可以下载可执行程序和手册了。如果你注册ORCA论坛时验证码刷不出来，或者根本连ORCA官网都打不开的话，说明需以特殊姿势上网。

为了测试安装后ORCA是否能正常运行，这里提供个简单的测试文件，将以下内容复制到比如test.inp里即可作为输入文件。此任务要求4核并行：

! BLYP def2-SVP pal4  
* xyz 0 1  
 C                  0.00000000    0.00000000   -0.56221066  
 H                  0.00000000   -0.92444767   -1.10110537  
 H                 -0.00000000    0.92444767   -1.10110537  
 O                  0.00000000    0.00000000    0.69618930  
*

顺带一提，有些人用ORCA只是想算很常见类型的问题，但不会写关键词。最最简单的做法就是用Multiwfn产生ORCA的输入文件，超级容易，里面的关键词都是绝对最恰当的，见《详谈Multiwfn产生ORCA量子化学程序的输入文件的功能》（<http://sobereva.com/490>）。此文是一个用Multiwfn创建输入文件结合ORCA做计算的实例：《Simulating UV-Vis and ECD spectra using ORCA and Multiwfn》（<http://sobereva.com/485>）；此视频是一个利用Multiwfn这个功能的综合实例：《基于ORCA量子化学程序对分子做优化、振动分析、观看红外光谱、观看轨道的简单演示》（<https://www.bilibili.com/video/av59599938>）。

## 1 Windows版的安装

ORCA的Windows版只有64bit的，如果你还在坚持使用老掉牙的32bit Windows，就别指望用Windows版了，要么装64bit Windows系统，要么在现有的32bit Windows下用VMware虚拟机装个64bit Linux跑ORCA Linux版。

ORCA是基于MPI方式进行并行运算的程序，目前的版本在Windows下是依赖于Microsoft MPI (MSMPI)库运行的，因此还要给系统安装MSMPI。ORCA 6可以搭配MSMPI 10.0运行。Google一下MSMPI 10.0就可以立刻找到MSMPI的下载地址，下载并安装之即可。

去ORCA论坛下载“ORCA [版本号], Windows, 64bit, Installer”页面里的压缩包，将之解压后，运行Orca[版本号].Win64.exe，就会启动安装程序，选择以Complete方式安装，对于ORCA 6.0.0装好后会占用13多GB硬盘。

下面测试ORCA能否正常并行运行。将本文开头给的测试文件拷到某处，然后进入Windows的cmd（命令提示符）界面，假设ORCA装到了D:\study\ORCA_6.0.0目录，就输入D:\study\ORCA_6.0.0\orca H2CO.inp > H2CO.out来执行H2CO.inp并将输出信息输出到H2CO.out。注意输入文件要求并行计算时，必须像这样输入ORCA的绝对路径才行。如果计算中途的输出信息看起来很正常，最后也显示****ORCA TERMINATED NORMALLY****，就说明没问题。如果并行不正常的话，可能会看到输出信息是混乱交错的，这是由于各个进程没有真正协同工作所致。

ORCA有一部分后HF和多参考计算功能是只有autoCI模块才能做的，比如FIC-MRCI、CCSDT等。如果你需要用这些方法，在按照前面的方法安装的基础之上，还需要进入官方论坛下载页面中的“ORCA [版本号], Windows, 64bit, autoci / parallel part”页面，把里面的压缩包下载下来并解压到ORCA的安装目录下。你会看到这个压缩包里包含的可执行文件开头都带着autoci_字样。把autoCI模块也装上的话，ORCA 6的目录最后会达到30多GB！

附：在Windows下使用ORCA的最便捷方法  
利用cmder可以令ORCA在Windows下的使用明显更方便，cmder是一个第三方的文本终端。首先去<https://cmder.app>下载Full版的cmder，然后解压到你平时安装应用程序的目录。之后进入操作系统的命令行窗口，在cmder的目录下，输入Cmder.exe /REGISTER ALL。从此在任意目录下点右键选cmder Here即可进入cmder命令行窗口，并且当前路径就是此文件夹。启动cmder窗口后，在cmder的标题位置点右键选Settings，在General页面里选择{bash::bash as Admin}，然后把cmder关了。从此之后，新开的cmder终端里的命令写法就和Linux的Bash环境下一样了，连awk、vi等常用工具都有。用文本编辑器打开cmder安装目录下的config\user_profile.sh，添加一行比如alias oo='D:/study/orca600/orca'，这里oo是你启动ORCA想用的自定义命令，后面是ORCA可执行文件路径。这样，进入cmder后就可以使用比如oo Roselia.inp |tee RAS.out来调用ORCA运行.inp文件，输出的信息不仅显示在屏幕上还同时输出到RAS.out里，比起在Windows的cmd或者PowerShell里运行ORCA方便省事得多。

## 2 Linux版的安装

下面的内容涉及到一些最基本的Linux常识性知识，如果你对Linux是零基础，看下面内容之前建议看看《Gaussian的安装方法及运行时的相关问题》（<http://sobereva.com/439>）的1.1节。

### 2.1 安装OpenMPI

ORCA在Linux下是通过OpenMPI这种MPI库实现并行的，并行方式运行ORCA之前需要先编译OpenMPI库。ORCA文件包的文件名当中直接体现了要求的OpenMPI库版本，比如文件名里有openmpi416就代表需要OpenMPI 4.1.6。不代表其它版本OpenMPI就一定不兼容。比如ORCA 6.0.0标配OpenMPI 4.1.6，但我实测结合4.1.1也完全可以用。所有版本的OpenMPI源代码都包可以在<https://www.open-mpi.org>上下载，比如4.1.6的下载地址为<https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.6.tar.bz2>。

先检查机子有没有装gcc和gfortran编译器，没有的话必须先装上。比如对于CentOS或Rocky Linux，分别运行yum install gcc、yum install gcc-gfortran就能安装。特别要注意，如果只装了gcc而没装gfortran，虽然OpenMPI能正常编译完成，但是此时会由于没有Fortran的接口而导致之后ORCA没法正常并行运行。

用诸如tar -xf openmpi-4.1.6.tar.bz2命令解压OpenMPI压缩包，进入此目录，输入以下命令，OpenMPI就会被安装到/sob/openmpi416目录下  
./configure --prefix=/sob/openmpi416 --disable-builtin-atomics  
make all install -j  
注：这里用-j是为了通过并行编译降低编译过程耗时。但如果编译中途出现诡异报错，去掉-j再试。

如果你的操作系统的shell是Bash（如CentOS、Rocky Linux就是），就编辑用户目录下的.bashrc文件，比如运行vi ~/.bashrc命令，将诸如以下两行加入到文件末尾，之后保存  
export PATH=$PATH:/sob/openmpi416/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/openmpi416/lib  
然后重新打开终端，以上设置就生效了。可以运行mpiexec -V命令，如果正常显示出了OpenMPI的版本，就说明已经装好了。之前解压出来的openmpi-4.1.6目录现在也可以删掉了。

### 2.2 安装ORCA

下载比如orca_6_0_0_linux_x86-64_avx2_shared_openmpi416.tar。然后用  
tar -xf orca_6_0_0_linux_x86-64_avx2_shared_openmpi416.tar  
命令即可解压之。文件名里的avx2代表CPU必须支持AVX2指令集才可以用，否则应当下载不带avx2字样的ORCA包。目前主流的CPU都支持AVX2，如果你的CPU较老，可以通过我整理的硬件资料库（<http://sobereva.com/datasheet.rar>）的查询支持的指令集。

假设ORCA解压后的目录是/sob/orca600/，就在.bashrc文件里加入以下内容并保存  
export PATH=$PATH:/sob/orca600  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/orca600

重新进入终端令以上语句生效后即可运行ORCA。并行运行时必须写明ORCA的绝对路径，如：  
/sob/orca600/orca test.inp > test.out  
如果懒得每次都写绝对路径，可以在.bashrc里加上下面这句  
alias orca='/sob/orca600/orca'  
这代表令orca命令等价于/sob/orca600/orca。

### 2.3 其它

有些系统如CentOS自带了名为orca的带有图形界面的没什么用的屏幕阅读器程序，直接输入orca命令启动的是那个程序，和本文的ORCA毫无联系。应当用rpm -e orca命令将自带的那个orca卸载掉。

如果你是在root用户下使用ORCA，由于OpenMPI的一个恶心的要求，必须每次执行的命令都带着-allow-run-as-root选项才行，这很烦人。可以在.bashrc里加入以下两行来避免，这在《root用户在用openmpi并行计算时避免加--allow-run-as-root的方法》（<http://sobereva.com/409>）里也说过：  
export OMPI_ALLOW_RUN_AS_ROOT=1  
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

如果你的机子里之前装有其它MPI库或OpenMPI的其它版本，且在终端里输入which mpiexec命令的时候指向的是那些库的目录，则ORCA有极大可能会无法正常并行，需要你恰当处理以避免其优先级盖过你自己新装的OpenMPI。具体怎么处理，关键取决于你当前机子里之前具体是怎么装的MPI库。如果你之前是把其它MPI库装到了你自定义的目录下而非默认的/usr/local/bin下面，你就把那个MPI库的目录名随便改一下，或者把那个MPI库在.bashrc里的配置语句注释掉（前面加#号）然后重新登录终端。如果其它MPI被你安装到了默认路径（如/usr/local下），可以把前文的$PATH:/sob/openmpi416/bin改为/sob/openmpi416/bin:$PATH、把$LD_LIBRARY_PATH:/sob/openmpi416/lib改为/sob/openmpi416/lib:$LD_LIBRARY_PATH，然后重新登录终端，之所以这样做会奏效是因为此时openmpi416的路径会先于其它路径出现在这俩环境变量里，会被优先利用。

如果想用非常强大的波函数分析程序Multiwfn（<http://sobereva.com/multiwfn>）对ORCA的计算结果进行波函数分析和观看轨道图形，运行orca_2mkl xxx -molden，就把ORCA计算时产生的xxx.gbw转化成了xxx.molden.input，此文件可以直接作为Multiwfn的输入文件。orca_2mkl是ORCA目录下自带的意义上类似于Gaussian的formchk的工具。如果把Multiwfn目录里的settings.ini里的orca_2mklpath参数设为当前机子里orca_2mkl可执行文件的实际路径，则Multiwfn还可以直接载入gbw文件，更方便了。

Multiwfn还可以基于ORCA的输出文件绘制光谱图，见《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（<http://sobereva.com/224>）。但注意，如果在Windows下运行ORCA，不要用PowerShell，要么用cmd要么用cmder。因为PowerShell里通过重定向产生的ORCA输出文件默认是Unicode编码的，Multiwfn没法读取里面的信息（注：此情况在Powershell 7做了改变，见<http://bbs.keinsci.com/thread-52770-1-1.html>）。《OfakeG：使GaussView能够可视化ORCA输出文件的工具》（<http://sobereva.com/498>）介绍的OfakeG程序也同样不认Unicode编码。用cmder的方法前面已经说了，在Win 10/11里如果想方便快速地进入cmd，只需运行一个注册表配置文件即可，见<http://bbs.keinsci.com/thread-22940-1-1.html>。
