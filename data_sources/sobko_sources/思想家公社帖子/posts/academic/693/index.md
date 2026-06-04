---
post_id: 693
title: 使用Dalton通过CC3方法极高精度计算激发态
url: http://sobereva.com/693
date: '2023-12-30T12:35:00+08:00'
source_categories:
- 量子化学
primary_topic: Dalton
secondary_topics:
- 激发态与光谱
- 量子化学
- 结构与文件格式
academic_relevant: true
classification_reason: 重点是用Dalton做CC3激发态计算，主软件非常明确。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**使用Dalton通过CC3方法极高精度计算激发态**

Extremely high-precision calculation of excited states using the CC3 method in Dalton program

文/Sobereva@[北京科音](http://www.keinsci.com)   2023-Dec-30

## 0 前言

耦合簇方法可以通过线性响应（linear response, LR）计算激发态。在常见范畴内，精度和耗时关系是LR-CC3>LR-CCSDR(3)≈EOM-CCSD(T)>LR-CCSD=EOM-CCSD>=CC2。LR-CC3如今被普遍视为是激发态计算的金标准（多参考特征很强以及双电子激发特征占主导的情况除外），激发能能精确到零点零几eV。但LR-CC3结合像样基组只能算得动个位数原子，对更大体系则可以用明显更便宜的LR-CCSDR(3)，精度也已经非常好了。

Dalton程序在耦合簇方面功能丰富，可以做LR-CC3、LR-CCSDR(3)、LR-CCSD、LR-CC2激发能计算，对于LR-CC2/CCSD/CC3还可以得到包括振子强度在内的诸多跃迁属性。Dalton的输入文件对于初学者来说比较复杂抽象，本文用尽可能简单易懂的语言完整介绍一下用免费的Dalton做这些激发态耦合簇计算的方法，使用有C2v对称性的非常典型的分子甲醛为例。读者如果对Dalton不熟悉，务必先阅读我之前写的《量子化学程序Dalton的编译方法和运行方式简介》（<http://sobereva.com/463>），我假定读者已经认真看过此文。

值得一提的是，虽然Dalton做LR-CC3计算如今在文献中很常见，但Dalton在这方面不是最快的，而且代码还没有并行化。如果追求更好的效率，可以用专门做耦合簇计算的e^T程序（<https://www.etprogram.org>），它的LR-CC3是所有程序中明显最快的。另外，LR-CCSD激发能和振子强度没任何必要非得用Dalton计算，常用的Gaussian和ORCA的EOM-CCSD也都做得很好，结果和Dalton的LR-CCSD是等同的。Dalton做耦合簇的激发能计算不支持考虑溶剂模型，而G16的EOM-CCSD则可以。还值得一提的是，Dalton的衍生程序LSDalton还额外支持RI-CC2，可以比Dalton的LR-CC2更高效率地计算较大体系，这不属于本文的范畴。

本文涉及的输入输出文件都可以在<http://sobereva.com/attach/693/file.zip>里获得。计算用的是2023-Dec-22通过git下载的Dalton最新的开发版。

本文下面的例子首先要重复知名的TBE1激发能测试集（J. Chem. Phys., 128, 134110 (2008)）里的LR-CC3/def-TZVP算的甲醛的1-1A2、1-1B1、2-1A1三个单重态的垂直激发能。如文章表1所示，结果分别为3.95、9.18、10.45 eV。此文用的几何结构是MP2/6-31G*级别优化的，对应的结构文件是file文件包里的H2CO.xyz，本文的计算也将基于这个结构。

## 1 确定不可约表示顺序

为了指定各个不可约表示的激发态各算几个态，需要先知道C2v点群的各个不可约表示在Dalton程序中的顺序。最简单的方法是做个DFT单点计算，看一开始输出的不可约表示的顺序。为此，我们用Multiwfn（<http://sobereva.com/multiwfn>）创建这个任务的输入文件。启动Multiwfn，然后依次输入  
H2CO.xyz  
100   //其它功能（Part 1）  
2   //导出各种文件  
19   //Dalton  
DFT.dal  //在当前目录下产生DFT.dal，对应B3LYP/6-31G*计算设置  
H2CO.mol   //在当前目录下产生Dalton格式的体系定义文件H2CO.mol

由于当前计算要考虑对称性，因此把H2CO.mol里的Nosymmetry删掉。然后基于DFT.dal和H2CO.mol做计算，从输出文件DFT_H2CO.out里可以看到在SCF开始之前就输出了当前自动判断的点群，以及相应的各个不可约表示的顺序

@    Full point group is: C(2v)            
@    Represented as:      C2v

@  * The irrep name for each symmetry:    1: A1     2: B1     3: B2     4: A2

## 2 做LR-CC3激发能计算

写一个文本文件LRCC3.dal，内容如下（这是最简单写法，默认设置就已经适合的选项就没再做额外设置）

**DALTON  
.RUN WAVE FUNCTIONS  
**WAVE FUNCTION  
.CC  
*CC INP  
.CC3  
*CCEXCI  
.NCCEXCI  
2 1 0 1  
**END OF DALTON

对当前体系默认是做闭壳层HF计算得到参考态波函数。**DALTON控制任务类型，.RUN WAVE FUNCTIONS要求算单点并得到波函数。**WAVE FUNCTION设置波函数计算类型，.CC要求做耦合簇计算。*CC INP设置做什么形式耦合簇计算，.CC3要求做CC3计算。*CCEXCI要求做耦合簇的激发能计算，.NCCEXCI下面按照不可约表示的顺序指定各个不可约表示的能量最低激发态各计算几个。当前为了重复TBE1测试集的数据，要求A1算两个（由此得到1-1A1和2-1A1），B1算1个（得到1-1B1），B2不算，A2算1个（得到1-1A2）。

然后把前述的H2CO.mol复制为H2CO_TZVP.mol，手动把里面的6-31G*替换为Turbomole-TZVP，这是Dalton内置的def-TZVP基组的写法，对应Dalton目录下的basis子目录中的Turbomol-TZVP这个文件的名字。

然后基于LRCC3.dal和H2CO_TZVP.mol做计算，得到LRCC3_H2CO_TZVP.out。本节的文件都已经提供在了前述的file文件包里。打开输出文件，从里面可以看到如下激发能信息，2-1A1为10.44842 eV，1-1B1为9.18343 eV，1-1A2为3.94711 eV，可见和TBE1原文里的10.45、9.18、3.95 eV完全一致。表中||T1||是单激发贡献，和TBE1原文里给出的也是一致的。

 +=============================================================================+  
  |  sym. | Exci.  |        CC3        Excitation energies            | ||T1||  |  
  |(spin, |        +------------------------------------------------------------+  
  | spat) |        |     Hartree    |       eV.      |     cm-1       |    %    |  
  +=============================================================================+  
  | ^1A1  |    1   |     0.3502215  |       9.53001  |     76864.734  |  91.00  |  
  | ^1A1  |    2   |     0.3839723  |      10.44842  |     84272.170  |  91.32  |  
  +-----------------------------------------------------------------------------+  
  | ^1B1  |    1   |     0.3374848  |       9.18343  |     74069.360  |  90.93  |  
  +-----------------------------------------------------------------------------+  
  | ^1A2  |    1   |     0.1450537  |       3.94711  |     31835.610  |  91.16  |  
  +=============================================================================+

如果想要计算三重态激发态，就在.NCCEXCI下面的第二行定义。比如下面的写法，代表除了计算如上那些单重态激发态以外，还计算1-3A2和1-3A1三重态激发态  
.NCCEXCI  
2 1 0 1  
1 0 0 1  
如果不需要计算单重态激发态，就写  
.NCCEXCI  
0 0 0 0  
1 0 0 1

笔者试了几个Dalton版本，包括2016、2018、2022开发版，算出来的三重态激发能都是错的，和TBE1表2里的1-3A2和1-3A1三重态激发能明显不符，而且||T1||严重偏低，我认为是bug。如果不利用对称性，即.mol文件里带着Nosymmetry，并且.NCCEXCI下面直接指定计算的激发态的总态数，则问题轻得多，可以看到||T1||都显著高于90%。

值得一提的是LR-CC3是对激发态一个一个独立计算的，故算的态数越多耗时明显越高。

如果只需要计算CC3基态能量，去掉*CCEXCI及下面的部分即可，相对于LR-CC3算激发态部分的耗时来说可以忽略不计。

## 3 做LR-CC3激发能+振子强度的计算

如果对上面算的激发态还要计算振子强度，就创建LRCC3mom.dal文件，写入以下内容，然后进行计算。其中**INTEGRAL指定要算基函数之间哪些类型的积分，.DIPLEN要求算长度形式的偶极积分，这是因为算振子强度要算跃迁偶极矩，会用到这类积分。*CCOPA模块用来计算耦合簇的基态到激发态的跃迁属性，对当前用的Dalton版本支持CCS、CC2、CCSD、CC3，其中CC3仅限单重态激发态。.DIPOLE要求计算长度形式的跃迁偶极矩及振子强度。

**DALTON  
.RUN WAVE FUNCTIONS  
**INTEGRAL  
.DIPLEN  
**WAVE FUNCTION  
.CC  
*CC INP  
.CC3  
*CCEXCI  
.NCCEXCI  
2 1 0 1  
*CCOPA  
.DIPOLE  
**END OF DALTON

从输出文件（file文件包里的LRCC3mom_H2CO_TZVP.out）可以看到各个激发态的跃迁偶极矩和振子强度，比如2-1A1的如下所示，振子强度为0.34867845。这个值很接近TBE1原文表VII里这个态的LR-CC2和LR-CCSD振子强度（这篇文章里没给CC3的振子强度），分别为0.368和0.374。

     Transition from ground state to:  
      number, multiplicity, symmetry :    2  ^1A1   
      frequency :   0.3839722612 a.u.    10.44842 e.V.     84272.2 cm^-1

     +-----------+-----------------+-----------------+---------------------+  
      | operator  |   left moment   |  right moment   | transition strength |  
      +-----------+-----------------+-----------------+---------------------+  
      | XDIPLEN   |      0.00000000 |      0.00000000 |       0.00000000    |  
      | YDIPLEN   |      0.00000000 |      0.00000000 |       0.00000000    |  
      | ZDIPLEN   |     -0.83921304 |     -1.62309631 |       1.36212358    |  
      +-----------+-----------------+-----------------+---------------------+  
        oscillator strength (length gauge)   :      0.34867845

上面表格里的ZDIPLEN（偶极矩的Z分量算符）的transition strength值1.36212358对应的是跃迁偶极矩Z分量的平方。

如果你只需要跃迁偶极矩的特定分量，比如Z分量，可以把.DIPOLE改为  
.OPERATOR  
ZDIPLEN  
这样耗时会比计算所有分量时稍微低一点。

## 4 LR-CC2/CCSD/CCSDR(3)激发态计算

LR-CC2、LR-CCSD、LR-CCSDR(3)计算只需要把前面例子里的.CC3分别改成.CC2、.CCSD、.CCR(3)即可。注意LR-CCSDR(3)只能算激发能而无法算包括振子强度在内的跃迁属性。

这些级别的激发能计算的输入输出文件在file文件包里的other目录下都给了，耗时跟LR-CC3比都不值得一提。整体来说按LR-CC2、LR-CCSD、LR-CCSDR(3)的顺序，结果和金标准LR-CC3的越来越接近。比如它们的1-1B1激发能分别为9.348、9.257、9.186 eV，LR-CC3的为9.183 eV。所以LR-CC3激发能很难算得动的时候用LR-CCSDR(3)是很好的平替。

## 5 冻核设置

Dalton默认是不冻核的。显然恰当冻核可以节约耗时而几乎不影响精度。这里演示对H2CO做LR-CC3计算时冻结能量最低两个分子轨道（对应C和O的1s轨道）的方式。首先得得知它们的不可约表示，从之前B3LYP/6-31G*的输出文件中可以看到各个占据轨道能量的负值（Koopmans定理对应的电离能，相关知识参考《正确地认识分子的能隙(gap)、HOMO和LUMO》<http://sobereva.com/543>）。

@ Summary of DFT KT ionization potentials [eV]:

@ Symmetry 1 (A1 ) :   521.511     279.798      28.621      17.429      12.139

@ Symmetry 2 (B1 ) :    10.711

@ Symmetry 3 (B2 ) :    13.454       7.303

@ Symmetry 4 (A2 ) :  No IPs in this symmetry

显然能量最低两个轨道是A1。

写一个LR-CC3激发能计算输入文件LRCC3_FC.dal，内容如下。其中.FROIMP下面第一行指定对各个不可约表示冻结多少个能量最低占据轨道，下面第二行指定对各个不可约表示冻结多少个能量最高空轨道。当前冻结的是能量最低的两个A1轨道。

**DALTON  
.RUN WAVE FUNCTIONS  
**WAVE FUNCTION  
.CC  
*CC INP  
.CC3  
.FROIMP  
2 0 0 0  
0 0 0 0  
*CCEXCI  
.NCCEXCI  
2 1 0 1  
**END OF DALTON

从file文件包里的此任务的输出文件LRCC3_FC_H2CO_TZVP.out可看到，现在冻核后耗时是1分49秒，1-1B1激发能是9.18872 eV，之前没冻核时是3分32秒，1-1B1激发能是9.18343 eV。明显冻核对激发能的影响可完全忽略不计，而耗时大为降低，因而有重要实际意义。
