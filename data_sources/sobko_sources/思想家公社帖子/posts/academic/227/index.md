---
post_id: 227
title: 使用Multiwfn计算激发态间的跃迁偶极矩和各个激发态的偶极矩
url: http://sobereva.com/227
date: '2015-06-08T00:07:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 激发态与光谱
- 波函数分析
academic_relevant: true
classification_reason: 文章讲用Multiwfn计算激发态间跃迁偶极矩和各激发态偶极矩，属于软件功能教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**使用Multiwfn计算激发态间的跃迁偶极矩和各个激发态的偶极矩**Using Multiwfn to calculate transition electric dipole moment between excited states and electric dipole moment of each excited state  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)  
First release: 2014-Mar-28   Last update: 2022-Apr-13

## 1 前言

计算激发态之间的跃迁偶极矩有一些用处，比如用于sum-over-states (SOS)方式计算(超)极化率（详见<http://sobereva.com/232>）、计算激发态到激发态的吸收光谱（用瞬态吸收光谱技术可以测定）。Gaussian的CIS、TDHF、TDA-DFT、TDDFT计算可以直接给出基态到激发态的跃迁偶极矩。CIS和TDA任务也提供了alltransitiondensities关键词可以把激发态之间的跃迁偶极矩输出出来，但是对于TDHF/TDDFT任务则没有这个关键词（虽然Gaussian有个density=transition=(n,m)关键词可以产生n到m激发态的跃迁密度，然而这个关键词在目前的版本中貌似功能不正常，而且光是有跃迁密度也没用，还得利用偶极矩积分才能得到跃迁偶极矩，但Gaussian也并不给出这样的信息）。

强大的波函数分析程序Multiwfn的电子激发分析模块中的子功能5能够计算所有态（包括基态和激发态）之间的跃迁电和磁偶极矩，可以用于上述研究。此外，这个功能还可以直接给出各个激发态的电偶极矩，通过与基态的偶极矩求差就可以考察电子激发过程中偶极矩的变化。在本文就简要演示一下这个功能的使用。请读者务必使用官网上最新版Multiwfn，可以在http://sobereva.com/multiwfn免费下载。如果对Multiwfn一无所知的话，建议先阅读《Multiwfn入门tips》（http://sobereva.com/167）和《Multiwfn FAQ》（<http://sobereva.com/452>）。

对于Gaussian用户，使用Multiwfn的上述功能需要两类文件：(1)Gaussian的CIS、TDHF、TDDFT或TDA-DFT的输出文件 (2)相应任务产生的.fch/fchk文件。Multiwfn的这个功能不限于Gaussian用户使用，也支持ORCA、GAMESS-US等程序，详见Multiwfn手册3.21.A节的说明。

Gaussian的输入文件对于CIS和TDDFT，分别写成类似这样  
# B3LYP/6-31+G(d) TD(nstates=10) IOp(9/40=4)  
# CIS(nstates=10)/6-31+G(d) IOp(9/40=4)  
这里假设算10个激发态。Multiwfn计算时需要利用Gaussian输出的激发态的组态系数，默认情况下只有绝对值大于0.1的系数会被输出出来，而较小的都不输出，这样的话Multiwfn算出的结果将会不太准确。IOp(9/40=x)的含义是将系数大于10^-x的组态都输出出来，因此IOp(9/40=4)会把系数绝对值大于0.0001的组态都输出。x设的越大，输出的组态越多，结果越准确，但是x太大的话Multiwfn的耗时也会非常大，通常x=3或4就够了，精度足够，计算速度也比较快。

在计算之后得到了.out/.log文件，还同时得到了.chk文件。用formchk将.chk转换为.fch/fchk，这个文件里记录了基函数的定义以及基态轨道信息，这是Multiwfn要利用的。

## 2 实例

下面例子涉及的文件都可以在<http://sobereva.com/attach/227/file.rar>下载。

下面以苯酚为例进行说明怎么利用Multiwfn计算激发态之间的跃迁偶极矩，输入文件如下，计算后得到phenol.out以及phenol.fch。  
%chk=C:\phenol.chk  
# b3lyp/6-311G* TD(nstates=5) IOp(9/40=4)  
[空行]  
b3lyp/6-311G** opted  
[空行]  
0 1  
 C                  0.01810200   -1.86802400    0.00000000  
 C                  1.23175000   -1.16732400    0.00000000  
 C                  1.23175000    0.23407600    0.00000000  
 C                  0.01810200    0.93477600    0.00000000  
 C                 -1.19554600    0.23407600    0.00000000  
 C                 -1.19554600   -1.16732400    0.00000000  
 H                  0.01810200   -2.93802400    0.00000000  
 H                  2.15839700   -1.70232400    0.00000000  
 H                  2.15839700    0.76907600    0.00000000  
 H                 -2.12219300    0.76907600    0.00000000  
 H                 -2.12219300   -1.70232400    0.00000000  
 O                  0.01810200    2.36477600    0.00000000  
 H                 -0.88699500    2.68477600    0.00000000

启动Multiwfn，依次输入以下命令，//后面的是注释。  
C:\phenol.fch    //先载入电子激发任务产生的fch文件  
18   //电子激发分析功能，包含多个子功能。这些功能无与伦比的强大，建议参看《Multiwfn支持的电子激发分析方法一览》（<http://sobereva.com/437>）  
5    //计算激发态间的跃迁偶极矩  
C:\phenol.out    //电子激发任务的Gaussian输出文件  
此时屏幕上首先输出了激发态的汇总信息  
 Exc.state#     Exc.energy(eV)     Multi.   MO pairs    Normalization  
        1           5.11440           1         1478        0.500002  
        2           5.93650           1         1697        0.500000  
        3           6.14320           1          919        0.499999  
        4           6.67690           1          828        0.499994  
        5           6.90240           1         1593        0.499994  
