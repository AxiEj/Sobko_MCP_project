---
post_id: 395
title: 在Multiwfn中分析比CCSD更高级别波函数的方法
url: http://sobereva.com/395
date: '2017-11-28T00:07:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 波函数分析
- 量子化学
academic_relevant: true
classification_reason: 文章讲在Multiwfn里分析比CCSD更高级别波函数的方法，核心是波函数分析。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**在Multiwfn中分析比CCSD更高级别波函数的方法**

The way of analyzing wavefunction higher than CCSD level in Multiwfn   
文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2017-Nov-28  Last update: 2021-May-19  
  

## 1 前言

Gaussian程序能产生的最高级别的波函数是CCSD，虽然这已经非常精确了，比如在Science, 355, 49 (2017)中作者以CCSD密度为金标准，考察了不同泛函对电子密度的重现性，但是有时候由于特殊原因，就是希望在更高级别下做波函数分析。例如在J. Chem. Theory Comput., 13, 4753 (2017)中，作者对CCSD密度还不知足，于是以CCSDTQ密度为参考考察了不同理论方法对电子密度及衍生量的计算精度；再比如，在J. Chem. Theory Comput., 13, 2705 (2017)中，作者提出了基于自然轨道占据数将动态和静态相关图形化展现的方法（此方法在Multiwfn中支持，看3.4.1及之后版本手册4.A.6节的例子），文中用到了FCI级别自然轨道，以使得对文中所考虑的电子结构复杂的情况，静态和动态相关都能完美展现。  
  
能够产生比CCSD更高级别波函数的程序较少。PSI4可以产生最高到CCSD(T)级别波函数，MRCC可以产生无穷高阶耦合簇和无穷高阶CI的波函数（包括FCI。但是产生不了微扰近似版本的耦合簇的波函数）。Multiwfn程序能够结合这两个程序在这些比CCSD更高的理论级别做波函数分析，下面就说一下具体方法。本文使用的PSI4为1.2.1版，MRCC为Sept 25, 2017版。Multiwfn为官网上的最新版本，绝对不要用更老版本！  
  
对Multiwfn不了解者请参考《Multiwfn入门tips》（<http://sobereva.com/167>）、《Multiwfn波函数分析程序的意义、功能与用途》（<http://sobereva.com/184>）。在阅读本文之前应当先阅读此文《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）了解一些基本信息。  
   

## 2 结合PSI4在CCSD(T)级别下做波函数分析

PSI4网址为<http://www.psicode.org>。Linux下安装方法：去官网下载比如psi4conda-1.2.1-py36-Linux-x86_6.sh，然后运行之，按照提示操作即可，会自动下载所有要用的小程序和库。最后按照提示在用户目录下的.bashrc里添加环境变量，如  
export PATH=/sob/psi4/bin:$PATH  
 export PSI_SCRATCH=/sob/psi4scr  
  
下面示例输入文件用于产生氟化氢的CCSD(T)级别的密度矩阵，并在当前目录下输出HF_CCSDpT.fch文件。PSI4默认是不冻核的，如果要求冻核的话是没法产生CCSD(T)级别的密度矩阵的。  
molecule HF {  
 H        0.0        0.0       -0.831975  
 F        0.0        0.0        0.092442  
}  
  
 set basis cc-pVTZ  
 grad, wfn = gradient('CCSD(T)', return_wfn=True)  
 fchk_writer = psi4.FCHKWriter(wfn)  
 fchk_writer.write('HF_CCSDpT.fchk')  
注：如果你用的PSI4版本>=1.4，上例最后两行应当被替换为fchk(wfn,'HF_CCSDpT.fchk')。

将上面输入文件的内容存到比如test.inp里，然后运行psi4 test.inp test.out，即开始计算并产生输出文件test.out。  
  
