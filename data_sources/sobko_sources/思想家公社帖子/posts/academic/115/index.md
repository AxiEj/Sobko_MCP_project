---
post_id: 115
title: AMBER程序支持的力场一览
url: http://sobereva.com/115
date: '2015-06-07T23:52:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- 分子动力学
- 综述/教程/投稿经验
- 静电势与电荷
academic_relevant: true
classification_reason: 标题是AMBER程序支持的力场一览，明确是AMBER及其力场教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**AMBER程序支持的力场一览**

Overview of force fields supported by AMBER program

文/Sobereva @[北京科音](http://www.keinsci.com/)  First release: 2011-Dec-27

本文主要介绍下Amber11中支持的众多版本的Amber力场，GAFF和GLYCAM顺便提一下。主要参考了AmberTools手册。顺带一提，后期Amber力场都是采用RESP电荷，计算RESP电荷最佳的工具是Multiwfn，使用非常简单，看《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）。  
   
AMBER=Assisted Model Building with Energy Refinement：适合蛋白和核酸的凝聚相模拟，有机小分子支持得少。函数形式简单。包含以下版本：  
ff10力场(parm10.dat)：对ff99的各种参数补丁的集合，相当于parm99.dat+frcmod.ff03+bsc0+chi.OL3+新的离子参数+原子和残基名的修改以顺应PDB format version 3。这是目前最好的amber力场。  
ff03.r1力场(parm99.dat+frcmod.ff03)：ff99力场的修改版。获取电荷时通过连续介电模型表现溶剂可极化效应，修改了蛋白phi、psi骨架参数，减少了对螺旋构象的偏爱。核酸参数相对于ff99没变。ff03.r1与amber9中的ff03略有不同，那时仍用的是ff94的方法得来的碳、氮端基原子电荷，如果仍想用那时代的ff03就调用oldff/leaprc.ff03.  
ff03ua力场(parm99.dat+frcmod.ff03+frcmod.ff03ua)：ff03力场的united-atom版本，侧链的氢原子被united了，骨架上的氢原子和芳香环上的氢原子仍被保留。由于骨架还是全原子故骨架势参数没变，侧链上的参数因用了united故重新拟合。核酸参数完全没变，且还是全原子。  
ff02力场(parm99.dat+frcmod.ff02pol.r1)：ff99力场的可极化版，给原子上增加了可极化的偶极子。frcmod.ff02pol.r1是对原ff02的扭转参数的修正。  
ff02EP力场(parm99EP.dat+frcmod.ff02pol.r1)：ff02力场基础上给诸如氧、氮、硫原子增加了偏离原子中心的点电荷以表现孤对电子效应。据称比ff02稍好点。  
ff99力场(parm99.dat)：大部分参数来自ff94力场，修改了许多扭转角的参数。甘氨酸的骨架参数有问题，螺旋和延展构象的平衡性不对。而对于DNA，ff99长时间模拟中亚稳态占统治地位，即alpha和gamma二面角倾向于分别为gauche+和trans状态。虽然在RNA中也有这问题，但不严重。ff99的这些毛病在ff94里也有。  
ff99SB力场(parm99.dat+frcmod.ff99SB)：对ff99的蛋白二面角参数进行修正，二级结构间分布的比例得到了改善，也解决了甘氨酸骨架参数问题。  
bsc0(frcmod.parmbsc0)：解决上述ff99在核酸模拟问题上的补丁，同时还改进了RNA的糖苷的gamma二面角扭转势。可参考http://mmb.pcb.ub.es/PARMBSC0。  
ff99SB+bsc0力场：把bsc0补丁用到ff99SB上，相对于ff99同时增进对蛋白和核酸的效果。这个组合使gamma二面角过分偏离了trans型。如果初始结构有很多gamma角为trans的情况，还是用ff99比较好。  
ff99SBildn(frcmod.ff99SBildn)：在ff99SB基础上修改氨基酸侧链参数的补丁。  
ff99SBnmr(frcmod.ff99SBnmr)：在ff99SB基础上修改骨架扭转项参数以更符合NMR数据的补丁。  
ff98力场(parm98.dat)：对ff94改进了糖苷的扭转角参数。  
ff96力场(parm96.dat)：与ff94扭转角不同，算出来的能量更接近量化结果。来自Beachy et al，由于构象有明显偏向beta等问题，使用不广泛。  
ff94力场(parm94.dat)：来自Cornell, Kollman et al。适合溶剂环境。电荷由RESP HF/6-31G*获得。  
ff86力场(parm91X.dat)：将ff84扩展为全原子力场。和ff84一样对氢键也是用Lennard-Jones 10-12势，故如果想在sander里用ff84/86，得重新带着-DHAS_10_12选项编译。之所以相应的文件叫parm91X是因为对原始ff86做了一些修正。（parm91X.dat是parm91.dat的补完版，加入了一些非键项，但非键项比如Mg、I等的参数都没调好，只是近似。）  
ff84(parm91X.ua.dat)：最早的AMBER力场，用于模拟核酸和蛋白质的联合原子力场。不推荐使用，但在真空或者距离依赖的介电常数下模拟还有用。  
parmAM1和parmPM3力场(parmAM1.dat/parmPM3.dat)：用这个参数对蛋白质优化可以得出与AM1/PM3相同的优化结果。如今已没什么价值。  
   
GAFF力场(gaff.dat)=Generation Amber Force Field：普适型有机小分子力场，函数形式和AMBER力场相同，与AMBER力场完全兼容。  
   
GLYCAM-06力场(GLYCAM_06g.dat)：对以前GLYCAM力场做了改进，并且纳入了一小部分脂类的参数。  
GLYCAM-04EP力场(GLYCAM04EP.dat)：将GLYCAM04扩展到可用于TIP5P模型下的模拟。给氧加上非原子中心点电荷表现孤对电子效应。  
GLYCAM-04力场(GLYCAM04.dat)=glycans and glycoconjugates in AMBER：专用于糖的模拟，和AMBER完全兼容，可一起用于糖蛋白的模拟。官网：<http://glycam.ccrc.uga.edu/ccrc/index.jsp>  
   
另外，Amber程序还支持AMOEBA力场，也可以通过自带的CHAMBER工具来支持CHARMM力场，这里就不提了。
