---
post_id: 467
title: 简化用了IOp(9/40=x)的Gaussian的CIS/TDDFT任务的输出文件的程序：simpIOp940
url: http://sobereva.com/467
date: '2019-02-19T19:47:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- 激发态与光谱
academic_relevant: true
classification_reason: 标题和摘要明确是Gaussian的CIS/TDDFT输出简化工具，核心围绕Gaussian输出文件处理。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**简化用了IOp(9/40=x)的Gaussian的CIS/TDDFT任务的输出文件的程序：simpIOp940**

simpIOp940: A code to simplify the output file of CIS/TDDFT task of Gaussian with IOp(9/40=x)

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2019-Feb-19  Last update: 2019-Sep-26

## 简介

《Multiwfn支持的电子激发分析方法一览》（<http://sobereva.com/437>）一文全面介绍了Multiwfn支持的丰富的电子激发分析，其中有些功能是依赖于组态系数的。由于Gaussian默认情况下只输出绝对值大于0.1的组态系数，光靠这些对激发态描述的精度不够，因此对于Gaussian用户，用Multiwfn做那些电子激发分析时一般需要用诸如IOp(9/40=x)关键词来输出所有绝对值大于10^-x的组态系数（一般x=4）。但是此时造成的问题就是输出文件里的组态系数特别多，有人觉得通过这样的文件人工查看激发态主要信息不方便。

为解决这个问题，笔者写了个小程序simpIOp940，可在此下载：<http://sobereva.com/soft/simpIOp940.rar>

此程序可以载入用了IOp(9/40=x)的Gaussian输出文件，然后自行输入一个组态系数绝对值的阈值，程序就会把激发态的信息连同大于阈值的组态系数都输出出来，使得人工查看比较方便。另外，这个程序还会把各个激发态里系数绝对值最大的轨道跃迁输出出来，令指认主要跃迁类型更为方便。

此程序文件包里带.exe后缀的是Windows版可执行文件，不带后缀的是Linux版可执行文件，Fortran源文件也附上了。

## 例子

例如此程序的压缩包里有一个uracil.gjf，TDDFT计算时用了IOp(9/40=4)，算出来的文件时uracil.out，里面列出的组态系数特别多：  
 Excited State   1:      Singlet-A"     4.7968 eV  258.47 nm  f=0.0001  <S**2>=0.000  
       9 -> 30        -0.00071  
       9 -> 31        -0.00043  
       9 -> 35         0.00028  
       9 -> 67        -0.00011  
       9 -> 73        -0.00016  
       9 -> 76         0.00012  
       9 -> 78        -0.00015  
       9 -> 79        -0.00020  
       9 -> 81        -0.00011  
       9 -> 82         0.00023  
       9 -> 88        -0.00021  
       9 -> 89        -0.00059  
...略

启动simpIOp940之后，输入uracil.out的路径，然后输入阈值0.1，当前目录下会产生new.out，这是处理好的结果文件，内容如下

 Excited State   1:      Singlet-A"     4.7968 eV  258.47 nm  f=0.0001  <S**2>=0.000  
       26 -> 30         0.11588  
       28 -> 30         0.67734  
       28 -> 31         0.13625  
   
 Excited State   2:      Singlet-A'     5.4219 eV  228.67 nm  f=0.1317  <S**2>=0.000  
       27 -> 30        -0.13650  
       27 -> 31        -0.14060  
       29 -> 30         0.67086  
   
 Excited State   3:      Singlet-A"     6.0180 eV  206.02 nm  f=0.0000  <S**2>=0.000  
       26 -> 30         0.54135  
       26 -> 31        -0.20634  
       28 -> 30        -0.15424  
       28 -> 31         0.36715

当前目录下还出现了largest_pair.txt：  
       1      28      30   0.67734  
       2      29      30   0.67086  
       3      26      30   0.54135  
第一列是激发态序号，第2、3列是贡献最大的MO对，最后一列是系数。

由于电子激发任务类型很多，此程序不一定兼容所有情况，碰见不兼容时请自行修改程序。
