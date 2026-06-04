---
post_id: 4
title: gromacs决定力场参数的方式
url: http://sobereva.com/4
date: '2015-06-01T17:37:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 分子动力学
- 结构与文件格式
academic_relevant: true
classification_reason: 内容讲GROMACS力场参数的确定方式，属于软件与MD参数设置。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**gromacs决定力场参数的方式**The way of determination of forcefield parameter of GROMACS  
文/sobereva @[北京科音](http://www.keinsci.com)    2009-Apr-5

  
Q:  
43a1力场中，有的键长、键角、二面角都是空白的，只有原子的信息，这种情况是不是constraint啊？  
  
比如这样：  
  
   51    91     2           
   52    53     2    gb_4  
  
A:  
[bonds]里面指定了原子间连接关系，不管后面力场参数是不是空的，都说明原子是相连的。此时，如果在mdp里面设了constraint=all-bonds，所有[bonds]里面的键就会被约束住(不是按照距离远近判断，而是看[bonds]里面怎么连接的)。比如51 91 2后面虽然没写力场参数，此时也会被约束住。如果写了力场参数，则力场参数视为无效，也按约束来处理，用gmxdump -s察看.tpr，看不到它们处于成键项(比如810 type=366 (G96BONDS) 796 797)，而会看到处于约束项(比如672 type=429 (CONSTR) 796 797)。也就是说constraint的优先级最高。  
  
  
不同的力场决定成键参数的方式不同。对于设constraint=none的情况下有两种情况：  
对于GROMOS96力场来说，用什么参数只取决于grompp时读入的所要研究体系的.top(或者被include的.itp)，里面写了哪些力场参数就发挥哪些效果，没有写的力场参数就当作没有(被设为0)。比如[bonds]里写51 91 2，虽然指定了连接关系，但没写力场参数，又没有设约束，等跑起来之后就可能会逐渐远离。  
  
对于OPLSAA力场来说，哪些键用哪个力场参数是在grompp时根据原子类型来决定的(类似amber中leap程序的方式)，而不像GROMOS96那样在.rtp里面事先定义。OPLSAA力场在所要研究体系的.top(或者被include的.itp)里面只定义有键结项(本文中键结项泛指键长、键角、二面角)并不直接定义参数，例如：  
[ bonds ]  
   1     2     1  
......  
  
[ pairs ]  
    1     9     1  
......  
  
[ angles ]  
    2     1     3     1  
......  
  
[ dihedrals ]  
    2     1     4     5     3   
......  
这和GROMOS96力场处理方式截然不同。虽然[bonds]里1 2 1没定义参数，但是用gmxdump -s看tpr却发现连接1和2原子的键存在，模拟过程中也保持一定距离。这说明对于OPLSAA力场，grompp从.top(或者被include的.itp)获知的仅仅是有哪些键结项，这些键结项涉及的原子会通过开头[ atoms ]段里面的定义将原子序号转化为原子的type(如opls_136)，再由ffoplsaanb.itp的定义转化为bond_type(如CT)，再从ffopsabon.itp里面找到对应参数，放进.tpr里面，在模拟过程中生效。  
  
  
对于[bonds]里的内容处理方法简单来说就是，设了constraint=all-bonds，不管什么力场，[bonds]里写了哪些项就约束哪些。如果constraint=none，用GROMOS96力场时有项有参数的就起作用，有项没参数就等于没写。OPLSAA里面有项没参数也起作用。  
  
PS：关于自定义constraints的情况可参考《解析gromacs的restraint、constraint和freeze》（<http://sobereva.com/10>）。  
  
善用gmxdump -s察看.tpr是最可靠的方法。  
  
  

---

  
  
在这里我将问题扩展一下，说一下gromacs决定键结参数的机制。实际上OPLSAA力场与GROMOS96力场都是遵循同样的方法来处理，但是如上所述，决定键结参数有很大区别，并非因为程序对它们处理机制的差异，而是力场参数文件的差异。下面都不考虑约束问题。  
  
例如用某个力场，研究的体系的.top里面的一个普通的成键定义：  
[ bonds ]  
   1     2     1    ga_1                //注意第二个1代表函数类型，不是原子号  
首先gmx会用C预处理程序(一般就是cpp)将ga_1还原为实际的参数，转换关系定义在ff????bon.itp里，在grompp时加上-pp，从得到的processed.top中就会看到ga_1被还原了。当然如果ga_1位置直接写的就是参数，就不必转换了。这样1和2之间的键参数就定下来了。  
  
另一种情况，虽然定义了成键项，但没写参数：  
[ bonds ]  
   1     2     1  
那么程序会首先将根据原子序号，在[ atoms ]里面查找到对应的原子类型，比如转换为CH2 N，然后按照原子类型到ff????bon.itp里面的[ bondtypes ]里面找原子类型相对应的参数，找到了就定下来了，如果没找到，在grompp的时候就会出Warning提示这个键的参数被设为0，相当于不存在。  
  
GROMOS96与OPLSAA定义力场参数的差异就在于它们的ff????bon.itp的内容。  
比如GROMOS96的ffG43a1bon.itp里面[ bondtypes ]几乎没有什么内容，只是二硫键和血红素用的几个键的定义。所以必须在[ bonds ]里面直接写出参数(这步由pdb2gmx完成，主要将.rtp里面的相应残基的键/角/二面角项和参数搬过来)，否则在ffG43a1bon.itp的[ bondtypes ]里也不会找到参数，那个成键项等于没有被定义。  
而比如OPLSAA的ffoplsaabon.itp，[ bondtypes ]里面包含了全部OPLSAA力场的成键项，所以就不必在体系.top的[ bonds ]里面直接写参数，grompp时在这里一般都能找到对应的。在ffoplsaa.rtp里面定义的除了原子电荷外，主要就是残基的连接关系，也就是[ bonds ]，没有参数，在[ angles ]和[ dihedrals ]里面几乎没有内容或者根本没有。这种情况下pdb2gmx的主要作用除了把.rtp的对应内容直接搬到.top里面以外，另一个主要工作就是根据连接关系自动补全角和二面角项，所以.top里面看到的键/角/二面角项是全的，如上所述没有写参数。  
  
从大体来说，实际上GROMOS96力场是有些特殊的，它直接在rtp中事先定义好了全部键结项和参数，top也包含全部键结项和参数，grompp调用的参数直接取自top。而OPLSAA则算是比较普通的情况，rtp只定义连接关系，在top中更进一步把全部的键结项表达出来，该用什么参数等grompp时再去从力场参数库中搜。amber的leap也是如此，载入结构载入的只是连接关系，各个键结项用的参数在saveamberparm的时候对应去搜。  
  
决定angle、dihedral的参数与决定bond的方式相同。另外如果比如[ bonds ]里面已经写了参数，同时在[ bondtypes ]里面也能找到原子类型对应的参数，则优先使用在[ bonds ]里面直接写的。  
  
这里再说一下对二硫键等特殊键的处理方式。pdb2gmx读取结构时，也载入specbond.dat，specbond.dat内如如下  
6  
CYS    SG    1    CYS    SG    1    0.2    CYS2    CYS2  
......  
这就说明如果发现在同一个链上有两个CYS上的SG间的距离在0.2nm附近(注意不是仅仅指的在0.2nm以内)，就认为这两个SG成键，并且残基名由CYS变成CYS2。这时这个半胱氨酸的参数就用的.rtp里面CYS2残基的参数，加氢时也使用.hdb里面CYS2残基的加氢方式而非默认的CYSH，也就是硫上面不加氢。在.top里面可以看到出现了这两个硫原子之间的成键项以及相关的角、二面角项，但是没有参数(无论是GROMOS还是OPLSAA)，这就说明要从比如[ bondtypes ]里面读对应的参数，这就是为什么比如ffG43a1bon.itp的[ bondtypes ]里面有S S 2 gb_33这样的二硫键参数定义。硫原子的原子名是SG但是原子类型是S，所以二硫键和这个参数项对应。对于血红素的一些特殊成键也是这么处理的。  
也可以自行添加、修改specbond.dat的内容来处理类似的特殊情况。  
  
  

---

  
这里也说说非键作用和1-4作用，下文所指的非键作用不包括1-4作用。  
  
**非键作用：**  
  
对于VDW参数的确定，GROMOS96力场在ffG43a1nb.itp里面的[ nonbond_params ]中提供了各种各样原子类型的组合，计算i、j两个原子间的VDW作用时会根据原子类型对应获得C(ij)参数(包括C6和C12项)。若计算两个原子间VDW作用时，发现[ nonbond_params ]里面没有对应的，就通过组合方法确定，从[ atomtypes ]中得到原子i的C(i)与原子j的C(j)，由于ffG43a1.itp里面comb-rule设的是1，会根据(C(i)*C(j))^1/2公式来获得C(ij)。由于OPLSAA并没有[ nonbond_params ]段，故所有C(ij)项都是如上算出来的(OPLSAA的comb-rule是3，详见手册)。  
  
对于静电作用，只依赖于原子电荷，没什么特殊的。  
  
要注意，在拓扑文件中的[ moleculetype ]段中，nrexcl决定了相隔多少个键以内不计算非键相互作用，例如nrexcl=3时，与某个原子相隔5个及以内的原子间都不计算非键作用。一般为3，即表明直接bonded的两个原子、构成angle项两端的两个原子，以及构成二面角项两端的两个原子都不计算非键作用。  
  
  
**1-4作用：**  
  
1-4作用项虽然看起来也属于非键作用，常被称为1-4非键作用，但gromacs对它的处理与非键作用完全不同。1-4作用包括库仑1-4和1-4VDW相互作用，哪些原子间有1-4相互作用都定义在体系.top里面[ pairs ]，里面每一项就是一个1-4作用项，如果没写就说明这两个原子间不拥有1-4相互作用（即便从成键关系上属于1-4关系的原子也不算）。如果两个原子包含在1-4作用项中，则不计算它们的非键作用，相当于从非键列表中排除了。nrexcl对1-4作用完全无效，根据nrexcl的设定，即便某两个原子间不计算非键作用，若存在于1-4作用项中，也会照常计算1-4作用。即nrexcl只管非键作用。  
  
1-4作用项中的库仑1-4作用，就是根据1-4原子间原子电荷照常计算静电作用然后乘以FudgeQQ(在比如ffoplsaa.itp的[ defaults ]中定义)。  
  
1-4作用项中的1-4 VDW作用，所用C(ij)参数与非键VDW中的不同，需要额外的参数，但是GROMOS96和OPLSAA的体系.top在[ pairs ]里默认都没写参数，这是因为：  
  
GROMOS96力场，明确定义了各种原子类型组合的1-4VDW参数，全部储存在比如ffG43a1nb.itp里面的[ pairtypes ]当中，体系.top里面[ pairs ]当中定义的每一个1-4VDW项的参数都从这里对照原子类型自动提取。在ffG43a1.itp当中会看到gen-pairs设为了no，意思是如果读不到对应的1-4VDW参数，就出现warning并将参数用0值代替。  
  
OPLSAA力场，各种原子类型之间的1-4VDW作用都是普通VDW作用乘以FudgeLJ因子0.5计算得到，也就是进行削弱(GROMOS96定义的1-4VDW参数也是被削弱的)，在ffoplsaa.itp里面可以看到gen-pairs被设为yes，意思是读不到的1-4VDW参数都通过上述方法计算生成。实际上ffoplsaanb.itp里面根本就没有[ pairtypes ]，所以如果不做人为修改，1-4VDW参数都是通过计算生成。  
  
如果直接在[ pairs ]当中的项的后面给出参数，这些项就直接用给的参数当作1-4VDW的参数。如果直接给的参数为0，或者没直接给参数、在ff????nb.itp里的[ pairtypes ]也没有对应项、而且把gen-pairs设为了no，则参数值会默认为0，这两种情况下1-4VDW作用效果皆为0。但此时1-4静电力仍会照常计算，除非把FudgeQQ也设为0，则彻底不计算1-4作用了。  
  
不计算1-4作用实际上有两种情况：一种是不写[ pairs ]的情况，1-4作用完全忽视掉，程序根本不算。另一种是写了[ pairs ]，程序也算了，但是因为上面一段所述的参数和设定原因，导致算出来的1-4作用为0，相当于没算，这种情况下仍然会花费计算时间，在mdrun的结尾会看到1-4作用计算的开销。  
  
  
PS: 基于GROMOS87的ffgmx力场，决定VDW参数方式同GROMOS96，决定键结参数方式同OPLSAA(但OPLSAA多了一步原子名的转换过程，即type到bond_type)。
