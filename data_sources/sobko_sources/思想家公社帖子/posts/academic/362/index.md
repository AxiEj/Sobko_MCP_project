---
post_id: 362
title: 使用Multiwfn通过LOBA方法计算氧化态
url: http://sobereva.com/362
date: '2017-02-23T01:25:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 静电势与电荷
- 第一性原理
academic_relevant: true
classification_reason: 文章讲Multiwfn通过LOBA方法计算氧化态，属于软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**后记**：Multiwfn从2024-5-23更新的版本开始已支持对周期性体系计算氧化态，具体做法和例子见《使用Multiwfn结合CP2K计算晶体中原子的氧化态》（<http://sobereva.com/711>）。

**使用Multiwfn通过LOBA方法计算氧化态**

Calculating oxidation state using LOBA method in Multiwfn

文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2017-Feb-22   Last update: 2019-May-10

  

## 1 原理

讨论化学体系中的原子，特别是配合物中的金属的时候经常用到氧化态(oxidation state)这个概念。这是完全人为的概念，不是可观测的。用氧化态这个概念时相当于假定所有键都是纯粹的离子键，电子在原子间转移量是精确的整数。显然，这个假定对绝大多数情况都是极为糟糕的。懂量子化学的人不爱用氧化态这个虚构的概念，因为原子电荷能明显能更真实客观地描述原子在化学体系中的实际带电状态。但氧化态这个概念不能说完全没用，它对于将物质进行分类、归属、类比还是比较有益的。  
  
要注意原子电荷和氧化态根本没有对应关系。虽然原子电荷的计算方法多种多样，见见《一篇深入浅出、完整全面介绍原子电荷的综述文章已发表！》（<http://sobereva.com/714>）和《原子电荷计算方法的对比》（<http://www.whxb.pku.edu.cn/CN/abstract/abstract27818.shtml>）中的介绍，但没有任何一种原子电荷计算方法的结果能与氧化态直接联系起来，因为氧化态是把电荷转移显著人为夸大后的产物。比如OsO4大家都公认Os的氧化态是8（一般将O的氧化态当做-2然后根据体系净电荷来判断其余原子的氧化态），但是在B3LYP结合6-31G*和SDD计算的时候，几种方式算的Os的原子电荷值Mulliken=1.762、NPA=1.476、Hirshfeld=0.872、ADCH=0.939、AIM=2.540都远小于氧化态。实际中也往往会碰到这样的情形：两个配合物中，过渡金属的原子电荷只相差零点几，但按照经验判断的氧化态却相差个位数。所以不要妄图通过原子电荷判断氧化态。  
  
有些人提出了一些通过波函数分析来计算氧化态的方式，使得氧化态不依赖于人为经验的判断，而是可以根据一定规则确切地算出来：  
(1) Inorg. Chem., 50, 10259 (2011)、Polyhedron, 114, 128 (2016)  
(2) Phys. Chem. Chem. Phys., 11, 11297 (2009)  
(3) J. Chem. Theory Comput., 11, 1501 (2015)  
其中(2)的方法称作localized orbital bonding analysis (LOBA)，是所有三种方法里最简单、最容易实现的。Multiwfn从3.3.9版开始已经支持这种方法，在下面会结合实例介绍。Multiwfn程序可以在<http://sobereva.com/multiwfn>上免费下载，不熟悉Multiwfn的人建议看看《Multiwfn入门tips》（<http://sobereva.com/167>）。  
  
LOBA方法原理很简单，思路很易懂：首先将MO转化为定域化轨道(LMO)，然后依次计算各个LMO中的原子成份，若某原子对这个LMO的贡献值大于指定阈值（如50%），就认为这个LMO的电子完全归属于此原子。最后将原子的核电荷数减去归属到它上面的电子数即是其氧化态。  
  