其中N_pairs代表这个激发态在输出文件中通过多少组态来表示，IOp(9/40=x)的x越大显然N_pairs也就越大。Multi.是激发态的自旋多重度。Sum coeff.^2越接近理想值说明结果精度越高，对于闭壳层和开壳层情况理想值分别是0.5和1.0。如果偏离理想值比较大，则应该加大x来保证结果精度。

然后选1，激发态间的跃迁电偶极矩就输出到了屏幕上。也可以选2输出到当前目录下的transdipmom.txt里。程序先给出了基态的偶极矩，然后给出基态到各个激发态的跃迁偶极矩、激发能和振子强度：  
 Ground state dipole moment in X,Y,Z:   -0.554241   -0.157977    0.000000 a.u.

 Transition dipole moment between ground state (0) and excited states (a.u.)  
      i     j         X             Y             Z        Diff.(eV)   Oscil.str  
      0     1    -0.4634428    -0.0387809     0.0000000     5.11440     0.02710  
      0     2    -0.0410220     0.4644091     0.0000000     5.93650     0.03161  
      0     3     0.0000000     0.0000000     0.0024911     6.14320     0.00000  
      0     4     0.0000000     0.0000000    -0.0776262     6.67690     0.00099  
      0     5    -1.3520332    -0.2422995     0.0000000     6.90240     0.31905

接下来，输出的是激发态之间的跃迁偶极矩<i|-r|j>、能量差和振子强度。对于i=j的情况来说，其数值<i|-r|i>对应的是第i激发态的偶极矩的由电子贡献的部分（注意这不等于这个态的偶极矩，因为还有另一部分，即原子核电荷对偶极矩的贡献）。  
  Note: In below output the case of i=j corresponds to contribution of electron t  
o dipole moment of excited state i  
 Transition electric dipole moment between excited states (a.u.):  
     i     j         X             Y             Z        Diff.(eV)   Oscil.str  
     1     1    -0.5515307     0.6638909     0.0000000     0.00000     0.00000  
     1     2     0.1289203     0.0072212     0.0000000     0.82210     0.00034  
     1     3     0.0000000     0.0000000    -0.0575947     1.02880     0.00008  
     1     4     0.0000000     0.0000000     0.0104765     1.56250     0.00000  
     1     5     0.0412045     1.1173067     0.0000000     1.78800     0.05476  
     2     2    -0.5370763     0.7195150     0.0000000     0.00000     0.00000  
     2     3     0.0000000     0.0000000    -0.0271832     0.20670     0.00000  
     2     4     0.0000000     0.0000000     0.0723899     0.74040     0.00010  
     2     5     0.7076947    -0.0614123     0.0000000     0.96590     0.01194  
     3     3     2.0119437    -3.9241936     0.0000000     0.00000     0.00000  
     3     4     0.3712230     1.1487737     0.0000000     0.53370     0.01906  
     3     5     0.0000000     0.0000000    -0.0330295     0.75920     0.00002  
     4     4    -0.2932424     2.0434979     0.0000000     0.00000     0.00000  
     4     5     0.0000000     0.0000000     0.0048938     0.22550     0.00000  
     5     5    -0.4634208     1.0586426     0.0000000     0.00000     0.00000

值得一提的是，如果在Gaussian中使用下面这样的关键词，在输出文件末尾就会由L601模块输出第3个激发态的偶极矩  
# b3lyp/6-311G* TD(root=3,nstates=5) density=rhoci  
给出的结果为（debye）  
X=              5.1144    Y=             -9.9743    Z=              0.0000  
换算成a.u.单位后，结果为X=2.0119 Y=-3.9238 Z=0.0000，可见和Multiwfn给出的2.0119437    -3.9241936     0.0000000很相符。注意这里用了rhoci关键词，如果只写density的话，那么Gaussian传递给L601模块的激发态的密度是弛豫的密度。而当用rhoci时，传递的是非弛豫的密度，这才是和通过组态系数和基态轨道直接产生的密度直接对应的，也正是与Multiwfn输出的是对应的。

如果你想得到各个态之间的跃迁磁偶极矩，进入功能18的子功能5后先选0，选Magnetic，然后再按上面做法操作即可。注意跃迁磁偶极矩定义为-i<i|r×▽|j>，而Multiwfn输出的值对应的是<i|r×▽|j>部分，这和Gaussian输出文件里给出的跃迁磁偶极矩用的形式相同。

Multiwfn也可以直接给出各个激发态的包含了原子核贡献的偶极矩。也就是进入功能18的子功能5后选择4，结果就会输出到当前目录下的dipmom.txt中，内容为：  
  Note: The electric dipole moments shown below include both nuclear charge and electronic contributions  
 Ground state electric dipole moment in X,Y,Z:   -0.554241   -0.157977    0.000000 a.u.

 Excited state electric dipole moments (a.u.):  
  State         X             Y             Z        exc.(eV)    exc.(nm)  
     1     -0.551525      0.663891      0.000000      5.1144      242.42  
     2     -0.537071      0.719515      0.000000      5.9365      208.85  
     3      2.011949     -3.924194      0.000000      6.1432      201.82  
     4     -0.293237      2.043498      0.000000      6.6769      185.69  
     5     -0.463415      1.058643      0.000000      6.9024      179.62

PS：之所以这里把原子核对电子态的贡献也考虑后，偶极矩数值和之前只考虑电子贡献的时候一样，那是因为Gaussian默认会把体系原点放置到核电荷中心位置，此时原子核对偶极矩贡献恰好为0。
