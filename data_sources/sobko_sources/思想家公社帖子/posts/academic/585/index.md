---
post_id: 585
title: 计算适用于OPLS-AA力场做模拟的1.2*CM5原子电荷的懒人脚本
url: http://sobereva.com/585
date: '2021-01-28T20:47:00+08:00'
source_categories:
- 分子模拟
primary_topic: 静电势与电荷
secondary_topics:
- 分子模拟
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题围绕用于 OPLS-AA 模拟的原子电荷计算，核心是电荷方法。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**计算适用于OPLS-AA力场做模拟的1.2*CM5原子电荷的懒人脚本**

A lazy script to calculate 1.2*CM5 atomic charges suitable for OPLS-AA force field simulation

文/Sobereva@[北京科音](http://www.keinsci.com)  2021-Jan-28

根据J. Phys. Chem. B., 121, 3864 (2017)中的测试，基于OPLS-AA力场的模拟很适合结合1.2*CM5原子电荷。虽然用1.2*CM5的时候水合自由能的计算精度稍逊于文中测试的另一种原子电荷1.14*CM1A-LBCC（因为这种原子电荷本来就是针对水合自由能训练的校正参数），但在计算其它属性上，如蒸发焓、密度，用1.2*CM5时的误差都更小，而且经验性更低、更有普适性。所以当大家用OPLS-AA力场研究新的小分子的时候，我比较推荐用1.2*CM5电荷。1.2*CM5电荷就是在Truhlar等人提出的原始的CM5电荷基础上乘上1.2，这相当于增大了原子电荷的数量级，等效地体现出了溶剂环境对溶质的极化作用。

笔者之前在《计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）》（<http://sobereva.com/476>）和《RESP2原子电荷的思想以及在Multiwfn中的计算》（<http://sobereva.com/531>）中分别给出了超级懒人计算RESP和RESP2电荷的Linux脚本，完全不会用Gaussian的人都能轻松计算，已经有不少人在用。最近碰到完全不会用Gaussian的人试图计算1.2*CM5电荷向我求助，我遂又写了个类似的计算1.2*CM5电荷的懒人Linux脚本，在这里说一下。

这个脚本是Multiwfn文件包里的examples\scripts\1.2CM5.sh，在2021-Jan-28及之后更新的Multiwfn中才有，Multiwfn可以在其主页<http://sobereva.com/multiwfn>免费下载。

此脚本使用很简单：先确保Gaussian在当前机子里已经装了，见《Gaussian的安装方法及运行时的相关问题》（<http://sobereva.com/439>），也确保将Multiwfn按照手册2.1.2节的说明在机子里装了。之后假设1.2CM5.sh和一个结构文件phenol.xyz都在当前目录下，只需要运行./1.2CM5.sh phenol.xyz，之后在屏幕上就会看到脚本的运行过程：  
Net charge was not defined. Default to 0  
 Spin multiplicity was not defined. Default to 1  
 Running optimization task via Gaussian...  
 Done!  
 Running formchk...  
 Running Multiwfn...  
 Finished! The optimized atomic coordinates with 1.2*CM5 charges (the last column) have been exported to phenol.chg in current folder

最终得到的phenol.chg用文本编辑器打开后可见，其中2、3、4列是优化后的XYZ坐标（埃），最后一列就是1.2*CM5电荷了。

脚本原理：这个脚本会将输入文件里的结构作为初猜结构用Gaussian在B3LYP-D3(BJ)/def2-SVP下做几何优化，然后调用formchk将得到的chk转化为fchk文件，然后调用Multiwfn计算CM5电荷，最后给出1.2*CM5电荷。

几点相关事项：  
• 用的输入文件可以是任意含有结构信息而且Multiwfn支持的文件格式，比如pdb/mol/mol2/xyz/fch/gjf/wfn等等等等，见《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）。  
• 默认情况下电荷当成0，自旋多重度当成1。如果是比如不带电的二重态体系，应当写比如./1.2CM5.sh phenol.xyz 0 2。  
• 如果运行脚本时提示没可执行权限，先运行chmod +x ./1.2CM5.sh  
• 此脚本调用的是Gaussian 16，如果当前机子里装的是诸如Gaussian 09，需要将文件的第22行改为Gaussian=g09。  
• 从脚本里的关键词可见，计算是在真空下进行的，这是刻意而为之，不要自行改成在溶剂模型下进行。  
• 如果脚本运行失败，有这么几种可能：(1)Gaussian根本没恰当安装，应当确保能手动调用Gaussian运行一个最简单的计算任务 (2)Multiwfn没按照手册2.1.2节恰当安装。其中有些图形库不方便装的话，可以用Multiwfn的noGUI版，此时不需要装图形库 (3)Gaussian计算失败，可能是版本太老而不支持em=GD3BJ关键词，可将脚本中此关键词去掉。也可能几何优化或SCF不收敛，注意看计算中途产生的gau.out文件内容判断原因。  
• 如果你手头已经有Gaussian或其它程序产生的Multiwfn支持的波函数文件了（fch/wfn/wfx/molden/mwfn等），就没必要再用这个脚本了。直接载入Multiwfn，依次输入7、16、1就能得到CM5电荷，再手动乘上1.2即可。  
• 前述J. Phys. Chem. B.文章中只是考虑了中性体系，没有考虑带电体系。带电体系用什么原子电荷结合OPLS-AA没有统一说法，一般情况下不能用1.2*CM5电荷，因为此时总电荷都不是整数了。笔者建议此时用Multiwfn算RESP2电荷，虽然与OPLS-AA兼容性没有充分测试，但原理上问题不大。  
• 如果使用此脚本计算1.2*CM5电荷，请按照Multiwfn程序包里How to cite Multiwfn.pdf文档的说明恰当引用Multiwfn。

如果你没买Gaussian，也可以用免费的ORCA量子化学程序结合Multiwfn算1.2*CM5原子电荷，笔者也提供了相应的傻瓜式脚本，见《ORCA结合Multiwfn计算RESP、RESP2和1.2*CM5原子电荷的懒人脚本》（<http://sobereva.com/637>）。
