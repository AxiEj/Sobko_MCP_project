---
post_id: 268
title: 使用Gromacs模拟碳纳米管的一个简单例子
url: http://sobereva.com/268
date: '2015-06-08T00:15:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 分子动力学
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 这是用Gromacs模拟碳纳米管的完整教程，核心软件是GROMACS。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**注**：本文的做法如今已经完全过时，如今强烈建议用Sobtop（<http://sobereva.com/soft/Sobtop>）建立纳米球/管/板的拓扑文件，比x2top灵活得多，参考网页里的例子。另外，北京科音分子动力学与GROMACS培训班（<http://www.keinsci.com/workshop/KGMX_content.html>）里有模拟纳米管、纳米板的完整讲解和详细的例子。

**使用Gromacs模拟碳纳米管的一个简单例子**  
A simple example of using Gromacs to simulate carbon nanotubes

文/Sobereva @[北京科音](http://www.keinsci.com)   2014-Dec-15

很早以前写过一个帖子《amber与gromacs读入碳纳米管的方法》（<http://sobereva.com/39>）介绍了怎么用gromacs处理碳纳米管，不过貌似还是有很多人不会。这里就提供一个在真空中和在水中模拟碳纳米管的简单且完整的例子。这个小教程本来是给一个国际友人写的，所以都是英文。本文用的是Gromacs 4.6.5，文中的CNT10指的是一个很普通的碳纳米管，cnt10.pdb是其结构文件，这可以用Nanotube Modeler很容易地产生。

文中涉及到的文件在此：[/usr/uploads/file/20150610/20150610055407_71312.rar](http://sobereva.com/usr/uploads/file/20150610/20150610055407_71312.rar)。

Create a new file named atomname2type.n2t in "share/gromacs/top/gromos54a7.ff" folder in gromacs directory, and then copy below content into it  
C    CR1    0.0    12.011  3    C 0.142   C 0.142  C 0.142  
C    CR1    0.0    12.011  2    C 0.142   C 0.142  
C    CR1    0.0    12.011  1    C 0.142

That means when we use x2top to generate topology file under G54A7 forcefield, if a carbon atom has one or two or three neighbours with a distance about 0.142nm (normal C-C bond length in CNT), then this carbon will be recognized as CR1 atom, which is the atomtype corresponding to the carbon in aromatic CH-group of G54A7. This atomtype is suitable for representing vdW interaction between CNT carbons and environmental atoms.

Run below command to generate the CNT10.top:  
g_x2top -f cnt10.pdb -o CNT10.top -ff select -nopbc -name CNT10 -kb 400000 -kt 600 -kp 150  
Select G54A7 from the forcefield list, then CNT10.top will be yielded in current folder, and the molecular name is CNT10 (specified by "-name"). -nopbc have to be specified, otherwise x2top can't work normally. -kb, -kt and -kp are used to define the force constant of bond, angle and dihedral terms.

In the CNT10.top, the [ bonds ] field looks like below  
    1     3     1  1.420000e-01  4.000000e+05  1.420000e-01  4.000000e+05   
    2     3     1  1.420000e-01  4.000000e+05  1.420000e-01  4.000000e+05   
    2     4     1  1.420000e-01  4.000000e+05  1.420000e-01  4.000000e+05   
    2    27     1  1.420000e-01  4.000000e+05  1.420000e-01  4.000000e+05   
    3   218     1  1.420000e-01  4.000000e+05  1.420000e-01  4.000000e+05   
...  
The 4th column is the equilibrium length determined based on the input geometry (cnt10.pdb), the 5th column is the force constant set by -kb. The last two columns are redundant, you can simply ignore or even directly delete them. The content of [ angles ] and [ dihedrals ] fields are similar to [ bonds ].

The bond, angle and dihedral forcefield parameters we set above are not important, they are mainly used to keep the nearly rigid structure of CNT during simulation, so the force constant can be simply set to a large value; however, too large values will cause high-frequency vibrations and make the simulation unstable. If you want to make the CNT more flexible (rigid), you can decrease (increase) the dihedral force contant. Currently, AFAIK, no forcefield contains bond, angle and dihedral parameters specifically optimized for CNT modelling.

Then there are two cases, you can follow either one

1 MD simulation in vaccum

grompp -f md_vacuum.mdp -c cnt10.pdb -p CNT10.top -o md_vacuum.tpr  
mdrun -v -deffnm md_vacuum

2 MD simulation in solvated box

editconf -bt triclinic -f cnt10.pdb -o cnt10_box.gro -d 2  
genbox -cp cnt10_box.gro -cs spc216.gro -o cnt10_wat.gro -p CNT10.top

Add below sentence at the head of CNT10.top  
#include "gromos54a7.ff/spce.itp"

Start simulation:  
grompp -f md.mdp -c cnt10_wat.gro -p CNT10.top -o md.tpr  
mdrun -v -deffnm md

模拟和石墨烯、碳球的过程和此文没有任何区别，把文中的cnt10.pdb替换为相应的结构文件即可。石墨烯结构也可以由Nanotube Modeler产生。Nanotube Modeler自带的富勒烯库里有大量碳球结构，各种原子数的各种富勒烯异构体也可以用CaGe产生，CaGe的基本使用方法见《生成富勒烯的螺旋算法简介以及使CaGe中的编号与Fowler-Manolopoulos编号相符的方法》（<http://sobereva.com/104>）
