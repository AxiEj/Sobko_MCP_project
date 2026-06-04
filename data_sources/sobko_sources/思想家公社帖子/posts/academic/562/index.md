---
post_id: 562
title: Quantum ESPRESSO在Linux下的安装方法
url: http://sobereva.com/562
date: '2020-07-10T12:01:00+08:00'
source_categories:
- 第一性原理
primary_topic: 其它软件
secondary_topics:
- 第一性原理
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 Quantum ESPRESSO 的 Linux 安装方法，属于未列出软件。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**Quantum ESPRESSO在Linux中的安装方法**

Installation method of Quantum ESPRESSO under Linux

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2020-Jul-10  Last update: 2020-Jul-23

## 1 前言

Quantum ESPRESSO (QE)是用户非常多、极为流行的第一性原理程序，而且完全开源免费。本文介绍一下QE在Linux下的安装过程。本文对于CentOS 7.x系列系统下安装QE 6.5是完全适合的，对于其它QE版本或其它Linux系统请自行尝试、随机应变。本文使用root账户，对于普通用户请安装到自己有读写权限的目录。本文基于OpenMPI库+MKL库+gfortran/gcc编译器进行编译。编译的是纯CPU版本，不支持GPU加速（GPU加速还需要有PGI Fortran编译器）。如果机子里还没装gcc和gfortran，应先用yum install gcc命令进行安装。

关于编译的更多细节可以看QE的手册<https://www.quantum-espresso.org/Doc/user_guide/node10.html>。

在CentOS下使用yum也可以不通过编译来安装，但有一些弊端，见此文第6节。

## 2 安装OpenMPI

为了让QE能基于MPI并行计算，需要先装MPI库，一般就用OpenMPI。笔者用的是OpenMPI 4.0.3，经测试与QE 6.5完全兼容。

去<https://www.open-mpi.org>下载最新的OpenMPI包，解压后进入此目录，运行以下命令将之编译并安装到指定目录下。这里笔者安装到了/sob/openmpi目录下。  
./configure --prefix=/sob/openmpi  
make all install

在~/.bashrc文件中加入以下内容  
export PATH=$PATH:/sob/openmpi/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/openmpi/lib

然后重新打开终端，以上设置就生效了。可以运行mpiexec -V，如果正常显示出了OpenMPI的版本，说明已经装好了。之后可以删掉OpenMPI压缩包和解压出的目录。

注：如果机子里之前还有其它MPI库，应当运行which mpiexec来看看是否确实指向的是新装的OpenMPI，如果指向的是其它的，则并行运行可能失败。比如如果你之前在机子里装过Intel编译器的时候顺带装了Intel MPI，则应当在编译QE以及运行QE前将~/.bashrc里的相应配置语句注释掉后重新进入终端，免得被利用的是Intel MPI而非新装的OpenMPI。

## 3 安装MKL库

为了让QE能利用效率很高的MKL数学库来提升计算速度，应当在编译QE前先把MKL装上。MKL库目前是免费的，CentOS下可以运行以下两行命令安装。期间会下载几百兆的文件，文件会被安装到/opt/intel目录下，占3GB多（对于2020-Jul-10时下载的版本而言）。如果你之前机子里装过Intel编译器，且在装的时候已经选择装了MKL，就不需要再这么装一遍了。

添加intel的源：  
yum-config-manager --add-repo https://yum.repos.intel.com/mkl/setup/intel-mkl.repo

下载并安装MKL：  
yum install -y intel-mkl

## 4 编译QE

在<https://github.com/QEF/q-e/releases>下载QE最新版源代码包，比如qe-6.5-ReleasePack.tgz。

解压并进入其中，运行以下命令。这里-enable-openmp使得QE也可以利用OpenMP来并行，如果不打算以OpenMP并行的话就不写这个。  
./configure --prefix=/sob/qe65 -enable-openmp  
make all install -j  
四核机子上经过几分钟编译完毕，可执行文件都被装到了/sob/qe65/bin目录下。解压出的目录和压缩包此时虽然可以删掉，但我建议还是留着解压出的目录，里面有些文件以后还用得着。

