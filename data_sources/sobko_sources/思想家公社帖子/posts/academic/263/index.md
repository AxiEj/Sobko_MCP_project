---
post_id: 263
title: Amber14安装方法
url: http://sobereva.com/263
date: '2015-06-08T00:14:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题就是Amber14安装方法，明确是AMBER软件安装教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

以前版本的安装方法参见：

《Amber11+AmberTools1.5及CUDA版安装方法，以及Amber12安装方法》（<http://sobereva.com/103>）

《Amber10安装方法》（<http://sobereva.com/3>）

**Amber14安装方法**  
Installation method of AMBER14

文/Sobereva @[北京科音](http://www.keinsci.com/)   2014-Nov-22

编译环境：RHEL6U1-64bit, root, bash。硬件：Core 2 Q6600，GTX770。安装到/sob/amber14。

Amber越来越多的东西都被挪到免费开源的AmberTools里面了。Amber14只剩PMEMD一个模块了，其它所有模块，包括曾经amber最核心的sander，都已经弄到AmberTools14里了。可以说，光靠AmberTools就已经足够进行动力学模拟了。如果需要更快的速度和GPU加速，才需要花钱买Amber。

## ====准备工作====

准备好Amber14.tar.bz2，去官网免费下载AmberTools14.tar.bz2。

安装ifort,icc 12.1.0到默认路径（其它版本我没试过）。MKL对性能影响很小，这里不用MKL。

编译openmpi：  
去<http://www.open-mpi.org>下载OpenMPI 1.6.5（更新的版本大抵也可以，笔者没测试），解压到/sob目录下，进入其目录，运行  
./configure CC=icc CXX=icpc FC=ifort F77=ifort; make all install  
此时openmpi的可执行文件、库文件、头文件等就被装到了/usr/local里面的对应目录下。

然后在.bashrc里加上  
export AMBERHOME=/sob/amber14  
export PATH=$PATH:$AMBERHOME/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$AMBERHOME/lib

运行bash使环境变量生效。

进入/sob目录，将AmberTools14.tar.bz2在当前目录下解压。将Amber14.tar.bz2也在当前目录下解压，这会合并掉一些目录，覆盖几个文件。然后amber14目录下应该会看到Ambertools、src、benchmarks等目录。

要保持联网畅通，以使得安装程序能自动使用官网上的补丁

## ====编译串行版本====

cd /sob/amber14  
./configure intel，程序检测到有补丁文件，输入y。

运行make install开始编译，耗时20多分钟。  
运行make test进行测试。测试时间相当长，两个小时左右。测试内容包括面向第三方量化程序的QMMM接口，如果机子上有gaussian、orca、terachem等等，在测试过程中都会被调用。笔者这里有11个测试failure，大部分是和orca有关的，这无关紧要。测试结果在/sob/amber14/logs目录下有汇总。

## ====编译并行版本====

./configure -mpi intel  
make install  
会在bin目录下生成MMPBSA.py.MPI、pmemd.amoeba.MPI、pmemd.MPI、sander.LES.MPI、sander.MPI等带.MPI后缀的文件。

进行测试，-np后面是测试时用的核数。  
export DO_PARALLEL="mpirun -np 4"  
make test  
一般的四核机子应该大概在半个小时内完成。笔者458个测试悉数通过。

编译OpenMP并行版NAB和Cpptraj  
./configure -openmp intel  
make openmp  
编译出来的名字和串行版本一样仍叫nab和cpptraj。

## ====编译GPU版PMEMD====

先去nVidia网站下载并安装CUDA toolkit到默认路径，笔者用的是5.5。然后在.bashrc里加入  
export CUDA_HOME=/usr/local/cuda-5.5  
export PATH=$PATH:$CUDA_HOME/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDA_HOME/lib64  
运行bash使之生效

cd /sob/amber14  
./configure -cuda intel  
make install  
./configure -cuda -mpi intel  
make install  
很快就编译完了，bin目录下产生了pmemd.cuda和pmemd.cuda.MPI。这是默认的SPFP版本，是精度和速度的最佳平衡。还有种DPFP版本，把-cuda改为-cuda_DPFP就可以编译，精度更高但计算消耗也明显更高，一般没必要。

测试串行版GPU版  
make test.cuda  
测试并行版GPU版  
export DO_PARALLEL="mpirun -np 4"  
make test.cuda_parallel

笔者这里提示的Possible failure竟接近半数。原因大抵是GPU跑动力学的重现性本来就比CPU跑更低，所以和参考值偏差容易较明显，但这也不能说当前设备跑的结果不合理，只不过是探索相空间的不同区域罢了。
