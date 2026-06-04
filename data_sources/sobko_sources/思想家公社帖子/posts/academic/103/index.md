---
post_id: 103
title: Amber11+AmberTools1.5及CUDA版安装方法，以及Amber12安装方法
url: http://sobereva.com/103
date: '2015-06-07T23:50:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是AMBER11和AmberTools1.5以及CUDA版的安装方法，典型软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

PS: 由于Amber11编译时是在Linux下面一边编译一边写的，又没装中文输入法，所以就写成英文了。Amber12安装方法只是很简单地写了下。

**Amber11+AmberTools1.5及CUDA版安装方法，以及Amber12安装方法**Installation method of Amber11+AmberTools1.5 and CUDA version, and that of Amber12

文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2011-Sep-23  Last update: 2014-Aug-21

## =============== Amber11安装方法 ===============

  
Platform: RHEL6-U1 64bit, Toshiba X500 notebook (i7-2630QM, 8GB memory, GTX460M with 1.5GB graphical memory), graphical driver is 280.13.  
user: root, shell: bash  
Amber11 will be installed to /sob/amber11  
  
  
1. Install intel compilers (The advantage in speed is huge relative to GNU compilers)  
#If you don't have intel C++ compiler (icc) and intel fortran compiler (ifort), goto http://software.intel.com/en-us/articles/non-commercial-software-download/ to apply for a non-commercial licenses (one year available) and download icc and ifort. The version used in present article is 2011.6.233. Copy the .lic files received from E-mail to /sob/licenses folder  
  
#Note: If the installer says that libstdc++ library cannot be found, you may need to install libstdc++-4.4.5-6.el6.i686.rpm first  
#Now install ifort, uncompress l_fcompxe_2011.6.233.tgz to /sob  
cd /sob/l_fcompxe_2011.6.233  
./install.sh  
#When installer asking you how to activate, choose "...or by using a license file...", then "Use a license file", input "/sob/licenses"  
#The component "Intel Debugger" is unnecessary and can be deselected. Use default target directory to install ifort now.  
  
#Use the same way described above to install icc (l_ccompxe_2011.6.233), in the component selection stage, only select Intel C++ Compiler, other components are useless.  
  
#Add "source /opt/intel/composer_xe_2011_sp1.6.233/bin/compilervars.sh intel64" to /root/.bashrc file, then input "bash" or reopen shell  
#Now you can delete l_fcompxe_2011.6.233 and l_ccompxe_2011.6.233 folders in /sob  
  
  
2. Install nVidia toolkit  
# Goto http://developer.nvidia.com/cuda-toolkit-40 and download "CUDA Toolkit 4.0" (Select the one corresponding to "CUDA Toolkit for RedHat Enterprise Linux 6.0")  
./cudatoolkit_4.0.17_linux_64_rhel6.0.run  
#Add below sentenses to /root/.bashrc, then input "bash" or reopen shell  
export PATH=$PATH:/usr/local/cuda/bin  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/lib  
export CUDA_HOME=/usr/local/cuda  
#cudatoolkit_4.0.17_linux_64_rhel6.0.run now can be deleted  
  
  
3. Install MPICH2  
#Goto http://www.mcs.anl.gov/research/projects/mpich2/ to download MPICH2 1.4.1p1 and uncompress it to /sob  
#In mpich2 1.4.1p1 folder:  
./configure FC=ifort CC=icc  !You may need to wait several minutes  
make  
make install  
#Now mpich2-1.4.1p1 folder can be deleted from /sob  
#Note: If error "...'MPD' object has no attribute 'myIP'..." occurs when running "mpd" command, you need to add "127.0.0.1 ltwd ltwd" to the last line of /etc/hosts, where ltwd is the name of local computer. Also note, in current mpich2 verison, you needn't to boot up MPD before running parallel programs by "mpirun -np x" as older mpich2 version.  
  
  
4. Prepare installation  
#Add below sentense to /root/.bashrc, then input "bash" or reopen shell  
export AMBERHOME=/sob/amber11  
#Uncompress Amber11.tar.bz2 to /sob/amber11, then uncompress AmberTools-1.5.tar.bz2 to /sob/amber11 (overwrite all files already existed), after that one can find /sob/amber11/AmberTools folder  
  
