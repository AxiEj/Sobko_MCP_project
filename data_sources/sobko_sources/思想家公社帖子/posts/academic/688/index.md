---
post_id: 688
title: Multiwfn在Linux下安装的中文说明
url: http://sobereva.com/688
date: '2023-10-22T10:44:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章是Multiwfn在Linux下的安装说明，属于软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**Multiwfn在Linux下安装的中文说明**

Chinese instructions for installing Multiwfn under Linux

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2023-Oct-22   Last update: 2026-Jan-3

非常流行的波函数分析程序Multiwfn（<http://sobereva.com/multiwfn>）在Linux下的安装方法在Multiwfn手册2.1.2节有充分的说明，但我发现老有人不仔细看，或者由于缺乏Linux最基本常识而无法正确follow，还有人因为那是英文就干脆不看而放弃安装。鉴于此，这里用中文完整、详细说一下Multiwfn在Linux环境下的安装。如果对Multiwfn一无所知，参看《Multiwfn FAQ》（<http://sobereva.com/452>）和《Multiwfn入门tips》（<http://sobereva.com/167>）。Multiwfn的可执行文件、源代码和手册都可以在官网<http://sobereva.com/multiwfn>中的Download页面下载。本文介绍的情况适用于目前Multiwfn官网上最新版本。本文里涉及的命令里的空格必须看清楚，眼睛不好就直接从本文中复制粘贴命令。如果仔细看本文还是安装不成功，可以去Multiwfn论坛<http://bbs.keinsci.com/wfn>发帖提问，必须把软件环境和遇到的问题交代得尽可能具体。

安装Multiwfn非常简单，本文文字多纯粹是因为讲解得详细。

### 0 关于Multiwfn的普通版与noGUI版

首先要知道Multiwfn的Linux版有普通版和noGUI版两种，前者在官网的下载页面上是Multiwfn_[版本号]_bin_Linux.zip形式的文件名，后者在文件名里多了个noGUI字样。普通版具有完整的功能，但运行时需要有motif图形库提供的libXm.so.4文件（这个文件本身是Multiwfn所用的dislin图形库所依赖的），否则无法启动，安装这个库需要root权限。然而在超算或者公用的服务器上，普通用户又拿不到root权限而没法安装motif库。为了解决这个矛盾，Multiwfn在官网上特意提供了noGUI版，由于它在启动时不需要motif库，因此也就不需要弄到root权限来安装它，故普通用户都可以很容易地安装。**noGUI版的缺点在于没法使用任何Multiwfn与图形有关的功能**，如无法显示出图形界面、没法绘制各种曲线图/平面图/等值面图（无论是在屏幕上显示还是保存为图像文件都不行）、做拓扑分析/盆分析/域分析等分析后无法直接可视化结果，等等。由于特意放到高性能Linux服务器上运行Multiwfn通常是为了让Multiwfn跑一些高耗时的任务，它们往往不直接涉及图像显示，所以这并不会带来明显问题。

下面就开始讲Multiwfn在Linux下的安装流程。

### 1 安装motif库（安装noGUI版直接跳过此节）

如果你用的是Redhat系操作系统，如Redhat Enterprise Linux，CentOS（包括stream）、Rocky Linux、Fedora等，在确保机子能正常访问Internet的情况下，在终端（即命令行界面里）输入yum install motif命令即可安装motif库。这需要root权限，要么以root方式登录，要么在普通用户下用sudo来执行此命令。  
注：如果你是Rocky Linux或相似系统 >=10版的用户，运行上述命令前需要先执行dnf install epel-release安装扩展程序源。

如果你无法访问Internet，可以自行去<https://motif.ics.com/motif/downloads>下载适合x86_64架构的最新的motif库，比如<https://motif.ics.com/sites/default/files/motif-2.3.4-1.x86_64_0.rpm>，放到Linux服务器上后用rpm -i motif-2.3.4-1.x86_64_0.rpm命令手动安装之。不过这样安装往往会提示缺一些乱七八糟的依赖库，所以还是建议尽量用yum方式安装。

如果你不知道当前机子里已经装了motif没有，运行rpm -qa|grep motif命令，如果找到了，那就不用再装了。

上面说的都是Redhat系Linux的情况。如果你是Debian系Linux如Ubuntu的用户，在连着Internet的情况下可以用sudo apt-get install libxm4 libgl1命令安装motif和相关的libgl1库。

### 2 检查SysV共享内存段

注：Rocky Linux、CentOS用户不需要这一步，默认就是合适的。

运行cat /proc/sys/kernel/shmmax命令检查SysV共享内存段的值，数值的单位为字节。有的系统这个值默认得非常小，比如就32MB，当Multiwfn做一些较耗内存的分析、载入较大波函数文件时会崩溃。发现需要增大的话，在/etc/sysctl.conf里加入比如kernel.shmmax = 2000000000然后重启系统，就可以令上限提升到大约2GB。修改此文件需要有root权限。

### 3 解压Multiwfn

去Multiwfn官网上下载同时带着bin字样（binary，即已编译好的可执行文件）和Linux字样的压缩包，放在Linux系统下，用unzip [文件名] 命令将之解压到当前目录下。图形界面里也可以在此文件上点右键后选择解压。