注：QE在编译过程默认调用gfortran、gcc和mpif90。如果想改默认的编译器，应对QE目录下的make.inc文件里的编译器设置进行修改，而且在之前编译OpenMPI的时候也用相应的编译器。

在~/.bashrc文件中加入以下内容（如果你用的不是root的话，前两行不用加）  
export OMPI_ALLOW_RUN_AS_ROOT=1  
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1  
export PATH=$PATH:/sob/qe65/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/compilers_and_libraries_2020.2.254/linux/mkl/lib/intel64_lin  
这里往LD_LIBRARY_PATH环境变量添加的Intel MKL库的目录名应当与你当前机子里的实际路径一致。

之后重新进入终端，QE的可执行文件就可以在任意目录下直接运行了。

以上述方式编译出来的QE没有包含EPW、PLUMED、Wannier90、WanT、YAMBO、GIPAW程序，如果需要编译的话，看官网上User's Guide for Quantum ESPRESSO文档的2.5节。

## 5 测试QE

下面对QE最关键的PWscf模块做简单测试。下载<http://sobereva.com/attach/562/diamond.zip>并解压，此任务是对金刚石做SCF计算。

QE是MPI和OpenMP混合方式并行的程序，实际并行核数是MPI进程数与每个下属的OpenMP线程数的乘积。

先测试纯MPI并行方式运行。进入diamond目录后，运行以下命令，使用4个MPI进程计算，每个MPI进程下属只有一个线程。  
export OMP_NUM_THREADS=1  
mpirun -n 4 pw.x < pwscf.in |tee pwscf.out  
如果任务能正常完成，末尾显示JOB DONE，就说明已经装好了。注：如果不设置OMP_NUM_THREADS环境变量的话，机子有多少核，OpenMP就会用多少个线程。

然后再测试纯OpenMP并行方式运行。运行以下命令，将使用一个MPI进程下属4个OpenMP线程进行计算  
export OMP_NUM_THREADS=4  
pw.x < pwscf.in |tee pwscf.out

也可以使用QE自带的测试集进行测试。做法是进入QE解压后的目录的test-suite子目录，在里面运行make run-tests-parallel命令，就会在并行运算下对所有任务进行测试，每一项对应的含义见此目录下的README。如果只想测试比如PWscf模块，则运行make run-tests-pw-parallel。

## 

## 6 在CentOS下使用yum安装QE

下面文字适用于CentOS，使用root的情况。会安装基于OpenMPI并行但不支持OpenMP并行的QE 6.5版。至少对于对于CentOS 7.7和8.0而言，被安装的是QE 6.5版。Ubuntu下也可以用apt-get装，本文就不提了。

运行以下命令：  
yum install epel-release  
yum install quantum-espresso-openmpi  
期间会自动安装OpenMPI、OpenBLAS、ScaLapack等包。如果你是用yum install quantum-espresso，则安装的是只能串行计算的版本，没实际价值。

之后在~/.bashrc文件里加入以下内容：  
export PATH=$PATH:/usr/lib64/openmpi/bin/  
如果你用的是root的话同时加入  
export OMPI_ALLOW_RUN_AS_ROOT=1  
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1  
之后重新进入终端即可使用。

QE的文件被安装到了/usr/lib64/openmpi/bin/目录下，可执行文件都带着_openmpi后缀。比如可以运行mpirun -n 4 pw.x_openmpi < pwscf.in。

对于计算密集型程序，像QE这种编译不麻烦的话，我鼓励自行编译，因为yum装的CentOS软件源里的预编译版为了兼容性、减少库的依赖，在一些地方可能会打一些折扣，比如没用MKL（对QE提供高质量的BLAS、ScaLapack和FFT）、用的编译选项比较保守，故性能可能逊于自己编译的。而且自己编译的话可以自定义文件产生的位置，虽然yum也可以用--installroot=...选项指定安装在哪，但是有些程序可能不能运行。

另外，QE的文档信息很零散，比如支持的泛函完整列表甚至还得去看源代码包里的func.f90里的注释等等，所以最好有源代码包。之前若自己用源代码包编译过之后还可以直接用make epw、make w90、make gipaw等命令编译安装与QE有关的程序。
