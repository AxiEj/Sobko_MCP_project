---
post_id: 153
title: 在Gromacs中模拟金纳米线拉伸过程（含视频）
url: http://sobereva.com/153
date: '2015-06-07T23:57:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 分子动力学
- 可视化
academic_relevant: true
classification_reason: 标题直接指向GROMACS中的金纳米线拉伸模拟，软件和工作流最核心。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**注**：**北京科音分子动力学与GROMACS培训班**（<http://www.keinsci.com/KGMX>）里面专门有一节“金属的模拟”非常全面详细讲使用GROMACS计算金属体系的方方面面，给了大量例子，内容远比此文深入详细全面得多，欢迎需要相关知识者参加。

**在Gromacs中模拟金纳米线拉伸过程**

Simulating stretching process of gold nanowire in Gromacs

文/Sobereva @[北京科音](http://www.keinsci.com)  2012-Jul-11

## 1 前言

前一阵子在多尺度材料模拟会议上看见有人演示了一段拉伸纳米线的动画，令我有些愉悦。虽然寡人并不是搞材料模拟的，不过还是想模拟一下玩玩，就用熟悉的gromacs做了一下拉伸金纳米线的过程，结果看上去还挺合理，这里把流程介绍下。当然了，纳米线拉伸这类问题用lammps去做最适合，gromacs做这个就是寓教于乐罢了。  
  
gromacs模拟金属最大的困难就是不支持模拟金属最常用的EAM势及其变种，gromacs只能直接支持对儿势，然而一般普遍认为对儿势对于模拟金属不好。不过，这个共识也并不完全正确，对儿势的形式用于金属，至少是特定的金属，不代表结果一定不好，只要能把参数搞好的话。在JPCC,112,17281就给出了一套很好的LJ 12-6或9-6对儿势形式的适合fcc金属（包括Ag, Al, Au, Cu, Ni, Pb, Pd, Pt）的参数，结果不逊于EAM势，而且计算量还大大降低，还可以直接结合AMBER, CHARMM, COMPASS, CVFF, OPLS-AA, GROMOS, PCFF这些用LJ势的分子力场在amber、gromacs、NAMD、Forcite等程序中研究与金属混合的分子体系，比如研究水在金属表面的行为。  
  
本文用的gromacs为4.5.5版。本文涉及的文件都可以从这里下载：<http://pan.baidu.com/s/1dFeEGEX>  
  

获得的拉伸过程的轨迹如下所示：<http://sobereva.com/attach/153/stretch_Au_nanowire.avi>

也顺便做了一下挤压纳米线的轨迹：<http://sobereva.com/attach/153/extrude_Au_nanowire.avi>

  

## 2 建模

我们首先建立一个金的纳米线的结构，具体来说，就是个25nm*6nm*6nm的金的圆棒。  
  
最方便的方法是用Material studio+VMD来建。首先在MS中选File-import，在...Materials Studio 6.0\share\Structures\metals\pure-metals目录下选中Au.msi，可知此晶胞的边长为4.078埃。我们要将它平移复制成一个金属条，然后从中挖出一个金属棒。我们选Build-symmetry-Supercell，为了能达到25nm*6nm*6nm的尺寸，在三个框分别填65,15,15。选File-export，将得到的超胞导出到Au.pdb文件中。  
  
用VMD打开Au.pdb，我们先找出这个超胞的中心。在控制台输入  
atomselect top all  
measure center atomselect0  
得到中心的坐标为（埃）：  
131.52516174316406 29.5676326751709 29.5676326751709  
  
将Au.pdb保存为新的pdb文件Au_rod.pdb，在保存时的selected atoms框里面输入：  
abs(x-131.525)<125 and (y-29.567)^2+(z-29.567)^2<30^2  
这样就以超胞中心作为纳米线的中心，挖出来了25nm*6nm*6nm的圆柱形。  
  
将刚保存出来的Au_rod.pdb载入VMD。此纳米线包含41480个原子。在gromacs中进行拉伸时，我们要将下图中黄色的区域原子同时向两侧拉，每个黄色区域厚12埃。（因为我们按照原文用12埃的cut-off方式计算VDW势，因此这样可以让黄色区域外的原子都不会感到边缘是被人为截断的）  
[1.png]  
为了能在gromacs中拉它们，必须将左右黄色区域的原子的序号分别写进index文件中，作为名为left和right的group。为此，我们先找出这个棒的最左端和最右端的坐标，即x最小值和x最大值。运行：  
measure minmax atomselect0  
返回结果  
{8.156999588012695 0.0 0.0} {254.8939971923828 59.1349983215332 59.1349983215332}  
  
下面这个tcl小脚本是将指定区域的原子的序号按照index文件允许的格式输出到c:\a.txt中。将这段脚本拷进控制台运行  
proc rangeindex {range {fps 0}} {  
set sel [atomselect top $range frame $fps]  
set result [open c:\\a.txt w]  
set k 0  
foreach i [$sel list] {  
incr k  
puts -nonewline $result [expr $i+1]\   
if {$k%6==0} {puts $result " "}  
}  
close $result  
$sel delete  
puts "total $k atoms"  
}  
  
接下来运行rangeindex {x<12+8.156999588012695}。将生成的a.txt改名为left.txt  
再运行rangeindex {x>254.8939971923828-12}。将a.txt改名为right.txt  
  
把Au_rod.pdb里"AU1 MOL"全都替换为"AU  AU "。这代表每个金原子作为一个分子对待，金原子的原子名和分子名都叫AU。  
  
  

## 3 在gromacs中设定参数文件并模拟

将下面这行  
   Au  196.9665  
添加到gromacs/top/gromos53a6.ff/atomtypes.atp当中  
  
编写一个拓扑文件，名为Au_rod.top，内容如下。其中金的参数来自JPCC,112,17281的表1的Au的B、A值。文中这两个参数的能量和长度单位是kcal和埃，这里转换为了gromacs用的KJ和nm。  
#include "gromos53a6.ff/forcefield.itp"  
  
[ atomtypes ]  
   AU   79      0.000      0.000     A  0.029247582 9.657102e-06  
  
#include "gromos53a6.ff/spce.itp"  
  
[ moleculetype ]  
; molname   nrexcl  
AU         1  
  
[ atoms ]  
; id    at type res nr  residu name at name  cg nr  charge   mass  
1       AU    1       AU         AU       1      0.0        196.9665  
  
[ system ]  
; Name  
Au_rod  
  
[ molecules ]  
; Compound        #mols  
AU  41480  
实际上我们没必要把整个gromos53a6的力场文件以及spce.itp给include进去，但是这样这个拓扑文件更为普适，以后可以直接往当前体系里加入水、小分子之类的东西一起模拟。如果不把gromos53a6力场include进去的话，至少得把gromos53a6.ff/forcefield.itp中的[ defaults ]段落替换到#include "gromos53a6.ff/forcefield.itp"所在的行。  
  
运行Make_ndx -f Au_rod.pdb  
把left.txt和right.txt里的原子序号都写到index.ndx最后，开头设的group名分别为[left]和[right]。  
  
构建md1.mdp，用于平衡模拟，内容如下  
define =  
integrator = md  
dt = 0.002  
nsteps = 50000 !100ps  
comm_mode = ANGULAR  
nstcomm = 10  
comm-grps = system  
nstxout = 1000  
nstvout = 1000  
nstfout = 0  
nstlog = 500  
nstenergy = 500  
nstxtcout = 1000  
xtc_grps = system  
freezegrps = left right  
freezedim = Y Y Y Y Y Y  
;  
nstlist = 10  
ns_type = grid  
pbc = no  
rlist = 1.2  
coulombtype = cut-off  
rcoulomb = 1.2  
vdwtype = cut-off  
rvdw = 1.2  
DispCorr = no  
;  
Tcoupl = Berendsen  
tau_t = 5  
tc_grps = system  
ref_t = 300  
本例是在真空下模拟。我们先做100ps的平衡模拟，让体系升温到300K，在此过程中纳米棒两端1.2nm厚度的原子都冻结不动。  
  
运行  
grompp -f md1.mdp -c Au_rod.pdb -p Au_rod.top -o Au_md1.tpr -maxwarn 5 -n index.ndx  
mdrun -v -deffnm Au_md1  
通过观看轨迹，会看到此体系很结实，原子排布没有变化，只是由于热运动原子有微微晃动。温度也早已平衡到300K了。  
  
接下来编辑拉伸过程的mdp文件。将md1.mdp复制为SMD.mdp，把nsteps设为250000，即模拟500ps。freezedim设为N Y Y N Y Y，即拉伸中只让两端1.2nm厚度内的原子在拉伸方向运动（否则可能斜着散架）。在末尾添加拉伸的设定：  
pull=constraint  
pull_dim=Y N N  
pull_geometry=distance  
pull_group0=left  
pull_group1=right  
pull_ngroups=1  
pull_init1=23.8  
pull_rate1=0.025  
这代表匀速x方向拉伸，让名为left和right的group的质心距离从23.8nm（这是开始时它们的质心在当前结构下实际的距离）开始以0.025nm/ps的速度逐渐加大（折合每秒25m...不要介意，本文目的只是带来愉悦）。这样在500ps内可以拉长12.5nm，即当前体系长度的一半。  
  
运行  
grompp -f SMD.mdp -c Au_md1.gro -p Au_rod.top -o Au_SMD.tpr -maxwarn 5 -n index.ndx  
mdrun -v -deffnm Au_SMD  
最终的轨迹应当是类似于前面的视频那样。如预期的，拉开后断面是尖的。有兴趣的话可以用JPCC,112,17281里的其它金属的参数也拉伸其它金属，或者将纳米线的直径改大点再跑跑，以及看看不同速度、温度下拉伸结果的差异。  
  
我们再做个挤压过程，也就是将pull_rate1=0.025改成pull_rate1=-0.025，模拟900ps，这样left和right的质心距离就剩23.8-900*0.025=1.3nm了，差0.1nm就相接了。
