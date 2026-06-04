---
post_id: 247
title: Gromacs 5.1.1与4.6.7编译方法
url: http://sobereva.com/247
date: '2015-06-08T00:10:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是Gromacs编译方法，典型的软件安装编译教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

注：本文已经过时，最新版本GROMACS安装方法参见《GROMACS的安装方法》（<http://sobereva.com/457>）

**Gromacs 5.1.1与4.6.7编译方法**Compilation method of GROMACS 5.1.1 and 4.6.7  
  
文/Sobereva @[北京科音](http://www.keinsci.com)  Last update: 2016-Jan-25

  
  

## Gromacs 5.0（5.1.1编译方法与此完全一样）

编译条件：RHEL6-U1 64bit, Intel Q6600, root。  
  
必须有cmake 2.8.8及以上。MKL、icc不是必需的，用MKL不比FFTW更快，用icc比gcc优势也不明显，故没必要装。单机并行不用装MPI库，因为用的是OpenMP并行。跨节点运行基于MPI，可以用OpenMPI 1.6及以上版本或MPICH 1.4.1及以上版本。  
  
运行cmake -version，如果显示的版本低于2.8.8，到这里下载最新的cmake源代码：http://www.cmake.org/cmake/resources/software.html  
解压cmake，进入其目录，运行./bootstrap;make -j;make install，就被安装到了/usr/local/bin下面。删掉cmake目录。  
  
tar -zxf gromacs-5.0.tar.gz解压之，进入Gromacs的解压目录  
mkdir build  
cd build  
cmake .. -DGMX_BUILD_OWN_FFTW=ON -DCMAKE_INSTALL_PREFIX=/sob/gromacs50 （注：如果用的CPU比较新，编译器版本又比较老，比如RHEL6自带的，这一步可能会报错提示说编译器不支持AVX2指令集，此时应当再加上-DGMX_SIMD=AVX_256来强制用AVX1指令集）  
make -j       //-j代表调用所有核并行编译  
make install  
在make过程中Gromacs会自动下载FFTW3.3.3并编译之。下载和编译总共只需几分钟。程序被安装到了/sob/gromacs50。删掉Gromacs安装目录，并在用户的.bashrc里加上export PATH=$PATH:/sob/gromacs50/bin。  
  
如果要编译双精度版本，cmake的时候写上-DGMX_DOUBLE=ON。此时不兼容GPU加速。编译出来的可执行文件默认都带着_d后缀，因此可以和单精度版安装到同一目录，不会冲突。  
  
  
**** CUDA版安装方法  
Gromacs通过CUDA支持nVidia的GPU来加速动力学计算，效率很好。如果用的是4核CPU，用高端GeForce显卡可加速>3倍，性价比很高。  
先去nVidia网站下载并安装CUDA toolkit到默认路径。其它同上，区别仅是cmake这一步：  
cmake .. -DGMX_GPU=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-5.5 -DGMX_BUILD_OWN_FFTW=ON -DCMAKE_INSTALL_PREFIX=/sob/gromacs50  
  
Gromacs从5.0开始也支持Intel XEON phi来加速计算，但只是初步支持，性价也远低于使用高端GeForce显卡，故这里就不说了。  
  
  
**** 自己装FFTW的情况  
有时候安装的机子不通网，Gromacs编译时没法自动联网下载FFTW，就必须先自行下载安装FFTW，然后在编译时调用。过程是：去ftp://ftp.fftw.org/pub/fftw/下载FFTW3.3.3或更高版本，解压并进入目录，运行  
./configure --prefix=/sob/fftw333 --enable-sse2 --enable-float --enable-shared  
make -j  
make install  
在编译Gromacs的cmake那步之前先运行  
export CMAKE_PREFIX_PATH=/sob/fftw333  
然后在cmake时去掉-DGMX_BUILD_OWN_FFTW=ON。  
注意--enable-float代表编译单精度版本FFTW。如果是给双精度Gromacs用的，应该把--enable-float去掉。  
  
  
**** 编译MPI版的方法  
去http://www.open-mpi.org下载openmpi，这里用1.6.5版。解压并进入目录后运行  
./configure  
make all install  
然后在cmake时加上-DGMX_MPI=on即可。编译出来的文件都带着_mpi后缀，因此和单节点并行的版本可以装到一起，不会冲突。  
  
  
注：Gromacs充分对主流的CPU支持的SIMD指令集进行优化，编译时会自动检测CPU架构，采用适当的编译选项，充分利用支持的指令集达到最佳性能。因此，如果几个机子的CPU架构不同，不要把编译好的Gromacs程序直接互拷，否则运行会出问题。  
  
  

## Gromacs 4.6.7

编译方法和5.0基本没有任何差异，下面只是简要写写，具体请参考上面的内容。  
  
编译条件：RHEL6-U1 64bit, Q6600, root。  
gmx 4.6开始完全使用cmake而不用./configure。必须有cmake 2.8及以上。MKL、icc不需要装。单机并行不用装MPI库，跨节点运行可以用openMPI或mpich。安装方法参考了http://www.gromacs.org/Documentation/Installation_Instructions。  
  
到这里下载最新的cmake源代码：http://www.cmake.org/cmake/resources/software.html  
解压cmake，进入其目录，运行./bootstrap;make;make install，就被安装到了/usr/local/bin下面。删掉cmake目录。  
  
tar -zxf gromacs-4.6.7.tar.gz解压之，进入gmx的解压目录  
mkdir build  
cd build  
cmake .. -DGMX_BUILD_OWN_FFTW=ON -DCMAKE_INSTALL_PREFIX=/sob/gromacs467  
make -j  
make install  
在make过程中gmx会自动下载fftw3.3.2并编译之。下载和编译总共只耗时<3分钟。程序被安装到了/sob/gromacs467。删掉gmx安装包及解压目录。  
  
如果要编译双精度版本，cmake的时候写上-DGMX_DOUBLE=ON。此时不兼容GPU加速。编译出来的可执行文件默认都带着_d后缀。  
  
**** CUDA版安装方法  
安装CUDA toolkit。其它同上，区别仅是cmake这一步：  
cmake .. -DGMX_GPU=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-5.5 -DGMX_BUILD_OWN_FFTW=ON -DCMAKE_INSTALL_PREFIX=/sob/gromacs467gpu  
  
**** 自己装fftw的情况  
解压fftw3.3.2，进去，运行  
./configure --prefix=/sob/fftw332 --enable-sse2 --enable-float --enable-shared  
make  
make install  
然后gmx里的cmake步骤改为  
export CMAKE_PREFIX_PATH=/sob/fftw332  
cmake .. -DCMAKE_INSTALL_PREFIX=/sob/gromacs467  
如果用于编译双精度gmx，--enable-float应去掉
