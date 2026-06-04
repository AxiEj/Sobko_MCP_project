---
post_id: 50
title: GAMESS-US 2009 R3版编译方法
url: http://sobereva.com/50
date: '2015-06-05T01:46:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 主要是 GAMESS-US 的编译方法，属于具体软件的安装编译教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**注**：此文已经完全过时，新版的编译方法见《GAMESS-US的编译方法》（<http://sobereva.com/193>）

**GAMESS-US 2009 R3版编译方法**Compilation method of GAMESS-US 2009 R3  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)     
First release: 2009-Oct-7  Last updated: 2010-Jan-20

  
  
操作系统：Fedora7-64bit，已装gcc 4.1.2（在系统安装过程中选择了安装软件开发这一类就会装上），系统中有csh（Fedora8及以后需手动安装csh），root用户，使用bash shell，GAMESS(US)版本为January 12, 2009 R3，CPU为Intel Core2 Q6600，2G内存。  
  
对于Intel CPU，相较使用GNU的编译器和其它数学库，使用ifort编译器结合MKL数学库可以使代码执行速度大大提升，所以这里用ifort+MKL方案。GAMESS也有少部分C语言的代码，主要是用在DDI(Distributed Data Interface)部分，而非计算密集的部分，对性能影响不大，故使用gcc足矣。  
  
去intel网站下载intel fortran compiler for linux（以下简称ifort），本文用的是10.1.015版，安装到默认文件夹opt/intel/fce/10.1.015。  
（如果安装时提示缺少libstdc++.so.5，将libstdc++-5.0.7-86.x86_64.rpm在图形界面下双击安装进系统）  
下载Intel Math Kernel Library（以下简称MKL），本文用的是10.0.4.023版，安装到默认文件夹/opt/intel/mkl/10.0.4.023。  
在/root/.bashrc中添加：  
source /opt/intel/fce/10.1.015/bin/ifortvars.sh  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/mkl/10.0.4.023/lib/em64t  
输入bash，使环境变量生效。  
  
在http://www.msg.chem.iastate.edu/GAMESS/download/register/页面中提交你要下载的文件的申请（即用于64 bit IA64/x86_64 under Linux with Intel compilers的GAMESS源码），提交后过一两天电子邮箱内会收到确认信，里面提供了下载页面和下载所需的用户名和密码。  
将下载到的gamess-current.tar.gz解压至/sob/gamess，最终可执行文件也将编译到这里。  
建议阅读一下misc文件夹下的readme.unix，介绍了编译方法和参数意义。  
  
修改gamess目录下的compall、comp、lked、runall文件的开头部分，TARGET=后面都改为linux-ia64（runall没有TARGET字段，此处不用改），chdir后面都改为/sob/gamess。rungms里面的SCR=后面改为/sob/gamess/scr，setenv ERICFMT和setenv MCPPATH后面的~mike都改为/sob，if ($os == Linux)一行的GMSPATH=后面改为/sob/gamess，~$USER全都替换为/sob/gamess。（注意gamess中的linux-ia64不仅仅指Itanium的IA64架构，也包括EM64T架构。此时默认，也只能使用ifort编译器和MKL数学库。）  
  
把/sob/gamess/tools/actvte.code复制为actvte.f，并把actvte.f中所有*UNX用四个空格替换。然后编译此文件ifort -o actvte.x -Vaxlib actvte.f。由于GAMESS对于不同架构的计算机都使用同一套源代码，在下面comp脚本编译源文件过程中，这个程序用来自动将源代码（.SRC文件）中的一些内容替换以迎合当前环境，成为.FOR文件，称为“激活”过程，FOR文件被编译为.o后会被自动删掉。  
  
在/sob/gamess目录下运行./compall，它会自动调用comp脚本来编译各个源文件成为.o并放到object目录中。编译约半个小时，最终会得到230多个.o文件。  
  
现在编译GAMESS的分布式数据接口(DDI)消息传递库，无论是否打算并行计算都必须编译，否则下面lked步骤通不过。假设现在主机名是f71（用hostname命令可以看到当前主机名），就在/etc/hosts里面填上一行当前主机的IP地址和主机名，例如192.168.153.3 f71，重启。进入/sob/gamess/ddi目录，修改compddi文件开头的set TARGET =后面为linux-ia64，把set MAXCPUS和set MAXNODES后面设成你的实际情况，前者代表每个节点中最多包含几个核心（每个节点内可以以SMP方式并行的核心数目），后者代表最多有几个节点，它们设的都可以比实际情况多。本文都设成2。在/sob/gamess/ddi/src/std_system.c里面的struct hostent *hp;后面加入一行name="f71";（f71是主机名，之所以要加入这么一行是因为GAMESS的bug，会将主机名强行认作为localhost而不是实际主机名，导致运行时提示TCP error之类错误。如果不添加也没有出现这个错误则无需添加这行）。最后运行./compddi >& compddi.log，很快就编译完成了。把得到的ddikick.x移动到上一级目录即/sob/gamess下。  
  
