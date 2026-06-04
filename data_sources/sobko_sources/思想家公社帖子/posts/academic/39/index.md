---
post_id: 39
title: Amber与Gromacs读入碳纳米管的方法
url: http://sobereva.com/39
date: '2015-06-05T00:59:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- GROMACS
- 结构与文件格式
academic_relevant: true
classification_reason: 主要讲 Amber 与 Gromacs 读入碳纳米管的方法，属于软件操作技巧。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**Amber与Gromacs读入碳纳米管的方法**

Loading carbon nanotube into Amber and GROMACS

文/Sobereva @[北京科音](http://www.keinsci.com)   2009-Mar-2

这里说一下Amber和Gromacs读入碳纳米管的方法。只说操作方法，不涉及选用力场等问题。  
  

## Amber：

碳纳米管结构比较大，而结构很有规律，一般仅有C原子。若不考虑边界问题，可以将全部电荷当成0，这种近似并不会对结果真实性有多少影响。对于碳纳米管这样的特征，适合当成一般的小分子来处理，但不宜用antechamber而且也没必要用。  
  
先用Nanotube modeler生成一段碳纳米管，含240个C原子，导出结构为tube.pdb。但是会发现，原子名都是相同的，而leap要求结构中相同残基中每个原子都有独立的名字，所以需要先改名。比较方便的方法是用ultraedit，打开后开启列模式，选定从第1个原子到最后一个原子的15和16列(即原子名C后面的两列)，选Column-Insert Number，OK，即把原子名改为了C1至C240，保存为tubename.pdb。  
  
这里假定C原子使用gaff力场的c2原子类型对应的力场参数，依次运行  
xleap -f leaprc.gaff  
a=loadpdb /sob/tubename.pdb  
bondbydistance a 默认是2埃内成键，故碳纳米管的碳原子都会正常成键，可用edit a 检查。  
然后把碳纳米管内全部240个原子都设成c2原子类型，可以用批处理脚本。由于leap只能一条一条运行批处理文件中的内容而不支持shell脚本的循环，需要将循环转化成普通命令脚本再在leap运行。写脚本：  
for ((i=1;i<=240;i=i+1))  
do  
echo "set a.1.$i type c2" >> leapdo  
done  
在shell下运行，得到leapdo，然后在leap里运行source leapdo即可  
check a 进行参数检查，应该OK。如果想改力场参数或缺少某些参数，可以edit gaff往里添加和修改。  
如果要加溶剂和普通情况无异，这里略过。  
最后saveamberparm a tube.top tube.inpcrd  
  
  

## gromacs:

还是用上面的tube.pdb为例子。小分子在gromacs中常用prodrg来处理，但是理由和antechamber一样并不适合，而且有更方便的办法。gromacs提供了一个构建拓扑文件的工具x2top，专适用于构建结构规律性很强的体系。x2top中有一些bug和“规矩”，而且在不同gromacs版本中bug和“规矩”还不一样，这里使用gromacs4.0.4的x2top。  
  
首先需要写n2t文件，比如使用ffgmx2力场，就在力场文件所在文件夹里写一个ffgmx2.n2t，内容如下：  
C    CX    0.0    12.011     3    C 0.14   C 0.14  C 0.14  
C    CX    0.0    12.011     2    C 0.14   C 0.14  
C    CX    0.0    12.011     1    C 0.14  
第一行说明如果体系中任何一个C原子，与周围3个C原子的距离都在0.14nm左右（判断标准大概为正负10%），就把它当作CX原子类型（原子类型名字自定，可以不属于力场包含的原子类型），电荷为0.0，相对原子质量为12.011。第二行和第三行与第一行意义类似，即代表与两个C原子和与一个C原子成键的C原子被当成什么类型、多少电荷、多少原子质量，此例中将碳纳米管所有原子都当成CX。  
  
运行x2top -f tube.pdb -o tube.top -ff gmx2  
这样就得到tube.top，里面包含这个碳纳米管全部键结项。  
-ff代表用什么力场，此处即ffgmx2，如果-ff select则是出现列表自行选择。这里如果使用ffgmx力场即便正确写了ffgmx.n2t也可能无法正确执行，即不能正确根据距离判断成键，此时应换用别的力场来执行x2top。  
如果运行后程序卡住不动，可尝试加-nopbc解决，这是一个bug。  
默认情况下，x2top会自动在.top里相应键结项加上力场参数，这种方式自动加入的力场参数并不是根据力场中相应原子类型间的键结参数加入的。平衡距离/键角/二面角就是tube.pdb中的相应项的距离/键角/二面角，键的力常数/键角力常数/二面角力常数默认是400000/400/5，可以分别用-kb、-kt、-kp设定。如果不想让其自动加入，可以加上-noparam。  
  
如果n2t中把C原子转换为ffgmx2力场中已有的类型，比如CB，那么此时这个.top搭配tube.pdb已经可以直接用于模拟了。  
此例将C设为力场中没有的原子类型CX，是因为假设要给它设定专门的力场参数。首先加入VDW参数，在ffgmx2nb.itp里的[atomtypes]和[nonbond_params]里面添加。  
如果前面x2top时加了-noparam，还需要设定键结参数。分两种情况：  
1 直接在.top里面每一个键结项后面加入相应力场参数，类似于x2top自动在.top里添加力场参数的方式，用ultraedit等软件的列模式批量加入效率最高。  
2 不在.top里面加，而是在ff???bon.itp里面的[bondtypes] [angletypes] [dihedraltypes]里面加入相应的项，或者把这些内容单独写进一个.itp文件，之后include进.top里。这种方法比较省事、易于修改。  
关于这两种参数定义方式的讨论，详见《gromacs决定力场参数的方式》（<http://sobereva.com/4>）  
  
之后加盒子、填充溶剂等与一般体系无异。
