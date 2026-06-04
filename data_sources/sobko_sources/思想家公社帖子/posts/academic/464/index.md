---
post_id: 464
title: DFT-D4色散校正的简介与使用
url: http://sobereva.com/464
date: '2019-02-13T19:52:00+08:00'
source_categories:
- 量子化学
primary_topic: 弱相互作用
secondary_topics:
- 量子化学
academic_relevant: true
classification_reason: 文章讲DFT-D4色散校正的原理和使用，核心服务于弱相互作用计算。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.9
image_count: 0
local_assets_dir: assets
---

**DFT-D4色散校正的简介与使用**

Introduction and use of DFT-D4 dispersion correction

文/Sobereva@[北京科音](http://www.keinsci.com/)

First release: 2019-Feb-13  Last update: 2025-Apr-5

之前笔者在《DFT-D色散校正的使用》（<http://sobereva.com/210>）中详细介绍了DFT-D3的函数形式以及使用方法，还有其它相关的文章：《乱谈DFT-D》（<http://sobereva.com/83>）、《谈谈“计算时是否需要加DFT-D3色散校正？”》（<http://sobereva.com/413>）。大家如果对DFT-D3尚不了解的话请先阅读以上几篇。本文笔者简要介绍一下DFT-D3的后继者DFT-D4以及其实际使用方法。由于笔者精力有限，此文在原理方面就不写得很详细了。

## 1 关于DFT-D4方法

DFT-D3色散校正如今已极度流行，不光可以使那些计算弱相互作用差的泛函在计算弱相互作用精度方面有质的改进，对于计算很多中、大体系，特别是涉及过渡金属反应的热力学数据往往也有明显改进。DFT-D3最大的一个软肋就是没法考虑体系的实际电子结构。同种元素的原子，在不同化学体系中的电子结构显然是不同的，这从原子电荷上就可以直接体现出来。特别是过渡金属，在不同配合物里往往以不同氧化态形式存在，虽然其原子电荷的差异没有形式上的氧化态的差异那么夸张（参见《使用Multiwfn通过LOBA方法计算氧化态》<http://sobereva.com/362>里的一些论述），但是差异还是相当显著的。DFT-D方法计算色散校正能是基于原子的色散系数计算的，这从《DFT-D色散校正的使用》一文的公式里可以看得很清楚。实际上原子的色散系数是显著依赖于原子的电子结构的，特别是原子电荷这个直接表征原子在分子中带的净电荷的量对色散系数的影响是明显不可忽视的。但是由于DFT-D3没有考虑这点，而只纯粹依赖于体系的几何结构，当体系中存在显著带电的原子的时候，比如过渡金属配合物、离子化合物，DFT-D3在原理上就不是特别理想了（尽管从实际表现上来看，对于牵扯过渡金属的体系，用DFT-D3比不用一般还是明显有改进的）。

色散校正的方法很多，有的是像DFT-D3一样不考虑实际电子结构，如OBS、DFT-ulg；也有的是能体现实际电子结构的，如XDM、dDSC、TS、LRD、vdW-DF/VV10、MBD@rsSCS等。那些能体现实际电子结构的做法普遍比形式超级简单的DFT-D3更昂贵，编程实现往往更费劲，大多没有解析梯度，被主流程序支持得也比较少，比如笔者撰文时最新的G16 B.01一个都不直接支持，而ORCA 4.1.1版只支持VV10（也被叫做DFT-NL）。

为了解决DFT-D3的上述不足，Grimme在JCP, 147, 034112 (2017)中提出了DFT-D4，关键性的改进就是让原子色散系数与原子电荷挂钩，从而能更好地反应实际情况。2017年这篇文章实际上是DFT-D4的最初版，发表之后，Grimme一直也没公开提供能做DFT-D4计算的程序，令人觉得很莫名其妙，不禁猜测是不是DFT-D4还存在什么问题。后来在2018年7月，Grimme往ChemRxiv上上传了介绍DFT-D4最终版文章的v1版，在2019年1月25日又上传了这篇文章的v2版，参见<https://doi.org/10.26434/chemrxiv.7430216.v2>。我估计过不多久，这篇介绍DFT-D4最终版本的重量级文章就会正式在期刊上发表了。目前计算DFT-D4的程序已经公开了。  
后记：DFT-D4最终版的正式文章已发表于J. Chem. Phys. 150, 154122 (2019)。

根据这篇预印版的DFT-D4最终形式的文章，可以看到最终形式的DFT-D4会有以下特征：  
·和DFT-D3(BJ)一样使用BJ阻尼函数。目前DFT-D4已经对所有主流泛函都拟合了阻尼参数  
·带有和DFT-D3一样的Axilrod–Teller–Muto (ATM)形式的三体校正项。DFT-D4也可以结合MBD形式的三体校正项，但更为昂贵，而且实测的精度并没有ATM那么好  
·色散系数依赖于electronegativity equilibration (EEQ)方法计算的原子电荷。EEQ这个方法和已经很流行的EEM方法差不多，都是基于电负性均衡原理的思想，依赖于和元素有关的经验参数，可以瞬间计算很大体系的原子电荷。EEM的一些介绍可以看Multiwfn程序手册的3.9.15节  
·有解析梯度（Hessian目前只有半数值的）。这是VV10之类其它依赖于电子结构的色散校正方法所不具备的  
·最高支持到86号元素（Rn）  
·和DFT-D3一样基本上都是零耗时  
·根据Grimme的测试，DFT-D4的精度能达到VV10这样更复杂的色散校正方法的精度，甚至有时更好

对于那些不存在显著带电原子的情况，D4和D3精度半斤八两，至少不输于D3。而对于有显著带电原子的情况，D4比D3的改进还是挺明显的，除了上述提到的Grimme的D4相关文章里有体现外，还可以看他的Acc. Chem. Res., 52, 258 (2019)，里面专门展示了DFT-D3、D4在金属有机体系上的效果。

DFT-D4原理上也可以结合其它原子电荷。2017年那篇JCP里初代DFT-D4结合的是GFN-xTB方法（一种半经验形式的DFT方法，类似DFTB）计算时顺带产生的Mulliken电荷，结合这种电荷时被称为DFT-D4(TB)，但测试发现这种形式不仅算原子电荷的过程更麻烦（需要依赖于专做GFN-xTB的xtb程序），增加了耗时，结果还不如结合EEQ电荷的最终版DFT-D4好。

Grimme的文章也表示，DFT-D这种色散校正形式到了DFT-D4这一代就基本没有油水进一步可榨了。由于最终形式的DFT-D4计算又快效果又好，应该在未来会很快普及、被大量量化程序直接支持。而且笔者也认为，有了DFT-D4，VV10等绝大部分以往提出的能够展现实际电子结构的色散校正方法就可以彻底退出历史舞台了（但有个别这些方法由于仗着更高级的计算形式，精度可能做到比DFT-D4更高一些，所以还不是完全没存在意义）。

当然，未来肯定有很多DFT-D4相关的测试文章接踵而至，也不排除DFT-D4方法的定义又出现一些改变，以上说法只是笔者撰文时的情况和看法。

## 2 Grimme的dftd4程序

### 2.1 简介

Grimme写的独立的做DFT-D4的程序dftd4已经发布在了<https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/dftd4>，可以直接下载源代码包。下文说的是笔者2019年2月13日在此处下载到的dftd4.2.0.tar.xz的情况，以后版本可能有些地方会有变动。

这个DFT-D4程序用法、用处和DFT-D3很相似。由于此程序里面没有包含xtb程序，因此做的DFT-D4只能是基于EEQ电荷的（如上所述，这也正是标准的DFT-D4的情况）。此程序的三体校正项支持前述的ATM和MBD形式，因此确切来说，此程序可以算的DFT-D4具体形式包括DFT-D4(EEQ)-ATM和DFT-D4(EEQ)-MBD。

dftd4得先编译才能运行。为便于读者使用，按照本节做法编译好的Linux版和Windows版我直接提供在此：<http://sobereva.com/soft/dftd4.2.0_binary.rar>。其中有.exe的是Win32版（libiomp5md.dll是其运行时需要的动态库文件，应放到与之相同的目录），没后缀的是Linux版，都是可执行文件，直接就能运行。

### 2.2 最简单粗暴的编译方法

下面说一下如何以最简单的方式编译。

Windows 32bit版：笔者机子里装了Visual Studio 2017以及Intel Parallel Studio XE 2019 Update 1里面的Intel Fortran compiler和Intel MKL库。启动Visual Studio 2017，新建一个项目，把dftd4压缩包里的include目录下的.f文件和source目录下的.f90文件都放到项目的文件夹里，并且加入项目里。把编译的配置从默认Debug改为Release。之后在项目属性里，在Fortran标签页下把Libaries里的Runtime Library设成Multithreaded，Use Intel Math Kernel Library设Sequential。Language标签页里Process OpenMP Directives设Generate Parallel Code。之后如果你愿意的话还可以去设对CPU和指令集的优化选项，这里就不用了。然后对项目直接编译，项目目录下的Release目录里就产生了dftd4.exe可执行文件，直接就能用了，而且传给别人别人也能用。

Linux版：笔者的机子里已经装了Intel Fortran compiler 19.0.1.144和MKL数学库（是按照《VASP最简单的安装方法》<http://sobereva.com/455>里面的做法装的Intel Parallel Studio XE 2019 Update 1里面的）。将dftd4压缩包解压后，将include目录下的.f文件拷入source目录，再进入source目录，直接运行以下命令即在当前目录下产生了dftd4可执行文件  
ifort *.f90 -qopenmp -qopenmp-link=static -mkl -static-intel -stand f08 -check bounds -o dftd4  
其中那些带static的选项是为了让编译出的可执行文件不依赖于动态库，从而在别人的机子里也确保能运行。

### 2.3 标准但麻烦的编译方法

dftd4基于meson+ninja的代码生成系统组合，如果你想形式上最“优雅”地编译（其实没任何好处），需要系统里有meson和ninja。这俩玩意儿比较新，可能很多人不熟悉，这俩程序其实就相当于常见的cmake和make，只不过有一些额外的特点而已。笔者认为DFT-D4这么简单的程序用mason+ninja纯粹是莫名其妙，也给用户添麻烦，一般系统里都不自带它们，还得现装。下面我们来通过meson+ninja编译DFT-D4，机子里已经装了上述Intel Fortran编译器和MKL库。笔者也尝试了用此系统自带的gfortran 4.8.5，发现编译不过去。

先运行以下命令以安装meson、lapack静态库（顺带会安装blas静态库）、ninja。由于yum这么安装之后ninja的可执行文件名是ninja-build，所以得做个符号链接成为ninja  
yum install lapack-devel  
yum install meson  
yum install ninja-build  
ln -s /usr/bin/ninja-build /usr/bin/ninja

将下载到的DFT-D4程序的压缩包解压，进入此目录，直接将以下内容输入命令行窗口，就会通过ifort来编译  
FC=ifort meson setup build && ninja -C build  
然后在当前目录下的build目录下就出现了名为dftd4的可执行程序，可以直接用了。编译过程中终端里会提示什么不识别-pipe之类选项的警告，不用管它，只要程序能用就行了。如果想运行得更快，而且你的机子里有MKL库的话，可以把编译时依赖的lapack给替换为MKL库，把dftd4目录下自带的meson.build替换为我提供的这个即可：<http://sobereva.com/attach/464/meson.build>。

### 2.4 基本用法

在含有dftd4的目录下直接用./dftd4就可以显示出此程序可以接的选项，一看就懂，就不多说了。比如下面的命令是对H2O.xyz这个文件里的体系基于BLYP泛函的参数计算标准形式的DFT-D4，即DFT-D4(EEQ)-ATM形式的色散校正能  
./dftd4 H2O.xyz --func blyp

瞬间看到以下信息  
           -------------------------------------------------  
          |                Calculation Setup                |  
           -------------------------------------------------  
   coordinate file      : H2O.xyz  
   number of atoms      :      3  
   charge               :      0  
   non-additivity corr. : ATM  
   charge model         : EEQ  
   functional           : b-lyp  
   omp threads          :      1  
   memory needed (est.) :    0.0 Mb

 O      q(ref)        CN(ref)   cov. CN(ref)     α(AIM,ref)  
     0.0000000      0.0000000      0.0000000      5.1967092  
    -0.3547147      0.9924594      0.8041679      6.1223924  
    -0.5988153      1.9886928      1.6112394      6.7491941  
     0.0000000      0.9985672      0.9798440      5.1987934  
 H      q(ref)        CN(ref)   cov. CN(ref)     α(AIM,ref)  
     0.0000000      0.0000000      0.0000000      5.0540161  
     0.0000000      0.9117922      0.8942243      2.7207580

           -------------------------------------------------  
          |               Damping Parameters                |  
           -------------------------------------------------  
   s6                   :     1.0000  
   s8                   :     2.3408  
   a1                   :     0.4449  
   a2                   :     4.0933

           -------------------------------------------------  
          |                     Results                     |  
           -------------------------------------------------  
 Edisp  /kcal,au:    -0.2980  -0.00047485

dispersion energy written to file .EDISP

即色散校正能为-0.00047485 Hartree。如果你用cat .EDISP显示刚产生的.EDISP隐藏文件，会看到更高精度的数据：-0.00047485257046358403。

dftd4另外常用的选项是--chrg，用于设定体系净电荷；--grad，用于计算色散校正能的梯度；--hess，用于计算色散校正能的半数值的Hessian。

DFT-D4程序支持的泛函在dftd4源代码包里dfuncpar.f90里可以看到。在这个文件里搜get_d4eeqbjatm，凡是下面有名字的都可以用。值得一提的是，截止到2019-May-8，目前官网上的dftd4的这个参数库文件里仍没有常用的M06-2X泛函的参数，因此DFT-D4没法结合M06-2X使用。

## 3 在量子化学程序中使用DFT-D4

Gaussian从25版开始支持了DFT-D4。

ORCA从4.2开始，支持且只支持DFT-D4(EEQ)-ATM形式的DFT-D4，直接写个D4关键词即可使用。

CP2K从2024.2开始支持了DFT-D4。按照《使用Multiwfn非常便利地创建CP2K程序的输入文件》（<http://sobereva.com/587>）说的方式在创建输入文件时选择设置色散校正，里面可直接选D4。

Molpro从2018.1开始支持了DFT-D4。Turbomole从7.3也支持了DFT-D4。

对于不支持DFT-D4的Gaussian 16，如果想在计算中使用的话，可以利用《将Gaussian与ORCA联用搜索过渡态、产生IRC、做振动分析》（<http://sobereva.com/422>）和《将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC、做振动分析》（<http://sobereva.com/421>）里介绍的Gaussian的external关键词自己写个接口让Gaussian可以在计算能量、受力、Hessian的时候调用DFT-D4，实现起来很简单。
