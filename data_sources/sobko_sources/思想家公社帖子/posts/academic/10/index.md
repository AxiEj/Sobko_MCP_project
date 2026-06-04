---
post_id: 10
title: 解析gromacs的restraint、constraint和freeze
url: http://sobereva.com/10
date: '2015-06-02T18:09:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 分子动力学
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章解释GROMACS中的restraint、constraint和freeze，明显是软件与MD概念说明。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**声明**：此文最初发布于Sobereva的百度博客，后在网上被一堆博客胡乱转载，却不注明真正来源。此文真正原文在此！鄙视胡乱转载但是不注明出处的人！

**解析gromacs的restraint、constraint和freeze**Explanation of restraint, constraint and freeze of GROMACS  
  
文/Sobereva @[北京科音](http://www.keinsci.com)   写于约2008年

  
  
gromacs里面人为固定坐标有三大类方式：restraint、constraint和freeze，有各自的特点。  
  

### 限制(restraint)

包括位置限制(也就是常说的正式MD前首先要进行的限制性动力学)，角度限制，二面角限制，方向限制，距离限制。限制的特点是可以让被限制的东西在一定范围内运动，而非彻底固定住，实际上就是施加一个谐振势来限制其移动。

  
位置限制就不必说了，posre.itp里面[ position_restraints ]定义的就是，默认相对于最初位置进行限制。  
  
角度限制包括两类，一类是两对儿原子间角度的限制，用[ angle_restraints ]来指定，例如：  
[ angle_restraints ]  
; i   j    k    l    type   theta0     fc     multiplicity  
651 1211 1683 1211    1      67.0     1500         1  
说明限制651-1211与1683-1211原子对儿之间的夹角在67度附近，力常数为1500。type无用。  
角度限制另一类包括一对儿原子与z轴夹角角度的限制，用[ angle_restraints_z ]来指定，例如：  
[ angle_restraints_z ]  
; #1 #2  type  theta0    fc     multiplicity  
22  45     1     90      500         2  
说明限制22与45号原子的连线与z轴垂直，力常数是500，多重性是2，使得90度夹角时候限制势能最低，0和180度时最高。type无用。  
  
二面角限制使用[ dihedral_restraints ]段落来定义，实际上improper项就是用二面角限制方式限制的。例如  
[ dihedral_restraints ]  
;   i    j     k    l    type  label  phi  dphi  kfac  power  
    5    7     9    15     1      1  180     0     1      2  
被限制的是5,7,9,15原子组成的二面角，type总是1，label没用，phi是参考角，dphi是超过参考角多少度开始使用限制势，power没用。kfac乘上mdp中的dihre_fc将作为限制势力常数。  
最后在mdp中加入例如：  
dihre               =  simple  
dihre_fc            =  100  
dihre_tau           =  0.0  
nstdihreout         =  50  
  
距离限制在[ distance_restraints ]里面定义，比如  
[ distance_restraints ]  
; i j type index type low up1 up2 fac  
10 16 1 0 1 0.0 0.3 0.4 1.0  
type总是1，index是计算的顺序，如果几个项index都一样，比如10-28和10-46，就同时计算。势能图见gmx3.3手册p60，low,up1,up2分别指图上的r0,r1,r2，可见原子间距离在low至up1区间内是不受限制的，这种方式可以达成NMR限制。fac是指这个因子乘上mdp中disre_fc作为限制势力常数。  
也可以定义两个原子在[ bonds ]里用bond type 6，就是个和普通键一样的谐振子势，但是这两个原子间被认为没有键连。  
  
应当注意以上限制方式中[]段落应当紧接着写在被限制分子的.itp后面（或者说对应的[ moleculetype ]后面），这样程序才知道其中的原子编号指的是哪种分子中的原子。  
  
  

### 约束(constraint)

用shake或lincs方法固定住原子之间的相对位置，固定的几何关系是绝对不变的。分为两种类型，type 1和type 2的效果其实一样，但是type 1被认为将这两个原子键连了，而type 2没有键连。一般被键连的原子间都不计算相互作用(在[ moleculetype ]里定义nrexcl来控制相隔几个键内的原子间不计算相互作用，也就是相当于被列进[ exclusions ])，比如type 1时一般就不计算这两个原子间的非键作用了，而type 2时仍然计算。

用哪种约束算法用.mdp里的constraint_algorithm设定，默认lincs。.mdp里的比如constraints = all-bonds也是应用这种约束方法，也就是约束住所有[ bonds ]项，原本[ bonds ]的设定就被覆盖了，即不体现成键效果（来回振动），只体现约束效果（距离固定不变）。

自定义约束项可以在拓扑文件中这么写:  
[ constraints ]  
1 8 2 0.153    //原子1 原子2 type 约束的距离(0.153nm)  
之后1 8原子距离会固定保持在0.153nm，即便1 8原子在[ bonds ]中定义是成键的也是如此。  
注意，.mdp里如果写constraint=none，只是说批量约束hbonds、all-bonds等没有了，在拓扑文件中自定义的constraint约束项仍然生效。

顺便一提，在默认情况下，gromacs的水的结构是被settle算法约束住的，也就是所说的rigid水，settle就是专用于水的约束算法，在spce.itp里面[settles]即是定义，不计算分子内氢、氧彼此之间的相互作用。而如果.mdp里面设define=-DFLEXIBLE，也就是激活了#ifdef FLEXIBLE后面那段，则不用settle算法约束结构，而是照常按照谐振势的键长键角项控制水的结构。-DFLEXIBLE开不开对溶质没什么影响，对计算速度也没什么影响(有一丁点减慢可忽略)。除了能量最小化外，都不要用-DFLEXIBLE，因为拟合水、力场参数的时候都一般是认为水是刚性(rigid water)情况下进行的(比如SPC水和使用SPC水的GROMOS力场)，即约束住键长键角，开了FLEXIBLE实际上参数还得再作调整。而在gmx4中，在能量最小化时自动是限制方法(restraint)，就没必要设-DFLEXIBLE了，从此可忘掉它。.mdp中constraints以及constraint_algorithm设定皆与水的约束无关，除非define=-DFLEXIBLE，否则水都是用settle算法约束住。

### 冻住(freeze)

彻底冻在最初坐标，一点也不动。但仍然计算与其它原子间的相互作用，所以并不会省时间，除非是写进[ exclusions ]。

使用时在.mdp里面定义比如：  
freezegrps = protein   设蛋白冻住  
freezedim = Y Y Y    设冻住的方向，分别对应X Y Z轴。  
  
  
同时使用freezegrps, constraints, pressure coupling可能会有问题，不要组合使用。  
  
注意绝对坐标与相对坐标的限制方式的不同，比如想保持一个结构的刚性，用位置限制或freeze是原地不动，而通过约束方法对分子内的结构进行约束，结构仍然可以有整体平动和转动。应根据实际情况选择。
