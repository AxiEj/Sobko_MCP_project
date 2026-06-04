---
post_id: 463
title: 量子化学程序Dalton的编译方法和运行方式简介
url: http://sobereva.com/463
date: '2019-02-11T15:39:00+08:00'
source_categories:
- 量子化学
primary_topic: Dalton
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题直接是Dalton程序的编译和运行教程，软件属性非常明确。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**量子化学程序Dalton的编译方法和运行方式简介**

An introduction to the compilation and running mode of Dalton quantum chemistry program

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2019-Feb-11   Last update: 2025-Sep-19

开源免费的量子化学程序Dalton（<http://daltonprogram.org>）虽然用起来比较复杂，对新手很不友好，但由于其擅长计算响应性质，是其它程序难以取代的，所以它有着独特的地位。笔者在北京科音高级量子化学培训班（<http://www.keinsci.com/KAQC>）会专门讲怎么样用Dalton计算磷光速率/寿命/旋轨耦合矩阵元、双光子吸收截面、CASSCF下的磁属性如NICS，欢迎参加。本文介绍怎么安装Dalton，也简单介绍一下怎么运行。本文说的Dalton都指的是Dalton suite中1983年开始发展的那个Dalton程序，而非Dalton suite中从Dalton分化出来的线性标度版Dalton（LSDalton）。

## 1 Dalton的编译

下文的安装过程对于Dalton 2020.1是适用的，其它版本不一定适用，请自行尝试。笔者的操作系统为Rocky Linux 9.0 64bit，Rocky Linux是最适合计算服务器用的Linux操作系统，下文的编译过程对于其它系统不一定适用，请随机应变。笔者用的是root用户。安装过程中机子可以访问Internet。笔者的计算机是《淘宝上购买的双路EPYC 7R32 96核服务器的使用感受和杂谈》（<http://sobereva.com/653>）里介绍的AMD EPYC 7R32 CPU的机子。

本文基于Intel Fortran/C++编译器、MKL数学库和Intel MPI进行编译。读者需要先google搜索Intel one API，去下载Intel oneAPI Base Toolkit和Intel HPC Toolkit软件包并进行安装（本文笔者用的是2024.0版Intel one API），其中前者安装时把DPC++/C++ Compiler和Math Kernel Library装上，后者安装时把Fortran Compiler和MPI Library装上，其它非必须的组件都不需要安装。之后编辑用户目录下的.bashrc文件，在里面加入source /opt/intel/oneapi/setvars.sh > /dev/null后重新进入终端。

PS：原则上，Dalton用gfortran/gcc+OpenMPI也可以编译，但不建议如此，毕竟这样编译出的代码比用ifort/icc慢，而且可能由于个别文件的语法兼容性问题编译不过去。

### 1.1 安装cmake 3.x

如果在你用的系统里输入cmake --version显示的是3.x版本，而且编译Dalton的过程没有提示cmake版本太低，那就可以略过此步。Rocky Linux 9就不需要自行安装cmake 3.x。

如果你用的是较老的系统，比如CentOS 7.2自带的cmake是2.8的，而由于Dalton 2020.1要求3.x版本，因此先得装更新的cmake。做法是在联网的情况下运行以下命令  
yum install cmake3  
mv /usr/bin/cmake /usr/bin/cmake2  
ln -s /usr/bin/cmake3 /usr/bin/cmake  
这里把自带的cmake 2.8备份为cmake2，而把新装的cmake3做了一个符号链接，这样试图调用cmake的程序就用的是cmake 3.x版了。

### 1.2 下载Dalton

在Linux的命令行下运行：  
git clone --recursive <https://gitlab.com/dalton/dalton.git>  
就会把最新版本Dalton下载到当前目录下作为dalton目录。这个“最新版本”体现了开发者迄今对dalton所做的所有最新的改动。然后手动将此目录改名为dalton_src。

注意，不要自行去<https://gitlab.com/dalton/dalton>点击download下载压缩包，因为Dalton的gitlab项目上的external目录的内容里包含外部project，直接下载的压缩包里面是没有那些project的文件的，只有用上面这种方式才能完整下载。之后你可以把这个下载的目录压缩后保留起来，便于以后用或者给其他人用。

如果下载中途意外中断，是网络问题导致，可以尝试其它网络环境再试。或者找别人按上面步骤下载下来，把dalton目录压缩后传给你，放到你自己的机子上解压。

