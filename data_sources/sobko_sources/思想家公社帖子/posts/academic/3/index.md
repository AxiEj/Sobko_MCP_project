---
post_id: 3
title: Amber10安装方法
url: http://sobereva.com/3
date: '2015-06-01T17:30:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- 综述/教程/投稿经验
- 结构与文件格式
academic_relevant: true
classification_reason: 标题就是Amber10安装方法，属于典型AMBER软件安装教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**Amber10安装方法**Installation method of Amber 10  
文/Sobereva @[北京科音](http://www.keinsci.com/)    2009-Oct-1

这里使用虚拟机中新装的RHEL5U1-64bit系统作为例子。

编译环境:  
主机：Q6600，2G，XP-SP2。虚拟机：vmware6.0.1，RHEL5U1-64bit，双核，512MB，10GB，默认分区，bash，root，intel-MKL-10.0.4.023，intel fortran compiler 10.1.015，gcc 4.1.2，mpich2-1.0.7/lam-7.1.4。工作目录/sob。  
  
到intel网站免费下载linux的MKL和ifc(皆Intel 64版)，在邮箱里得到相应安装所需的.lic文件。  
  
默认设置安装intel fortran compiler到默认文件夹(opt/intel/fce/10.1.015)  
在/root/.bashrc中添加：  
source /opt/intel/fce/10.1.015/bin/ifortvars.sh (会加入一些信息到/etc/profile)  
export FC=/opt/intel/fce/10.1.015/bin/ifort  
(如果安装时提示缺少libstdc++.so.5，下载这个rpm文件，并安装进系统： ftp://fr2.rpmfind.net/linux/opensuse/distribution/10.3/repo/oss/suse/x86_64/compat-libstdc++-5.0.7-86.x86_64.rpm   此文件在本贴附件中)  
  
默认设置安装MKL到默认文件夹(/opt/intel/mkl/10.0.4.023)  
在/root/.bashrc中添加:  
export MKL_HOME=/opt/intel/mkl/10.0.4.023  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/mkl/10.0.4.023/lib/em64t  
  
输入bash使环境变量生效  
  

并行环境可以用mpich2或lammpi或intel mpi

===========用mpich2===============

到http://www.mcs.anl.gov/research/projects/mpich2/ 下载mpich2-1.0.7.tar.gz  
mpich2-1.0.7.tar.gz解压到/sob/mpich2-1.0.7，进入此目录，运行：  
./configure  
make  
make install          (此时编译好的mpich2的文件已经被安装到默认路径/usr/local的各个子目录下)  
touch /etc/mpd.conf  
chmod 700 /etc/mpd.conf  
  
将下面加入/etc/mpd.conf:  
secretword=<secretword>            (比如secretword=ltwd)  
(输入mpd&，然后mpdtrace是否能显示主机名，如果能出现代表安装成功。  
如果提示诸如gethostbyname_ex failed for xxx，xxx是主机名，则修改/etc/hosts，加入<ip号> <主机名称> <主机别名>，比如192.168.2.3 f7 f7)  
  

===========用lam-mpi===============

到http://www.lam-mpi.org/7.1/download.php下载lam-7.1.4  
解压到/sob/lam-7.1.4，进入此目录，运行：  
./configure  
make  

make install

===========用intel mpi=============

到intel官方网站下载intel mpi for linux的30天评估版，从填写的电子邮箱中得到.lic  
解压压缩包，并把.lic放进解压后的目录里，运行./install.sh用默认设置和目录安装。  
  
也可以从verycd上下载Linux版Intel Cluster Toolkit Compiler V3.1.1，内含ifort、icc、MKL、mpi、debugger等，没有时间限制。挂载到linux之后先复制到硬盘某目录，注意目录不能有空格，进入这个目录后，将Crack子目录下的.lic复制到当前目录，并运行chmod 777 -R *  之后执行./install.sh按说明安装。  
  
安装好后将此加入/root/.bashrc： export PATH=$PATH:/opt/intel/impi/3.1/bin  

---

  
在/root/.bashrc中添加:  
export MPI_HOME=/usr/local    (如果是intel mpi，目录写/opt/intel/impi/3.1)  
export AMBERHOME=/sob/amber10  
export PATH=$PATH:/sob/amber10/bin  
  
输入bash使环境变量生效  
  
将AmberTools-1.2.tar.bz2解压至/sob/amber10  
将amber10.tar.bz2也解压至/sob/amber10，使两个压缩包的文件在一个目录下  
下载最新的amber10的bugfix，http://amber.scripps.edu/bugfixes/10.0/bugfix.all，复制到/sob/amber10目录中，改名为bugfixab.all  
下载最新的AmberTools1.2的bugfix，http://amber.scripps.edu/bugfixes/AmberTools/1.2/bugfix.all，复制到/sob/amber10目录中，改名为bugfixat.all  
/sob/amber10> chmod 777 -R *  
/sob/amber10> patch -p0 -N -r patch-rejects < bugfixab.all  
/sob/amber10> patch -p0 -N -r patch-rejects < bugfixat.all  
/sob/amber10/src> ./configure_at gcc  
更改config.h中FC=gfortran为FC=ifort，FFLAG中的-O1改为-O3，并加上-axT，删除-fno-automatic。  
/sob/amber10/src> make -f Makefile_at  
/sob/amber10/src> ./configure_amber ifort  
更改config_amber.h中FOPTFLAGS中的-axWP为-axT  
/sob/amber10/src> make serial  (使用intel mpi可能出现和netcdf相关的错误，make clean然后重新make serial就能解决)  
/sob/amber10/src> make clean  
/sob/amber10/src> ./configure_amber -mpich2 ifort  (若用lammpi，把-mpich2改为-lam。若用intel mpi，把-mpich2改为-intelmpi)  
更改config_amber.h中FOPTFLAGS中的-axWP为-axT  
/sob/amber10/src> make parallel   
  
***安装pmemd***  
/sob/amber10/src/pmemd> ./configure linux_em64t ifort mpich2 bintraj (也支持其它并行环境，见./configure --help)  
更改config.h中F90_OPT_HI中的-xP为-axT  
/sob/amber10/src/pmemd> make install  
***************  
  
安装完毕，进行测试  
  
测试串行版本：  
/sob/amber10/test>make test  
/sob/amber10/test>make test.serial.QMMM  
我这里bintraj和divcon是failure，其它都PASS，应该是程序自身的bug。  
  
测试并行版本:  
如果用lam-mpi，把/root/.bashrc中设定的环境变量都复制到某个用户的主目录下的.bashrc，然后登陆到那个用户再执行下列命令，因为root用户不能启动lamboot。  
/sob/amber10/test>mpd&               (若用lam-mpi，输入lamboot。若用intel mpi，输入mpdboot)  
/sob/amber10/test>export DO_PARALLEL='mpirun -np 2'      (有些项目需要-np 4并行，-np 2时自动跳过)  
/sob/amber10/test>make test.parallel  全部PASS  
/sob/amber10/test>make test.parallel.QMMM  全部PASS  
为节省空间，此后可删掉test目录。src目录下除了mm_pbsa目录以外都可以删掉节省空间，因为mm_mmpbsa.pl在执行时还需要那个文件夹里的文件。  
  
  
  
此外，还有一种更简单的安装方法，直接调用amber10里面自带的lam-7.1.3的配置脚本。  
MKL、ifort安装过程不变。然后略过装lam-7.1.4那步，也不用设MPI_HOME。其它过程都不变，一直到make serial并且make clean之后，输入  
./configure_amber -lamsource ifort  
更改config_amber.h中FOPTFLAGS中的-axWP为-axT  
./configure_lam   (这步自动将自带的lam-7.1.3装上)  
make parallel  
就装好了，测试步骤同上  
  
  
  
PS:  
Intel的CPU为提高性能一定要用ifort。C语言编的部分运算量不大，除非要用ambertools中NAB做长时间模拟，否则一般不需要用icc，也无须专门设置优化参数。  
用不用MKL对性能影响约1/6。  
ambertools基本上只有自带的MOPAC7是fortran语言编的，用不到半经验方法的话用gfortran对性能不会有什么损失。  
系统不要用太新或者太旧的版本，自带库文件版本和编译器版本有异等因素都可能造成编译失败，RHEL5U1、Fedora7是我推荐的。  
-axT是优化选项，针对Core2架构，对不同类型intel的CPU应当用不同优化选项，详见/opt/intel/fce(or cce)/10.1.015/doc/Doc_index.htm，进入Document那项，选Optimizing Applications-Using Compiler Optimizations
