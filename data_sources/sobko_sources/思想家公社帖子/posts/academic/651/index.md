---
post_id: 651
title: 详谈使用CP2K产生给Multiwfn用的molden格式的波函数文件
url: http://sobereva.com/651
date: '2022-08-31T22:27:00+08:00'
source_categories:
- Multiwfn
- CP2K
- 第一性原理
primary_topic: CP2K
secondary_topics:
- Multiwfn
- 结构与文件格式
- 可视化
academic_relevant: true
classification_reason: 文章详谈用CP2K生成供Multiwfn分析的molden波函数文件。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**详谈使用CP2K产生给Multiwfn用的molden格式的波函数文件**

On the using CP2K to generate wavefunction files in molden format for Multiwfn

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2022-Aug-31  Last update: 2026-Jan-9

## 0 前言

强大的波函数分析程序Multiwfn（<http://sobereva.com/multiwfn>）已经有很多分析功能支持免费又速度极快的CP2K程序产生的周期性波函数，诸如AIM拓扑分析、原子电荷计算、Mayer键级计算、轨道成分分析、绘制DOS图、模拟隧道显微镜图、空穴-电子分析、IRI/IGMH/NCI相互作用分析、计算ELF/LOL/密度差、轨道定域化，等等等等，目前已明确支持周期性体系的功能详见最新版Multiwfn手册2.9.2.2和2.9.2.3节的列表。我也写过一些CP2K结合Multiwfn做波函数分析的博文，参看<http://sobereva.com/category/CP2K/>。

用Multiwfn做周期性体系波函数分析需要CP2K产生记录原子、基函数、轨道等信息的molden文件作为输入文件，在本文将全面、详细介绍如何使用CP2K产生这样的文件。本文是对于当前Multiwfn最新版本而言的，对于CP2K是对>=8.1版的情况而言的，并且截止到本文最后更新时的最新CP2K版本来说都是适用的。如果你不了解Multiwfn，建议参看《Multiwfn FAQ》（<http://sobereva.com/452>）和《Multiwfn入门tips》（<http://sobereva.com/167>），另建议参看《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）以对Multiwfn的输入文件支持情况有更全面的了解。

如果你不熟悉CP2K，非常推荐通过**北京科音CP2K第一性原理计算培训班**（<http://www.keinsci.com/KFP>）完整系统地学习。

本文涉及到的文件可以在<http://sobereva.com/attach/651/file.zip>里得到，便于读者对照。

## 1 产生molden文件

在CP2K输入文件的&DFT字段中加入以下内容就可以在SCF收敛后在当前目录下产生.molden为后缀的文件

&PRINT  
  &MO_MOLDEN  
    NDIGITS 9  
  &END MO_MOLDEN  
&END PRINT

其中NDIGITS控制输出的轨道展开系数。上例要求绝对值大于1E-9的展开系数才会被输出。NDIGITS越大不仅输出的系数越多，系数保留的有效位数也越多，也因此在Multiwfn里分析结果越准确，但文件也相应地越大。NDIGITS的设置不影响在Multiwfn里的分析耗时。NDIGITS 9对于波函数分析的目的足够精确了。

在《使用Multiwfn非常便利地创建CP2K程序的输入文件》（<http://sobereva.com/587>）里专门介绍过使用Multiwfn创建CP2K输入文件的功能，在此界面里选-2将状态切换为Yes后再产生的输入文件即包含以上内容。

对任何CP2K支持的半经验级别的方法，比如GFN1-xTB、PM6、DFTB，CP2K都无法产生molden文件。顺带一提，Grimme的xtb程序倒是可以产生GFN-xTB级别下的波函数文件，可以用于Multiwfn做波函数分析，不过xtb主要面向的是孤立而非周期性体系。

考虑k点时也无法产生molden文件，因此晶胞必须足够大，不够大就需要扩成超胞来算。

对于MD等涉及结构变化的任务，加了以上字段后，默认每一步都输出一个molden文件，可以通过&MO_MOLDEN中的&EACH子字段控制对各种任务输出molden文件的频率。利用这个特征，可以令分子动力学模拟过程中不断产生molden文件，然后写脚本批量调用Multiwfn做波函数分析，以考察电荷、成键等方面随模拟过程的变化，还可以制作成动画。参考《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>）、《通过键级曲线和ELF/LOL/RDG等值面动画研究化学反应过程》（<http://sobereva.com/200>）、《制作动画分析电子结构特征》（<http://sobereva.com/86>）。