#Goto http://ambermd.org/bugfixesat.html to download "bugfix.all" for AmberTools1.5, move it to /sob/amber11  
cd $AMBERHOME  
patch -p0 -N < bugfix.all  
  
#Goto http://ambermd.org/bugfixes11.html to download bugfix package of Amber11 (current name is bugfix.1to17.tar.bz2) and apply_bugfix.x. Copy these two files to /sob  
cd /sob  
./apply_bugfix.x bugfix.1to17.tar.bz2  
  
  
5. Install serial version of AmberTools 1.5  
cd /sob/amber11/AmberTools/src  
./configure intel  
make install !Takes ~20min. Don't try to use -j option to speed up compilation  
#Let's test, may take *rather* long time  
cd ../test  
make test  
#Goto /sob/amber11/AmberTools/test/logs/test_at_serial to check .diff file  
  
  
6. Install serial version of Amber11 (PMEMD is not needed to be compiled separately as previous version of amber)  
cd /sob/amber11  
./AT15_Amber11.py  !Patch amber11 source code for compatibility with AmberTools1.5  
cd src  
make serial !Takes ~5min  
#Let's test, may take *rather* long time  
cd /sob/amber11/test  
make test  
#Goto /sob/amber11/test/logs/test_amber_serial to check .diff file  
  
#Add below sentense to /root/.bashrc, then input "bash" or reboot shell  
export PATH=$PATH:/sob/amber11/bin  
  
  
7. Install CUDA version of PMEMD (SPDP mode, which is default. In Amber11 only PMEMD support CUDA)  
cd /sob/amber11/AmberTools/src  
make clean  
./configure -cuda intel  
cd /sob/amber11/  
./AT15_Amber11.py  
cd src  
make clean  
make cuda !Take 3~4 minutes  
#pmemd.cuda is now presented in /sob/amber11/bin, let's test if it works  
cd /sob/amber11/test/  
./test_amber_cuda.sh !Takes 1min16s on my computer, only tip4pew_box_npt and tip4pew_oct_nvt are shown to be possibly failed. By checking .diff file in /sob/amber11/test/logs/test_amber_cuda, I found the differences are very small (0.0001 in BOND term), so the failures can be safely ignored.  
  
  
8. Install parallel version of AmberTools 1.5  
cd /sob/amber11/AmberTools/src  
make clean  
./configure -mpi intel  
make install !Since parallel version of AmberTools is rarely used, this step can be simply skipped. This compilation generates such as pbsa.MPI, ptraj.MPI, mpinab...  
  
  
9. Install parallel version of Amber11  
cd /sob/amber11  
./AT15_Amber11.py  
cd src  
make clean  
make parallel !Takes ~6min. This compilation generates such as pmemd.MPI, sander.MPI...  
#Let's test  
cd /sob/amber11/test  
export DO_PARALLEL="mpirun -np 4"  
make test.parallel  
#Only 1 possible failure on my computer  
  
  
10. Install Multiple GPU version of PMEMD. If you don't have multiple GPUs installed, this step should be omitted.  
cd /sob/amber11/AmberTools/src  
make clean  
./configure -cuda -mpi intel  
cd /sob/amber11  
./AT15_Amber11.py  
cd src  
make clean  
make cuda_parallel !pmemd.cuda_SPDP.MPI is generated in this step  
#Let's test  
cd ../test  
./test_amber_cuda_parallel.sh  
  
  
11. Benchmark  
#Here we use two instances provided in the official benchmark package, the package can be downloaded from http://ambermd.org/gpus/benchmarks.htm, uncompress it to /sob  
  