如果你想下载某一特定正式版Dalton比如2020.1，则应当输入git clone -b Dalton2020.1 --recursive <https://gitlab.com/dalton/dalton.git>

### 1.3 编译Dalton的MPI并行版

Dalton主要是靠MPI并行的。由于当前机子里已经有了Intel MPI，所以就不用再额外装MPI库了。MPI版Dalton应当链接串行版MKL库。

下面的过程将把Dalton安装到/sob/dalton目录下。依次运行  
cd dalton_src  
./setup --fc=mpiifort --cc=mpiicx --cxx=mpiicpx --mkl=sequential --prefix=/sob  
cd build  
make install -j  
在笔者的2*7R32 96核服务器上不到2分钟就编译完毕了。现在出现了/sob/dalton目录，里面包含了可执行文件和相关文件。（在vmware虚拟机下用-j可能会在编译中途卡住，去掉-j以串行方式编译，得花大约半个小时）

把以下内容加入到用户主目录下的.bashrc文件中：  
export PATH=$PATH:/sob/dalton  
export DALTON_TMPDIR=/sob    （之后临时文件默认都将产生在/sob/DALTON_scratch_root目录下）  
export DALTON_LAUNCHER="mpirun -np 96"  （-np后面设的是默认情况下运行用的并行进程数）  
重新进入终端，以使以上语句生效。现在就可以通过输入dalton命令来运行了。

在dalton_src/build目录下运行ctest命令进行测试，Dalton 2020.1版总共约570个测试，在笔者的机子上并行执行总共花了1700秒。总共有7个测试结果是Failed，不必担心，一般来说只要编译成功，出现Failed并不是编译有问题，而更可能是开发者提供的参考文件有问题或者测试项目本身有问题（比如有的功能不支持MPI并行），想一探究竟的话可以去Dalton的临时文件目录下找failed的项目的输出文件，看到底是怎么回事。

bug提醒：笔者实测至少对于Dalton 2018、2022，结合Intel编译器时做AMFI方式的旋轨耦合计算存在严重bug，结果明显不合理，讨论见https://gitlab.com/dalton/dalton/-/issues/186。改用gcc编译可避免。做法是确保Intel编译器处于非活动状态、gcc已安装、OpenMPI已装好并处于活动状态的情况下，把前述的./setup那行命令改为./setup --mpi --prefix=/sob/dalton，则脚本自动会识别到gcc、gfortran、OpenMPI。其它安装过程同前即可。这样编译出来的Dalton比按前文编译出来的运行速度往往慢几倍！所以不需要做AMFI计算的人不推荐这样编译，而需要做AMFI计算的人建议gcc+gfortran+OpenMPI和Intel两种都编译，安装到不同目录下，平时用后者，仅当AMFI计算用前者。

### 1.4 编译Dalton的串行+MKL并行版（以下简称MKL并行版）

Dalton的有些功能并不支持MPI并行，比如耦合簇计算功能。使用这些功能时如果你用的是MPI并行版Dalton，那并行进程数只能设为1，或者使用Dalton的串行版。由于Dalton所调用的Intel MKL数学库在运行的时候是支持OpenMP方式并行的，因此对于Dalton的不支持MPI并行的功能，你若在计算的时候想利用多核提升速度，可以编译Dalton的串行版但是链接并行版本的MKL库。下面来编译一下这种版本。

先把之前编译出来的Dalton MPI并行版的目录改个名免得被覆盖掉，比如叫dalton_MPI。然后进入dalton_src目录，把之前的build目录删掉，然后运行  
./setup --fc=ifort --cc=icx --cxx=icpx --mkl=parallel --prefix=/sob  
cd build  
make install -j  
在.bashrc里把export DALTON_LAUNCHER="mpirun -np 96"前面加上#注释掉，再加入export OMP_NUM_THREADS=96来让MKL库默认通过96线程并行，之后重新进入终端使设置生效。

通过MKL实现并行可以跑所有任务，而通过MPI实现并行只能跑支持MPI并行的任务。凡是能用MPI并行的任务建议用MPI并行版来跑，耗时一般比用MKL并行版更低，毕竟Dalton里调用MKL数学库的代码本身就是很有限的，但也不排除有反例，可以实测一下。

所有前述编译都完成，而且测试也都完成后，dalton_src目录就没用了，可以删了。另外值得提醒的是，时间长了可能在Dalton的临时文件目录里积攒很多老旧临时文件，记得时不时清一清。