## 2 盒子信息的添加

molden文件没有标准的字段用来记录盒子（或称晶胞）信息，因此如果直接把CP2K对周期性体系产生的molden文件当Multiwfn的输入文件用，Multiwfn做的分析将无法考虑周期性，显然对于周期性体系来说得到的结果是明显错误的，至少是对于靠近盒子边界的原子来说。

为了让Multiwfn获得盒子信息，需要用文本编辑器打开molden文件，在里开头部分插入[Cell]字段，里面通过三行来分别定义盒子的三个平移矢量的X、Y、Z分量（以埃为单位），例如

[Molden Format]  
[Cell]  
 16.99927817     0.00000000     0.00000000  
 -8.49963911    14.72180676     0.00000000  
  0.00000000     0.00000000    22.46050431  
[Atoms] AU  
Cl       1      17       3.212398       1.854679      23.537502  
Fe       2      26       0.000000       0.000000      21.222101  
略...

显然可以直接把CP2K输入文件或者restart文件里的&CELL中的A/B/C后面的信息直接粘贴到[Cell]字段里。

也可以通过盒子的三个边长(a,b,c)和夹角(α,β,γ)来定义盒子信息，例如下面的写法定义a = 15 Å, b = 13 Å, c = 18.5 Å, α= 90°, β= 90°, γ= 121.3°  
[Cell]  
15 13 18.5 90 90 121.3

此外，如果你不想修改molden文件就能给Multiwfn提供盒子信息，可以在当前目录下创建一个叫[Cell].txt的文件，内容是本应写在[Cell]下面的信息，即对应三个平移矢量的三行信息，或者对应六个晶胞参数的一行信息。当Multiwfn发现molden文件里没有[Cell]字段而当前目录下有[Cell].txt，就会问你是否从此文件里读取（此特性从2022-Dec-17更新的Multiwfn才支持）。

## 3 有效核电荷数的添加

molden文件不记录原子的有效核电荷数（即元素序数减去被赝化的内核电子数，也即在计算中被基函数所描述的原子在孤立状态下的价电子数），因此当使用赝势时，若用molden文件作为Multiwfn的输入文件，原子电荷等涉及到核电荷数的分析功能的结果可能不正常。另外，Multiwfn内置了一套内核电子密度数据库EDFlib，只有当Multiwfn知道了原子被赝化了的电子是多少时，才能自动取用恰当的内核电子密度信息，这带来的好处是直接基于电子密度的分析结果将和使用全电子基组时基本一样，比如AIM拓扑分析可以找到核临界点、能产生出完整的键径。为了令Multiwfn在载入molden文件时能正确地得知有效核电荷数，需要用文本编辑器打开molden文件并手动修改。

有两种改法，第一种方法是把molden文件的[Atoms]字段里每个原子的第三列改为其有效核电荷数，比如  
 [Molden Format]  
 [Atoms] AU  
 Cl       1       7       3.212398       1.854679      23.537502  
 Fe       2      16       0.000000       0.000000      21.222101  
 Cl       3       7       0.000000       3.709358      18.906700  
略...

另一种办法是在molden文件头部插入一个[Nval]字段，里面记录各种元素的有效核电荷数，比如  
 [Molden Format]  
 [Nval]  
 Cl 7  
 Fe 16  
 [Atoms] AU  
 Cl       1      17       3.212398       1.854679      23.537502  
 Fe       2      26       0.000000       0.000000      21.222101  
略...

以上两种写法都代表Cl的有效核电荷数是7，Fe是16。

在当前用的赝势下，各种元素的有效核电荷数是多少可以去看基组定义，比如在CP2K的data目录下的BASIS_MOLOPT文件中可以看到有一行Cl DZVP-MOLOPT-SR-GTH DZVP-MOLOPT-SR-GTH-q7，其中q后面的数字就是有效核电荷数（价电子数）。在目前版本Multiwfn产生的使用GTH赝势的输入文件中，直接看BASIS_SET后面的基组名的q后面的值立马就知道有效核电荷数是多少。

