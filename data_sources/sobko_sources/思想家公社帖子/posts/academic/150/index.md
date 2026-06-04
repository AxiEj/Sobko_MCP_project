---
post_id: 150
title: CFOUR程序的编译和使用方法简介
url: http://sobereva.com/150
date: '2015-06-07T23:57:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 量子化学
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 内容是CFOUR程序的编译和使用简介，软件教程属性很强。
topic_family: 软件
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**CFOUR程序的编译和使用方法简介**An introduction to compiling and using the CFOUR program

文/Sobereva @[北京科音](http://www.keinsci.com/)  2012-Jul-5

## 1 前言

CFOUR程序的全称是Coupled-Cluster techniques for Computational Chemistry。它是由ACESII-MAB程序改名而来，而ACESII-MAB程序是ACESII程序的一个分支，ACESII (Advanced Concepts in Electronic Structure)是从1990年代初开始开发的从头算程序，特别适合微扰和耦合簇的大规模并行计算。  
  
CFOUR继承了ACESII的大部分特征，是一个以做耦合簇见长的从头算程序，同时也支持HF、微扰、CI、QCI计算，但是不支持DFT。CFOUR的耦合簇最高能做到CCSDT，并且在这样的级别下还能支持二阶解析导数，相比之下，常用的Gaussian计算能量只支持到CCSD(T)，而其一阶解析导数最高只支持到CCSD。CFOUR做耦合簇的效率号称很高，CCSD(T)计算对于高对称性体系比Gaussian快2、3倍是有的，结果相符也很好，但是无对称性体系下却并不总比Gaussian09快。CFOUR对GIMIC, MRCC, DIRAC, NEWTON-X程序提供了接口，利用GIMIC可以分析感应电流密度，借助MRCC可以做无穷高阶耦合簇，DIRAC是著名的能支持四分量相对论计算的程序，NEWTON-X是一个BO近似下做分子动力学的程序。  
  
CFOUR可以执行多种任务计算多种属性，比如单点、几何优化，寻找过渡态，算激发态（EOM-CC），算红外、拉曼、NMR、g张量、静态/含频极化率和超极化率等。  
  
CFOUR是免费开源的程序，但是获得它相对麻烦点，必须在其主页http://www.cfour.de上下载授权表，签字后通过传真或者实体邮件发给开发者。为方便大家我也传在了这里：[/usr/uploads/file/20150609/20150609182404_74068.tar.gz](http://sobereva.com/usr/uploads/file/20150609/20150609182404_74068.tar.gz)。  
  
CFOUR比ACESII相对来说更user-friendly一些（尽管仍远称不上user-friendly），容易编译，而ACESII包括后来的ACESIII则都是面向开发者的程序，一般用户编译使用起来极其艰苦。不过CFOUR终究还是面向有一定量化经验的用户，不适合初学者，手册写得粗糙晦涩简陋，很多地方让人糊涂，且只有在线版手册，给新用户入门带来些麻烦，可以去http://www.qtp.ufl.edu/ACES/index.shtml下载一份ACESII的pdf版手册在必要时作为参考，写得更为详细。  
  
CFOUR在线手册地址：http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.Manual  
CFOUR关键词一览：http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.ListOfKeywordsInAlphabeticalOrder  
CFOUR输出文件介绍：http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.FileStructure  
  
CFOUR单点计算支持的方法一览：  
R/U/ROHF,TCSCF  
MP2/3/4  
CC2/3  
CCD, CCSD, CCSD+T, CCSD(T), CCSDT, CCSDT-n (n=1-4), Brueckner-CCD (B-CCD), B-CCD(T), Orbital-optimized CC (OO-CC)   
CID, CISD  
QCISD, QCISD(T)  
  
CFOUR一阶解析梯度支持的方法一览：  
HF-SCF,TCSCF   
MP2/3/4  
CC2/3  
QCISD,QCISD(T)  
CCD, CCSD, CCSD(T), CCSDT-n (n=1-4), CCSDT  
  
CFOUR二阶解析梯度支持的方法一览：  
HF-SCF (RHF, UHF, ROHF)   
MP2/3/4 (RHF, UHF)  
CCD, CCSD, CCSD(T) (RHF, UHF)   
CCSDT-n (n=1-4), CCSDT (RHF)  
  
总的来说，CFOUR的最主要用处有三：获得很高精度的能量、结构或密度；更快地做耦合簇计算；与GIMIC相连接分析感应电流（将在其它帖子专门介绍）  
  
  

## 2 编译方法

CFOUR支持MPI并行（OpenMPI、lammpi、mpich2都可以），支持MKL库，并可以通过MKL库的多线程模式来实现并行。编译时可以根据情况挂上不同选项，网站上给了一些例子（http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.Examples），但是很凌乱，这里给出最常用的64bit Linux平台下的串行和并行版本编译方法。CFOUR的代码兼容性比较好，不同Linux发行版本下，用gfortran和ifort都能顺利编译。寡人用的是RHEL6U1+mpich2 1.4.1p1+ifort 12.1环境，intel i7-2630QM。12分钟可以编译完毕。  
  
注意，如果你用的是ifort 12.x，由于其bug，在下面的步骤中执行./configure产生make.config文件后，要将make.config中的-O3都改为-O2才能执行下一步，不这样将优化等级适当调低的话编译到中途可能卡主。如果是gfortran或者老版本ifort，比如ifort 10，则不存在这个问题。  
  
串行版本的最简单的编译方式：  
1 解压CFOUR源代码包，进入其目录，假设为/sob/cfour_v1  
2 运行./configure FC=ifort （没装ifort就改成FC=gfortran）  
3 make。编译出的文件会在bin目录下  
4 将export PATH=$PATH:/sob/cfour_v1/bin加入到当前用户的.bashrc文件中，输入bash命令或重新启动控制台使之生效。  
  
并行版本+mpich2+MKL+GIMIC程序的接口的编译：  
1 把ifort 12.1（连带着安装包内含的MKL）安装到默认路径  
2 安装mpich2到默认路径。也就是解压后运行./configure FC=ifort，然后make，然后make install。将127.0.0.1 ltwd ltwd加到/etc/hosts最后，ltwd代表当前实际主机名。  
3 export MKLPATH=/opt/intel/mkl/lib/intel64 （如果是老版本ifort，默认的MKL路径可能不一样，根据实际情况调整）  
4 解压CFOUR源代码包，进入其目录，假设为/sob/cfour_v1  
5 将下面这一串作为一整行复制到控制台中执行。由于这里加了--enable-gimic，因此会编译出xcpdens程序，这是给GIMIC用的，和GIMIC包里自带的xcpdens其实是完全一样的。  
./configure FC=ifort MPIFC=mpif90 --enable-gimic --with-blas="$MKLPATH/libmkl_solver_ilp64.a -Wl,--start-group $MKLPATH/libmkl_intel_ilp64.a $MKLPATH/libmkl_intel_thread.a $MKLPATH/libmkl_core.a -Wl,--end-group -openmp -lpthread" --enable-mpi=mpich --with-mpirun="mpirun -np \$CFOUR_NUM_CORES" --with-exenodes="mpirun -np \$CFOUR_NUM_CORES"   
5 make  
6 将export PATH=$PATH:/sob/cfour_v1/bin加入到当前用户的.bashrc文件中，输入bash命令或重新启动控制台使之生效。  
  
  

## 3 使用方法

CFOUR的输入文件必须命名为ZMAT。运行前要将CFOUR目录下basis文件夹里的GENBAS基组文件拷到ZMAT所在目录下，如果用赝势，也要把basis文件夹里的ECPDATA文件拷到那里。然后在ZMAT所在目录下输入xcfour即可开始运算。运行过程信息输出到屏幕上，同时还会在当前目录下产生一大堆文件，如果之后要算新任务，应该把它们删掉。  
  
如果用的是按上面方法编译的并行+MKL版，运行前需要先设定两个环境变量，比如有8个CPU核心时可以这么设  
export CFOUR_NUM_CORES=4  
export MKL_NUM_THREADS=2  
这里CFOUR_NUM_CORES设定的是MPI并行时启用多少个进程，设为n的话那么内存及硬盘的开销就会约为之前的n倍。MKL_NUM_THREADS设定的是每个MPI进程中在调用MKL数学库时启用多少个线程，这并不会增加资源消耗。上面的例子，运行时总共就会有4*2=8个线程并行。由于程序中利用MKL库的部分是有限的，所以靠MKL_NUM_THREADS并行明显不如用CFOUR_NUM_CORES并行程度充分，对于四核机子，通常这两个参数为4/1时比1/4的时候要快很多。然而，由于做较大的后HF计算时总是要频繁、大量读写硬盘，进程太多就会使硬盘I/O速度成为严重的瓶颈，反倒会拖慢速度，而且还大幅增加了硬盘使用量，所以，4/1时常不如2/2的时候快。这两个参数怎么设效率最高，应当在自己条件下实际测试一下。  
  
MPI并行运算时依然是直接输入xcfour即可，不要在前面自己写mpirun -np x，因为程序会自动把它加上去。  
  
CFOUR支持MPI并行的功能主要是耦合簇计算，必须在输入文件中包含CC_PROGRAM=ECC和ABCDTYPE=AOBASIS关键词才行（即便不并行，带上它们也比默认情况算得更快）。  
  
对于不支持MPI并行的任务，如MP2，如果想达到并行化，就只能靠MKL_NUM_THREADS来实现。也就是说，此时要用串行版本来计算，且在编译串行版本的./configure这一步后面加上这一串以利用MKL：--with-blas="$MKLPATH/libmkl_solver_ilp64.a -Wl,--start-group $MKLPATH/libmkl_intel_ilp64.a $MKLPATH/libmkl_intel_thread.a $MKLPATH/libmkl_core.a -Wl,--end-group -openmp -lpthread"  
假设有n个核，就设export MKL_NUM_THREADS=n  
  
  

## 4 输入文件格式

典型的输入文件格式为  
Water CC-LR/DZP at experimental equilibrium geometry  
O  
H 1 R  
H 1 R 2 A  
  
R=0.958  
A=104.5  
  
*CFOUR(CALC=CCSD,BASIS=DZP,EXCITE=EOMEE)  
  
%excite*  
1  
1  
1 5 0 6 0 1.0  
[空行]  
第一行是注释，接下来是分子坐标（默认为埃），元素名必须顶头写。*CFOUR()里面是关键词，显然，CALC和BASIS就是指方法和基组。最后一部分是特殊任务才要输入的（这里是对EOM-CCSD算激发态任务的设定）。  
  
每行不得超过80个字符，然而关键词那行经常会超过这要求，此时可以分多行写，例如  
*CFOUR(CALC=HF,BASIS=cc-pVDZ,PROP=NMR,SYMMETRY=ON   
CC_PROGRAM=ECC,ABCDTYPE=AOBASIS)  
注意换行处末尾不加逗号，而且要有个空格。因此上面SYMMETRY=ON后面跟着个空格，不要忽略。  
  
如果想优化结构，不需要专门写关键词，将相应的变量上打星号即可，如  
O  
H 1 R*  
H 1 R* 2 A*  
  
  

## 5 常用关键词

此程序很多关键词都平时用不上，或者不需要修改，这里我总结出最常用的关键词的主要含义，建议过目一遍，具体信息还要去查阅在线手册，在日后新版本很多参数可能都会变名字。注意CFOUR程序做后HF时默认是不冻芯的。  
  
EMORY=xxx将可用内存设为xxx，默认单位为INTEGERWORDS。对于32/64bit平台分别乘以4/8就是KB。用MEM_UNIT可以将单位改为kB, MB, GB, TB  
ECP=ON：使用赝势  
CHARGE：体系的电荷  
MULTIPLICITY：体系的自旋多重度  
COORDINATES：控制体系的坐标描述。默认的INTERNAL是内坐标，CARTESIAN可以用笛卡尔坐标，但是不能做几何优化。XYZ2INT是提供内坐标连接关系但使用笛卡尔坐标描述位置。  
SCF_CONV=N：密度矩阵最大变化小于10^-N就停了。默认为7  
SCF_DAMPING：设500有益于解决SCF不收敛  
SCF_MAXCYC：SCF最大迭代次数，默认150  
SCF_EXTRAPOLATION：是否用DIIS，默认为ON  
SPHERICAL：默认的ON是用球谐型高斯函数，OFF用笛卡尔型  
SUBGROUP：默认使用最高阶的阿贝尔点群对称性。C1就相当于SYMMETRY=OFF  
PRINT=1：可以比默认的0输出更多细节信息  
  
GEO_METHOD=TS：找过渡态  
GEO_CONV=N：设定优化收敛限为N Hartree/bohr  
GEO_MAXCYC：最大优化步数，默认为50  
GEO_MAXSTEP：设几何优化的最大步长为millbohr。默认300  
EVAL_HESS=N：每隔N个优化步算一次精确Hessian，默认为从不，也就是用准牛顿法  
  
EXCITE：设定EOM-CC/LR-CC的处理类型，默认为NONE，EOMEE是计算激发态，EOMIP是计算离子化态，EOMEA是计算electron-attached态  
ABCDTYPE=AOBASIS：建议对最高至CCSD(T)的各种计算都加上，可以加快速度。默认是=0 (STANDARD)  
XFIELD,YFIELD,ZFIELD：XYZ方向加电场  
PROPS=FIRST_ORDER：计算一阶属性（多极矩，相对论校正，电场梯度，自旋密度，Mulliken电荷）；SECOND_ORDER计算静态可极化率；DYNAMICAL；计算含频可极化率；NMR：计算NMR；HYPERPOL：计算静态超极化率；DYN_HYP计算含频率超极化率  
RAMAN_INT=1：算拉曼  
RELATIVISTIC：设定相对论校正  
DBOC=1：做diagonal Born-Oppenheimer对能量的校正  
VIBRATION=ANALYTIC：用解析二阶导数计算谐振频率  
  
CC_PROGRAM：控制做CC的程序，默认是VCC，对于CCSD, CCSD+T, CCSD(T), closed-shell CCSDT-n, CC3 和CCSDT，建议设为ECC来加快速度  
FROZEN_CORE：CFOUR默认在post-HF中不冻芯。如果设为ON，则内核轨道在post-HF过程中都被冻结。如果想设定具体哪些被冻，则用DROPMO来设定  
DROPMO：如果输入比如1>10-55-58>64，就代表1,2,3,4,5,6,7,8,9,10,55,58,59,60,61,62,63轨道都被冻结  
FROZEN_VIRT：默认为OFF，如果设为ON，高于指定能量的虚轨道将不被考虑  
HFSTABILITY：ON代表做SCF波函数稳定性测试  
REFERENCE：RHF、UHF、ROHF、TCSCF(Two-configureational SCF)  
RESTART_CC=1：重启CC计算  
CC_CONV=N：CC收敛标准为系数最大改变值小于10^-N。默认为7。实际上此时能量变化远小于1D-7了，想节省时间的话可以事先停了  
  
  
附1：BASIS关键词可用的参数（对大小写敏感）  
STO-3G  
3-21G  
4-31G  
6-31G  
6-31G*  
6-31G**  
6-311G  
6-311G*  
6-311G**  
DZ  
DZP  
TZ  
TZP  
TZ2P  
PVDZ  
PVTZ  
PVQZ  
PV5Z  
PV6Z  
PCVDZ  
PCVTZ  
PCVQZ  
PCV5Z  
PCV6Z  
AUG-PVDZ  
AUG-PVTZ  
AUG-PVTZ  
AUG-PVQZ  
AUG-PV5Z  
AUG-PV6Z  
D-AUG-PVDZ  
D-AUG-PVTZ  
D-AUG-PVQZ  
D-AUG-PV5Z  
D-AUG-PV6Z  
cc-pVDZ  
cc-pVTZ  
cc-pVQZ  
cc-pV5Z  
cc-pV6Z  
cc-pCVDZ  
cc-pCVTZ  
cc-pCVQZ  
cc-pCV5Z  
cc-pCV6Z  
PWCVDZ  
PWCVTZ  
PWCVQZ  
PWCV5Z  
PWCV6Z  
PwCVDZ  
PwCVTZ  
PwCVQZ  
PwCV5Z  
PwCV6Z  
svp  
dzp  
tzp  
tzp2p  
qz2p  
pz3d2f  
13s9p4d3f  
WMR  
ANO0  
ANO1  
ANO2  
EVEN_TEMPERED  
  
附2：CALC关键词可用的设定（还有些关键词比如FCI、CC4、CCSDTQPH等都需要外挂MRCC才能实现）  
SCF (or HF)  
MBPT(2) (or MP2)  
MBPT(3) (or MP3)  
SDQ-MBPT(4) (or SDQ-MP4)  
MBPT(4) (or MP4)  
CCD  
CCSD  
CCSD(T)  
CCSDT-1  
CCSDT-1b  
CCSDT-2  
CCSDT-3  
CCSDT-4  
CCSDT   
CC2  
CC3  
QCISD   
QCISD(T)  
CID  
CISD  
UCC(4)  
B-CCD
