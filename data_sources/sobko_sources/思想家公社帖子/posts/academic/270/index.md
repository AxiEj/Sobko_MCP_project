---
post_id: 270
title: NWChem的编译方法
url: http://sobereva.com/270
date: '2015-06-08T00:15:00+08:00'
source_categories:
- 量子化学
primary_topic: NWChem
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题就是NWChem编译方法，明显是软件安装编译教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**NWChem的编译方法**Compilation method of NWChem  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)  
First release：2014-Dec-22   Last update：2024-Sep-20

本文介绍编译NWChem 7.2.3的最简单的方法。笔者的操作系统是CentOS 9 64bit，用户是root。编译器用的gfortran。官方也有编译说明，见<https://nwchemgit.github.io/Compiling-NWChem.html>，但里面的内容比较混乱。

编译OpenMPI库：  
去<http://www.open-mpi.org>下载OpenMPI 4.1.1，解压到/sob目录下，进入其目录，运行  
./configure prefix=/sob/openmpi411  
make all install -j  
此时OpenMPI的可执行文件、库文件、头文件等就被装到了/sob/openmpi411里面的对应目录下。然后可以把OpenMPI解压的目录删掉。

在~/.bashrc中加入  
export PATH=$PATH:/sob/openmpi411/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/openmpi411/lib  
保存后，输入bash命令使以上环境变量生效。

运行以下命令设置环境变量  
export NWCHEM_TOP=/sob/nwchem-7.2.3  
export NWCHEM_TARGET=LINUX64  
export NWCHEM_MODULES=all  
export BLAS_SIZE=8  
export USE_MPI=y  
export USE_MPIF=y  
export USE_MPIF4=y  
export USE_INTERNALBLAS=y

注：NWChem为了节约编译时间，不常用的模块默认是不编译的。如果你想编译它们，使用以下命令定义额外的环境变量，需要哪些就执行哪些  
export MRCC_METHODS=y：编译多参考耦合簇代码  
export CCSDTQ=y：编译TCE模块的CCSDTQ和EOM-CCSDTQ代码

去NWChem发布页面<https://github.com/nwchemgit/nwchem>，点击Release链接，下载NWChem 7.2.3源代码包，然后解压到/sob/nwchem-7.2.3目录。之后运行  
cd /sob/nwchem-7.2.3/src  
make nwchem_config  
make -j  
这里用-j是为了并行编译，此时在笔者的2*7R32 96核机子下13分钟编译完毕了（设了MRCC_METHODS=y和CCSDTQ=y的情况），不用-j的话会编译得更慢。

编译完成后可执行文件生成在了/sob/nwchem-7.2.3/bin/LINUX64目录下。把下面的语句加入到~/.bashrc的末尾：  
export PATH=$PATH:/sob/nwchem-7.2.3/bin/LINUX64  
保存后，输入bash命令使此环境变量生效。

现在进行测试，做B3LYP/cc-pVTZ级别下优化N2分子的任务。将以下内容写进test.nw：  
title "Nitrogen cc-pvtz SCF geometry optimization"  
geometry  
n 0 0 0  
n 0 0 1.08  
end  
basis  
n library cc-pvtz  
end  
task scf optimize

然后运行nwchem test.nw查看输出是否正常。也运行mpirun -np 4 nwchem test.nw查看并行执行的输出是否正常，-np后面是调用的核数。

以下内容是NWChem老版本的情况，最后更新于2017-Apr-13

---

本文有两部分，第一部分是NWChem 6.6在Redhat Enterprise 6 Update 1 64bit下的安装，第二部分是NWChem 6.6在CentOS 7.2 64bit下的安装。后者过程更简单。编译器用的gfortran，用ifort也可以，但实测编译出的nwchem运行速度并不会更快，而且在编译耗时长得多，特别是CCSDTQ部分耗时极长，10个小时都编译不完。

编译条件：root, bash。将安装到/sob/nwchem-6.6。

本文的编译方法对nwchem 6.8经测试也完全适用，但是编译时必须能联网，因为会自动下载GlobalArray包。

  