有时候计算是在远程服务器上，如果由于特殊原因编辑molden文件不方便的话，可以在本机写一个文本文件，比如add.txt，里面是[Cell]和[Nval]字段，比如  
[Cell]  
 22.55600000     0.00000000     0.00000000  
-11.27800000    19.53406901     0.00000000  
  0.00000000     0.00000000     6.80000000  
[Nval]  
O 6  
N 5  
C 4  
  <---有空行

之后把add.txt上传，然后运行cat add.txt org.molden > final.molden，就把[Cell]和[Nval]字段加入到原先的org.molden文件开头，得到了可以用于Multiwfn做分析的final.molden。

## 4 关于轨道的记录

CP2K默认是不计算空轨道的，因此默认产生的molden文件里只有占据轨道信息，这对于只依赖于占据轨道信息的分析足矣，诸如原子电荷计算、Mayer键级计算、IRI/IGMH分析，但没法用于涉及到空轨道的分析，如电子激发分析、看空轨道图形、绘制DOS（涉及费米能级以上区域时）等。

对于使用对角化做SCF的情况，在&SCF里写ADDED_MOS N就会把最低N个空轨道也计算并输出到molden文件里。而OT则不兼容ADDED_MOS关键词。

注意Multiwfn内部要求基函数数目与轨道数目是相等的，比如你的molden文件定义了100个基函数，但只记录了20个轨道的信息，那么载入Multiwfn后会有100个轨道，其中21~100号轨道是空的（轨道系数、占据数、能量都为0）。

**2026-1-9注**：这一节下面的文字是对于CP2K <=2025.2版而言的。从2026.1版开始，OT计算产生的molden文件也正常记录了轨道能量，但以下文字依然有价值，因为OT无法直接利用ADDED_MOS求解空轨道。如果你之前用的是OT又想在molden文件里记录空轨道的波函数和能量需要用下面的方法1，如果仍非得要用OT又需要molden文件里有空轨道的能量需要用下面的方法2中的(2)。

用对角化时，轨道的能量会在SCF过程中计算并最终写入到molden文件里，然而OT方式的计算则无法直接向molden文件里写入轨道能量。molden文件里没有能量信息的话自然没法做牵扯到能量的分析，比如没法绘制DOS、STM图。用OT算大体系更快，对复杂大体系有时候不用OT还极难收敛。对于必须用OT又需要把轨道能量写入molden文件的情况，有以下两种做法：  
• **方法1：基于OT收敛的波函数做对角化**  
先做一次OT计算，完成之后在当前目录下会出现记录收敛的波函数的wfn文件（注意这和《高斯fch文件与wfn波函数文件的介绍及转换方法》<http://sobereva.com/55>里介绍的能被Multiwfn直接载入的那种wfn文件完全是两码事）。然后再用相同的设定做一次对角化的单点计算，并且要求产生molden文件、要求从wfn中读取之前收敛的波函数当初猜，有需要的话还可以同时再加上ADDED_MOS要求计算出空轨道。此时往往只需要一轮或很少几轮SCF迭代就可以完成（但有些情况也可能仍然难收敛），耗时很低，得到的molden文件里就有轨道能量信息了。举个例子，下面对Multiwfn文件包里examples\COF_12000N2.cif体系先用OT计算，然后做对角化计算以得到记录最低20个空轨道和轨道能量信息的molden文件，用的是CP2K 2022.1。启动Multiwfn，然后输入  
examples\COF_12000N2.cif  
cp2k  //进入产生CP2K输入文件的界面  
lycoris.inp  //要产生的CP2K输入文件名  
4  //从默认的对角化切换为OT  
0  //产生CP2K输入文件  
cp2k  //再次进入产生CP2K输入文件的界面  
lycoris2.inp  //输出的文件名  
4  //从OT切换为对角化  
-2  //要求产生molden文件  
-9  //其它设置  
12  //设置要求的空轨道数  
20  //算20个  
0  //返回  
0  //产生CP2K输入文件  
当前目录下的lycoris.inp是基于OT算单点的任务的输入文件，算完后当前目录下就有了lycoris-RESTART.wfn。然后把lycoris2.inp里的  
#   WFN_RESTART_FILE_NAME lycoris2-RESTART.wfn  
改为  
    WFN_RESTART_FILE_NAME lycoris-RESTART.wfn  