#The first system consists of 2492 atoms, GB solvation model is used, no upper limit for cutoff is set, run 50ps. Let's test CUDA performance first  
cd /sob/Amber11_Benchmark_Suite/GB/myoglobin  
time pmemd.cuda -O -i mdin -o mdout -p prmtop -c inpcrd  
#In my computer, this task takes 3m11s (The "real" term shown on the screen), equals to 22.6ns/day.  
#Now test CPU performance  
time mpirun -np 4 pmemd.MPI -O -i mdin -o mdout -p prmtop -c inpcrd  
#This task takes 36m29s, equals to 1.97ns/day, the speed up by using CUDA is 10.5x.  
  
#The second system is a protein in TIP3P waters, 23558 atoms in total, NVT ensemble, PME is used, run 20ps.  
cd /sob/Amber11_Benchmark_Suite/PME/JAC_production_NVT  
time pmemd.cuda -O -i mdin -o mdout -p prmtop -c inpcrd  
#This run takes 2m11s (2m50s in NPT), equals to 13.2ns/day.  
time mpirun -np 4 pmemd.MPI -O -i mdin -o mdout -p prmtop -c inpcrd  
#This run takes 5m18s (6m39 in NPT, 5min19s in NVE), equals to 5.4ns/day. Apparently, the speed up by CUDA in explicit solvation model under PME+NVT is not so huge as in GB model, of course, GTX460M itself is also not powerful enough.  
  
  
  
Postscript:  
In the compilation process given above, Intel Math Kernel library (MKL) was not used. Because I found MKL doesn't affect the simulation performance (at least for PMEMD) in explicit solvation model at all, whether for CPU or CUDA version. Only the performance of CPU version in GB model can be benefited from MKL (improve efficiency by ~25%).  
If you would like to compile Amber under MKL support, simply run "export MKL_HOME=/opt/intel/mkl" before the configuration step (assume that MKL has been installed to default place). Notice that if the MKL version you used is 12.0 or newer, you also have to open /sob/amber11/AmberTools/src/configure by an text editor, then replace "em64t" in this sentense by "intel64": mkll="$MKL_HOME/lib/em64t".  
  

## =============== Amber12安装方法 ===============

  
安装ifort,icc 12.1.0到默认路径。MKL对性能影响很小，这里不用MKL  
  
安装mpich 1.4.1p1  
./configure FC=ifort CC=icc  
make  
make install  
  
.bashrc里加入  
AMBERHOME=/sob/amber12  
PATH=$PATH:$AMBERHOME/bin  
  
进入/sob目录  
将AmberTools12.tar.bz2在当前目录下解压。（此时会看到/sob/amber12/下面有AmberTools目录）  
将Amber12.tar.bz2在当前目录下解压，这会合并掉一些目录，覆盖几个文件。  
  
进入/sob/amber12目录  
  
---------  
要保持联网畅通  
  
先编译串行AmberTools12和Amber  
export SSE_TYPES=SSE4.2  
./configure intel  
会自动检测有没有AmberTools12和Amber12的补丁。选y，将自动下载目前已发布的所有补丁，然后自动调用patch_amber.py使之应用到源代码文件上。如果没有联网，可以事先从官网上下载补丁文件，然后自行用patch_amber.py使之生效，见AmberTools12手册1.5节说明。  
make install 花费约24分钟。由于已经把amber12也解压了，所以这一步不仅会把ambertools编译出来，也会把amber12编译出来  
make test 测试要花费很长时间，在rism1d测试中卡主动不了了。  
  
编译并行AmberTools12和Amber  
./configure -mpi intel  
make install 会生成MMPBSA.py.MPI  pmemd.amoeba.MPI  pmemd.MPI  sander.LES.MPI  sander.MPI  
export DO_PARALLEL="mpirun -np 4"  
make test 测试并行版amber12。一般的四核机子应该大概在半个小时内完成。19个测试悉数通过。  
  
编译OpenMP并行版NAB和Cpptraj  
make openmp 编译出来的名字和串行版本一样仍叫nab和cpptraj  
  
  
  
附：Amber10安装方法 <http://sobereva.com/3>