在/sob/gamess目录下运行./lked gamess 03 >& lked.log，目的是将编译好的.o文件、DDI库文件和数学库连接到一起成为可执行文件，很快就得到了最终可执行文件gamess.03.x。编译参数中的03是随意取的，也可以是00、01等等，目的只是区分不同GAMESS版本可执行程序，作为一个标识。（如果只运行./lked gamess >& lked.log，则默认生成gamess.00.x）  
  
因为可执行文件名用了03标识，故将runall里面的set VERNO=后面默认的00改为03。  
建立/sob/gamess/scr文件夹作为GAMESS运行的临时文件夹。  
在/sob/gamess目录下运行./runall来对编译好的GAMESS程序进行测试，自动运行44个测试文件，将在当前目录下得到一批exam??.log文件。修改tools/checktst目录下checktst文件的set GMSPATH=为/sob/gamess，然后运行此文件，出现提示时输入/sob/gamess，会将所得log文件的结果与标准结果相对比，检查任务是否已正常结束，以及计算误差是否超过阈值。对于failed的任务，检查相应的log文件。除掉毛病后，把scr目录下文件都删掉，再运行runall和checktst看是否都已通过。  
  
笔者在测试中exam36和43通不过，打开相应log文件发现如下提示：Check system limits on the size of SysV shared memory segments。这是因为linux默认的单个共享内存段的最大值太小造成的，使用/sbin/sysctl -a|grep shmmax命令察看默认只设了32MB，而这两个任务需要约48MB。遂修改/etc/sysctl.conf，在里面加入一行kernel.shmmax = 1610612736，这就将上限提高到了1.5G，之后重启（也可以运行/sbin/sysctl -w kernel.shmmax=1610612736来立刻生效而无需重启）。重新runall并运行checktst，发现任务均已Passed。  
  
如果想用SMP方式并行双核运行，在rungms的if ($NCPUS > 2) set NCPUS=2那行的上面插入一行case f71:（如果是四核机子，就在if ($NCPUS > 4) set NCPUS=4前面插入这行）。之后比如运行./rungms exam01.inp 03 2 &> a.txt就说明用单节点双核调用gamess.03.x执行exam01.inp任务。若只输入./rungms exam01.inp则说明用单核心调用gamess.00.x执行exam01.inp任务。  
  
最后编译图形应用程序，进入graphics目录，将complink文件里面的chdir后面改为/sob/gamess/graphics，set TARGET=后面改为linux-pc，if ($TARGET == linux-pc)   set FORT=后面改为'ifort -O2'，之后运行./complink来编译。  
  
  
附注：  
完整地编译成功后，如果修改了src目录下某个源代码文件，比如是int2a.src，想重新编译可执行文件使改动生效，只需要在/sob/gamess目录下运行./comp int2a，然后删掉原GAMESS可执行文件，重新lked即可。不必用compall把所有文件再编译一遍。  
  
在32bit系统+任意CPU（不限intel）+gfortran下的编译方法：  
步骤与上述一致，只要把上文相应部分替换为下述即可。  
数学库不用额外安装，会自动编译并连接GAMESS自带的blas库，但缺点是慢。  
上述提到的改为linux-ia64的地方都改为linux32  
ifort -o actvte.x -Vaxlib actvte.f改为gfortran -o actvte.x actvte.f  
lked的302行，即if ($TARGET == linux32) then下面，把set FORTRAN=后面改为gfortran。  
comp的1138行，把set FORTRAN=后面改为gfortran。  
ddi目录下compddi的540行，即if ($TARGET == linux32) then下面，把set FORTRAN=后面改为gfortran。  
graphics目录下complink的if ($TARGET == linux-pc)   set FORT=后面改为'gfortran -O2'  
  
在64bit系统+任意CPU（不限intel）+gfortran下的编译方法  
与上面32bit下安装一致，把其中linux32都改成linux64即可。lked、comp和compddi里对linux64模式默认就是用gfortran，不必再手动改了。但需要把lked中的#  Using blas.o will give a successful link, to slow matrix multiply routines.这一行下面的exit 4删掉，否则若没装MKL或Atlas或ACML库会报错，而这样改后就会用自带的blas库代替。