获得定域化轨道的方式很多，LOBA原文里表示结果对于所用的定域化方法并不敏感。一般就用Multiwfn轨道定域化模块默认的Pipek-Mezey方法做定域化就行了，而且只需要将占据轨道部分做定域化就够了，记得此时绝对不能带弥散函数。详细信息可以看《Multiwfn的轨道定域化功能的使用以及与NBO、AdNDP分析的对比》（<http://sobereva.com/380>）。你也可以让量化程序用自带的定域化方法，产生包含定域化轨道的记录基函数信息的文件（如.fch、.molden）。

LOBA方法用的阈值有一定含糊性，多数情况用50%就行，但如果结果觉得诡异，可以适当调大再尝试，比如60%、70%。对于LOBA方法很适用的情形，感兴趣的原子的氧化态并不会随着阈值的这种程度的改变发生变化。如果结果对阈值特别敏感，则暗示LOBA方法并不适用于判断此原子的氧化态。

Multiwfn的LOBA功能计算原子对LMO的贡献的时候用的是Hirshfeld方法，此方法比较稳健。详见《谈谈轨道成份的计算方法》（<http://sobereva.com/131>）中的介绍。

## 2 实例

下面的例子用到的fch文件和对应的.gjf文件都在这个文件包中：[LOBA.rar](http://sobereva.com/attach/LOBA.rar)  
  

### 2.1 [Fe(CN)6]3-

这是很典型的氢氰酸根阴离子与铁阳离子形成的配合物。我们用B3LYP泛函，对Fe用SDD赝势基组，对配体用6-311G*基组对其优化。虽然这是阴离子体系，但用3-zeta基组完全足够合理描述波函数，并不需要非得加弥散，而且用Pipek-Mezey定域化时有弥散函数的话结果也会很不好。  
  
启动Multiwfn，输入  
Fe(CN)6_3-.fch   //Gaussian输出的chk文件转化成的fch文件  
19   //轨道定域化  
1   //只对占据轨道做定域化，这对LOBA分析够了  
此时Multiwfn把定域化后的轨道导出到了当前目录下的new.fch，然后自动载入之，此时内存里的轨道已经是定域化轨道了，可以开始做LOBA分析了。接着输入  
8   //轨道成分分析  
100   //LOBA方法计算氧化态  
50   //判断轨道归属的阈值用50%  
结果如下  
Oxidation state of atom   1(Fe) :  3  
Oxidation state of atom   2(C ) :  2  
Oxidation state of atom   3(C ) :  2  
Oxidation state of atom   4(C ) :  2  
Oxidation state of atom   5(C ) :  2  
Oxidation state of atom   6(C ) :  2  
Oxidation state of atom   7(C ) :  2  
Oxidation state of atom   8(N ) : -3  
Oxidation state of atom   9(N ) : -3  
Oxidation state of atom  10(N ) : -3  
Oxidation state of atom  11(N ) : -3  
Oxidation state of atom  12(N ) : -3  
Oxidation state of atom  13(N ) : -3  
The sum of oxidation states:  -3

可见，氧化态总和为-3，正好对应体系的净电荷。Fe的氧化态为3，十分合理。N的电负性比C大，所以氧化态是负值(-3)，C是正值(+2)，也很合理。

### 2.2 二茂铁

启动Multiwfn，载入Ferrocene.fch，一切操作同上一节，也用50%判断阈值，结果如下：  
Oxidation state of atom   1(C ) :  2  
Oxidation state of atom   2(C ) :  2  
Oxidation state of atom   3(C ) :  2  
Oxidation state of atom   4(H ) :  1  
Oxidation state of atom   5(H ) :  1  
Oxidation state of atom   6(Fe) :  2  
Oxidation state of atom   7(C ) :  2  
Oxidation state of atom   8(C ) :  2  
Oxidation state of atom   9(H ) :  1  
Oxidation state of atom  10(H ) :  1  
Oxidation state of atom  11(H ) :  1  
Oxidation state of atom  12(C ) :  2  
Oxidation state of atom  13(C ) :  2  
Oxidation state of atom  14(C ) :  2  
Oxidation state of atom  15(C ) :  2  
Oxidation state of atom  16(C ) :  2  
Oxidation state of atom  17(H ) :  1  
Oxidation state of atom  18(H ) :  1  
Oxidation state of atom  19(H ) :  1  
Oxidation state of atom  20(H ) :  1  
Oxidation state of atom  21(H ) :  1  
The sum of oxidation states:  32  
  
可见结论是Fe的氧化态为+2，这是很合理的。注意LOBA往往不能对体系中的每个原子都给出合理的氧化态，也因此虽然体系净电荷为0，但这里显示氧化态总和为32。即便把阈值设为其它值，氧化态总和照样不会成为应有的0。至于为什么会这样，思考LOBA的原理很容易理解，因为并非每个LMO都一定会归属到某个原子上，比如一个LMO当中A原子贡献了40%，B原子贡献了40%，C原子贡献了20%，那么当阈值设成50%的时候，LMO不会被归属到A、B、C中任意一个，因此这个LMO上的电子就废了。根据经验，LOBA给出的过渡金属的氧化态还是合理的。  
  
做LOBA的时候可以定义片段，LOBA给出的片段的氧化态往往比单个原子的更合理。我们考察茂环的氧化态，在LOBA界面里输入-1，然后输入一个茂环对应的原子序号范围，即输入1-5,7-11。之后再输入阈值50看结果，此时输出信息末尾多了一行：  
Oxidation state of the fragment:  -1  
说明茂环的氧化态是-1，这很合理，两个茂环以及Fe的氧化态相加恰为整体的净电荷0。  
   

### 2.3 顺铂

文件包里的cisplatin.fch对应的是b3lyp结合6-311G**以及Lanl2TZ(f)赝势基组计算的顺铂体系（顺式二氯二胺合铂），做LOBA分析操作同前，结果如下  
Oxidation state of atom   1(Pt) :  2  
Oxidation state of atom   2(Cl) : -1  
Oxidation state of atom   3(Cl) : -1  
Oxidation state of atom   4(N ) : -3  
Oxidation state of atom   5(H ) :  1  
Oxidation state of atom   6(H ) :  1  
Oxidation state of atom   7(N ) : -3  
Oxidation state of atom   8(H ) :  1  
Oxidation state of atom   9(H ) :  1  
Oxidation state of atom  10(H ) :  1  
Oxidation state of atom  11(H ) :  1  
The sum of oxidation states:   0  
  
铂的氧化态判断得很合理，是+2，和一般观念一致，而且随意把阈值提高一些也不会使得这个结论有所变化。对于NH3，把其中各个原子的氧化态加和，或者作为一个片段来算氧化态，结果都是0，也能说得通。而Cl的氧化态被判断为-1，也是合理的。  
   

### 2.4 OsO4

此体系用B3LYP结合6-311G*和SDD计算，LOBA分析操作同前，还是用50%阈值，结果如下  
Oxidation state of atom   1(O ) : -2  
Oxidation state of atom   2(O ) : -2  
Oxidation state of atom   3(O ) : -2  
Oxidation state of atom   4(O ) : -2  
Oxidation state of atom   5(Os) :  8  
The sum of oxidation states:   0

氧的氧化态是-2，Os是+8，和化学观念一致。

从本文的例子可见，基于Pipek-Mezey定域化轨道+Hirshfeld方法算的轨道成份做LOBA分析，用50%阈值，对于判断过渡金属配合物当中过渡金属的氧化态是合理的，起码对于本文的例子都表现得很好。

顺带一提，如果将Multiwfn的settings.ini里的outmedinfo设为1，则LOBA分析时会显示出各个LMO上的电子都被归属到了哪个原子、片段上，结合轨道图形和轨道成份，对于搞清楚LOBA给出的氧化态本质上是怎么来的很有帮助。