**===== NWChem 6.6 + Redhat Enterprise 6 Update 1 64bit ======**

  
编译openmpi：  
去http://www.open-mpi.org下载OpenMPI 1.6.5（更新的版本大抵也可以，笔者没测试），解压到/sob目录下，进入其目录，运行  
./configure prefix=/sob/openmpi165  
make all install -j  
此时openmpi的可执行文件、库文件、头文件等就被装到了/sob/openmpi165里面的对应目录下。然后可以把OpenMPI解压的目录删掉。  
  
在~/.bashrc中加入  
export PATH=$PATH:/sob/openmpi165/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/openmpi165/lib  
输入bash使环境变量生效。  
  
运行以下命令设置环境变量  
export NWCHEM_TOP=/sob/nwchem-6.6  
export NWCHEM_TARGET=LINUX64  
export NWCHEM_MODULES=all  
export USE_MPI=y  
export USE_MPIF=y  
export USE_MPIF4=y  
export USE_INTERNALBLAS=y  
export MPI_LOC=/sob/openmpi165  
export MPI_LIB=/sob/openmpi165/lib  
export MPI_INCLUDE=/sob/openmpi165/include  
export LIBMPI="-lmpi_f90 -lmpi_f77 -lmpi -ldl -Wl,--export-dynamic -lnsl -lutil"  
  
NWChem为了节约编译时间，许多不常用的模块默认是不编译的。如果你想编译它们，使用以下命令定义额外的环境变量，需要哪些就执行哪些  
export MRCC_METHODS=y：编译多参考耦合簇代码  
export CCSDTQ=y：编译TCE模块的CCSDTQ和EOM-CCSDTQ代码  
export CCSDTLR=y：编译TCE模块的线性响应CCSDT、CCSDTQ代码，用于解析地算静态/动态极化率  
export IPCCSD=y：编译TCE模块的IP-EOM-CCSD代码用于算电离能  
export EACCSD=y：编译TCE模块的EA-EOM-CCSD代码用于算电子亲和能  
  
把nwchem6.6压缩包解压到/sob/nwchem-6.6，运行  
cd /sob/nwchem-6.6/src  
make nwchem_config   
make  
可执行文件生成在了/sob/nwchem-6.6/bin/LINUX64目录下。把下面的语句加入到~/.bashrc的末尾：  
export PATH=$PATH:/sob/nwchem-6.6/bin/LINUX64  
  
笔者在Intel i7-2630QM四核机子上花一刻钟编译完毕。如果把上述全部额外的功能都编译的话，耗时约一个小时。make时不需要写-j，而且写不写都会自动用双线程编译。  
  
现在测试。将以下内容写进test.nw：  
title "Nitrogen cc-pvtz SCF geometry optimization"  
geometry  
n 0 0 0  
n 0 0 1.08  
end  
basis  
n library cc-pvtz  
end  
task scf optimize  
  
然后运行nwchem test.nw查看输出是否正常。也运行mpirun -np 4 nwchem test.nw查看并行执行的输出是否正常。-np后面是调用的核数。  
  
  

**===== NWChem 6.6 + CentOS 7.2 64bit ======**

  
运行以下命令添加EPEL源和安装openMPI（机子需要能联外网）  
yum install epel-release  
yum install openmpi-devel openmpi  
  
将以下内容复制到命令行窗口设置环境变量  
export NWCHEM_TOP=/sob/nwchem-6.6  
export NWCHEM_TARGET=LINUX64  
export NWCHEM_MODULES=all  
export USE_MPI=y  
export USE_INTERNALBLAS=y  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/openmpi/lib/  
export PATH=$PATH:/usr/lib64/openmpi/bin/  
若要编译NWChem额外的功能，需要额外设定的环境变量和上文提到的一致。  
  
把nwchem6.6压缩包解压到/sob/nwchem-6.6，运行  
cd /sob/nwchem-6.6/src  
make nwchem_config   
make  
可执行文件生成在了/sob/nwchem-6.6/bin/LINUX64目录下。  
  
把下面的语句加入到~/.bashrc的末尾：  
export PATH=$PATH:/sob/nwchem-6.6/bin/LINUX64:/usr/lib64/openmpi/bin/  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/openmpi/lib/  
alias mpirun='mpirun --allow-run-as-root'  
  
重新进入终端后就可以用比如mpirun -np 4 nwchem test.nw运行了。
