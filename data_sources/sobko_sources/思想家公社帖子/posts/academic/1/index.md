---
post_id: 1
title: Amber力场二面角参数的解释
url: http://sobereva.com/1
date: '2015-06-01T13:25:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- 分子动力学
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章解释Amber力场二面角参数含义，属于AMBER与力场参数知识。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**Amber力场二面角参数的解释**Interpretation of dihedral parameters of Amber force field

文/Sobereva @[北京科音](http://www.keinsci.com/)    写于约2008年

在xleap中edit parm99时，进入参数修改界面，每个参数都有介绍。在二面角参数设置中，PK/IDIVF就相当于那些amber参数中nonbond项第二列参数(即Vn/2，也称作PK)除以第一列参数的值，第一列代表两端原子数乘积(即redundancy，也称作IDIVF)，所以PK/IDIVF意思相当于平均每二面角的势垒。Vn代表的是二面角旋转过程中势能最高时值，即torional barrier。E_tors = (PK/IDIVF)*(1+cos(PN*phi-PHASE))

像这样原子明确的二面角CT-CT-N-C，IDIVF都是1。而X-CT-CT-X这样两端可以是任意原子的，IDIVF是两边可以连接的原子数的乘积，比如这里CT每边都可以任意连3个，所以IDIVF是3*3=9。此时PK项是指这9个扭转项的总势垒的一半。

在参数的二面角项，有的PN是负值(PN即n，调整周期性)，这代表继续读下面的值，重复的就累加上(前面读了X-CT-CT-X这样的任意原子的项不算重复)。负值和正值是等价的，因为cos是偶函数。比如

```
   redundancy(IDIVF) Vn/2(PK)  phase           PN(m或n)
 H1-CT-C -O    1    0.80          0.0            -1.         Junmei et al, 1999
 H1-CT-C -O    1    0.08        180.0             3.         Junmei et al, 1999
```

说明这种扭转势能项需要同时用两个参数叠加才能拟合。

对于united-atom力场，比如frcmod.ff03ua，在parm99.dat中加入了C1、C2、C3三种原子类型和相应的参数，由于原子名不同，与ff99结合互不矛盾。C1代表CH原子团，C2代表CH2，C3代表CH3。united-atom力场的IDIVF数目不算H的，只算此原子上连的非氢的。所以乘的时候，C1算2，C2算1。比如X-CT-C2-X的IDIVF就是3*1=3。因为C2连了2个H，1个CT，只能和另外一个原子成键了。  
例如X-CT-C2-X    3    1.40          0.0             3.

一般文献给出力场参数都给出PK、phase、PN，有时给出IDIVF，如果没给，比如原始amber力场文献就没给出，根据原子特点自己推理一下就知道了。

在parm99.dat的扭转角列表后面，以X-X-C-O开始的那一堆，都是improper项，用于保持某些基团处于平面构型或者避免联合原子出现消旋。improper项与普通二面角项不同，其势垒高度不需要除以IDIVF，因此没有IDIVF项。其中第三个原子指的就是平面中心的原子。
