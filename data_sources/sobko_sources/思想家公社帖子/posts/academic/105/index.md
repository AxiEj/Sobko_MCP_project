---
post_id: 105
title: GAMESS-US 2011-Aug-11版编译方法
url: http://sobereva.com/105
date: '2015-06-07T23:51:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 量子化学
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 这是GAMESS-US的编译方法，属于典型软件安装教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**注**：此文已经完全过时，新版的编译方法见《GAMESS-US的编译方法》（<http://sobereva.com/193>）

**GAMESS-US 2011-Aug-11版编译方法**Compilation method of GAMESS-US version 2011-Aug-11  
文/Sobereva @[北京科音](http://www.keinsci.com/)  
First release: 2011-Oct-9

两年前笔者已经写过了GAMESS-US的2009 R3版编译方法，见<http://sobereva.com/50>。由于在目前最新的2011-Aug-11版中编译过程发生了一些变化，所以重新写一遍编译方法。但这次就不进行那么多解释了，这样文章也显得更清晰整洁。编译过程的解释可以参考2009 R3版编译方法的帖子。官方对编译过程的说明可以参考gamess/misc/readme.unix文档。

GAMESS-US版本：2011-Aug-11  
编译器和数学库：ifort 12.1.0+MKL。均安装在默认路径。  
系统：RHEL6-U1 64bit（Vmware7.1.2虚拟机）  
用户：root  
计算姬：Toshiba X500 (i7-2630QM)。程序将安装在/sob/gamess下。

1. 生成配置文件  
将压缩包解压至/sob/gamess，并进入此目录  
执行./config，依次输入（[enter]代表直接敲回车跳过提示）  
[enter]  
linux64  
[enter]   //即使用默认路径  
ifort  
12  
[enter]  
[enter]  
mkl  
/opt/intel/mkl  
skip  
[enter]  
[enter]  
sockets  
此时配置文件install.info在当前目录下生成了

2. 编译ddi  
cd ddi  
./compddi  
把得到的ddikick.x移动到上一级目录，即/sob/gamess下。

3. 编译代码并连接为可执行文件  
cd ..  
./compall  
经过近20min编译，objects目录下生成了255个.o文件

./lked gamess 00

4. 配置运行环境  
建立/sob/gamess/scr文件夹

对rungms文件作如下修改：  
setenv AUXDATA ~mike/gamess/auxdata改为setenv AUXDATA /sob/gamess/auxdata  
~$USER全都替换为/sob/gamess  
所有/home/mike替换为/sob  
if ($os == Linux)   set GMSPATH=/cu/mike/gamess改为if ($os == Linux)   set GMSPATH=/sob/gamess  
set SCR=/scr/$USER改为set SCR=/sob/gamess/scr  
如果想要单机多核计算，在约556行处的switch (`hostname`)这行下面插入以下内容。其中xxx是本机名，即运行hostname命令所显示的内容。  
         case xxx:  
            set NNODES=1  
            set HOSTLIST=(`hostname`:cpus=$NCPUS)  
            breaksw

5. 测试  
把runall文件的chdir /u1/mike/gamess改为chdir /sob/gamess

./runall进行测试。经过10分钟左右，全部44个任务测试完成。  
修改tools/checktst目录下checktst文件的set GMSPATH=后面为/sob/gamess，然后运行此文件，出现提示时输入/sob/gamess。笔者机子上44个测试全部通过。

同时也测试一下单机多核方式能否正常运行，运行比如./rungms exam01.inp 00 4，其中4代表用4核。笔者这里直接测试通过。