## 2 Dalton的运行

### 2.1 运行格式

一般情况需要一个.dal文件，内含计算任务的说明；还需要一个.mol文件，内含分子结构、基组定义。

一般运行的格式：dalton [选项] [.dal] [.mol]  
例如，dalton DFT1 H2O代表用DFT1.dal里定义的设置和任务去算H2O.mol里的体系。

运行完毕后在当前目录下的出现的"dal名_mol名.out"是输出文件（dal和mol名相同时只包含一次名字）。同时还产生同名的.tar.gz文件，这个压缩包内含运行期间输出的各种零碎文件，其中molden.inp就是.molden输入文件，可以用笔者开发的Multiwfn程序（<http://sobereva.com/multiwfn>）直接载入此文件做各种波函数分析、观看结构和轨道（主功能0）。相关常识看《Multiwfn入门tips》（<http://sobereva.com/167>）、《使用Multiwfn观看分子轨道》（<http://sobereva.com/269>）。

运算期间不会在屏幕上显示运算过程细节信息。如果运算期间要监控运算过程，可以随时查看这个文件的内容：$DALTON_TMPDIR/DALTON_scratch_用户名/dal名_mol名_pid号/DALTON.OUT。也可以用tail -f [文件名]的做法来实时把此文件里最新写入的信息同步输出到屏幕上便于监控。

### 2.2 常用选项

直接输入dalton命令就可以查看能够接的选项，这里说几个常用的。

-N 96：代表用96个MPI进程进行并行运算，仅对于MPI并行版Dalton有意义。如果没用此选项，就会用DALTON_LAUNCHER环境变量里设的核数来并行计算  
-omp 96：代表通过MKL库以OpenMP方式并行时用96个线程并行运算，仅对于MKL并行版有意义。用这个选项时实际上会自动将控制OpenMP并行线程数的OMP_NUM_THREADS环境变量临时地设成你指定的线程数，因此如果没用此选项，就会用当前机子里的OMP_NUM_THREADS环境变量指定的线程数。另外注意对MKL库来说MKL_NUM_THREADS环境变量定义的并行线程数的优先级高于OMP_NUM_THREADS，因此如果机子里已经定义了MKL_NUM_THREADS，那么-omp选项是不起作用的。还值得注意的是并不总是OpenMP并行线程数越大越好，有可能设得太大后反倒慢，甚至还不如不并行。建议自行测试  
-mb 2500、-gb 5：分别设定当前计算最多用2500MB、5GB内存。注意对于MPI版，这个设的是每个MPI进程的内存上限量，而非所有进程的总和。默认用的最大内存量也可以用WRKMEM环境变量来设，单位是双精度word（8字节）  
-noarch：不让当前任务产生.tar.gz文件  
-nobackup：不备份以前的输出文件。默认情况下如果之前有同名的输出文件存在，会在后面加上数字作为后缀来备份  
-ow：计算过程产生的输出文件"dal名_mol名.out"直接输出到当前目录。默认情况下在运算过程中输出文件被输出到前述DALTON_TMPDIR定义的目录里，算完之后才自动挪到当前目录  
-o [文件名]：直接指定输出文件名字，而且运算过程中就直接产生

Dalton运行时用的命令"dalton"实际上是dalton目录下面的一个bash脚本，用来设定运行环境，并调用实际可执行文件dalton.x。这类似于GAMESS的rungms脚本。如果想把一些选项设为默认的，可以在dalton脚本中修改74行开始的位置（此位置是对于Dalton 2020.1的而言）的一些参数。比如想把nobackup、noarch、ow作为默认启用的选项，就把opt_nobackup、opt_noarch都设为1，把opto设为2。稍微读一下此脚本就知道为什么这么设了。

如果MPI并行版和MKL并行版在平时研究中都用得着，MKL并行版放在了/sob/dalton目录，MPI并行版放在了/sob/dalton_MPI目录，为了能方便地同时使用，建议在.bashrc里既不设DALTON_LAUNCHER也不设OMP_NUM_THREADS，但是加一句alias daltonmpi='/sob/dalton_MPI/dalton'。此时就可以这样运行了：  
96核跑MKL并行版：dalton -omp 96 love live  
96核跑MPI并行版：daltonmpi -N 96 love live

### 2.3 输入文件简介与简单例子