下文假定解压后的目录是/home/sob/Multiwfn_[版本号]_bin_Linux/，在里面应当可以看到Multiwfn程序的各种文件。

### 4 配置~/.bashrc文件

每个用户主目录下都有一个.bashrc文件，记录了每次进入终端后自动执行的命令。由于这是隐藏文件，所以默认情况下看不到。你可以输入vi ~/.bashrc（看清楚vi后面的空格）用vi编辑器去编辑它，也可以在Linux图形界面中要求显示隐藏文件，然后通过操作系统自带的有图形界面的文本编辑器去编辑它。在此文件末尾加上以下内容  
ulimit -s unlimited  
export OMP_STACKSIZE=200M  
export Multiwfnpath=/home/sob/Multiwfn_[版本号]_bin_Linux  
export PATH=$PATH:/home/sob/Multiwfn_[版本号]_bin_Linux  
然后保存文件。

下面解释一下以上命令的意义。

ulimit -s unlimited用来去除某些操作系统对堆栈内存使用的限制。某些系统默认的限制设置非常脑残，不这么设一下的话用Multiwfn处理稍微大一点的波函数都会出现Segmentation fault报错而终止。

export OMP_STACKSIZE=200M用来将OMP_STACKSIZE环境变量设为200M，代表200MB。注意不可写成200m。Multiwfn并行运算是通过OpenMP技术实现的，即计算会分摊到不同的线程上，往往有很多数组要储存在每个线程的堆栈内存里。每个线程可以用的堆栈内存量上限就是通过OMP_STACKSIZE来设的，以上例子设成了200MB通常够用了，如果不够的话会导致计算崩溃。并行核数乘以OMP_STACKSIZE值必须显著小于物理内存可用量。

Multiwfn目录下的settings.ini文件记录了Multiwfn的配置信息。Multiwfn启动时首先在当前目录下寻找settings.ini，如果找不到，则会在Multiwfnpath环境变量设定的目录下找settings.ini，如果还找不到，则会使用默认设定（和程序压缩包里settings.ini里的原始设置相同）。由于在Linux下启动Multiwfn时通常不是在Multiwfn目录下启动的，这是为什么上面要定义Multiwfnpath环境变量，用来避免Multiwfn找不到settings.ini。

PATH是Linux系统的一个重要的环境变量，里可以包含一大堆目录。如果将一个可执行文件所在目录加入其中，那么在任意目录下都可以直接输入可执行文件名而不用带着目录名就可以启动之。如上将Multiwfn所在目录加入PATH环境变量就是为了这个目的。

### 5 增加可执行权限

Multiwfn的普通版的可执行文件是Multiwfn目录下的Multiwfn，noGUI版是Multiwfn目录下的Multiwfn_noGUI。现在给它们加上可执行权限使之可以被运行。

对于普通版，在终端里运行chmod +x /home/sob/Multiwfn_[版本号]_bin_Linux/Multiwfn。如果是noGUI版，显然把其中的Multiwfn替换成Multiwfn_noGUI。

### 6 配置settings.ini

编辑Multiwfn目录下的settings.ini，搜索nthreads，将之数值改为计算时要用的并行核数，通常设为CPU的物理核心数即可。

settings.ini里还有几个其它设置想改的话可以根据需要修改一下  
• formchkpath：定义的是Gaussian目录下的formchk程序的路径。formchk是干嘛的在《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）里明确说了。如果把它设成了formchk的实际的路径，Multiwfn就可以直接载入Gaussian的chk文件（在载入时会自动调用formchk转换成fch文件后载入）。  
• orca_2mklpath：如果设成了ORCA目录下的orca_2mkl可执行文件的路径，Multiwfn就可以直接载入ORCA计算产生的gbw文件（在载入时会自动调用orca_2mkl转换成molden文件后载入）。  
• gaupath和orcapath：当它们分别设成了Gaussian和ORCA的可执行文件的路径，Multiwfn的一些功能才能自动调用Gaussian和ORCA进行计算，如《使用Multiwfn超级方便地计算出概念密度泛函理论中定义的各种量》（<http://sobereva.com/484>）介绍的功能。

### 7 测试

退出终端（关闭终端窗口，或者断开链接），然后重新进入终端，之后直接输入Multiwfn（普通版）或Multiwfn_noGUI（noGUI版）应当就能进入Multiwfn了。之后可以随便做简单的测试，比如载入Multiwfn程序包自带的examples目录下的文件然后做简单的计算。例如载入examples/CH3CONH2.fch，之后依次输入  
9  
8  
屏幕上马上就会输出《Multiwfn支持的分析化学键的方法一览》（<http://sobereva.com/471>）里介绍的拉普拉斯键级。

### 8 其它

如果你是通过纯文本界面连接远程Linux服务器并在上面执行Multiwfn的普通版，并且发现启动Multiwfn时会短暂卡住，在~/.bashrc文件末尾加入export DISPLAY=":0"可以避免。

《在Linux系统下安装Multiwfn 3.6的演示（CentOS 7.6）》（<https://www.bilibili.com/video/av41402462/>）是一个较老版本Multiwfn在Linux下的安装演示，如果你在follow上文时遇到困难可以参考。里面有些流程和细节与本文不同，以本文为准。
