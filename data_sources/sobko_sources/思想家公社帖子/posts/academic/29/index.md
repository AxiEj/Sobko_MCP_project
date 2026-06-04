---
post_id: 29
title: Gromacs 4.0.3、4.5.5版安装方法
url: http://sobereva.com/29
date: '2015-06-05T00:13:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 内容是GROMACS的安装方法，明确属于软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

注：本文已经过时，最新版本GROMACS安装方法参见《GROMACS的安装方法》（<http://sobereva.com/457>）。

**Gromacs 4.0.3、4.5.5版安装方法**Installation method of GROMACS 4.0.3 and 4.5.5

文/Sobereva @[北京科音](http://www.keinsci.com/)    Last update: 2012-Jan-6

下面是gromacs4.0.3安装方法。4.5.5版安装方法见本文后半。

## gmx4.0.3安装方法

平台：F7-64bit、Q6600、gcc4.1.2、mpich2-1.0.7、root、ifort 10.1.015，软件版本gromacs4.0.3，安装在/sob/gromacs  
安装的是并行版本、单精度版本。

指定编译器和编译选项：  
export CC=gcc  
export CXX=g++  
export CFLAGS="-O3 -msse -msse2 -msse3 -mssse3 -march=core2"  
export CXXFLAGS="-O3 -msse -msse2 -msse3 -mssse3 -march=core2"  
export FFLAGS="-O3 -axT" //用C编译器编译内核的话不用这步

复制mpich2-1.0.7.tar.gz到/sob，解压到/sob/mpich2-1.0.7，进入此目录，运行：  
./configure  
make   
make install

运行  
touch /etc/mpd.conf   
chmod 700 /etc/mpd.conf  
将下面加入mpd.conf:  
secretword=<secretword> (比如secretword=ltwd)

解压fftw3.1.2压缩包到/sob下，进入fftw-3.1.2目录  
./configure --enable-float --with-gcc-arch=core2  
make  
make install  
默认安在了/usr/local/include(lib)下。

解压gromacs-4.0压缩包到/sob下，进入gromacs-4.0目录，  
./configure --prefix=/sob/gromacs --enable-mpi -enable-fortran  
make  
make install

在/root/.bashrc中添加PATH=$PATH:/sob/gromacs/bin，MANPATH=$MANPATH:/sob/gromacs/share/man。输入bash使环境变量生效

此时可删掉/sob下的fftw3.1.2目录、gromacs-4.0目录和mpich2-1.0.7目录。留下安好的gromacs目录。

*******  
如果我们要进行QMMM计算，需要编译时设定，目前gromacs支持gamess-UK、mopac7、gaussian98/03，这里介绍把mopac7编进gromacs的方法。  
下载<http://wwwuser.gwdg.de/~ggroenh/qmmm/mopac/dcart.f>  
下载<http://wwwuser.gwdg.de/~ggroenh/qmmm/mopac/SGI/mopac7.tar.gz>  
把mopac7.tar.gz解压，把刚下载的dcart.f放进去替换原文件，把目录下的mopac.f、moldat.f、deriv.f删掉。运行：  
ifort -O2 -c *.f  
ar rcv libmopac.a *.o  
ranlib libmopac.a然后把libmopac.a放到/lib下  
export CPPFLAGS=-DUSE_MOPAC   
export LIBS=-lmopac  
之后同样进行configure步骤，但多加一个参数--with-qmmm-mopac，即运行：  
./configure --prefix=/sob/gromacs --enable-mpi -enable-fortran --with-qmmm-mopac  
之后make、make install即可。  
********

PS:

用mkl的话，先修改./configure  
把两处LIBS="-lmkl $LIBS"改成LIBS="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core $LIBS"  
然后运行./configure --prefix=/sob/gromacs4mkl --enable-mpi -enable-fortran --with-fft=mkl CPPFLAGS=-I/opt/intel/mkl/10.0.4.023/include LDFLAGS=-L/opt/intel/mkl/10.0.4.023/lib/em64t，串行版本比fftw有提升，但是并行版本相对fftw却没有提升。如果是32bit平台，-lmkl_intel_lp64改为lmkl_intel，把.../lib/em64t改为.../lib/32

如果硬盘空间紧张，可以在./configure时加入--enable-shared来使用共享库，最终得到的bin非常小，gmx4.0中只有2.3MB，远小于使用静态库的172.65MB，只不过gromacs/lib文件夹里面会多出4约20MB。另外需要再添加环境变量LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/gromacs/lib。使用静态库或者动态库对运行速度基本没有影响。

gmx的内核有C语言和fortran两套版本，默认是C语言编译，如果用了-enable-fortran就是用fortran编译器编译，此时建议用ifort。用这个选项对gmx3.3.x来说并不会使性能有所多少提升，但对gmx 4.0.x来说性能提升明显。./configure的时候可以在后面加F77=xxx来指定fortran编译器。用gfortran可能会报错。

没必要用icc，性能相比用gcc不会有丝毫提升。

如果已经make过了，之后想./configure接新的选项重新编译，应当先执行make distclean

--program-suffix=[suffix]给出来的程序名加个后缀，可以区分单双精度版本、串行并行版本。比如先不加--enable-mpi编译一遍，然后make distclean，再加上--enable-mpi和--program-suffix=_mpi编译一遍，这样mdrun和mdrun_mpi串并行版本互不干扰。实际上没有必要单独编译串行版本，如果只是1个CPU用，就当成-np 1即可。

--disable-float或--enable-double可以编译成双精度版本(默认采用的是单精度)，双精度版本速度约为单精度60%，对常规分子动力学来说单精度就够了，除了简正振动分析等情况。

老gmx版本有一些问题，在gmx4.0.3皆已修正，写在这里作为参考。  
gmx4.0.0开-enable-fortran编译出错：把src/gmxlib/libxdrf.c的第1156行#define XDR_INT_SIZE 4挪到第68行，即在#ifdef GMX_FORTRAN之前。  
编译得到的g_spatial和g_cluster完全一样：把src/tools/g_spatial.c里面的gmx_cluster改成gmx_spatial(gmx4.0.3已修正)

在configure文件中可以看到：

CC C compiler command 一般这个环境变量就是gcc  
CFLAGS C compiler flags 编译时的参数，一般是-O3  
LDFLAGS linker flags, e.g. -L<lib dir> if you have libraries in a  
nonstandard directory <lib dir> 库文件目录  
LIBS libraries to pass to the linker, e.g. -l<library> 设的时候不用“-l xxx”，无需引号  
CPPFLAGS C/C++/Objective C preprocessor flags, e.g. -I<include dir> if  
you have headers in a nonstandard directory <include dir>  
F77 Fortran 77 compiler command 一般这个环境变量就是gfortran或ifort  
FFLAGS Fortran 77 compiler flags 编译时的参数，一般是-O3  
CCAS assembler compiler command (defaults to CC)  
CCASFLAGS assembler compiler flags (defaults to CFLAGS)  
CPP C preprocessor  
CXX C++ compiler command 一般是g++  
CXXFLAGS C++ compiler flags  
CXXCPP C++ preprocessor  
XMKMF Path to xmkmf, Makefile generator for X Window System

Optional Features:  
--disable-FEATURE do not include FEATURE (same as --enable-FEATURE=no)  
--enable-FEATURE[=ARG] include FEATURE [ARG=yes]  
--enable-shared[=PKGS] build shared libraries [default=no]  
--disable-float use double instead of single precision  
--enable-double same effect as --disable-float  
--enable-fortran use fortran (default on sgi,ibm,sun,axp)  
--enable-mpi compile for parallel runs using MPI  
--disable-threads don't try to use multithreading  
--enable-mpi-environment=VAR only start parallel runs when VAR is set  
--disable-ia32-3dnow don't build 3DNow! assembly loops on ia32  
--disable-ia32-sse don't build SSE/SSE2 assembly loops on ia32  
--disable-x86-64-sse don't build SSE assembly loops on X86_64  
--disable-ppc-altivec don't build Altivec loops on PowerPC  
--disable-ia64-asm don't build assembly loops on ia64  
--disable-cpu-optimization no detection or tuning flags for cpu version  
--disable-software-sqrt no software 1/sqrt (disabled on sgi,ibm,ia64)  
--enable-prefetch-forces prefetch forces in innerloops  
--enable-all-static make completely static binaries  
--disable-dependency-tracking speeds up one-time build  
--enable-dependency-tracking do not reject slow dependency extractors  
--enable-static[=PKGS] build static libraries [default=yes]  
--enable-fast-install[=PKGS]  
optimize for fast installation [default=yes]  
--disable-libtool-lock avoid locking (might break parallel builds)  
--disable-largefile omit support for large files

Optional Packages:  
--with-PACKAGE[=ARG] use PACKAGE [ARG=yes]  
--without-PACKAGE do not use PACKAGE (same as --with-PACKAGE=no)  
--with-fft=[fftw3/fftw2/mkl(>=6.0)/fftpack]  
FFT library to use. fftw3 is default, fftpack built  
in.  
--with-external-blas Use system BLAS library (add to LIBS). Automatic on  
OS X.  
--with-external-lapack Use system LAPACK library (add to LIBS). Automatic  
on OS X.  
--without-qmmm-gaussian Interface to mod. Gaussian0x for QM-MM (see website)  
--with-qmmm-gamess use modified Gamess-UK for QM-MM (see website)  
--with-qmmm-mopac use modified Mopac 7 for QM-MM (see website)  
--with-gnu-ld assume the C compiler uses GNU ld [default=no]  
--with-pic try to use only PIC/non-PIC objects [default=use  
both]  
--with-tags[=TAGS] include additional configurations [automatic]  
--with-dmalloc use dmalloc, as in  
<http://www.dmalloc.com/dmalloc.tar.gz>  
--with-x use the X Window System  
--with-motif-includes=DIR Motif include files are in DIR  
--with-motif-libraries=DIR Motif libraries are in DIR  
--without-gsl do not link to the GNU scientific library, prevents certain analysis tools from being built  
--with-xml Link to the xml2 library, experimental

---

## gmx4.5.5安装方法

RHEL6-U1 64bit, 2630QM, root  
  
#Install Intel Fortran Composer XE(Linux) 2011.1.107 to default folder (/opt/intel)  
  
#This step can be skipped if you want to use threats parallelization  
#In mpich2 1.4.1 folder:  
./configure  
make  
make install  
#Now mpich2 1.4.1 folder can be deleted  
  
#In fftw-3.3:  
./configure --enable-threads --enable-single --enable-sse2 --enable-avx F77=ifort --prefix=/sob/fftw3.3  
make -j 4  
make install  
#Now fftw-3.3 folder can be deleted  
  
#In gromacs-4.5.5 folder  
#If you prefer to use MPI parallelization, add --enable-mpi to below command  
./configure --with-fft=fftw3 --prefix=/sob/gromacs455 LDFLAGS="-L/sob/fftw3.3/lib" CPPFLAGS="-I/sob/fftw3.3/include" -enable-shared=no  
make -j 4  
make install  
#Now gromacs-4.5.5 folder can be deleted  
#Add "export PATH=$PATH:/sob/gromacs455/bin" to /root/.bashrc  
  
注：如果想用fortran编译内核，先export F77=ifort，并在./configure中加上--enable-fortran。然而性能并不会有丝毫提升，甚至还略微下降。threads并行和MPI并行在单机上效率差不多，前者并没体现出额外优势，只是方便了。