首先注意几点：  
Dalton对基组的大小写敏感，比如aug-cc-pVDZ不能写为aug-cc-pvdz。  
Dalton主要用来计算闭壳层的基态，因此多数情况下并不需要给出自旋多重度，默认就是1。  
Dalton默认对所有基组都用球谐函数。  
Dalton默认是不冻核的。  
.dal里可以用#或!进行注释。

下面是一个CCSD(T)单点计算的dal文件例子：  
**DALTON INPUT     //**是主选项  
.RUN WAVE FUNCTIONS   //.后面代表设定。RUN后面设的是要干什么、调用什么模块  
**WAVE FUNCTIONS  
.CC   //耦合簇波函数  
*CC INPUT   //对CC计算进行进一步设定  
.CC(T)  
**END OF INPUT

下面是一个B3LYP下优化任务的dal文件例子。注意Dalton默认的B3LYP的定义与Gaussian不同，B3LYPg代表使用与Gaussian相同的定义：  
**DALTON INPUT  
.OPTIMIZE  
**WAVE FUNCTIONS  
.DFT  
 B3LYPg  
**END OF INPUT

下面是一个甲酰胺的mol文件例子：  
ATOMBASIS  //代表每个原子分别设定基组。如果这里写BASIS，然后下面再加一行6-31G*，则说明所有原子都用这个基组，每类原子里的Basis=6-31G*就不要再写了  
test molecule  //标题行，内容任意，必须有  
Generated by Multiwfn  //同上  
Atomtypes=4 Angstrom Nosymmetry charge=0  //关键词顺序随意，大小写敏感。可以只写前三个字符。当前设置说明体系里包含四类原子，坐标单位是埃，不用对称性，是电中性  
Charge=1.0 Atoms=3 Basis=6-31G*  //此类原子的实际核电荷数、原子数、基组  
H1   -0.45438149    1.43099761    0.00000000   //原子名可随意定义，程序不检查  
H2   -0.64184099   -1.52402451    0.00000000  
H3   -1.92375124   -0.35013241    0.00000000  
Charge=6.0 Atoms=1 Basis=6-31G*  
C1    0.00000000    0.41905994    0.00000000  
Charge=7.0 Atoms=1 Basis=6-31G*  
N1   -0.94010085   -0.56081903    0.00000000  
Charge=8.0 Atoms=1 Basis=6-31G*  
O1    1.20008496    0.23181661    0.00000000

上面设的Atomtypes指的不是元素种类，而是原子类型。比如O3，是C2v点群，虽然只有一种元素，但是有两种非等价的氧，故Atomtypes=2。如果懒得考虑这个，直接用Nosymmetry，这样Atomtypes就直接对应元素数了。

基组库目录(dalton\basis)下的基组都可以用basis或atombasis来使用，基组名就是基组文件名字。赝势都在basis/ecp_data里，可以通过ECP=xxx来使用。比如可以Basis=stuttgart_rlc_ecp ECP=stuttgart_rlc_ecp，因为无论是这个基组名还是这个赝势名都在basis和basis/ecp_data里有同名文件。

由于Dalton的.mol文件格式定义得很麻烦，得一类一类定义，因此不好从结构文件或其它量化程序的输入/输出文件里直接粘过去，因此最好的做法就是用Multiwfn产生Dalton的输入文件。启动Multiwfn后，载入任意一个含有结构信息的Multiwfn支持的格式，比如gjf、mwfn、wfn、fch、molden、pdb、xyz、mol等，然后依次输入  
100  //主功能100  
2  //导出文件  
19  //导出Dalton的输入文件  
idol.dal  //导出的.dal的文件名。不需要产生它的话这一步直接按回车  
master.mol  //导出的.mol文件名  
此时当前下就有了idol.dal和master.mol。这个.dal文件对应B3LYP单点计算。.mol文件包含此体系结构，并且对应使用6-31G*基组、不利用对称性的情况。之后大家根据实际计算要求对这两个文件进行修改即可，比手动从头写它们方便多了。

如果你载入到Multiwfn的文件包含了基函数信息，如.fch、.molden、.mwfn等，Multiwfn还可以把波函数写入到.dal文件里作为Dalton计算的初猜，详见《利用Multiwfn令Dalton计算时使用其它程序产生的轨道作为初猜》（<http://sobereva.com/740>）。

如果Multiwfn产生Dalton输入文件的功能给你的研究带来了便利，**建议在你的文章中引用Multiwfn启动时提示的Multiwfn程序的原文**。