并把SCF_GUESS RESTART这行开头的#去掉以启用之。然后运行lycoris2.inp，算完后当前目录下就有了需要的lycoris2-MOS-1_0.molden。

• **方法2：让Multiwfn读取输出文件里的轨道能量**  
可以做OT时要求CP2K把轨道能量计算出来并输出到输出文件里，然后用Multiwfn（必须用2023-Oct-14及之后的版本）载入molden文件后，在主菜单里输入cp，再输入7，Multiwfn就会问你读取哪种情况输出的轨道能量（见下），并让你输入CP2K输出文件的路径，然后轨道能量就被读入Multiwfn了。CP2K有以下两种方式将轨道能量输出到输出文件里，都是加入到&DFT/&PRINT字段中：  
(1)加入以下信息后，SCF收敛后会输出全部求解出的轨道能量（用对角化时如果用了ADDED_MOS还会输出空轨道能量）  
&MO  
  ENERGIES T  
  OCCUPATION_NUMBERS T          
  &EACH  
    QS_SCF 0  
  &END EACH  
&END MO  
(2)加入以下信息后，SCF收敛后会显示所有占据轨道能量和最低3个（可自己指定）空轨道的能量。即便对于SCF过程中无法求解空轨道的OT也可以用这种方法得到空轨道能量。但注意此时用OT产生的molden文件里仍然只有占据轨道的波函数，**也因此没法用Multiwfn对空轨道部分绘制PDOS**（计算PDOS需要计算空轨道的轨道成份，这需要空轨道的波函数。因此此时只能是在TDOS曲线里体现空轨道）  
&MO_CUBES  
  NHOMO 1    
  NLUMO 3  
  WRITE_CUBE F  
&END MO_CUBES  
本文的文件包里h2o目录下是这种方式计算的例子，输入输出文件和molden文件都给了。Multiwfn载入h2o-MOS-1_0.molden文件后，依次输入cp、7、2、h2o.out的路径、3即可载入所有占据轨道和最低3个空轨道的能量。

如果你想检查molden文件里有没有轨道能量信息，把molden文件载入Multiwfn后，进入主功能0，左上角选择Orbital info. - Show occupied orbitals，从文本窗口里显示的能量上就能判断，如果molden文件没有能量信息的话所有轨道能量都为0。如果当前不方便进入图形界面的话，也可以进入主功能6的子功能3查看。

## 5 关于做波函数分析时基组的选用

CP2K用户通常使用CP2K开发者搞的MOLOPT系列赝势基组做计算，此系列基组用于波函数分析完全可以，但如果你是做实空间函数的分析（对三维空间中一批点做特定函数的计算），比如AIM拓扑分析、IGMH/IRI/ELF分析等，而且体系又很大、CPU又不给力，用MOLOPT系列的话在Multiwfn中的计算耗时会很高，主要在于MOLOPT系列基组是完全广义收缩基组，源高斯函数特别多。因此希望耗时更低的话，可以用诸如TZVP-GTH或更好的TZV2P-GTH赝势基组，其质量做波函数分析就算不错了。如果想用全电子基组，pob-TZVP是很好的选择，大小适中，精度也不错。

Multiwfn支持的分析当中有一部分在原理上是不兼容弥散函数的，如果基函数的弥散特征比较明显，分析结果会很糟糕，比如Mulliken分析、SCPA分析、Pipek-Mezey轨道定域化等。我实测发现这些分析往往不适合用诸如DZVP-GTH、TZVP-GTH这样的基组，因为有弥散程度较高的基函数。对这些分析可以用pob-TZVP，或者MOLOPT-SR-GTH系列基组。虽然MOLOPT-SR基组涉及的一些源高斯函数也有弥散特征（指数很小），之所以它此时能用是在于它是完全广义收缩的，并不独立存在弥散程度明显的基函数。

## 6 总结

本文详细介绍了如何用CP2K产生能给Multiwfn做波函数分析用的molden文件。最关键的就是这几点：  
(1)别忘了把盒子信息添加进去  
(2)用赝势时别忘了把有效核电荷数添加进去  
(3)需要空轨道时别忘了让CP2K求解空轨道  
(4)别忘了用OT时molden文件里默认是没有轨道能量信息的（对于2026.1以前版本而言）  
(5)注意基组的选择
