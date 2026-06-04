---
post_id: 517
title: 将Gaussian等程序收敛的波函数作为ORCA的初猜波函数的方法
url: http://sobereva.com/517
date: '2019-10-11T01:38:00+08:00'
source_categories:
- 量子化学
- ORCA
primary_topic: ORCA
secondary_topics:
- Gaussian
- 量子化学
academic_relevant: true
classification_reason: 标题直接讲将 Gaussian 等程序的波函数作为 ORCA 初猜，主软件是 ORCA。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**将Gaussian等程序收敛的波函数作为ORCA的初猜波函数的方法**

The method of using the converged wavefunction of Gaussian or other program as the initial guess wavefunction of ORCA

文/Sobereva@[北京科音](http://www.keinsci.com/)

First release: 2019-Oct-11  Last update: 2021-Oct-1

## 1 说明

ORCA是非常强大的量子化学程序，笔者之前也写过不少相关文章，开发了不少辅助工具，见<http://sobereva.com>右侧的ORCA分类，并且笔者在**北京科音高级量子化学培训班**（<http://www.keinsci.com/KAQC>）里对ORCA有超级全面深入系统的讲授。ORCA相对于最常用的量子化学程序Gaussian来说，有一个缺点是SCF收敛做得不够好，很多Gaussian能收敛的情况ORCA难以收敛，而且Gaussian的SCF不收敛的解决方案比较成熟，见《解决SCF不收敛问题的方法》（<http://sobereva.com/61>）。另外，ORCA在产生初猜波函数方面也没Gaussian灵活，比如Gaussian用户可以用GaussView构建片段组合波函数作为初猜，而且利用stable=opt关键词还可以自动优化出稳定的波函数，这对于双自由基、反铁磁性耦合体系的研究十分重要，参看《谈谈片段组合波函数与自旋极化单重态》（<http://sobereva.com/82>）。虽说ORCA也不是没法算这类自旋极化单重态体系，利用%SCF FlipSpin也可以实现，但往往明显不如Gaussian方便。

显然，如果能让其它量子化学程序，特别是波函数初猜以及SCF迭代方面做得很好的Gaussian产生的波函数作为ORCA的初猜波函数，就能令ORCA取长补短，从很多恼人的问题中解脱。

Multiwfn（主页&下载地址：<http://sobereva.com/multiwfn>）程序支持载入.fch、.molden、GAMESS-US/Firefly输出文件这些含有基组定义以及轨道信息的格式（在Multiwfn里称为“基函数信息”），并且可以导出各种含有波函数信息的格式，支持的文件格式详见《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）。Multiwfn支持绝大多数主流量化程序产生的波函数，并可以作为波函数文件格式的转换器来用。从2019-Oct-10更新的Multiwfn开始，Multiwfn的导出文件功能更是新增了产生.mkl文件的功能。.mkl文件是老版本Molekel的输入文件，可以被ORCA自带的orca_2mkl工具转换成.gbw文件，ORCA计算时可以从.gbw文件中读取轨道作为初猜波函数。显然，利用Multiwfn可以直接实现将其它量化程序产生的波函数作为ORCA的初猜波函数的目的。甚至可以说，只要存在一种量化程序有办法得到当前体系当前级别下收敛的波函数，用ORCA计算也一定能收敛。

有一点要提及的是ORCA是基于球谐型高斯函数做的计算，因此用Multiwfn实现这个目的，其它程序计算时也应当用球谐型高斯函数。不了解这方面的话看《谈谈5d、6d型d壳层基函数与它们在Gaussian中的标识》（<http://sobereva.com/51>）。

如果本文介绍的Multiwfn的功能给你的研究带来了帮助，**请在论文中引用Multiwfn刚启动时提示的Multiwfn程序的原文**，这是对Multiwfn开发和维护最好的支持！

## 2 例子：丁烷双自由基

这里举个例子，计算丁烷双自由基C4H8，用以说明如何将Gaussian收敛的波函数作为ORCA的初猜波函数，请大家举一反三。本例涉及的文件都在<http://sobereva.com/attach/517/file.rar>里。

本例使用2020-Jul-1更新的Multiwfn，Gaussian使用G16 A.03版，ORCA使用4.2版。

首先用Gaussian运行C4H8.gjf，内容如下。任务是对C4H8在B3LYP/def2-SVP级别下产生最稳定波函数，对此体系也是对称破缺波函数。使用def2-SVP的时候Gaussian默认用的是球谐型基函数。

%chk=C:\C4H8.chk  
# B3LYP/def2SVP stable=opt  
[空行]  
ub3lyp/6-31g(d) opted  
[空行]  
0 1  
 C                 -0.74400100    1.78566400    0.00000000  
 H                 -0.60282700    2.33865300    0.92499500  
 H                 -0.60282700    2.33865300   -0.92499500  
 C                 -0.74400100    0.30988100    0.00000000  
 H                 -1.25452600   -0.08746700    0.88463900  
 H                 -1.25452600   -0.08746700   -0.88463900  
 C                  0.74400100   -0.30988100    0.00000000  
 H                  1.25452600    0.08746700   -0.88463900  
 H                  1.25452600    0.08746700    0.88463900  
 C                  0.74400100   -1.78566400    0.00000000  
 H                  0.60282700   -2.33865300   -0.92499500  
 H                  0.60282700   -2.33865300    0.92499500

然后用formchk将chk转换为fch，载入Multiwfn后依次输入  
100  //其它功能 Part 1  
2   //导出文件  
9   //导出mkl文件  
C4H8.mkl  
y   //表明产生的mkl文件是给ORCA当初猜用，程序会做特殊处理  
现在当前目录下就有了C4H8.mkl。

在当前目录下运行orca_2mkl C4H8 -gbw，就把C4H8.mkl转换为了C4H8.gbw。下面，我们将C4H8.gbw里的轨道作为初猜波函数，用ORCA也在B3LYP/def2-SVP下跑一下这个双自由基的单点。输入文件如下，将之命名为C4H8.inp，把它和C4H8.gbw都放在当前目录下，然后进行计算。运行时ORCA会自动从C4H8.gbw中读取轨道作为初猜波函数。由于C4H8.gbw里的波函数是非限制性波函数，因此写了UKS关键词。由于ORCA的B3LYP和Gaussian的定义不同，所以加了/G来和Gaussian一致。此文件里的结构和上面Gaussian输入文件里的结构精确一致。

! UKS B3LYP/G def2-SVP miniprint nopop  
* xyz   0   1  
 C                 -0.74400100    1.78566400    0.00000000  
 H                 -0.60282700    2.33865300    0.92499500  
 H                 -0.60282700    2.33865300   -0.92499500  
 C                 -0.74400100    0.30988100    0.00000000  
 H                 -1.25452600   -0.08746700    0.88463900  
 H                 -1.25452600   -0.08746700   -0.88463900  
 C                  0.74400100   -0.30988100    0.00000000  
 H                  1.25452600    0.08746700   -0.88463900  
 H                  1.25452600    0.08746700    0.88463900  
 C                  0.74400100   -1.78566400    0.00000000  
 H                  0.60282700   -2.33865300   -0.92499500  
 H                  0.60282700   -2.33865300    0.92499500  
 *

迭代过程信息如下  
ITER       Energy         Delta-E        Max-DP      RMS-DP      [F,P]     Damp  
               ***  Starting incremental Fock matrix formation  ***  
  0   -157.0020361024   0.000000000000 0.00099750  0.00002892  0.0004319 0.7000  
  1   -157.0020389471  -0.000002844760 0.00101224  0.00002810  0.0003439 0.7000  
                               ***Turning on DIIS***  
  2   -157.0020411727  -0.000002225540 0.00299633  0.00007975  0.0002632 0.0000  
  3   -157.0020467355  -0.000005562801 0.00029108  0.00000721  0.0000572 0.0000  
  4   -157.0020467759  -0.000000040442 0.00006147  0.00000180  0.0000542 0.0000  
                 **** Energy Check signals convergence ****

               *****************************************************  
               *                     SUCCESS                       *  
               *           SCF CONVERGED AFTER   5 CYCLES          *  
               *****************************************************

可见由于用了Gaussian收敛的波函数当做初猜，收敛非常快和顺利，第一轮迭代时的能量和密度矩阵变化就已经极小了，之后很快就收敛了。之所以不是一轮就收敛，是因为Gaussian和ORCA用的DFT积分格点有异。如果二者都用的是HF方法的话，ORCA里仅仅一轮就能收敛。

如果gbw和输入文件不同名，为了能从gbw中读取初猜波函数，应当写上moread关键词，然后加上一行诸如%moinp "/sob/Azusa_Nakano.gbw"来指明读取的gbw文件位置。

为了让Gaussian收敛的波函数放到ORCA里能够收敛的概率尽可能高，有以下一些注意事项和建议  
(1)确保Gaussian里用的基组和ORCA里精确一致。比如Gaussian里用6-31G系列基组时，默认是用笛卡尔型d基函数，而ORCA总是用球谐型基函数，因此Gaussian计算时要写5d关键词（不过ORCA用户极少会用Pople系列基组，所以这无所谓）  
(2)让Gaussian计算时实际坐标与ORCA一致。Gaussian在计算时会自动将输入朝向摆到标准朝向，因此chk文件最后转出来的gbw里的笛卡尔坐标（标准朝向的）可能和ORCA计算时的不一样，因此要么ORCA输入文件里的坐标就用标准朝向的，要么Gaussian计算时候加上nosymm关键词避免摆到标准朝向下，详见《谈谈Gaussian中的对称性与nosymm关键词的使用》（<http://sobereva.com/297>）。  
(3)Gaussian为了节约电子积分计算的耗时，广义收缩基组如ANO，以及部分广义收缩基组，如Dunning相关一致性基组、Cl等一部分元素的6-311G系列基组，在计算的时候会自动把某些指数重复的primitive GTF给去掉。程序还会把收缩系数很小的primitive GTF给去掉。由于ORCA不自动做这种处理，可能导致个别情况下Gaussian里收敛的波函数拿到ORCA里还是难收敛或没法收敛。为避免这个问题，可以在Gaussian计算时加上int=NoBasisTransform关键词避免去掉任何primitive GTF，即基组原始怎么定义的就怎么用。如果你不清楚什么是（部分）广义收缩基组的话，**强烈建议总是带上这个关键词！**  
(4)建议带上IOp(3/32=2)关键词（尤其是带弥散函数时）避免Gaussian自动去除线性依赖的基函数，以确保和ORCA计算使用的基函数的一致性。  
(5)对于DFT计算，如果上面问题都已经考虑了，但放到ORCA里还是不能收敛，可以让Gaussian和ORCA在计算时都用更好的DFT积分格点精度，并且在ORCA里不开RI。

顺带一提，利用Multiwfn还能将其它量化程序产生的波函数作为GAMESS-US的初猜波函数，因为如果载入的波函数文件含有基函数信息，Multiwfn产生的GAMESS-US输入文件里可以直接带初猜信息。Multiwfn也可以将其它量化程序产生的波函数当Gaussian的初猜，因为Multiwfn可以导出fch格式，用Gaussian的unfchk转成chk后，就可以用guess=read来从中读取波函数当初猜了。若有不清楚的，参看前述的《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》。

## 3 chk到gbw的批量转换脚本

为了让大家可以更方便地把chk转换成gbw，笔者写了一个批量自动转换的bash小脚本chk2gbw.sh，可以在这里下载：<http://sobereva.com/attach/517/chk2gbw.sh>。运行前需要先把Gaussian、Multiwfn、ORCA都安装好，运行过程中会自动调用formchk、Multiwfn和orca_2mkl工具。

运行此脚本后，脚本会对当前目录下每个chk文件进行转换。比如有个文件叫popipa.chk，运行此脚本后会得到popipa_Gau.gbw，还会得到popipa.inp，这是ORCA输入文件，打开一看就会看到里面已经写了moread关键词和%moinp "popipa_Gau.gbw"，坐标和chk里的直接对应，因此用户现在只需要把定义计算级别的关键词改成实际情况即可开始ORCA计算。可见此脚本方便至极！

运行时输出信息示例：  
Converting B2H6.chk to B2H6.gbw ... (1 of 3)  
Converting C2H5F.chk to C2H5F.gbw ... (2 of 3)  
Converting CCl4.chk to CCl4.gbw ... (3 of 3)

## 4 gbw到chk的批量转换脚本

从2020年8月21日更新的Multiwfn开始，在其examples\scripts目录下提供了gbw2chk.sh文件，只要运行，就会把当前目录下的所有gbw文件转化为同名的chk文件，以便通过Gaussian使用guess=read关键词读取其中的波函数当初猜。运行前需要先把Gaussian、Multiwfn、ORCA都安装好。注：如果波函数是UHF/UKS计算得到的，必须用2021年10月1日及以后更新的Multiwfn。