得到的HF_CCSDpT.fchk里面记录的轨道是参考态HF级别的，而记录的密度矩阵则是CCSD(T)的。Multiwfn是基于轨道做波函数分析的，从输入文件里载入的也是轨道而非密度矩阵。因此，若以正常方式令Multiwfn载入这个.fchk，程序只会载入HF轨道，因此之后分析的也都是HF级别的情况。为了能让Multiwfn分析CCSD(T)波函数，需要做以下步骤：  
(1)将HF_CCSDpT.fchk载入Multiwfn  
(2)进入主功能200的子功能16  
(3)输入CCSD。此时Multiwfn就会载入此fchk文件里的Total CCSD Density字段的矩阵，由于当前PSI4做的是CCSD(T)计算，所以这个字段对应的是CCSD(T)密度。之后程序立刻输出了将CCSD(T)密度矩阵对角化得到的自然轨道占据数  
(4)输入y，这将在当前目录下导出new.mwfn，其中包含了CCSD(T)级别的自然轨道。然后Multiwfn会自动再载入之，此时内存里的密度矩阵、基函数的系数矩阵、GTF信息都是CCSD(T)自然轨道的了。之后任何分析也都是CCSD(T)级别的了

如果.fchk文件是对应开壳层体系，程序还会问你产生哪种类型的自然轨道，可以产生总密度对应的自然轨道、自旋密度对应的自然轨道、alpha/beta各自的自然轨道。更多相关信息可参考《在Multiwfn中基于fch产生自然轨道的方法与激发态波函数、自旋自然轨道分析实例》（<http://sobereva.com/403>）。

## 3 结合MRCC在高阶耦合簇/CI级别下做波函数分析

MRCC网址为<https://www.mrcc.hu>，下载预编译的包，解压到本机，将目录添加到PATH环境变量后即可直接使用。输入文件名必须叫MINP。运行诸如dmrcc |tee out.txt，就会启动MRCC，读取当前目录下的MINP，并将信息同时输出到屏幕和out.txt文件中。  
  
下面的输入文件内容用于在CCSDT/cc-pVTZ下计算氟化氢单点，并且产生相应级别的密度矩阵（若不写dens=1则只计算能量）。  
basis=cc-pvtz  
 calc=CCSDT  
 mem=2500MB  
 dens=1  
  
 geom=xyz  
 2  
  
 H        0.0        0.0       -0.831975  
 F        0.0        0.0        0.092442  
  
计算完毕后，会在当前目录下产生MOLDEN文件，这是Molden输入文件，里面记录的是参考态HF轨道。还输出了CCDENSITIES文件，可以用文本编辑器打开，第一部分记录了二阶约化密度矩阵(2RDM)，有四个标号；之后记录的是一阶约化密度矩阵(1RDM)，有两个标号（另外两个标号都是0）。这些密度矩阵以MO为基，标号是从第一个考虑电子相关的MO开始计的。我们也得像上一节那样，把1RDM转化成自然轨道存到.molden文件里，才能被Multiwfn利用并在当前级别下做波函数分析。  
  
启动Multiwfn，输入MRCC产生的MOLDEN文件路径，然后进入主功能1000的子功能97，输入CCDENSITIES文件的路径，然后输入有多少个轨道被冻结。MRCC默认是冻核的，当前体系有两个内核电子（输出文件中可看到Number of core electrons:     2），当前体系又是闭壳层的，每个占据轨道有俩电子，所以冻结的是1个轨道，因此输入1。之后Multiwfn会计算自然轨道，然后输出自然轨道占据数，会看到那个冻核的轨道占据数是精确的2.0，其它都是非整数。如屏幕上的提示所示，Multiwfn已将自然轨道输出到了一个.mwfn文件里。之后如果输入y，程序会直接载入这个.mwfn文件，之后做的各种波函数分析就都是CCSDT级别的了。  
  
MRCC做各种CI，以及FCI，也都是把密度矩阵输出到CCDENSITIES里。基于CI密度进行分析和上述完全相同。MRCC里做FCI很简单，把calc=后面写FCI即可。下面是在FCI/aug-cc-pVDZ下计算拉长的LiH的输入文件，不做冻核近似  
basis=aug-cc-pvdz  
 calc=fci  
 mem=2500MB  
 dens=1  
 core=0  
  
 geom=xyz  
 2  
  
 H        0.0        0.0      0.0  
 Li       0.0        0.0      3.0
