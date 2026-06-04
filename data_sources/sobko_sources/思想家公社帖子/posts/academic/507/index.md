---
post_id: 507
title: 让体系(跃迁)偶极矩平行于某个笛卡尔轴的方法
url: http://sobereva.com/507
date: '2019-08-24T20:51:00+08:00'
source_categories:
- 量子化学
- VMD
primary_topic: VMD
secondary_topics:
- 量子化学
- 可视化
academic_relevant: true
classification_reason: 文章介绍用 VMD 让偶极矩平行于笛卡尔轴的方法，属于软件操作技巧。
topic_family: 软件
exclude_reason: ''
confidence: 0.93
image_count: 0
local_assets_dir: assets
---

**后记**：此文用VMD的做法已经没有意义了，用Multiwfn来实现方便得多！仔细看《Multiwfn中非常实用的几何操作和坐标变换功能介绍》（<http://sobereva.com/610>）中的介绍，特别是2.6节的例子。

**让体系(跃迁)偶极矩平行于某个笛卡尔轴的方法**

Method to make (transition) dipole moment of a system parallel to a certain Cartesian axis

文/Sobereva@[北京科音](http://www.keinsci.com)  2019-Aug-24

## 1 前言

有时需要让分子的偶极矩、跃迁偶极矩（或者其它什么矢量）平行于某个笛卡尔坐标轴，这等价于令分子进行旋转。这有一些实际用途，例如：  
(1)在《使用Multiwfn分析Gaussian的极化率、超极化率的输出》（<http://sobereva.com/231>）里提到了第一超极化率(beta)顺着体系偶极矩的分量是可以通过EFISHG实验来确定的，这个量也是经常被讨论的。beta可以基于不同电场下计算的极化率(alpha)通过有限差分方法来计算。让体系偶极矩平行于某个笛卡尔坐标轴之后，beta在偶极矩方向的分量就可以通过在相应笛卡尔轴方向上加不同电场时得到的alpha来计算了。  
(2)在《使用Multiwfn计算（超）极化率密度》（<http://sobereva.com/305>）中提到beta可以通过超极化率密度的方式考察空间不同位置对beta的贡献，这需要对不同电场下产生的电子密度做有限差分计算。如果先让偶极矩方向顺着某个笛卡尔轴，那么在计算偶极矩方向的超极化率密度时，加电场时写起来就省事多了（比如Gaussian里只需要用诸如field=z+50这种关键词而不需要用field=read读取外电场矢量）。  
(3)在《使用Multiwfn绘制跃迁密度矩阵和电荷转移矩阵考察电子激发特征》（<http://sobereva.com/436>）中，笔者介绍了如何利用跃迁电偶极矩密度以及跃迁电偶极矩矩阵对决定两个电子态之间的概率大小的跃迁电偶极矩的本质进行讨论，而在Multiwfn里只能对跃迁偶极矩的X、Y、Z分量进行相应的考察。显然对大多数体系，跃迁电偶极矩不是恰好平行于某个笛卡尔轴的，此时就得先让跃迁电偶极矩平行于某个笛卡尔轴，之后才能用Multiwfn对其内在特征进行分析。

## 2 方法

让体系的某个矢量顺着笛卡尔轴最简单的做法是借助VMD提供的命令。VMD可以在<http://www.ks.uiuc.edu/Research/vmd/>免费下载。

将体系的结构文件（如.pdb、.xyz、.mol2）载入VMD后，如果这个体系的某个矢量是(-1.8916 0.7861 0.0)，输入以下命令就可以令这个矢量冲着X轴的正方向。  
set sel [atomselect top all]  
 $sel move [transvecinv "-1.8916 0.7861 0"]

如果要冲着Z轴正方向，接着输入  
$sel move [transaxis y -90]

如果要冲着Y轴正方向，则在$sel move [transvecinv...那条命令运行后输入  
$sel move [transaxis z 90]

## 3 例子

例如，使用Gaussian计算甲胺输出的偶极矩信息是  
X= -1.2918    Y= 0.4031    Z= 0.0000   Tot= 1.3532  
若想让偶极矩冲着Z轴正方向，就把输出文件载入GaussView，保存为pdb格式，再载入VMD，然后在VMD的命令行窗口将以下内容粘进去运行  
set sel [atomselect top all]  
 $sel move [transvecinv "-1.2918 0.4031 0"]  
 $sel move [transaxis y -90]  
之后用VMD的File - Save coordinates，将当前结构保存为.xyz格式文件，然后把里面的坐标拷到gjf文件里，用原先级别再做一次单点计算任务，并且同时写上nosymm关键词避免分子朝向被自动旋转到标准朝向（详见《谈谈Gaussian中的对称性与nosymm关键词的使用》<http://sobereva.com/297>）。从如下输出的偶极矩信息可见，确实此时偶极矩已经完全冲着Z方向了  
X=  0.0000    Y=  -0.0007    Z=  1.3532   Tot=  1.3532  
由上也可看到Y分量不精确为0，这是因为pdb格式保存的坐标只保留小数点后三位。如果先用GaussView保存成gjf格式，再手动修改成.xyz格式并载入VMD，则可以令坐标保持高精度。

顺带一提，如果你是希望让某个键平行于笛卡尔坐标轴，参看《让指定化学键平行于笛卡尔坐标轴的方法》（<http://sobereva.com/177>）。
