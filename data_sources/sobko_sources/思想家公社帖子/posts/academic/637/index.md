---
post_id: 637
title: ORCA结合Multiwfn计算RESP、RESP2和1.2*CM5原子电荷的懒人脚本
url: http://sobereva.com/637
date: '2022-03-08T06:12:00+08:00'
source_categories:
- Multiwfn
- 分子模拟
primary_topic: ORCA
secondary_topics:
- Multiwfn
- 静电势与电荷
academic_relevant: true
classification_reason: 标题是 ORCA 结合 Multiwfn 计算原子电荷的脚本。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**ORCA结合Multiwfn计算RESP、RESP2和1.2*CM5原子电荷的懒人脚本**

A lazy script for ORCA combined with Multiwfn to calculate RESP, RESP2 and 1.2*CM5 atomic charges

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2022-Mar-15  Last update: 2022-Aug-6

之前笔者在以下文章中提供了三个Linux shell脚本，分别用来自动调用机子里的Gaussian和Multiwfn程序实现一键计算1.2*CM5、RESP和RESP2原子电荷，它们对于做经典力场的分子动力学非常重要。  
计算适用于OPLS-AA力场做模拟的1.2*CM5原子电荷的懒人脚本  
<http://sobereva.com/585>（<http://bbs.keinsci.com/thread-21462-1-1.html>）  
计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）  
<http://sobereva.com/476>（<http://bbs.keinsci.com/thread-12858-1-1.html>）  
RESP2原子电荷的思想以及在Multiwfn中的计算  
<http://sobereva.com/531>（<http://bbs.keinsci.com/thread-16190-1-1.html>）

如今用免费的ORCA量子化学程序的人也很多，笔者写了不少相关博文（<http://sobereva.com/category/ORCA/>），在北京科音高级量子化学培训班（<http://www.keinsci.com/KAQC>）里对ORCA的使用还有非常全面深入的讲授。为了便于那些主要做分子动力学模拟、没买Gaussian又不太懂ORCA程序使用的人也能便利地计算上述原子电荷，笔者写了能自动调用ORCA和Multiwfn的计算那些电荷的Linux shell脚本。这些脚本提供在了Multiwfn程序文件包里（可以在Multiwfn主页<http://sobereva.com/multiwfn>免费下载），必须是2022年3月8日及以后更新的Multiwfn版本里才有，包括：  
examples\RESP\RESP_ORCA.sh：计算RESP电荷的脚本  
examples\RESP\RESP2_ORCA.sh：计算RESP2电荷的脚本  
examples\scripts\1.2CM5_ORCA.sh：计算1.2*CM5电荷的脚本

这些脚本的用法和前述帖子里介绍的基于Gaussian的脚本精确一致，需要留意的地方也都相同，只不过脚本中调用Gaussian的地方变成了调用ORCA而已，故不再累述用法。如果不会装ORCA的话看《量子化学程序ORCA的安装方法》（<http://sobereva.com/451>）。

这些脚本运行之前记得用文本编辑器打开，把ORCA=和orca_2mkl=后面的内容分别改为当前机子里实际的ORCA和orca_2mkl工具的路径。并把nprocs=后面的值改为计算时要调用的CPU核心数。脚本里maxcore=后面的值是ORCA的每个并行进程的内存使用量（MB）上限，与nprocs的乘积必须明显小于空余物理内存量，其默认值一般是合适的。如果空余物理内存不够则需要适度减小maxcore或nprocs，而如果要算几百个原子的大体系则需要适度加大maxcore，否则可能计算崩溃。

RESP_ORCA.sh和RESP2_ORCA.sh里默认用的优化级别和基于Gaussian的脚本（RESP.sh和RESP2.sh）有所不同，这里用的是ORCA才支持的B97-3c，因为这个级别做优化很快，结果准确度也不错。由于这个差异，以及ORCA和Gaussian在溶剂模型的实现上有所差异，所以基于Gaussian和基于ORCA的脚本得到的RESP或RESP2电荷可能有零点零几的差别，这点没必要在意，都是合理的。

关于使用脚本时哪些溶剂可以直接用、溶剂名怎么写，请在ORCA手册里搜“solvents in the SMD library”查看内置的溶剂名列表。注意ORCA里有些溶剂名是带空格的，对这种情况要把溶剂名用双引号扩住，例如./RESP2_ORCA.sh HF.pdb 0 1 "ETHYL ETHANOATE"。

如果你的输入的结构文件里的结构就已经足够好，不想让脚本自动再做优化浪费时间，可以用examples\RESP\目录下的RESP_ORCA_noopt.sh和RESP2_ORCA_noopt.sh分别代替前述的RESP_ORCA.sh和RESP2_ORCA.sh，它们的用法完全一样，只不过带_noopt后缀的不做优化步骤。

使用这些脚本计算原子电荷发表文章的话**必须在文中恰当引用Multiwfn**，引用方式在《Multiwfn FAQ》（<http://sobereva.com/452>）里明确说了。并且注意在网上提问、描述情况的时候要明确说是**使用本文提供的脚本，用Multiwfn基于ORCA产生的波函数计算RESP或RESP2电荷**（我在网上答疑时老看到有人说成是“ORCA计算了RESP电荷”，明显是大错特错，ORCA自己根本没有算RESP电荷的功能）。
