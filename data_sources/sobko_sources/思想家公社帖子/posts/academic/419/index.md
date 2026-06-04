---
post_id: 419
title: 高性价比热力学组合方法G4(MP2)-6X的计算方法
url: http://sobereva.com/419
date: '2018-05-27T00:00:00+08:00'
source_categories:
- 量子化学
primary_topic: 量子化学
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章介绍G4(MP2)-6X热力学组合方法的计算方式，属于量子化学方法。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.92
image_count: 0
local_assets_dir: assets
---

**高性价比热力学组合方法G4(MP2)-6X的计算方法**

Cost-effective thermodynamics composite method G4(MP2)-6X

文/Sobereva @[北京科音](http://www.keinsci.com)

First release: 2018-May-26  Last update: 2019-Jul-30

在2011年，J. Chem. Theory Comput., 7, 112-120中，几个非Gn系列方法的官方人员提出了G4(MP2)-6X热力学组合方法，号称耗时与G4(MP2)相仿佛，而精度很接近昂贵得多的G4。其相对于G4(MP2)最主要变化是把MP2换成了SCS-MP2，把CCSD(T)的CCSD和(T)部分的相关能乘了系数，把优化和振动分析的泛函从B3LYP改为BMK。此方法竟然一直到当下最新的G16 B.01里都仍然没有被加入，好在文章的补充材料里给出了基于Gaussian做此方法计算的Perl脚本，使用很简单，这里简单说一下用法。原作者给的脚本只能输出H(0)和H(T)，没法输出指定温度下的自由能和内能，因此我对脚本进行了一些修改使之能够输出。  
  
首先需要编辑模板.gjf文件，内容如下，也可以直接从这里下：[G4MP2_6x.gjf](http://sobereva.com/attach/419/G4MP2_6x.gjf)。需要将此文件中的坐标、电荷和自旋多重度改成自己分子的情况  
%chk=mol.chk  
 # BMK/6-31+G(2df,p) Opt  
  
 A molecule G4(MP2)-6X calculation  
  
 0 1  
  C                  0.00000000    0.00000000   -0.56221066  
  H                  0.00000000   -0.92444767   -1.10110537  
  H                 -0.00000000    0.92444767   -1.10110537  
  O                  0.00000000    0.00000000    0.69618930  
  
 --Link1--  
 %chk=mol.chk  
 # Geom=AllCheck Guess=Read BMK/6-31+G(2df,p) Freq  
  
 --Link1--  
 %chk=mol.chk  
 # Geom=AllCheck Guess=Read CCSD(T,FrzG4)/GTBas1  
  
 --Link1--  
 %chk=mol.chk  
 # Geom=AllCheck Guess=Read MP2(FrzG4)/GTMP2LargeXP  
  
 --Link1--  
 %chk=mol.chk  
 # Geom=AllCheck Guess=Read HF/GFHFB3  
  
 --Link1--  
 %chk=mol.chk  
 # Geom=AllCheck Guess=Read HF/GFHFB4  
  
用Gaussian运行此脚本，产生比如G4MP2_6x.out。G09和G16经测试都可以用。  
  
下载此Perl脚本：[G4MP2_6x.pl](http://sobereva.com/attach/419/G4MP2_6x.pl)。把Gaussian输出文件文件和这个.pl文件都拷到Linux下，运行G4MP2_6x.pl G4MP2_6x.out，这个Perl脚本就会自动把相关数据从Gaussian输出文件中提取出来并进行处理，默认是在标况下算的。输出信息例子如下  
   Temperature (K)   298.15  
   Pressure (atm)     1  
   NImag     0  
   E_ele    -114.40450436  
   H(0K)    -114.37806386  
    H(T)    -114.37424742  
    U(T)    -114.37519161  
    G(T)    -114.39906286  
  
Nimag就是虚频数目，E_ele就是电子能量，其它的都不言自明，单位是Hartree。  
  
如果需要计算别的温度和大气压的情况，用文本编辑器打开.pl脚本，修改开头的$temp和$pres即可。

注：后来此方法的作者又提出了G4(MP2)-XK，把G4(MP2)-6X用的Pople基组改为了def2系列，使得此方法可以用于H~Rn的主族体系，对前四周期精度和G4(MP2)-6X相仿佛。在其原文DOI: 10.1021/acs.jctc.9b00449的补充材料里提供了相应的结合Gaussian使用的Perl脚本。
