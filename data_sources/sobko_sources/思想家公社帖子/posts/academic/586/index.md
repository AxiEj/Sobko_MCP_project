---
post_id: 586
title: CP2K第一性原理程序在Linux中的安装方法
url: http://sobereva.com/586
date: '2021-02-16T21:00:00+08:00'
source_categories:
- CP2K
- 第一性原理
primary_topic: CP2K
secondary_topics:
- 第一性原理
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 CP2K 在 Linux 下的安装教程，主题非常明确。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**CP2K第一性原理程序在Linux中的安装方法**  
Installation method of CP2K first principle program in Linux

文/Sobereva@[北京科音](http://www.keinsci.com)  
First release: 2021-Feb-16  Last update: 2026-Jan-9

## 1 前言

CP2K（<https://www.cp2k.org>）是非常优秀、功能十分强大、流行度相当高的第一性原理程序，开源免费，跑中、大周期性体系的速度甩基于平面波的程序如Quantum ESPRESSO和VA$P一条街以上。笔者开发的Multiwfn（<http://sobereva.com/multiwfn>）的创建CP2K输入文件的功能使得CP2K创建常见任务的输入文件十分方便（见《使用Multiwfn非常便利地创建CP2K程序的输入文件》<http://sobereva.com/587>），尤其是笔者从2023年起开设了真正全面、系统、深入浅出讲解CP2K正确使用的**“北京科音CP2K第一性原理计算培训班”（**[**http://www.keinsci.com/KFP**](http://www.keinsci.com/KFP)**）**，从而有了极好的从零开始系统学习CP2K并达到精通的机会，使得CP2K在国内已变得相当流行。本文就详细介绍一下CP2K怎么在Linux系统中进行安装。本文讲的是最标准的自行编译的安装方式。也有一些安装预编译版本的方法，流程虽然更为简单，但预编译版本为了兼容性考虑，无法充分利用你的CPU指令集并针对CPU架构进行优化，因此原理上性能不如自己编译的好。

由于CP2K从2026.1版本开始编译方式有了极大的变化，因此本文分为两部分，第2节讲CP2K >=2026.1版本的安装和运行方法（2026-Jan-8最初写的，之后会不断更新），第3节讲<=2025.2版本的安装和运行方法（2021-Feb-16最初写的，最后一次更新于2025-Sep-12，之后不再更新）。这两部分内容有很多是重复的。

提醒零基础初学者：看清楚本文里每一个空格！并且为了免得照抄都抄不对，建议直接从本文里复制命令！

## 2 CP2K >=2026.1版本的安装和运行

### 2.1 前言

下面的安装方法在Rocky Linux 9.1和10.1亲测都顺利通过，不建议用更老版本系统（更老的系统可能需要自己升级gcc，需要折腾）。Rocky Linux是我目前最推荐的用于科学计算目的计算机的Linux操作系统，没有之一，作为服务器和个人计算机的系统都很适合。CentOS Stream和Redhat与Rocky Linux没实质区别，其用户也可以直接用下文的方法。对于Ubuntu（我不喜欢）等其它Linux操作系统的用户我不提供帮助，可参考本文根据实际遇到的情况随机应变。

PS：常有人问我装Rocky Linux的时候应该选什么，建议Base Environment选Workstation，组件选GNOME Applications、Legacy UNIX Compatibility、Development Tools、Scientific Support（不同版本系统能选的选项或选项名有所差异，随机应变）。

CP2K是基于Fortran的程序，但它依赖的一堆库很多都是C/C++写的，所以Fortran和C/C++编译器都得有。CP2K的编译对于编译器有明确的要求，兼容情况见<https://www.cp2k.org/dev:compiler_support>。本文基于Linux系统自带的gcc/gfortran进行编译，运行gcc -v命令可以看到当前系统里的gcc版本。用合适版本的Intel的icc和ifort编译器来编译CP2K及相关的库也可以，但本文不涉及。

如果你的机子里还没装gcc/gfortran，也即运行gcc命令、gfortran命令时提示command not found，应当在联网的情况下运行dnf install gcc以及dnf install gcc-gfortran安装上。

CP2K会利用到BLAS和LAPACK标准库中的子程序。默认情况下会用OpenBLAS库提供的这部分子程序，但据说OpenBLAS的LAPACK子程序的效率不如Intel的MKL数学库好，因此改用MKL可能计算速度更快，不过笔者的一些简单的对比测试并未发现用MKL时速度有显著优势，因此本文不用MKL，省得读者还要额外安装MKL。

CP2K的少部分计算也支持GPU加速，但对于广大草根阶层的用户，相对于纯CPU计算来说并没有什么性价比，因此本文不涉及编译GPU加速版。

下面就开始安装过程的说明。这里以安装2026.1版为例，对于之后的版本也都适用。如果情况发生了变化，我大概率会更新本文，请注意本文开头写的更新日期。笔者使用的是root用户（PS：对于个人独占的计算机，用root用户最方便，笔者从未翻过车，并且极度反感坊间妖魔化root的说法）。

### 2.2 安装CP2K依赖的库

去<https://github.com/cp2k/cp2k/releases/>下载CP2K源代码包cp2k-2026.1.tar.bz2，运行tar -xf cp2k-2026.1.tar.bz2命令解压之。下文假设解压后的目录是/sob/cp2k-2026.1/。

CP2K依赖于一大堆库，最方便的方法是用自带的toolchain脚本一次性安装。运行以下命令  
cd /sob/cp2k-2026.1/tools/toolchain/  
./install_cp2k_toolchain.sh --with-openmpi=install --with-plumed=install --with-tblite=install --with-dftd4=install -j [你机子的CPU物理核心数]  
之后这个toolchain脚本就会依次下载各个库的压缩包到toolchain/build目录下并解压和自动编译，编译产生的可执行文件、库文件、头文件等都自动装到了toolchain/install目录下。其中其中最耗时的是编译libint那一步。

一些重要细节：  
• 运行./install_cp2k_toolchain.sh --help可以查看toolchain的帮助。可见有的库默认是安装的，有的默认不装，通过选项来决定，可以按需调整。以上命令已经把CP2K最重要的库都装上了。toolchain脚本的使用细节见<https://github.com/cp2k/cp2k/blob/master/tools/toolchain/README.md>。  
• --with-openmpi=install代表安装OpenMPI库，这使得编译出来的CP2K可以通过MPI方式并行计算。CP2K也支持其它MPI库如Intel MPI和MPICH。我个人比较习惯用OpenMPI，这也是目前最主流的。重要提示：如果你的机子里已经有了OpenMPI，应当用--with-openmpi=system，这使得CP2K直接用机子里现成的OpenMPI，否则额外再自动装一个OpenMPI可能造成一些冲突。  
• --with-plumed=install代表安装默认不自动装的PLUMED库，这使得CP2K可以结合PLUMED做增强采样的动力学。如果你不需要此功能的话可以不加这个选项，可以节约少量编译时间。  
• --with-tblite=install明确要求编译tblite，这使得CP2K可以利用tblite做GFN2-xTB计算。你若不需要这个可以写--with-tblite=no避免安装。  
• --with-dftd4=install明确要求编译dftd4，这使得CP2K支持DFT-D4色散校正，此方法参见《DFT-D4色散校正的简介与使用》（<http://sobereva.com/464>）。你若不需要这个可以写--with-dftd4=no避免安装。  
• toolchain默认用所有CPU逻辑核心并行编译，可以自行加上-j [并行核数]来明确指定用多少核，建议设成物理核心数。编译的耗时和CPU核数关系很大。  
• toolchain默认自动下载和编译cmake。如果你通过yum或dnf已经装过cmake而且其版本较新，可以再加上--with-cmake=system用当前系统里的cmake，能节约编译时间。  
• 对于CP2K 2026.1，在上述命令执行完毕后，toolchain/build目录约占8 GB，里面的文件之后用不着，因此toolchain运行成功后可以把这个build目录删掉节约硬盘。  
• 如果toolchain运行过程中某个库编译失败，可以去toolchain/build目录下的那个库的目录中去找编译过程输出的log文件，在里面搜error根据报错试图分析原因。toolchain运行失败后可以重新运行，它会根据根据toolchain/build目录的内容做判断，之前已经下载和编译成功的库会自动跳过，而从失败的库继续编译。如果把build和install目录都删了，则toolchain会从头执行。  
• 如果在安装某个库的过程中一直卡着，通过top命令发现CPU也没在编译库，那么几乎一定是因为网速太慢导致那些库的压缩包老也下载不完（在大陆区域不可描述的访问国际互联网的条件下尤为常见）。可以去tools/toochain/build目录下看看正在装的这个库的压缩包，如果尺寸特别小，而且尺寸增加得特别缓慢，说明就是这个问题所致。解决方法是开微*N加速访问国际互联网。还一个办法是找个访问国际互联网通畅的机子或者拜托朋友，在那里安装一次当前版本的CP2K，然后把build目录下的.tgz、.tar.gz、.tar.bz2那些库的压缩包拷到之前那个机子的build目录下，这样那个机子在安装CP2K过程中就会直接用这些包而不会试图下载了，对于没法访问Internet的机子也可以这样离线安装CP2K。还有一种方法是直接自己去<https://www.cp2k.org/static/downloads/>下载CP2K编译过程中要用到的各种包放到build目录下。但要注意，tblite安装过程中还会（讨厌地）联网下载额外的东西，因此没有网的话应当加上--with-tblite=no。

### 2.3 编译CP2K

接着上一节，运行以下命令  
source /sob/cp2k-2026.1/tools/toolchain/install/setup  
cd /sob/cp2k-2026.1  
mkdir build  
cd build  
cmake -S .. -DCP2K_USE_EVERYTHING=ON -DCP2K_USE_DLAF=OFF -DCP2K_USE_PEXSI=OFF -DCP2K_USE_LIBSMEAGOL=OFF -DCP2K_USE_DEEPMD=OFF -DCP2K_USE_ACE=OFF -DCP2K_USE_TREXIO=OFF -DCP2K_USE_GREENX=OFF -DCP2K_USE_LIBTORCH=OFF -DCP2K_USE_MIMIC=OFF -DCMAKE_INSTALL_PREFIX=/sob/cp2k-2026.1/exe/ -DCP2K_DATA_DIR=/sob/cp2k-2026.1/data  
make install -j96  （96是并行编译用的物理核心数，你的机子实际是多少就写多少）  
我在双路7R32 96核机子上5分多钟编译完毕。  
注：cmake这一步的更多的信息可以参考<https://manual.cp2k.org/trunk/getting-started/build-from-source.html>和<https://manual.cp2k.org/trunk/technologies/libraries.html>。

编译出的可执行程序现在都产生在了/sob/cp2k-2026.1/exe/bin目录下，里面的cp2k.psmp就是CP2K的可执行文件了。

把以下内容加入到~/.bashrc文件里（这是你的用户主目录下的隐藏文件.bashrc，要求文件管理器显示隐藏文件时才能看到。也可以运行vi ~/.bashrc命令利用vi文本编辑器编辑）：  
source /sob/cp2k-2026.1/tools/toolchain/install/setup  
export PATH=$PATH:/sob/cp2k-2026.1/exe/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/cp2k-2026.1/exe/lib64  
重新进入终端后，就可以通过cp2k.psmp命令运行cp2k了。运行cp2k.psmp -v可以查看CP2K的版本、编译时用的库和参数信息。

### 2.4 运行和测试CP2K

这里提供一个简单的输入文件用于测试：<http://sobereva.com/attach/586/test.inp>。这是Multiwfn生成的2*2*2金刚石超胞做PBE/DZVP-MOLOPT-SR-GTH单点计算的输入文件。

cp2k.psmp同时支持MPI并行和OpenMP并行，并且可以二者结合，即每一个MPI并行进程下属多个OpenMP线程。例如16个物理核心的机子，有几种跑法：  
(1)MPI进程数=16，OpenMP线程数=1。此时完全靠MPI方式并行  
(2)MPI进程数=4，OpenMP线程数=4。此时靠MPI与OpenMP结合并行（也可以用其它组合，比如8*2、2*8等，乘积等于物理核心数即可）  
(3)MPI进程数=1，OpenMP线程数=16。此时完全靠OpenMP方式并行  
靠MPI并行速度一般比靠OpenMP并行更快，因为CP2K很多代码只支持MPI并行而不支持OpenMP并行，而且OpenMP并行当线程数多的时候存在内存访问争抢问题，因此速度是(1)>(2)>(3)。但OpenMP方式并行可以在不同核心之间充分共用内存中的数据而避免很多重复储存，因此内存消耗量也是(1)>(2)>(3)。

MPI并行进程数由mpirun -np后面的数值决定。OpenMP线程由OMP_NUM_THREADS环境变量决定，如果你运行export OMP_NUM_THREADS=4命令将这个环境变量定义为4，就代表每个MPI进程下属4个OpenMP线程。注意哪怕你完全不想用OpenMP方式并行，也不能不设OMP_NUM_THREADS环境变量，而必须设为1，否则OpenMP线程数会自动设为所有逻辑核心数（如果此时还利用了MPI并行，则相当于要求的并行核数远超实际物理核心数，将会因为资源争抢而算得超极慢）。

这里给出运行例子，输入文件是test.inp，输出信息既存到test.out里也显示在屏幕上：  
(1)MPI进程数=16，OpenMP线程数=1：在已运行过export OMP_NUM_THREADS=1的前提下运行mpirun -np 16 cp2k.psmp test.inp |tee test.out  
(1)MPI进程数=4，OpenMP线程数=4：在已运行过export OMP_NUM_THREADS=4的前提下运行mpirun -np 4 cp2k.psmp test.inp |tee test.out  
(3)MPI进程数=1，OpenMP线程数=16：在已运行过export OMP_NUM_THREADS=16的前提下运行cp2k.psmp test.inp |tee test.out

一些技巧和细节：

如果不希望输出信息同时显示在屏幕上，把|tee改成>

为了避免每次进入终端都需要重新定义OMP_NUM_THREADS环境变量，建议把定义它的语句写入到~/.bashrc文件里，每次进入终端后会自动生效。

可以在mpirun后面直接指定运行当前任务用的临时的OMP_NUM_THREADS设置，例如下面的例子用6个MPI进程、4个OpenMP线程，总共24核并行：  
mpirun -np 6 -x OMP_NUM_THREADS=4 cp2k.psmp test.inp > test.out

为了运行时省事，可以在~/.bashrc里加入alias cp2k='mpirun -np 16 -x OMP_NUM_THREADS=1 cp2k.psmp'。重新进入终端后，只要输入  
cp2k test.inp |tee test.out就等于用16核完全靠MPI并行了，即等价于输入了mpirun -np 16 -x OMP_NUM_THREADS=1 cp2k.psmp test.inp |tee test.out。

如果没特殊情况，强烈建议完全通过MPI方式并行，效率最高。但对于一些任务恰当利用一些OpenMP并行是必须的，否则往往会遇到内存不足而崩溃。典型的就是振动分析和跑NEB任务，需要跑一大堆副本。北京科音CP2K第一性原理计算培训班（<http://www.keinsci.com/KFP>）里讲相应类型计算的时候很细致地介绍了在并行方式上需要做的重要考虑。杂化泛函计算对周期性大体系、大基组来说要算的双电子积分量巨大，这一点我在《CP2K做杂化泛函计算的关键要点和简单例子》（<http://sobereva.com/690>）中说了。为了能让内存中尽可能多地储存双电子积分避免SCF迭代过程中重复计算，往往也需要MPI与OpenMP相结合来节约内存。

## 3 CP2K <=2025.2版本的安装和运行

### 3.1 前言

最初写本文的时候我用的是CentOS，后来我改用Rocky Linux 9后实测也可以用与本文完全相同的方式安装。Rocky Linux是我目前最推荐用于科学计算目的计算机的Linux操作系统，没有之一。对于Ubuntu等其它Linux操作系统的用户我无法提供帮助，请参考本文随机应变。

最初写本文的时候CP2K最新的是8.1版。后来以同样的方法，经测试也可以顺利编译从8.2一直到2025.2的全部版本。安装其它版本的情况请随机应变。

CP2K有sopt、ssmp、popt、psmp四种版本，如果你不了解的话，先看一下本文文末附录中的介绍。

CP2K有三种安装方式：  
(1)先依次手动编译CP2K所需要的各个库，然后再编译CP2K，具体过程见官方说明<https://github.com/cp2k/cp2k/blob/master/INSTALL.md>。我不推荐这种做法，因为CP2K涉及的库特别多，一个一个手动编译颇为麻烦。如果你有经验和耐心可以这么鼓捣。  
(2)使用CP2K自带的toolchain脚本。toolchain可以自动把CP2K依赖的各种库都一一下载并且自动编译，最后输入几行命令再把CP2K编译出来就OK了。整个过程非常简单省事，下文第2节就介绍这种做法。  
(3)直接用官方预编译的ssmp版，下载后直接就能用，极为方便，下文第3节会说具体做法。

### 3.2 基于toolchain安装CP2K

### 3.2.1 相关知识

CP2K是基于Fortran的程序，但它依赖的一堆库很多都是C/C++写的，所以Fortran和C/C++编译器都得有。CP2K的编译对于编译器有明确的要求，兼容情况见<https://www.cp2k.org/dev:compiler_support>。可见如果用gcc+gfortran来编译的话，gcc必须>=5.5版。CentOS 7.x自带的gcc是4.8.5版，因此没法直接编译，要么升级gcc编译器（具体做法自行google，有把系统弄出毛病的风险），要么用CentOS >=8.0版。CentOS 8.0自带的gcc是8.3.1，可以非常顺利地结合toolchain编译CP2K（PS：常有人问我装CentOS或Rocky Linux的时候应该选什么，建议Base Environment选Workstation，组件选GNOME Applications、Legacy UNIX Compatibility、Development Tools、Scientific Support。不同版本能选的选项或选项名可能有所差异，随机应变）。

用合适版本的Intel的icc和ifort编译器来编译CP2K及相关的库也可以，这样CentOS 7.x的用户也省得升级gcc或者换系统了。但19.0.1版结合toolchain用的时候笔者发现有的库编译不过去，笔者不打算深究，本文就不说这种做法了。

toolchain运行过程中会自动下载很多库的压缩包，所以必须联网，而且网速还不能太慢，否则有的库半天也下不下来，甚至最终失败。如果你在大陆，强烈建议通过科学的方式加速对外部网络的访问。

关于MKL数学库

CP2K会利用到BLAS和LAPACK标准库中的子程序。默认情况下会用OpenBLAS库提供的这部分子程序，但据说OpenBLAS的LAPACK子程序的效率不如Intel的MKL数学库好，因此改用MKL可能计算速度更快，不过笔者的一些简单的对比测试并未发现用MKL时速度有显著优势。如果你想用MKL的话，那么运行下一节的toolchain前先把MKL装到系统里，即运行下列命令：  
dnf config-manager --add-repo <https://yum.repos.intel.com/mkl/setup/intel-mkl.repo>  
rpm --import <https://yum.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB>  
dnf install intel-mkl  
此时MKL会被装到/opt/intel/目录下，被装到笔者机子里的是MKL 2018版，占2.2GB硬盘。把下面的语句加入到~/.bashrc文件中，然后重新进入终端使之生效  
source /opt/intel/parallel_studio_xe_2018.0.033/bin/psxevars.sh  
上面这行语句会使得MKLROOT环境变量指向MKL库的目录。当运行toolchain的时候发现MKLROOT环境变量被指定了，就会自动利用MKL数学库（无需额外写--with-mkl选项）。

如果你想离线安装MKL，可以去Intel官网免费注册并下载Intel OneAPI base toolkit离线安装包。安装的时候只选择安装其中的MKL就够了。装好后把下面这句加入~/.bashrc文件里，然后重新进入终端使之生效  
source /opt/intel/oneapi/mkl/[实际版本号]/env/vars.sh  
但这样装MKL的情况下，笔者遇到过CP2K 8.1的toolchain在装COSMA库的时候编译不过去的问题。如果你也遇到了此问题，把toolchain的命令后头加上--with-cosma=no避免装COSMA库即可，这对性能影响甚微。

### 3.2.2 通过toolchain安装CP2K依赖的库

去<https://github.com/cp2k/cp2k/releases/>下载CP2K压缩包cp2k-8.1.tar.bz2，运行tar -xf cp2k-8.1.tar.bz2命令解压之。下文假设解压后的目录是/sob/cp2k-8.1/。

运行以下命令  
cd /sob/cp2k-8.1/tools/toolchain/  
./install_cp2k_toolchain.sh --with-sirius=no --with-openmpi=install --with-plumed=install  
之后这个toolchain脚本就会依次下载各个库的压缩包到toolchain/build目录下并解压和自动编译，编译产生的可执行文件、库文件、头文件等都自动装到了toolchain/install目录下。在笔者的普通四核机子结合非常畅通的网络下，整个过程耗时约两个小时。其中最耗时的是编译libint那一步，花了一个小时有余，一定要耐心。

以下信息应了解一下  
• 如果运行上述脚本后提示ERROR: (./scripts/install_gcc.sh) cannot find gfortran，应当运行dnf install gcc-gfortran先把gfortran编译器装上，然后重新运行脚本。  
• 运行./install_cp2k_toolchain.sh --help可以查看toolchain的帮助。可见有的库默认是安装的，有的默认不装，通过选项来决定，可以按需调整。toolchain脚本的使用细节见<https://github.com/cp2k/cp2k/blob/master/tools/toolchain/README.md>  
• --with-sirius=no选项代表不装本来自动会装的SIRIUS库。这个库使得CP2K可以像Quantum ESPRESSO那样完全基于平面波+赝势做计算，但一般这用不上，想做这种计算的人一般直接就用Quantum ESPRESSO了，其安装见《Quantum ESPRESSO在Linux中的安装方法》（<http://sobereva.com/562>）。  
• --with-openmpi=install代表安装OpenMPI库，这使得编译出来的CP2K可以通过MPI方式并行计算。CP2K也支持其它MPI库如Intel MPI和MPICH。我个人比较习惯用OpenMPI，这也是目前最主流的。重要提示：如果你的机子里已经有了OpenMPI，应当用--with-openmpi=system，这使得CP2K直接用机子里现成的OpenMPI，否则额外再自动装一个OpenMPI可能造成一些冲突。  
• --with-plumed=install代表安装默认不自动装的PLUMED库，这使得CP2K可以结合PLUMED做增强采样的动力学。如果你不需要此功能的话可以不加这个选项，可以节约少量编译时间。  
• 从CP2K 2024.2开始支持了DFT-D4色散校正，这种校正的常识见《DFT-D4色散校正的简介与使用》（<http://sobereva.com/464>）。想用DFT-D4的话必须再额外带上--with-ninja --with-dftd4。  
• toolchain默认用所有CPU核心并行编译，可以自行加上-j [并行核数]来明确指定用多少核。编译的耗时和CPU核数关系很大。笔者在36核机子上也就花了不到20分钟就把toolchain过程全都完成了。  
• toolchain默认自动下载和编译cmake。如果你通过yum或dnf已经装过cmake而且其版本较新，可以再加上--with-cmake=system用当前系统里的cmake，能节约编译时间。  
• 注意硬盘的空余空间应当足够。对于CP2K 8.1在上述命令执行完毕后，toolchain/build目录约占9GB，toolchain/install目录占约2GB。如果硬盘吃紧，建议toolchain运行成功后把这个build目录删掉，里面的文件之后用不着。  
• 如果toolchain运行过程中某个库编译失败，可以去toolchain/build目录下的那个库的目录中去找编译过程输出的log文件，在里面搜error根据报错试图分析原因。toolchain运行失败后可以重新运行，它会根据根据toolchain/build目录的内容做判断，之前已经下载和编译成功的库会自动跳过，而从失败的库继续编译。如果把build和install目录都删了，则toolchain会从头执行。  
• 如果在安装某个库的过程中一直卡着，通过top命令发现CPU也没在编译库，那么几乎一定是因为网速太慢导致那些库的压缩包老也下载不完（在大陆区域不可描述的访问国际互联网的条件下尤为常见）。可以去tools/toochain/build目录下看看正在装的这个库的压缩包，如果尺寸特别小，而且尺寸增加得特别缓慢，说明就是这个问题所致。解决方法是开微屁恩加速访问国际互联网。还一个办法是找个访问国际互联网通畅的机子或者拜托朋友，在那里安装一次当前版本的CP2K，然后把build目录下的.tgz、.tar.gz、.tar.bz2那些库的压缩包拷到之前那个机子的build目录下，这样那个机子在安装CP2K过程中就会直接用这些包而不会试图下载了，对于没法访问Internet的机子也可以这样离线安装CP2K。还有一种方法是直接自己去<https://www.cp2k.org/static/downloads/>下载CP2K编译过程中要用到的各种包放到build目录下。

### 3.2.3 编译CP2K

接着上一节，现在把/sob/cp2k-8.1/tools/toolchain/install/arch/下所有文件拷到/sob/cp2k-8.1/arch目录下。这些文件定义了编译不同版本的CP2K所需的参数，其内容是toolchain脚本根据装的库和当前环境自动产生的。

然后运行以下命令  
source /sob/cp2k-8.1/tools/toolchain/install/setup  
cd /sob/cp2k-8.1  
make -j 4 ARCH=local VERSION="ssmp psmp"  
-j后面的数字是并行编译用的核数，机子有多少物理核心建议就设多少。在笔者的普通4核机子上花了40分钟编译完。

注：如果编译中途报错，并且从后往前找error的时候看到cannot find -lz的报错提示，则运行dnf install zlib-devel命令装上zlib库，再重新运行上面的make那行命令即可。

编译出的可执行程序现在都产生在了/sob/cp2k-8.1/exe/local目录下，共1.1GB。这里面cp2k.popt、cp2k.psmp、cp2k.sopt、cp2k.ssmp就是我们所需要的CP2K的可执行文件了（popt和sopt其实分别是psmp和ssmp的符号链接）。

把以下内容加入到~/.bashrc文件里：  
source /sob/cp2k-8.1/tools/toolchain/install/setup  
export PATH=$PATH:/sob/cp2k-8.1/exe/local  
重新进入终端后，就可以通过cp2k.ssmp等命令运行cp2k了。运行诸如cp2k.ssmp -v可以查看CP2K的版本、编译时用的库和参数信息。

注1：上面source这行必须有，因为有的库提供的.so文件是CP2K启动时所需的，source这个脚本使得相应的库的目录被加入到动态库的搜索路径中。而且用了这个之后toolchain过程中装的OpenMPI的可执行文件mpirun等才能直接用。

注2：cp2k-8.1目录下的lib和obj目录分别存的是CP2K编译过程产生的静态库文件和.o文件，总体积不小。由于之后用不着，因此如果想省硬盘可以把这俩目录删掉。

### 3.2.4 直接用官方的预编译版CP2K

对于CP2K 8.1，官方预编译版只提供了ssmp的，并且为了兼容性考虑，编译选项比较保守，没有根据CPU内核进行优化、没有利用SIMD指令集、用的是-O2而非更激进优化的-O3选项，也没用MKL。不过这并不代表官方预编译版的就很慢，笔者对简单任务测试过发现在速度上和自己编译的ssmp版差异不太大。不过，如果对某些类型任务发现ssmp版的CPU占用率普遍较低，吐血建议自己编译popt版，此时有可能二者速度差异超大、用ssmp完全发挥不出CP2K本来的代码效率，甚至可能ssmp版几乎算不动。

使用官方的预编译的ssmp版CP2K的做法如下：  
和2.2节所述相同，先下载cp2k-8.1.tar.bz2压缩包并解压到比如/sob/cp2k-8.1目录。  
去<https://github.com/cp2k/cp2k/releases/>下载CP2K的预编译版可执行文件cp2k-8.1-Linux-x86_64.ssmp，改名为cp2k.ssmp并随便放到一个位置，假设放到了/sob/cp2k-8.1目录下。  
将下面两行加入到~/.bashrc文件中：  
export PATH=$PATH:/sob/cp2k-8.1  
export CP2K_DATA_DIR=/sob/cp2k-8.1/data  
保存后重新进入终端，CP2K就可以通过cp2k.ssmp命令使用了（ssmp版CP2K不是必须叫cp2k.ssmp，也可以改名为cp2k，这样运行更方便）。

为什么设CP2K_DATA_DIR环境变量这里说一下。在CP2K输入文件中，如果诸如BASIS_SET_FILE_NAME、POTENTIAL_FILE_NAME等关键词只定义了文件名而没有给路径，程序默认先在当前目录下搜索相应文件，找不到的话去CP2K_DATA_DIR搜索。CP2K_DATA_DIR对应的是编译的时候CP2K目录下的data目录的路径，但开发者在编译的时候其对应的路径显然跟我们当前情况不符，因此这里通过export来将CP2K_DATA_DIR环境变量改成自己机子里实际的data目录的路径。

### 3.2.5 运行和测试CP2K

这里提供一个简单的输入文件用于测试：<http://sobereva.com/attach/586/test.inp>。这是Multiwfn生成的2*2*2金刚石超胞做PBE/DZVP-MOLOPT-SR-GTH单点计算的输入文件。

先测试ssmp版。将test.inp放到当前目录下，运行：cp2k.ssmp test.inp |tee test.out。输出信息会在屏幕上显示，也同时写入到了test.out里。默认情况下所有CPU核心都会被用于OpenMP并行计算，如果比如想只用4核，就先运行export OMP_NUM_THREADS=4命令然后再运行CP2K，此时运行过程中CP2K进程的CPU占用率应当在300~400%。

再测试popt版。假设用4核通过MPI方式并行，就执行：mpirun -np 4 cp2k.popt test.inp |tee test.out。在top中看到会有4个cp2k.popt在运行，占用率皆接近100%。

如果你是自己编译的CP2K，建议默认用popt版而不要用ssmp版，因为在某些情况下后者运行效率远不及popt版（但也有些任务二者速度差异不大，看具体情况）。为了运行popt版省事，建议在~/.bashrc里面加入一行alias cp2k='mpirun -np 4 cp2k.popt'。重新进入终端后，只要输入cp2k test.inp |tee test.out就等价于输入mpirun -np 4 cp2k.popt test.inp |tee test.out了，用起来省事多了。

注：跑sopt、popt版时，不管设不设OMP_NUM_THREADS、设多少，OMP_NUM_THREADS都会被强行视为1。

### 3.3 附：CP2K的并行以及四种版本

CP2K支持MPI方式并行也支持OpenMP方式并行。最初CP2K是完全基于MPI并行的，但每个核心对应一个MPI进程来并行跑CP2K的话，对某些任务、较大体系消耗内存较高。CP2K如今很多代码也利用OpenMP方式实现了并行化，OpenMP并行的好处是很多数据可以在不同线程之间共享而不用保存副本，从而比MPI并行明显更节约内存。但由于有些CP2K代码仍只能通过MPI方式并行，因此单纯靠OpenMP并行的话某些任务的速度可能明显不及MPI并行，而且并行核数很多时纯OpenMP的并行效率比纯MPI并行的略低是很多科学计算程序中常见的现象。CP2K也支持MPI和OpenMP混合并行，比如CPU有36核，那么可以比如用9个MPI进程，每个MPI进程下属4个OpenMP线程，这样9*4把36个核都利用上，比直接用36个OpenMP线程并行效率可能明显更高，而比用36个MPI进程则明显更省内存（这对于杂化泛函计算比较重要。杂化泛函耗内存远高于纯泛函，如果借助OpenMP节约内存，使得有足够内存储存所有双电子积分，即in-core方式做SCF，就可以避免每次迭代过程中重算这些积分，令SCF迭代过程耗时低得多）。

MPI或MPI+OpenMP可以跨节点并行（OpenMP限于节点内），而纯OpenMP只能单机并行，因为OpenMP是基于共享内存的并行技术。

根据支持的并行方式的不同，CP2K分为四个版本：  
sopt：只能单机单核计算，无法并行。s意为single  
ssmp：OpenMP并行，可以单机多核运行。smp意为Symmetric multiprocessing  
popt：MPI并行，可以单机并行也可以跨节点并行。p意为parallel  
psmp：MPI+OpenMP混合并行，可以单机并行也可以跨节点并行

sopt版严格等价于ssmp版结合OMP_NUM_THREADS=1，popt版严格等价于psmp版结合OMP_NUM_THREADS=1。

实际上还有sdbg和pdbg版，前者相当于ssmp结合debug设置，后者相当于psmp结合debug设置，但这对于开发者调试程序才有意义，所以本文2.3节我们没有编译这俩版本。
