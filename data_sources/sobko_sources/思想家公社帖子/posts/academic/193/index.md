---
post_id: 193
title: GAMESS-US的编译方法
url: http://sobereva.com/193
date: '2015-06-08T00:02:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 综述/教程/投稿经验
- 量子化学
academic_relevant: true
classification_reason: 内容是 GAMESS-US 的编译方法，属于具体软件的安装/编译教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**GAMESS-US的编译方法**  
Compilation method of GAMESS-US

文/Sobereva@[北京科音](http://www.keinsci.com)  
First release: 2013-Jul-3   Last update: 2024-Sep-26

本文介绍GAMESS-US程序的编译方法，版本是2024-R2 Patch 1，对于未来的版本可能适用也可能不适用，请随机应变。以下是笔者的编译环境。  
CPU：双路AMD EPYC 7R32。此机子的介绍见<http://sobereva.com/653>  
操作系统：RockyLinux 9.0  
用户：root  
编译器：Intel oneAPI HPC 2024.0提供的Intel Fortran编译器和Intel oneAPI base提供的MKL数学库。Intel oneAPI可以在Intel网站免费下载，Google一搜就有。先装base再装HPC  
程序将安装在/sob/gamess下。

一定要用Intel MKL数学库，否则如果只用程序自带的子程序，根据编译脚本里的说法，MP2会慢两倍，CCSD(T)会慢5倍。即便你用的是AMD的CPU，也可以用Intel的Fortran编译器和MKL数学库。

GAMESS-US的用法在本文就不说了，在北京科音高级量子化学培训班（<http://www.keinsci.com/workshop/KAQC_content.html>）中专门有一节系统讲GAMESS-US的使用，欢迎参加。

## 1 获取GAMESS-US

进入<https://www.msg.chem.iastate.edu/GAMESS/download/register/>，输入E-mail地址，选择要下载的类型，选上64 bit x86_64 under Linux using Intel OneAPI compilers，点提交即可。邮箱不需要非得是edu邮箱，比如我用的aliyun邮箱申请，隔了一个工作日就收到下载地址和下载密码的邮件了。

下载压缩包后放到/sob目录下，用tar -xf [压缩包名]解压GAMESS-US压缩包，得到/sob/gamess目录。

## 2 生成配置文件

进入/sob/gamess目录，运行./config命令执行配置脚本，依次输入以下内容（[enter]代表直接敲回车，//后面的是注释）  
[enter]   //跳过提示  
linux64   //操作系统类型  
[enter]   //使用默认路径/sob/gamess  
[enter]   //使用默认路径/sob/gamess  
[enter]   //使用默认版本号00  
[enter]   //不对特定超算环境编译  
oneapi-ifort   //编译器  
[enter]   //接下来设置数学库  
mkl   //然后会提示找到MKL库在opt/intel/oneapi/mkl/2024.0  
/opt/intel/oneapi/mkl/latest   //当前MKL数学库的位置（我发现输入opt/intel/oneapi/mkl/2024.0的话不认，是脚本的bug）  
[enter]   //接下来设置GAMESS DDI  
sockets  
[enter]   //接下来开始对GAMESS的编译选项进行设置。如果下面的所有选项都用no的话，直接按住回车键都用默认的no就行了  
no   //不编译可以令GAMESS-US支持更多DFT泛函的libxc界面（否则还需要联网下载）  
no   //不建立MDI界面（用于和其它代码交互的界面）  
no   //不编译MSU CCT3、CCSD3A、ACP、DEA/DIP-EOMCC代码，否则会花费很多时间，而且一般用不着  
no   //不编译用于GPU加速的LIBCCHEM 2.0  
no   //不编译VeraChem's VM2库  
no   //不建立TINKER插件  
no   //不建立VB2000插件  
no   //不建立XMVB插件  
no   //不建立NEO（考虑核量子效应的方法）插件  
no   //不建立NBO插件  
no   //不建立RISM-SCF-cSED插件

此时配置文件install.info在当前目录下生成了。之后运行比如make -j 64代表用64核并行编译，我的机子上45秒就编译完了，会看到/sob/gamess目录下已出现GAMESS-US可执行文件gamess.00.x，其中00是版本号，和程序的版本号是两码事。

## 3 配置运行环境

建立/sob/gamess/scr文件夹作为临时文件目录（当然也可以选别的地方）。对/sob/gamess/rungms运行脚本文件作如下修改：

把set TARGET=sockets下面的三行改为  
set SCR=/sob/gamess/scr  
set USERSCR=/sob/gamess/scr  
set GMSPATH=/sob/gamess

把这里的NCPUS后面的数值改成默认用的CPU核心数：if (null$NCPUS == null) set NCPUS=1

注：可以在rungms文件一开头的#!/bin/csh部分下方加上rm -f /sob/gamess/scr/*，使得每次调用rungms时都自动清空临时目录，省得临时文件目录下的文件逐渐越积越多。

在用户主目录下的.bashrc文件中加入一行  
export PATH=$PATH:/sob/gamess  
这使得任何目录下都可以用rungms命令运行GAMESS-US。

重新进入终端后就可以用比如rungms test.inp |tee test.out来调用GAMESS-US对当前目录下的输入文件test.inp进行计算了，输出的信息既显示在屏幕上也输出到test.out里，默认的并行运算核数就是上面提到的NCPUS后面设的。如果想指定用比如64个核心并行运行，就用rungms test.inp 00 64。这里00是可执行文件的版本号。

## 4 全面测试

把/sob/gamess/runall文件里第一处si.msg.chem.iastate.edu改为本机名。把./rungms exam$NUM $VERNO 1里面的1改为测试时的并行核数。

进入/sob/gamess/目录，运行./runall 00进行测试，然后直接按回车。共40多个测试任务将依次执行，产生的40多个log文件会不断出现在/sob/gamess下。

笔者用双路7R32机子96核并行花了几分钟就跑完了测试脚本。将所有产生的log文件拷贝到/sob/gamess/tests/standard目录下，进入此目录后运行./checktst，此脚本会将计算结果与标准结果进行对照。只要大部分任务都通过测试就行，少部分没通过测试的大概率是测试文件和当前版本GAMESS-US特征不兼容，以及有的任务只能串行运行所致。

如果之前已经用runall做过了测试，那么应当先把/sob/gamess/scr目录下清空。

-----------以下是本文的老版本，如果大家需要编译老版本GAMESS-US可以参考-----------

不同版本的GAMESS-US的编译方法总有一些不同。本文介绍GAMESS-US 2013-May和2014-Dec版编译方法。2016-Aug版编译方法和本文一样，只不过下面输入skip那一步改为输入proceed就行了。  
GAMESS-US 2011-Aug-11版编译方法见<http://sobereva.com/105>  
GAMESS-US 2009 R3版编译方法见<http://sobereva.com/50>

2021-Apr-6注：本文的编译方法对于CentOS 8结合Intel OneAPI 2021版编译GAMESS-US 2020(R2)版经测试依然使用。但是执行./config生成配置文件的对话有所变化，需根据提示随机应变。让你输入mkl版本号的时候应当输入12而不要输入当前实际版本号，否则在执行./lked gamess 00的时候无法连接MKL。此外，第4节在switch (`hostname`)后面插入额外内容的那一步不再需要。

编译环境：  
编译器和数学库：ifort 12.1.0+MKL。均安装在默认路径。编译器的获取方法可参考《Amber11+AmberTools1.5及CUDA版安装方法》（<http://sobereva.com/103>）  
系统：RHEL6-U1 64bit（Vmware7.1.2虚拟机）  
用户：root  
计算姬：Toshiba X500 (i7-2630QM)。程序将安装在/sob/gamess下。

1. 生成配置文件  
将压缩包解压至/sob/gamess，并进入此目录  
执行./config，依次输入（[enter]代表直接敲回车跳过提示）  
[enter]  
linux64  
[enter]   //使用默认路径  
[enter]   //使用默认路径  
[enter]   //使用默认版本号00  
ifort  
12  
[enter]   //忽略ifort 12.0有bug的提示  
[enter]  
mkl  
/opt/intel/mkl  
skip  
[enter]  
[enter]  
sockets  
no  //不尝试LIBCCHEM，这是用来通过nVidia的GPU加速HF和MP2任务用的，还很不成熟。  
此时配置文件install.info在当前目录下生成了

2. 编译ddi  
cd ddi  
./compddi  
把得到的ddikick.x移动到上一级目录，即/sob/gamess下。

注：如果你的CPU核心超过32个，应当将compddi里第一次的set MAXCPUS=后面的值改为当前的CPU核心数之后再执行compddi。

3. 编译代码并连接为可执行文件  
cd ..  
./compall  
经过十几分钟的编译，objects目录下生成了近300个文件。并且/sob/gamess下产生了gamess.00.x可执行文件。（如果没产生，手动执行./lked gamess 00）

4. 配置运行环境  
建立/sob/gamess/scr文件夹  
对/sob/gamess/rungms文件作如下修改：  
把set TARGET=sockets下面的三行改为  
set SCR=/sob/gamess/scr  
set USERSCR=/sob/gamess/scr  
set GMSPATH=/sob/gamess

把这里的NCPUS后面的数值改成想默认用的CPU核心数：if (null$NCPUS == null) set NCPUS=1

为了能单机多核计算，在switch (`hostname`)这行下面插入以下内容。其中xxx是本机名，即运行hostname命令所显示的内容。  
         case xxx:  
            set NNODES=1  
            set HOSTLIST=(`hostname`:cpus=$NCPUS)  
            breaksw

PS：建议在rungms文件一开头的#!/bin/csh部分下方加上rm -f /sob/gamess/scr/*，使得每次调用rungms时都自动清空临时目录。

之后就可以用比如./rungms test.inp来运行了，并行运算用的核数就是上面NCPUS设的。如果想指定用比如3个核心并行运行，则用./rungms test.inp 00 3。

5. 测试  
把/sob/gamess/runall文件里第一处si.msg.chem.iastate.edu改为本机名。把./rungms exam$NUM $VERNO 1里面的1改为并行的核数。

运行./runall 00进行测试，一开始按回车。共47个测试任务将依次执行，产生的log文件产生在/sob/gamess下。  
将所有产生的log文件拷贝到/sob/gamess/tests/standard目录下，进入此目录后运行./checktst，此脚本会将计算结果与标准结果进行对照。笔者机子上47个测试任务的结果全部检验通过。

注意如果之前已经用runall做过了测试，那么应当先把/sob/gamess/scr目录下清空。

附：  
如果想对某个源程序文件进行修改，使之生效，而不想重新编译整个程序，可以这样：比如自己修改了int2a.src，则运行./comp int2a，然后./lked gamess 00。
