---
source_id: software_doc:sobtop
title: Sobtop：A tool of generating forcefield parameters and GROMACS topology file
url: http://sobereva.com/soft/Sobtop/
date: 2026-01-16
source_type: software_doc
software_tags:
- Sobtop
- GROMACS
- Gaussian
- ORCA
- CP2K
- xTB
- Multiwfn
- AMBER
- OpenBabel
topic_tags:
- 分子动力学
- 结构与文件格式
- 第一性原理
- 周期性DFT
- 综述/教程/投稿经验
authority_level: A
version: 2026.1.16
download_url: http://sobereva.com/soft/Sobtop/sobtop_2026.1.16.zip
package_sha256: d8a6726ad80a930d45bbcc34f5d32ea47ecca201aacd34ce1a870680d45c3c38
---

# Sobtop：A tool of generating forcefield parameters and GROMACS topology file

------------------------------------------------------------------------

**Latest version**：2026.1.16 　(Release date is the same as version name)

**Index of this page**:  
[Developer](http://sobereva.com/soft/Sobtop/#developer)　[Citation](http://sobereva.com/soft/Sobtop/#citation)　[Download](http://sobereva.com/soft/Sobtop/#download)　[Introduction](http://sobereva.com/soft/Sobtop/#intro)　[Examples](http://sobereva.com/soft/Sobtop/#examples)　[Skill](http://sobereva.com/soft/Sobtop/#skill)　[FAQ](http://sobereva.com/soft/Sobtop/#FAQ)　[TODO list](http://sobereva.com/soft/Sobtop/#todo)　[Update history](http://sobereva.com/soft/Sobtop/#history)

### Developer

Dr. [Tian Lu](http://sobereva.com/Tian_Lu.html) (Contact: sobereva\[at\]sina.com. [Beijing Kein Research Center for Natural Sciences](http://www.keinsci.com) 北京科音自然科学研究中心)

If you encountered any difficulty in using Sobtop, or you found bug, or you have any suggestion on improving Sobtop, please post on Molecular Modeling board of [http://bbs.keinsci.com](http://bbs.keinsci.com) or send E-mail to me.

Sobtop can be freely used for both academic and commerical purposes. Sobtop must be properly cited if the work will be published. You may also use Sobtop to do calculations for others (i.e. 代算), while you should explicitly tell them that Sobtop needs to be cited in their publication.

### Citation

If Sobtop is utilized in your work, **it must be cited as** follows in main text (rather than SI):

Tian Lu, Sobtop, Version \[当前版本\], http://sobereva.com/soft/Sobtop (accessed on 日 月 年)　注：此处的时期是你最后访问本页面的日期

Sobtop在进一步完善后会写详细的手册并发布正式版，然后专门写成介绍paper发在学术期刊上，届时请引用期刊上的文章（记得提交proof前关注本页面看这里写的最新的引用方式）。

### Download

**Executable file**: [sobtop_2026.1.16.zip](http://sobereva.com/soft/Sobtop/sobtop_2026.1.16.zip) ("sobtop.exe" and "sobtop" are executable files of Sobtop in Windows and Linux, respectively)

### Introduction of Sobtop

**What is Sobtop?**

GROMACS is the most popular molecular dynamics code. To simulate a molecule by GROMACS, topology file must be created first for every kind of species involved in the simulation system. Although there have been numerous codes that can generate topology file of GROMACS, all of them have severe limitations in different aspects, for example: (1) Difficult to use and install (2) Only support specific kind of system, such as organic molecules only, while molecules containing transition metals and boron can hardly be treated (3) Cannot automatically determine missing bonded parameters based on Hessian matrix (4) Too slow and unable to deal with large systems such as polymer (5) Only support isolated system (6) Not flexible enough to create topology for complicated systems.

Sobtop aims at eliminating all limitations in existing topology file generators, providing an extremely easy-to-use, universal and robust code to generate forcefield parameters and GROMACS topology file for ***any*** system!!! I sincerely hope Sobtop could be a perfect and final solution of generation of GROMACS topology file.

(Meaning of "Sobtop": Sobereva topology)

**Features of Sobtop**

- Freely available.
- Very easy to use, the steps for generating GROMACS topology file are minimized as much as possible. Preparing any running environment is not needed (in contrast to many Python scripts. Sobtop is written in Fortran).
- The program is interactive, users do not need to memorize any keyword or argument. User can also write shell script to invoke Sobtop to generate topology file for a batch of systems.
- Very fast. Even macromolecules containing thousands of atoms can be processed.
- Can deal with any kind of system (organic molecules, inorganic molecules, transition metal coordinates, covalent atomic clusters, polymers, inorganic materials, etc.) containing any element.
- Both isolated and periodic systems are supported. The x2top utility in GROMACS can be completely replaced.
- GAFF/GAFF2, AMBER and UFF atomic types can be automatically determined (for the former two cases, .mol2 file should be used, in other cases .pdb file can also be used). Users can also provide a file containing rules of determination of atomic types according to chemical environment.
- Prebuilt forcefield parameters and definition of atomic types are completely open to users, thus they can very conveniently modify and extent the parameters by editing force field files.
- Force constants of bond, angle and dihedrals can be directly derived based on Cartesian Hessian matrix calculated by Gaussian, ORCA and xtb (for isolated systems) or CP2K (for periodic systems). Four methods are supported for this purpose: Seminario, mSeminario, m2Seminario, DRIH. These methods can be automatically employed during generating .itp file, and minimum, maximum and average of each kind of derived bond/angle/dihredral types are outputted to a text file so that users can then easily put them into forcefield parameter file. In addition, a specific function is also provided in Sobtop to allow users manually calculate bond/angle/dihredral parameters by directly inputting atomic indices.
- Bonded parameters can be assigned in flexible ways. For example, one can request Sobtop to derive parameters for bonds and angles based on Hessian (thus more accurate than GAFF parameters), while employ torsion parameters of GAFF to account for rotatability of dihedrals. Another example, one can specify a rigid region, all bonded terms involved in this part are represented by harmonic potential, whose parameters are derived based on Hessian, while other parts employ GAFF parameters and thus dihedral flexibility can be represented.
- Atomic charges can be directly loaded from .chg file exported by atomic charge calculation (e.g. RESP, ADCH) of Multiwfn. EEM and Gasteiger atomic charges (via invoking Multiwfn) and MMFF94 atomic charges (by invoking OpenBabel) can also be automatically assigned.
- Very detailed comments are given in the generated topology file, which greatly facilitates users to check and manually modify parameters.
- .gro file can be exported, which exactly corresponding to the generated .itp file.
- .rtp file can be generated, which can be used by pdb2gmx tool.
- Some utility functions: Printing current redundant internal coordinates, exporting Wilson B matrix and related matrices, generating and exporting Hessian matrix in redundant internal coordinate, and so on.  

### Examples

全面包含各类体系例子的手册目前还没时间写。这里仅给一些简单的例子，以及一些要点的说明，大家请举一反三。基本上看过一遍后就能对Sobtop的各方面主要特征有个全面的了解。**强烈建议按顺序阅读**，因为这些例子和相关讲解是循序渐进的，**也绝对不要断章取义**。使用Sobtop的过程中要注意看屏幕上的提示，信息非常丰富、细致、易懂。

**例子列表**：  
[例1](http://sobereva.com/soft/Sobtop/#ex1)：产生SF6的GROMACS的拓扑和gro文件：力常数全基于Hessian计算得到  
[例2](http://sobereva.com/soft/Sobtop/#ex2)：产生苯甲酸甲酯的GROMACS的拓扑和gro文件：参数完全基于GAFF的  
[例3](http://sobereva.com/soft/Sobtop/#ex3)：产生苯甲酸甲酯的拓扑和gro文件：bond和angle参数基于Hessian得到，其它部分用GAFF的  
[例4](http://sobereva.com/soft/Sobtop/#ex4)：产生过渡金属配合物的拓扑文件  
[例5](http://sobereva.com/soft/Sobtop/#ex5)：产生聚合度为40的氯丁二烯聚合物的拓扑文件  
[例6](http://sobereva.com/soft/Sobtop/#ex6)：产生跨越盒子的无限长氯丁二烯聚合物的拓扑文件  
[例7](http://sobereva.com/soft/Sobtop/#ex7)：产生碳纳米管的GROMACS拓扑文件  
[例8](http://sobereva.com/soft/Sobtop/#ex8)：产生金刚石晶体的拓扑文件  
[例9](http://sobereva.com/soft/Sobtop/#ex9)：产生二氧化硅晶体的拓扑文件  
[例10](http://sobereva.com/soft/Sobtop/#ex10)：产生金属有机框架化合物MOF-5的拓扑文件  
[例11](http://sobereva.com/soft/Sobtop/#ex11)：产生FeCl2二维材料的拓扑文件  

#### **例1：产生SF6的GROMACS的拓扑和gro文件：力常数全基于Hessian计算得到**

**注：绝对不要以为什么时候都得像本例这样提供含有Hessian的文件并让Sobtop计算力常数。如果你要对普通有机体系产生拓扑文件，应该效仿的是例2直接用GAFF的参数，那是最省事的。老有人只看了本例，居然连例2都不看就去胡搞！也记得把[FAQ10](http://sobereva.com/soft/Sobtop/#FAQ11)和[FAQ11](http://sobereva.com/soft/Sobtop/#FAQ11)看了，搞清楚什么时候才有必要基于Hessian算力常数。**

SF6是典型的非有机体系，那些基于有机分子力场的拓扑文件产生工具如acpype、antechamber、Ligpargen、CGenFF、ATB等碰到这种体系就完全无能为力了。碰到这种体系一般都建议让Sobtop基于Hessian矩阵计算出来力场参数。对于\[H3O\]+、Sb4O6、P4、\[PF6\]-、\[AuCl4\]-、B2H6等等乱七八糟的无机刚性体系一律都可以用本节的做法非常容易地得到拓扑文件。

首先用Gaussian对SF6做优化+振动分析并保留.fch/fchk文件，或使用ORCA做优化+振动分析并保留.hess文件，里面都包含了要用的笛卡尔Hessian矩阵和优化后的坐标信息。然后把优化后的结构保存成mol2文件，这用GaussView就可以。注意此文件里的键连关系必须和实际要产生的力场项对应，在GaussView里可以肉眼检查，不符的话就调整。只要连接关系正确就行，而成键方式随意。

在Windows下可双击Sobtop.exe图标启动。在Linux下可进入Sobtop目录后运行chmod +x \*加上可执行权限，再输入./sobtop启动（不要在其它目录下启动，否则无法正常运行）。启动Sobtop后依次输入以下命令，//后是注释  
examples\SF6\SF6.mol2  
2 //产生gro文件  
\[回车\] //默认的gro文件产生路径  
-1 //设置产生力常数的方法  
4 //DRIH方法  
1 //产生GROMACS拓扑文件  
2 //指认GAFF原子类型，没法指认的自动用UFF原子类型  
2 //所有力常数都通过DRIH方法得到  
examples\SF6\SF6.fchk　//Gaussian的freq任务得到的，用于给Sobtop提供Hessian矩阵。这一步用ORCA的freq任务产生的.hess文件、xtb的--ohess任务产生的名为hessian的文件、CP2K振动分析的输出文件亦可  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径  
当前目录下已经有了SF6.itp、SF6.top和SF6.gro。此例原子类型都是GAFF的，平衡键长来自SF6.fchk，力常数使用DRIH方法基于Hessian产生。SF6.itp里包含的是SF6分子的拓扑信息，包括定义此分子的\[ moleculetype \]字段，以及定义其中涉及到的原子类型的\[ atomtypes \]字段。由\[ moleculetype \]下面的信息可见Sobtop自动设的分子名就是结构文件去除后缀后的名字。SF6.top是主top文件，包含了GAFF/AMBER力场下模拟适用的\[ defaults \]字段、整个体系名\[ system \]字段，以及分子数目字段\[ molecules \]。

如果mol2文件里记录了原子电荷的话，它们会被读取并写入到产生的itp里。由于当前mol2文件里没有记录原子电荷信息，所以所有原子电荷都为0。因此要自行用Multiwfn算RESP或RESP2(0.5)原子电荷添加进itp中的\[ atoms \]部分，溶液中的模拟用RESP2(0.5)最为推荐。具体做法参考下文，可以手动用Multiwfn基于Gaussian产生的fch文件或ORCA产生的molden文件算，也可以直接用下面的懒人脚本一行命令便利地得到。  
RESP拟合静电势电荷的原理以及在Multiwfn中的计算  
[http://sobereva.com/441](http://sobereva.com/441)（[http://bbs.keinsci.com/thread-10880-1-1.html](http://bbs.keinsci.com/thread-10880-1-1.html)）  
计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）  
[http://sobereva.com/476](http://sobereva.com/476)（[http://bbs.keinsci.com/thread-12858-1-1.html](http://bbs.keinsci.com/thread-12858-1-1.html)）  
RESP2原子电荷的思想以及在Multiwfn中的计算（内含懒人脚本）  
[http://sobereva.com/531](http://sobereva.com/531)（[http://bbs.keinsci.com/thread-16190-1-1.html](http://bbs.keinsci.com/thread-16190-1-1.html)）  
ORCA结合Multiwfn计算RESP、RESP2和1.2\*CM5原子电荷的懒人脚本  
[http://sobereva.com/637](http://sobereva.com/637)（[http://bbs.keinsci.com/thread-28178-1-1.html](http://bbs.keinsci.com/thread-28178-1-1.html)）

顺带一提，也可以先用Multiwfn计算出包含原子电荷的chg文件，在产生拓扑文件之前读进Sobtop，这样chg文件里的原子电荷直接就出现在产生的itp的\[ atoms \]里。具体做法是启动Sobtop后，在主菜单里选7 Assign atomic charges，再选10 Load atomic charges from .chg file of Multiwfn，输入.chg文件的路径，然后回到主菜单，按照前面的例子操作即可。图省事的话，也可以在Sobtop主菜单里直接输入.chg文件的路径，也会从里面载入原子电荷。

**注意**：如果基于上面的DRIH方法产生拓扑文件进行模拟遇到报错，可以尝试后面提到的mSeminario或m2Seminario方法产生力常数，或者干脆让Sobtop自动猜谐振势形式的力场参数而不基于Hessian计算（即让你选择如何生成力场参数时，选择4 Same as option 3, but missing ones are arbitrarily guessed。反正对于这种刚性体系，力常数不重要，只要大小足够维持住体系的刚性就够了）。

**练习**：examples\exercise\COBH3.mol2是用Gaussian在B3LYP/def2-TZVP级别下优化好的COBH3分子对应的mol2文件，请读者对它效仿本节的步骤产生拓扑文件。

**小知识：如何检验拓扑文件的合理性**

如果想检验拓扑文件是否合理、其中的参数是否合适，可以写个对应真空、常温条件下短时间动力学的mdp，与前文得到的itp、top、gro相结合跑模拟。通过在VMD里看轨迹动画，或者每隔一定帧数叠加显示，靠肉眼判断结构变化和波动是否合理。通常凭直觉就可以大致判断合理性，如果有基于DFT的从头算动力学的轨迹作参照那就更容易检验，可以对比基于力场跑的轨迹的RMSF、角度分布等参数与从头算动力学跑的偏差。

在examples目录下给了个md_vac.mdp，是控温在300 K、用步长1 fs跑真空下100 ps动力学的mdp。没有用PBC条件，只兼容GROMACS 2018及以前的版本。可以用以下命令进行动力学模拟  
gmx grompp -f md_vac.mdp -c SF6.gro -p SF6.top -o md.tpr -maxwarn 1  
gmx mdrun -v -deffnm md -ntmpi 1

也要注意并不是真空下模拟下看起来合理，在溶剂环境下模拟也就一定合理。因为溶剂环境下涉及到分子与溶剂的非键相互作用，以及溶剂与分子的碰撞，情况明显更为复杂。如果构建的拓扑文件的实际目的是用于溶剂下的模拟，显然还是要以溶剂中模拟的轨迹作为合理性的最终判据。

文献里衡量力场参数准确性的一种参见做法是基于力场先做充分的能量极小化再做振动分析，和量子化学算的频率对比看偏离程度。GROMACS的双精度版本是可以做振动分析的，虽然有时候有bug。虽然这样检验力场参数确实显得比较严格，但其实对于实际模拟来说我觉得用处不大。因为对刚性体系只要结构能在动力学过程中维持好就行了，频率相符程度差一些也无所谓，只不过是结构波动情况可能没那么精准而已，但这不是一般关心的。而对于涉及到可旋转键的柔性分子，就算极小点位置的频率算得不错，也不代表动力学行为就一定很理想，因为实际的动力学牵扯到势能面上较广阔区域，而频率的计算精度仅体现极小点位置的局部势能面曲率的合理性而已。

**小知识：基于Hessian产生力常数的方法**

Sobtop支持多种基于Hessian产生力常数(k)的方法，对bond、angle、dihedral都可以产生力常数。显然这种情况下的二面角是视为刚性的而不可旋转，此时Sobtop也不会试图产生维持pi共轭区域平面性的improper项。默认方法可以通过settings.ini里的k_method设置。

Sobtop支持的各种基于Hessian产生力常数的方法简要说明如下：

• Seminario方法：原文是Int. J. Quantum Chem.: Quantum Chemistry Symposium, 30, 1271 (1996)。已经过时了，算的键角力常数严重高估。总是不建议使用。不过键角力常数高估其实对实际MD模拟来说不算大问题，只不过是高估了键角的刚性而已。

• Modified Seminario (mSeminario)方法：原文是J. Chem. Theory Comput., 14, 274 (2018)。是对Seminario方法产生键角力常数的改进，解决了高估的问题。但mSeminario和Seminario方法在原理上不严格，导致的一个问题是对于某些体系对称的键角给出来的力常数可能明显不同，可能因此跑MD的时候分子对称性被破坏，比如对CLi4、SF6就都有这个问题。用户可自行检查一下itp里\[ angles \]部分等价键角的力常数值。另外，此方法产生的i-j和j-i键的力常数可能有轻微不同，即序号顺序会影响结果，这也是违背逻辑的，但由于此问题很轻微所以不用太在意。

• Diagonal elements of redundant internal coordinate Hessian (DRIH)方法：先将读入的笛卡尔Hessian矩阵通过Wilson B矩阵转化成冗余内坐标下Hessian矩阵，其中每个冗余内坐标直接对应一个bonded项，然后取对应的对角元当做力常数。此方法原理上比mSeminario更严格。对于有高对称的刚性小体系如CLi4、Sb4O7、SF6，用DRIH多数情况比mSeminario更好（从基于力场计算的频率相对于量子化学算的频率的吻合来说），也完全没有其空间对称等价的键角力常数不相同（实际中由于数值精度原因，可能还是有微小不同，可以无视）、i-j和j-i键力常数轻微不同的问题。另外用DRIH方法时itp文件里会有以\[ angles \]字段记录的键-键耦合项，因此对键伸缩描述精度比mSeminario好得多，虽然这对于实际模拟来说不是重点。但对有些体系，比如苯、二茂铁，用DRIH时我发现二面角力常数偏小，导致模拟过程中结构波动偏大。而且DRIH结合GAFF力场的二面角项使用时，对量子化学算的中、低频率的重现性往往比mSeminario结合GAFF的二面角项时差一些。**注意**：使用DRIH方法产生力常数时，如果体系实际是有点群对称性的，一定要让初猜结构就满足点群对称性，通常这可以令最终优化出的结构也满足点群对称性。如果偏离实际对称性，有可能令DRIH方法给出的力常数不合理。

• The second modified Seminario (m2Seminario)方法：卢天提出。改进了mSeminario方法中用的不太合理的Hessian矩阵非对角块的投影方法，使得等价的键角的力常数完全相同，而且i-j和j-i的力常数也完全相同。虽然此方法比mSeminario原理上更严格，但对于个别体系的个别力常数，mSeminario方法由于内在的“错错得对”效应，算的力常数反倒比此方法更好。例如此方法算的水的键角力常数明显偏小，而mSeminario算的则更合理。另外，结合GAFF力场的二面角项使用时，此方法对量子化学算的频率的重现性往往稍微比mSeminario差一些（但也有反例）。

总的来说，没有绝对完美的方法。一般对于纯刚性，尤其是有对称性的体系，我建议先考虑DRIH或m2Seminario。对于含有可旋转键的有机分子，建议mSeminario计算键+键角，结合GAFF的二面角项（会顺带产生pair和improper项）。如果你不怎么讲究，有机分子全用内置的GAFF参数也可以，如后面的苯甲酸甲酯的例子，但如果体系有成键方式比较特殊、在GAFF力场中没充分考虑的部分，可能此时很不理想。

如果你实在不确定哪种最好，可以都试试（Seminario方法除外），然后按照前述的“检验拓扑文件的合理性”里的做法予以检验。

值得一提的是，力常数越大，动力学模拟过程中相应变量的波动程度就会越小。Sobtop的主界面上有个-2 Set scale factor for derived force constants选项，可以给基于Hessian算出来的不同类型力常数乘上特定的系数。比如模拟中你嫌分子骨架整体波动有点太厉害，就可以用这个选项把二面角力常数要乘的系数设成一个明显大于1的值，然后再模拟试试。

 

#### **例2：产生苯甲酸甲酯的GROMACS的拓扑和gro文件：参数完全基于GAFF**的

**本节的做法是产生普通有机分子拓扑文件最简单快速的做法，没有之一。**

启动Sobtop，然后输入  
examples\Methyl_benzoate\Methyl_benzoate.mol2  
2 //产生gro文件  
\[回车\] //默认的gro文件产生路径  
1 //产生GROMACS拓扑文件  
2 //指认GAFF原子类型，没法指认的自动用UFF原子类型  
4 //从力场库文件中取合适的参数，缺的就猜一个（此模式对于bond和angle项，平衡值设为当前结构文件里的值，力常数分别用差不多是c3-c3和c3-c3-c3的值，但取了个尽量整的数。对于二面角项则将旋转势垒设为0）  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

当前目录下已经有了Methyl_benzoate.itp、Methyl_benzoate.top和Methyl_benzoate.gro。其中LJ参数和成键相关参数都是GAFF力场的。在屏幕上没有提示有任何bond、angle、dihedral参数缺失。虽然提示ca-ca-ca-c的improper参数缺失，但Sobtop自动用X -X -ca-ha的improper参数来代替的做法通常都是合理的，足够维持局部平面性。

最后，记得用Multiwfn算出来RESP或RESP2(0.5)原子电荷添加进去，在上一节明确说了。

**练习**：examples\exercise\7-helicene.mol2是7-螺烯的mol2文件，大家对此分子也按本例的流程产生拓扑文件，然后在真空下跑跑动力学，看看结构维持得怎么样。

**小知识：关于缺参数的处理**

至于怎么搞缺的参数，看具体缺什么：

如果是缺可旋转二面角参数，最好是构建个简单的模型体系（关注的二面角所处的化学环境要和实际分子中一致，无关区域应尽可能简化以避免碍事和浪费计算时间），用量子化学程序做二面角的柔性扫描（看比如《详谈使用Gaussian做势能面扫描》[http://sobereva.com/474](http://sobereva.com/474)），然后靠Origin、自己写的程序或者现成工具（如http://rotprof.lncc.br）拟合成周期势。显然这个过程略麻烦，如果这个二面角不重要的话，也可以自己去bonded_param.dat的\$DIHEDRAL里凭感觉找个能凑合用的参数。另外，还可以用Google（never Baidu!）搜A-B-C-D parameter，其中A/B/C/D替换为实际缺的原子类型名，说不定有的文章里提供了参数。如果是缺刚性二面角参数，让Sobtop基于Hessian直接算出来就完了，因此上面选4的地方应该选3，此时Sobtop会要求你输入.fch/fchk或.hess的路径，产生itp文件过程中有缺的bonded参数时就会自动算。

如果缺的是bond和angle参数，一般都应当让Sobtop基于Hessian算出来。如果你希望图省事，不怎么要求准确度，那就干脆直接用Sobtop给你猜的，平衡键长/键角就是当前结构文件里的值，而力常数是一个足够大的值。

**小知识：关于指认原子类型**

在指认原子类型的那一步里，从屏幕上可见Sobtop支持的指认原子类型方式相当灵活丰富。除前述例子用到的外，还有其它选项：自动指认AMBER原子类型、给没指认的原子类型自动用UFF的、手动设置原子类型、根据assign_AT.dat里的规则判断原子类型、从外部文件读取各个原子的原子类型、导出当前的原子类型等。在这一步里，屏幕上会显示当前所有原子的原子类型，用户需要用界面上的选项把所有未定义类型的原子的类型都定义了，才能选0进入下一步。而前面的例子用的选项2算是快捷选项（先指认GAFF原子类型，没指认成功的自动用UFF原子类型），选完了直接就进入了下一步。

**小知识：Sobtop的力场库文件**

由于Sobtop的力场库文件完全透明、格式清晰、注释详细，因此Sobtop极为灵活、普适，相当于一个通用的框架。由于用户可以自己修改力场库文件，故Sobtop能自动提供的参数绝不仅限于GAFF和AMBER力场的。不过，Sobtop目前只支持GAFF/AMBER的力场形式，其它力场如果用了特殊形式，就不可能被支持，例如CHARMM力场有Urey-Bradley项因此不支持，GROMOS力场的bond和angle项是特殊形式因此不支持。

在Sobtop目录下有**LJ_param.dat**文件，里面包含所有原子类型的LJ参数和原子类型含义的注释。itp文件里的LJ参数就是直接取自这里的。此文件里默认包含各种UFF力场、GAFF力场（原子类型为小写）和AMBER19SB+parmbsc0+OL3力场（原子类型为大写）的原子类型。用户可以自己用文本编辑器编辑此文件，修改参数或添加新原子类型，详见文件中的注释部分。添加新原子类型时原子类型名不要超过10个字符，注意区分大小写，也不要和已有的冲突。

在Sobtop目录下有**bonded_param.dat**文件，里面包含了所有预置（prebuilt）的bond、angle、dihedral、improper参数（统称为bonded参数），分别在不同字段里记录，各字段以\$开头，包括\$BOND、\$ANGLE、\$DIHEDRAL、\$HARM_DIH、\$IMPROPER。Sobtop会根据被指认的原子类型和成键关系，在此文件里搜索对应的参数。搜索是从前往后搜索，取最后一次匹配的，所以二面角参数中涉及到X的通配项一定要出现在专一项之前，以确保最终用的尽可能是专一项。此文件里的注释极其详细，用户可以很方便地自行修改里面的值、添加新的值。此文件里默认包含了所有GAFF和AMBER19SB+parmbsc0+OL3力场定义的bonded参数。

应知道二面角可以分为两类，一种是可旋转（rotatable）二面角或者叫柔性（flexible）二面角，用周期性的扭转势（torsion potential）描述；另一种是刚性二面角，用谐振势（harmonic potential）描述。bonded_param.dat文件里\$DIHEDRAL字段记录的是前者的参数，\$HARM_DIH记录的是后者的参数。Sobtop先搜索前者后搜索后者，因此如果某个二面角参数在两处都定义了，那么会取\$HARM_DIH里的，并因此作为刚性二面角对待。

bonded_param.dat的\$IMPROPER字段不仅决定了improper参数是什么，也决定了Sobtop会生成哪些improper项。此文件里A-B-C-D项对应于C在中央，A、B、D在其周围的情况。例如此文件里有一行是X -c3-n -c3，则原子类型为n的原子若与三个原子成键，其中两个是c3，一个是任意类型，就会产生一个improper项，并且用这里提供的参数。顺带一提，在GAFF/AMBER力场里，improper项在函数形式上和普通二面角项并无差异，也是周期势函数。如果想当谐振势对待，应当在\$HARM_DIH里进行定义。

**小知识：关于pair项的产生**

Sobtop对于柔性二面角会产生对应的pair项，由此GROMACS会计算1-4作用，它和dihedral参数对应的扭转势相组合定义实际二面角扭转时感受到的势。那些缺参数的二面角也会产生对应的pair项，因此如果不补参数的话，这些二面角也并非完全是自由旋转的。那些被谐振势描述的刚性二面角就不会产生pair项了，本来也没任何必要，而且基于Hessian计算的刚性二面角参数本身就已经把二面角改变时感受到的势完全体现了。

注意pair项和柔性二面角并不是一一对应关系。比如环丁烷，四个碳C1,C2,C3,C4按顺序排列，此体系里有C1-C2-C3-C4二面角，用GAFF参数时是当做柔性二面角对待的，虽然好像应该产生(C1,C4)的pair项，但由于C1和C4实际上是直接成键的，因此它们是1-2而不是1-4关系，因此得到的itp里不会对它产生pair项。

 

#### **例3：产生苯甲酸甲酯的拓扑和gro文件：bond和angle参数基于Hessian得到，其它部分用GAFF的**

GAFF力场里虽然定义了bond和angle参数，质量整体也不错，但相对于基于较好质量Hessian矩阵直接计算的bond和angle参数来说还是有一定差距，尤其是对于成键方式特殊的体系，毕竟GAFF里的那些参数不是针对当前体系专门获得的。而且涉及到特殊成键、有机体系里不常见的元素时，GAFF里可能根本没有相应的bond和angle项。Sobtop允许bond和angle参数基于Hessian矩阵计算出来，而其它部分（dihedral和improper）从力场文件里查询得到，其中若有缺的再基于Hessian计算得到。这样做bond和angle项的参数质量又好又不会出现缺失项，又能兼顾柔性二面角的可旋转特征。

启动Sobtop，然后输入  
examples\Methyl_benzoate\Methyl_benzoate.mol2  
2 //产生gro文件  
\[回车\] //默认的gro文件产生路径  
1 //产生GROMACS拓扑文件  
2 //指认GAFF原子类型，没法指认的自动用UFF原子类型  
7 //bond和angle参数基于Hessian计算得到，其它的用力场文件里的，其中若有缺失的基于Hessian计算得到  
examples\Methyl_benzoate\Methyl_benzoate.fchk  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

从屏幕上可以看到哪些参数是靠Hessian算出来的。现在当前目录下已经有了Methyl_benzoate.itp、Methyl_benzoate.top和Methyl_benzoate.gro。最后，记得用Multiwfn算出来RESP或RESP2(0.5)原子电荷添加进去。

顺带一提，如果你还想要更好精度的拓扑文件，建议对可旋转的二面角做势能面扫描再拟合得到参数，然后将当前itp里的相应参数替换掉，但这就比较费时费事了。仅当你的研究对二面角旋转势垒、极小点位置准确度要求很高的时候才值得这样做。

 

#### **例4：产生过渡金属配合物的拓扑文件**

此例专门有个很详细的文章《使用Sobtop超级方便地创建二茂铁的GROMACS的拓扑文件》 [http://sobereva.com/635](http://sobereva.com/635)。对任何过渡金属配合物都可以按照此例来搞。双核甚至多核金属配合物也都可以这么搞，没有特殊性。

此例一个关键点是Fe这样GAFF不支持的元素，要求Sobtop自动用UFF的原子类型，其原子类型名以UF_开头，后面跟元素名。UFF力场里实际上每种元素不区分原子类型，而且UFF力场对周期表里几乎所有元素都有定义，因此当一个原子遇上没有专门的原子类型的时候都可以用UFF原子类型来凑合。Fe的UFF原子类型在Sobtop里就叫UF_Fe，可见在LJ_param.dat文件中有其LJ参数的定义。

有人觉得对过渡金属是不是用Merz等人搞得很全面的离子的LJ参数会更好，我的意见是否定的，在于：Merz的金属离子参数对于重现离子在溶液中的不同属性（自由能、离子-氧距离、第一配位层的配位数）分别优化了不同的LJ参数，而且往往数值相差还不小，没法说用哪种合适。而UFF力场每种元素就只有一种LJ参数，因此没有这种含糊性。本来也没证据证明在配合物中用某一种Merz的离子参数就有什么优势。另外，过渡金属配合物中金属的数目相对于配体原子来说是非常少的，它对于配合物与其它分子间的范德华作用贡献很小，因此就算LJ参数不是特别理想也不至于有明显实际问题。顺带一提，UFF和Merz的过渡金属参数都是离子的，如果是计算金属单质，都不适用，必须用一些文章里提供的专门的LJ参数。另外，如果体系中过渡金属原子数目非常多，比如FeCl2、MoS2二维材料，可能得自行专门去优化过渡金属的LJ参数才能得到很理想的结果（UFF的LJ参数还是略糙的，而且作为普适性的参数肯定不如考虑了具体化学环境专门优化出来的参数好）。

**练习**：examples\exercise\ZPT.mol2是吡硫鎓锌二聚体，里面有两个Zn，每个Zn和两个硫和两个氧配位。请读者按照本节的做法对它产生拓扑文件，并检验在真空下做动力学是否能正常维持结构。

**Hint：搞柔性与刚性混合体系的拓扑文件**

如果你的体系一部分是刚性，一部分柔性，例如过渡金属卟啉配合物上面还接了一段柔性有机基团（显然柔性部分必须考虑二面角的可旋转性），在Sobtop问你怎么产生bonded参数的时候应当选择选项5，然后输入一批原子序号将之作为刚性部分。然后刚性部分涉及到的bonded项会自动基于Hessian计算得到，柔性部分会从力场文件里取对应的参数，柔性部分若有缺失参数的话也会基于Hessian计算得到。

更具体来说，用选项5时Sobtop是用这样的规则：  
bond项：只要有哪怕一个原子在选中的范围，就使用基于Hessian计算的参数  
angle项：只要有哪怕一个原子在选中的范围，就使用基于Hessian计算的参数  
dihedral项：只要二面角中间两个原子都在选中的范围，就基于Hessian计算参数。因此，如果中间两个原子中有一个不在选中的范围，这个二面角就是可旋转的（如果力场文件里\$DIHEDRAL里有定义的话）。  
其它情况直接检索从力场文件里取参数。

 

#### **例5：产生聚合度为40的氯丁二烯聚合物的拓扑文件**

这个例子产生聚合度为40，末端用氢封闭的氯丁二烯聚合物的拓扑文件，结构文件是examples\polymer\Neoprene_40.mol2。GAFF对于描述有机聚合物是完全没问题的，本例直接指定GAFF原子类型并且用相应的bonded参数。对此体系为了图省事，就直接用MMFF94原子电荷，它只适合有机体系，且只依赖于原子间连接关系经验性地得到原子电荷（也因此不受输入文件里聚合物构象的影响，没有构象依赖性在某种程度上算是一个优点），可以瞬间对巨大体系算出来。虽然其对静电势重现性肯定不及RESP电荷理想，因此对于动力学模拟的目的并不算多理想，但要求不高的话对有机类体系勉强能凑合用，起码比QEq、Gasteiger、Mulliken、NPA之类强多了，也明显比不用原子电荷要好。如果RESP电荷是10分的话，MMFF94电荷可以给个7分左右。Sobtop可以调用免费的OpenBabel程序（[http://openbabel.org/docs/index.html](http://openbabel.org/docs/index.html)）计算MMFF94原子电荷，启动Sobtop之前要把sobtop.ini里的OpenBabel_cmd设为OpenBabel可执行文件的实际路径（对于Windows版，强烈不建议把OpenBabel装到默认的带空格的路径下！否则可能调用不成功）。

启动Sobtop，然后输入  
examples\polymer\Neoprene_40.mol2  
7 //设置原子电荷  
5 //MMFF94电荷。由屏幕上提示可见，Sobtop调用了OpenBabel，一瞬间402个原子的MMFF94电荷就产生出来了  
0 //返回  
2 //产生gro文件  
\[回车\] //默认的gro文件产生路径  
1 //产生GROMACS拓扑文件  
2 //指认GAFF原子类型，没法指认的自动用UFF原子类型  
4 //用预置的力场参数，缺失的自动猜  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

现在当前目录下就有了Neoprene_40.itp、Neoprene_40.top和Neoprene_40.gro了。可以尝试做一下真空下的模拟，应当会看到聚合物链不断扭动，这很合理。

从Sobtop窗口中提示可看到（在Neoprene_40.itp中搜missing也可以发现），c3-c2-cl参数是缺失的，即缺了“sp3杂化碳-sp2杂化碳-Cl”这样的键角参数。当前用Sobtop自动猜的参数就跑得很理想，所以没什么必要去补它，本来这种刚性键角的力常数大点小点对动力学行为都不会有什么影响。只有可旋转的二面角参数才是真正关键的，因为它们直接影响分子的柔性和构象变化，而当前itp里这些参数都没缺。另外，从Sobtop窗口中的提示还可见c3-ha-c2-c2和c2-c3-c2-cl的improper项是缺失的，sp2杂化的碳理应有improper项维持它所在的局部三角区域的平面性。对缺失的improper项Sobtop都是自动用X -X -ca-ha型improper参数凑合，这是没什么问题的，从实际模拟结果会看到局部平面性维持得是合理的。

如果你特别讲究的话，就是想把那个缺的c3-c2-cl力常数准确得到，可以构造一个三个氯丁二烯单元组成的分子，两边加氢，然后用Gaussian或ORCA做优化和振动分析。之后启动Sobtop载入其mol2文件，选5 Derive rigid parameter for specific bond/angle/dihedral，再载入fch/fchk或hess文件，然后输入对应c3-c2-cl键角的那三个原子的序号，Sobtop马上就会输出相应的平衡键角和力常数值。之后在bonded_param.dat的\$ANGLE字段里加入c3-c2-cl项及对应的参数。下次再重复前面的步骤产生聚合物的拓扑文件时就会用这些参数了。

**Hint：关于给聚合物用RESP原子电荷**

如果能给聚合物所有原子都用RESP电荷那当然是最理想的。但十分不建议对整个聚合物直接算RESP电荷，一方面在于优化、算电荷的耗时会很高，尤其是原子数达到500以上很难算得动（对于2022年的主流几十核服务器来说）；另一方面是在于这样算的原子电荷构象依赖性较大，用聚合物的不同构象来算的时候有些原子电荷可能差异不小；还有一方面在于没法令每个中间的重复单元里等价的原子的电荷是相同的，且每个重复单元的净电荷也不恰好为整数，这不够优雅（做过蛋白质动力学模拟的人都知道，每种残基里相同原子名的原子电荷都是相同的，每个残基净电荷为整数，聚合物也应当如此）。

一般来说，正确得到聚合物RESP电荷的做法是构造一个寡聚物（目的是让被计算的残基在寡聚物中所处的电子结构环境和实际体系足够相似。如果重复单元很小像聚乙烯，建议含五个单元；如果重复单元稍大如聚碳酸酯，三个单元就够；如果重复单元很大，如包含几十个原子，那就只保留它与相邻单元成键的一部分，如几个到十几个原子左右即可），再对寡聚物两边进行饱和避免有悬键，并且要用平直的构象（但如果优化后卷起来了，导致其它部分的原子妨碍感兴趣部分原子的RESP电荷的拟合，应当考虑做限制性优化，适当固定一些关键的二面角以避免卷曲）。之后用量子化学程序在DFT级别下做几何优化，通常B3LYP/6-31G\*就可以。基于优化后的结构再用B3LYP/def2-TZVPP算个单点任务得到更好质量的波函数用于给Multiwfn算RESP电荷。电荷算三次，第一次算RESP电荷的时候把首端单元的总电荷约束为0；第二次将最中间的单元的总电荷约束为0；第三次将尾端单元的总电荷约束为0。这样三次计算后，首端、中间、尾端单元的原子电荷就都有了。上述过程的具体操作可以效仿《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（[http://sobereva.com/441](http://sobereva.com/441)）里获得氨基酸残基原子电荷的例子。之后，对实际的聚合物，首端和尾端单元的原子电荷套用前面得到的，中间每个单元都套用前面得到的中间单元的。至于怎么令这个套用原子电荷的过程尽可能方便，请大家结合实际情况开动脑筋，不要懒得去写脚本（笔者以后会提供个完美、便利的解决方案）。显然，整个聚合物里各单元中的原子排列顺序必须得和寡聚物模型中相一致，否则就乱套了。

上面说的得到聚合物单元RESP电荷的做法是对于均聚物来说的，对于共聚物，请在理解上面文字的原理的前提上当意即妙考虑怎么构造寡聚物模型和获得不同单元的原子电荷。

 

#### **例6：产生跨越盒子的无限长氯丁二烯聚合物的拓扑文件**

这个例子示例一下怎么得到跨越盒子无限延展的物质的拓扑文件，还是拿氯丁二烯聚合物作为例子。从此例会看到，对这种体系，只要mol2里记录了跨盒子的键即可，在产生拓扑文件的过程上没有丝毫特殊性。

examples\polymer\Neoprene_10_cross.mol2是一个聚合物为10，两头跨越盒子，因此无限延展的聚合物结构。用文本编辑器打开它的话，会看到@\<TRIPOS\>BOND字段里有4 1 73 1，这是说此体系中第4个键是1和73号原子之间的键，形式键级为1。1和73之间的键正是跨盒子的键（如果你用GaussView看的话，会看到有一个超长的从体系最左端的碳连到最右端的碳的键，这是因为GaussView没按照周期性来显示键）。

Sobtop构造拓扑文件的流程和构造孤立体系的流程没有丝毫差异。启动Sobtop，载入这个mol2文件后，屏幕上会看到  
Atom X Y Z Charge Bonds to  
1C -1.90300 0.55280 0.00000 0.00000 2H 3H 4C 73C  
...略

可见确实1和73之间跨盒子的键被识别了。之后还是让Sobtop自动指认GAFF原子类型，从屏幕的提示中会看到1和73都正确地识别成了sp3杂化的碳（c3原子类型）。然后照常产生itp和top文件，会看到itp里的\[ bond \]项里也有1-73的，\[ angles \]和\[ dihedrals \]也都有涉及1-73的，显然拓扑文件是很合理的。

在GROMACS里做此体系的动力学模拟的时候别忘了在mdp里要加上periodic-molecules = yes，这样GROMACS才能考虑跨盒子的力场项，否则当前体系从拓扑关系上会被当做一个孤立的环状体系看待。

对当前体系也可以照常让Sobtop调用OpenBabel指认MMFF94原子电荷。如果要用RESP电荷算当前体系，显然每个聚合物单元都应当套用模型体系算出来的中间单元的RESP电荷。

 

#### **例7：产生碳纳米管的GROMACS拓扑文件**

值得一提的是，Sobtop不仅支持mol2也支持pdb作为输入文件，但pdb无法给sobtop提供连接关系信息，因此sobtop会根据原子间距离自动猜，只要两个原子距离小于它们的共价半径和的1.15倍就被视为成键（阈值可以通过sobtop.ini里的bondcrit改，在bondcrit.dat文件里还可以对不同元素区分设置）。注意载入后应看看屏幕上显示的连接关系对不对，另外也可以用Sobtop主界面里的选项4导出记录了当前判断出的连接关系的gjf文件，然后载入GaussView用肉眼检查。用pdb的话Sobtop没法自动指认GAFF原子类型，需要以其它方式指认。

此例产生碳纳米管拓扑文件，结构文件是examples\CNT\CNT.pdb。由结构可见，位于中间的碳形成三个C-C键，位于边缘的碳形成两个C-C键。这个体系适合所有碳原子都用ca（GAFF里的芳香碳原子）。如果以mol2作为输入文件且让Sobtop自动判断GAFF原子类型的话会发现中间的碳判断成了ca，而边缘的碳判断成了c1（GAFF里sp杂化的碳），明显不合适。另外，由于当前体系一大堆环连在一起，让Sobtop自动判断GAFF原子类型时耗时也较高。由于以上原因，再加上本来此体系就只有一种原子类型，所以此例最适合手动直接设置原子类型。

启动Sobtop，然后输入  
examples\CNT\CNT.pdb  
1 //产生GROMACS拓扑文件  
6 //手动设置原子类型  
\[回车\] //选择所有原子  
ca //设为ca原子类型。然后屏幕上提示所有原子的原子类型已经被指认了  
0 //进入下一步  
4 //用预置的力场参数，缺失的自动猜  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

现在当前目录下就有了CNT.itp和CNT.top了。此例就不产生gro文件了，因为GROMACS的grompp也能基于pdb文件产生tpr文件。

实际上GAFF、OPLS-AA、GROMOS等力场里都没有专供碳纳米管（以及富勒烯、石墨烯）的力场参数，从itp里的注释中可见当前的二面角参数是取的GAFF里的通配项X-ca-ca-X，故只算是凑合用。如果比如你想让碳纳米管刚性更强，一种做法是直接替换itp里当前的二面角的势垒高度值（当前是15.167）为更大的值，也可以比如在bonded_param.dat的\$DIHEDRAL字段末尾加上ca-ca-ca-ca项，在里面定义专供碳纳米管、石墨烯等体系用的纯ca间的二面角的参数。另外，从当前itp文件里\[ dihedrals \] ; impropers下面的部分还可以看到用于维持平面性的improper项，实际上GAFF没有定义ca-ca-ca-ca的improper参数，从注释上可知当前Sobtop自动套用了X -X -ca-ha的improper项，大家也可以在bonded_param.dat的\$IMPROPER里加上相应的专一项。

 

#### **例8：产生**金刚石晶体的拓扑文件

这个例子产生金刚石晶体的拓扑文件，主要有三个目的，一是让大家了解怎么写assign_AT.dat文件自定义判断原子类型的规则，另一方面也让大家看到用pdb作为输入文件的时候Sobtop也可以直接判断跨盒子的键，本节还示例怎么自定义新的原子类型。看过这个例子，大家肯定就再也不想用GROMACS里的x2top了，因为Sobtop灵活强大太多了。

assign_AT.dat文件类似于x2top的n2t文件，具体语法和例子在此文件里的注释中写得都很明白。Sobtop可以根据此文件里定义的判断规则，根据原子在结构文件中所处的实际环境指定原子类型和原子电荷。可以用的判断条件包括元素、成键的总数、必须满足的与其它元素原子成键的形式键级、与其它元素原子的距离范围、和不同元素原子间的键角范围。相比之下，x2top程序的n2t文件只能通过元素间距离在某个值附近来指定原子类型，远没有Sobtop灵活。

此例用的结构文件是examples\diamond_3x3x3\diamond_3x3x3.pdb，是Multiwfn基于金刚石原胞构造出的3\*3\*3超胞的pdb文件，注意此文件开头的CRYST1字段定义了此超胞的盒子信息，这个信息必须有，否则Sobtop没法根据坐标判断出跨盒子的键。当前这个体系其实用sp3杂化的碳作为原子类型就可以，可以直接手动在Sobtop里把所有原子都定义成c3原子类型，但这里作为示例我们通过定义assign_AT.dat来实现。当前体系特征非常简单，每个原子都形成四个键，故只需要把规则定义为形成四个键的原子就被设为某种原子类型即可。在assign_AT.dat中加入以下内容  
\$Ctest  
nbond 4  
代表成键数为4的原子的原子类型都判断为Ctest。原子类型后面没写原子电荷，因此此类原子的原子电荷默认为0。

由于Ctest原子类型是我们自己创造的，故还要在LJ_param.dat中加入它的LJ参数和注释（分号后的信息）：  
Ctest 1.9255 0.105 ;My carbon

此体系涉及Ctest原子类型间的bond、angle、dihedral项，因此在bonded_param.dat的\$BOND里加入自定义参数：  
Ctest-Ctest 300.9 1.5375  
在\$ANGLE里加入：  
Ctest-Ctest-Ctest 62.9 111.51  
在\$DIHEDRAL里加入：  
Ctest-Ctest-Ctest-Ctest 1 0.18 0.0 -3.  
Ctest-Ctest-Ctest-Ctest 1 0.25 180.0 -2.  
Ctest-Ctest-Ctest-Ctest 1 0.20 180.0 1.  
PS：上面这些参数值其实都是GAFF里c3间的参数，本节借用过来作为例子。

启动Sobtop，依次输入  
examples\diamond_3x3x3\diamond_3x3x3.pdb //载入后从屏幕上可见所有原子都形成四个键，确实Sobtop根据原子坐标和晶胞信息猜的成键都是对的  
1 //产生GROMACS拓扑文件  
5 //根据assign_AT.dat里的规则指认原子类型。之后从屏幕上的信息可见所有原子都被指认为了Ctest原子类型  
0 //进入下一步  
4 //用预置的力场参数，缺失的自动猜  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

现在当前目录下就有了diamond_3x3x3.itp和diamond_3x3x3.top，与diamond_3x3x3.pdb相结合就可以做动力学模拟了。还是别忘了mdp里要加上periodic-molecules = yes。

实际上，这一节的例子如果把\$Ctest设为\$c3的话，就不需要自己修改LJ_param.dat和bonded_param.dat了，因为本身GAFF力场里就有c3-c3、c3-c3-c3、c3-c3-c3-c3的参数。

效仿本例，大家也可以产生比如碳化硅、氮化硼等原子晶体的拓扑文件，只要在assign_AT.dat里根据情况定义多个判断原子类型的规则，并在bonded_param.dat里添加涉及的bonded参数即可。诸如硼这种元素，既可以在assign_AT.dat里定义你专门命名的原子类型并在LJ_param.dat里定义LJ参数（B的LJ参数可借用里面的UF_B的，即UFF力场的硼的）；也可以在assign_AT.dat里定义\$UF_B项，即设置UFF力场的B的原子类型判断规则，这样LJ_param.dat里就不用再新加一个原子类型了。由于碳化硅、氮化硼这些体系是化合物而非单质，因此别忘了应当在assign_AT.dat里也把相应原子类型要用的原子电荷写上去。原子电荷用Multiwfn基于CP2K产生的molden文件计算CM5电荷通常就不错（可参看[http://sobereva.com/588](http://sobereva.com/588)了解CP2K的molden文件怎么产生。Multiwfn载入后用主功能7的子功能16就能计算CM5电荷）。

对于MOF、COF、黑磷、MoS2、MXene等更复杂的周期性体系，也都可以在这一节的做法基础上举一反三。对于里面涉及到的缺的bonded参数，平衡键长/键角/二面角可以直接用晶体结构里的值，结合自己猜的足够大的力常数（只要力常数够大，就能维持刚性。对这些体系通常我们对其实际的结构波动程度不感兴趣，故不用太较真，只要能维持晶体结构稳定就行了）。也可以截取不同的簇并饱和边缘，用Gaussian或ORCA做振动分析，然后通过Sobtop得到里面涉及的一些项的力常数（显然，被求力常数的这些内坐标应当处于簇模型的靠中间部分，以避免边界效应）。也可以用CP2K直接对周期性体系做振动分析，输出文件里有Hessian矩阵，Sobtop可以靠它来一次性得到所有力常数。这类体系，由于直接与真空区接触，原子电荷用CP2K算REPEAT电荷是不错的选择，输入文件可以直接由Multiwfn创建，见《使用Multiwfn非常便利地创建CP2K程序的输入文件》（[http://sobereva.com/587](http://sobereva.com/587)）。

 

#### 例9：产生二氧化硅晶体的拓扑文件

这一节用Sobtop产生二氧化硅晶体的拓扑文件，本例要把Chem. Mater., 26, 2647 (2014)一文中给出的体相二氧化硅的原子电荷、LJ 12-6参数、bond和angle项参数补进来，见此文表3和表4。此文作者认为对这种体系没必要考虑dihedral项，因此没给dihedral参数。

用VMD自带的Extensions - Modeling - Inorganic Builder可以构建二氧化硅晶体结构。本例用的examples\SiO2_3x3x3\SiO2_3x3x3.pdb是通过此工具构造的二氧化硅3\*3\*3超胞。

根据文献里的原子电荷和LJ参数，在LJ_param.dat里写入以下信息，新增加两种原子类型  
Si_bulk 2.075 0.093 ;Si in bulk SiO2  
O_bulk 1.735 0.054 ;O in bulk SiO2  
注意：Chem. Mater., 26, 2647 (2014)文献里公式1的形式是错的，此式里的σ实际上应当为r0（势能曲线极小点的距离），因此上面LJ_param.dat里定义的(r0)/2项是此文里给的σ的一半（而如果你看到的某篇文献里给的是一般意义的σ参数，即势能曲线为0处的距离，那么在LJ_param.dat里应当按照(r0)/2 = 2<sup>(1/6)</sup>\*σ/2的关系来定义）。

在bonded_param.dat里的\$BOND中添加  
Si_bulk-O_bulk 285 1.65  
在\$ANGLE里添加  
O_bulk-Si_bulk-O_bulk 100 109.5  
Si_bulk-O_bulk-Si_bulk 100 149.0  

在assign_AT.dat里添加以下内容。1.1和-0.55分别是体相二氧化硅里硅和氧的原子电荷。这里写element Si要求元素必须是硅，这是为了能和上个例子里形成四个键的碳进行区分。  
\$Si_bulk 1.1  
nbond 4  
element Si

\$O_bulk -0.55  
nbond 2  
element O

启动Sobtop，然后输入  
examples\SiO2_3x3x3\SiO2_3x3x3.pdb  
1 //产生拓扑文件  
5 //根据assign_AT.dat里的规则指认原子类型。之后从屏幕上的信息可见所有原子都被正确指认了原子类型  
0 //进入下一步  
4 //用预置的力场参数，缺失的自动猜  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

现在当前目录下就有了SiO2_3x3x3.itp和SiO2_3x3x3.top。由于我们没有添加二面角参数，故当前itp里\[ dihedrals \]中的参数都是缺失的，Sobtop自动对它们填的参数里势垒为0，因此等价于不设这些二面角项。你如果把整个\[ dihedrals \]字段全都删掉也可以，不影响结果。如果你把sobtop.ini里的iskipgendih设为1，那么所有二面角项都将不会产生（对很大的体系，这能大幅节约产生和写入二面角项的耗时！）。\[ pairs \]不要删掉，因为Chem. Mater.这篇文章里在给出参数的时候是已经考虑了计算1-4作用项时优化的参数。

之后将SiO2_3x3x3.itp、SiO2_3x3x3.top和SiO2_3x3x3.pdb相结合，就可以试试跑模拟了。在examples目录下给了个md_PBC.mdp，是在NPT下跑100 ps常温下动力学的文件，由于当前晶体尺寸很小，为了cutoff不超过晶胞最短边长的一半，所以cutoff设得很小。运行以下命令即可执行测试。观看轨迹会发现晶体结构和晶胞尺寸维持得特别好，极度理想！  
gmx grompp -f md_PBC.mdp -c SiO2_3x3x3.pdb -p SiO2_3x3x3.top -o md.tpr -maxwarn 2  
gmx mdrun -v -deffnm md


#### 例10：产生金属有机框架化合物MOF-5的拓扑文件

此例对金属有机框架化合物MOF-5的单胞产生拓扑文件，此体系里有Zn-O配位键。examples\MOF-5\MOF-5.cif是MOF-5的晶体文件。用GaussView打开它，确认里面成键关系（特别是Zn-O配位键）都是正确的，然后保存为mol2文件。  
**注1**：此例用mol2而非pdb格式原因有二：(1)Sobtop会从mol2文件里读取连接关系，并且连接关系可以在GaussView里可视化检验正确性。若用pdb格式的话，Sobtop根据原子间距离和元素半径自动猜的连接关系和你期望的未必一致，特别是对MOF-5这样键的类型略多的情况检验起来略麻烦 (2)用mol2格式时才能让Sobtop自动指认GAFF原子类型。 如果你打算自己写合适的assign_AT.dat来定义原子类型的判断规则，那么像之前的例子一样用pdb格式也完全可以  
**注2**：如果你要让Sobtop自动猜参数缺失的参数，应当按照[http://sobereva.com/soft/Sobtop/#FAQ14](http://sobereva.com/soft/Sobtop/#FAQ14)里说的，手动给GaussView保存出来的mol2文件里加入晶胞信息，否则Sobtop不会将之视为周期性体系，猜的参数可能完全错误！

启动Sobtop，输入  
examples\MOF-5\MOF-5.mol2  
1 //产生拓扑文件  
2 //指认GAFF类型，缺失的用UFF的。从屏幕提示上会看到Zn被指认为了UFF原子类型，其它的都是GAFF原子类型  
4 //用预置的力场参数，缺失的自动猜  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

现在当前目录下就有了MOF-5.itp和MOF-5.top。从屏幕上会看到缺失的bond项有UF_Zn-os，缺失的angle项有：  
UF_Zn-os-UF_Zn  
UF_Zn-os-ce  
os-UF_Zn-os  
os-ce-os  
缺失的dihedral项有：  
UF_Zn-os-UF_Zn-os  
UF_Zn-os-ce-os  
UF_Zn-os-ce-ca  
os-UF_Zn-os-ce  
os-ce-ca-ca  
缺失的improper项有ce-ca-ca-ca，这个不用管，原因同前。

对于不是特别讲究的情况，bond和angle项缺就缺了，如上可见这些都是涉及Zn的，而这些项的刚性也都很强，就用Sobtop默认猜的参数就能维持其状态。缺失的dihedral项里前四个都是和Zn有关的，你去看MOF-5的结构图的话，就会认识到这些二面角项没有也没什么关系，因为光靠angle项也足矣维持每4个Zn所在的局部单元的刚性和立体结构，从实际模拟得到的动力学轨迹上也会发现这一点。

缺的os-ce-ca-ca这个二面角完全无视掉不太好。如果直接用Sobtop默认赋予它的参数（旋转势垒为0）的话，模拟过程中苯环部分会过于自由、快速地旋转，而实际中旋转不可能容易到这种程度。当然构建个模型体系做二面角扫描再去拟合参数是最好的，但步骤略繁琐。这里要求不高，就试图直接用力场库文件里其它的二面角参数凑合借用一下。这个二面角中间部分其中一个是ca，对应于苯环上的碳，这个是必须要存在的，而且不好替换成别的原子类型。因此要在bonded_param.dat的\$DIHEDRAL部分里搜索-ca-，可以找到好多项，再要求另一个中间部分原子的元素也必须是碳，筛选出的就只剩下面这些了，都是通配项：  
X -c -ca-X 4 4.000 180.000 2.000  
X -c1-ca-X 2 0.000 180.000 2.000  
X -c2-ca-X 4 2.800 180.000 2.000  
X -c3-ca-X 6 0.000 0.000 2.000  
X -ca-ca-X 4 14.500 180.000 2.000  
X -ca-cp-X 4 14.500 180.000 2.000  
X -ca-cq-X 4 14.500 180.000 2.000  
去看LJ_param.dat里原子类型的定义可知，我们缺的二面角中间部分涉及的ce原子类型对应的是共轭区域内部的sp2杂化的碳原子（但不是在芳环中），在当前体系中它来自于羧基碳，上面的这些通配项里中间原子与之最接近的就是c2了（sp2杂化的碳，只不过没限定是处于共轭部分）。因此我们把X -c2-ca-X 4 2.800 180.000 2.000复制并修改为  
os-ce-ca-ca 4 2.800 180.000 2.000 ;Same as X -c2-ca-X  
并插入到\$DIHEDRAL里面。我习惯上插入到字段开头，便于修改。

之后再按照前面的过程重新生成一次MOF-5的拓扑文件，我们添加的os-ce-ca-ca就会被利用了，产生拓扑文件时屏幕上也不会提示缺os-ce-ca-ca的参数了。

之后我们跑一下MOF-5的动力学。给grompp用的结构文件可以这么得到：启动Multiwfn，载入MOF-5.cif，进入主功能100的子功能2，选择保存为pdb文件，命名为MOF-5.pdb（注意不能用GaussView载入cif文件后保存pdb文件，因为这样的pdb里没有盒子信息。也不能用Sobtop将mol2文件转成gro文件直接用于动力学模拟，是因为GaussView保存的mol2里没盒子信息，因此得到的gro文件里也没盒子信息，除非你自己修改其最后一行把晶胞信息如实填进去）。

之后将上面得到的MOF-5.pdb、MOF-5.itp、MOF-5.top以及examples\md_PBC.mdp相结合，就可以跑动力学模拟了：  
gmx grompp -f md_PBC.mdp -c MOF-5.pdb -p MOF-5.top -o md.tpr -maxwarn 3  
gmx mdrun -v -deffnm md  
从模拟轨迹中会看到MOF-5的形态维持得很好，该刚性的部分一直保持刚性，苯环也可以适度地发生旋转。

以上没有涉及原子电荷，显然如果你要研究比如MOF-5吸附其它分子之类的模拟，原子电荷肯定得有。CP2K程序对周期性体系可以算REPEAT电荷，对静电势重现性很好，故很适合这种目的，推荐看《一篇深入浅出、完整全面介绍原子电荷的综述文章已发表！》（[http://sobereva.com/714](http://sobereva.com/714)）文中REPEAT电荷部分了解相关知识。算REPEAT电荷的CP2K输入文件靠Multiwfn能很容易地生成，看《使用Multiwfn非常便利地创建CP2K程序的输入文件》（[http://sobereva.com/587](http://sobereva.com/587)）。examples\MOF-5\CP2K_REPEAT.in是这个任务的输入文件，同名的.out是输出文件，CP2K_REPEAT-RESP_CHARGES.resp是此任务产生的记录各个原子REPEAT电荷的文件，把里面的电荷拷到MOF-5.itp里即可。

如果实在不方便用CP2K，还有另一种做法可以得到适合模拟MOF和COF体系用的原子电荷，而且速度很快，看[sobtop+GROMACS模拟MOF、COF体系时可以用的快速计算原子电荷的方法：PACMAN](http://bbs.keinsci.com/thread-46231-1-1.html)。

**基于簇模型和Hessian矩阵获得缺失的和Zn有关的参数**

如果你做的模拟要用于发表文章，对于以上那些和Zn有关的缺失的参数，我建议还是自己搞出来，这样更严格，这其实很容易。因为根据MOF-5的结构可看出，和Zn有关的缺失的二面角参数用谐振势描述就够了，因此都不涉及到费事的势能面扫描。具体做法是把MOF-5复制成超胞，再把其中一个连接单元截出来并且把边缘用氢饱和，然后做优化和振动分析得到fch文件。这个模型的Gaussian输入文件是examples\MOF-5\MOF-5_fragment.gjf，产生的fch文件比较大，我就不提供了。将优化完的结构保存为MOF-5_fragment.mol2。

作为例子，这里获得缺失的UF_Zn-os-UF_Zn的angle参数。当前的模型是Td点群对称的，随便找对应这个键角类型的三个原子，从MOF-5_fragment.gjf中可见Zn11-O15-Zn13就适合。启动Sobtop，然后依次输入  
MOF-5_fragment.mol2  
-1 //修改产生力常数的方法  
3 //m2Seminario。当前体系有对称性，此方法此时比mSeminario更好，用后者算等价的键角可能得到明显不同的结果。此体系也不太适合DRIH，会发现有些键角力常数明显太小  
5 //对特定键、键角、二面角产生刚性参数  
MOF-5_fragment.fchk  
11,15,13 //对应Zn11-O15-Zn13  
屏幕上明确提示了加入\$ANGLE里要用的参数，应当在里面加入UF_Zn-os-UF_Zn 22.34 109.47。

此体系的缺失的二面角如UF_Zn-os-UF_Zn-os不太好弄成谐振势形式加入\$HARM_DIH，因为此体系里这种二面角有0、120、-120度三种情况，因此比较适合弄成有三个极小点的周期势函数，但对这个体系不太好做旋转扫描。可以用当前功能得到其谐振力常数，然后自己设计一个周期势函数，使其在0、120、-120度极小点处的力常数与m2Seminario得到的大致吻合。

如果你只需要模拟一个MOF-5单胞的话，其实补全参数最简单的方法是直接用CP2K做优化和振动分析，基于Hessian自动算出来所有缺的力场项，参考下面FeCl2的例子。

 

#### 例11：产生FeCl2二维材料的拓扑文件

此例产生FeCl2层状二维材料的拓扑文件。这一节分为两部分，第一部分演示懒人法，直接基于晶体结构，靠Sobtop猜的参数；第二部分做法较严格，基于CP2K对周期性结构做振动分析得到Hessian，让Sobtop严格地计算出所有力常数，但CP2K里振动分析的耗时很高。如果你只为了在模拟过程中维持FeCl2的刚性结构，用第一种做法就行了。FeCl2的原胞很小，仅有一个Fe和两个Cl，这一节我们对FeCl2的5\*5\*1的超胞结构来产生拓扑文件。

**1 懒人法：直接用猜的参数**

首先构造超胞的pdb文件。启动Multiwfn，载入Sobtop目录下的examples\FeCl2\FeCl2.cif，然后输入  
300 //主功能300  
7 //几何操作  
19 //构造超胞  
5 //第一个晶格矢方向复制成原先的5倍  
5 //第二个晶格矢方向复制成原先的5倍  
1 //第三个晶格矢（垂直于界面方向）保持不变  
-2 //保存pdb文件  
FeCl2_5x5x1.pdb //要产生的文件名

启动Sobtop，载入FeCl2_5x5x1.pdb，从屏幕上的信息可见每个Fe都是与6个Cl相连，每个Cl都与3个Fe相连，自动猜的连接关系符合实际情况。然后输入  
1 //产生拓扑文件  
6 //手动设置原子类型（由于当前用的不是mol2文件，故接下来没法选2先自动用GAFF原子类型然后用UFF的补全，而需要手动设置原子类型）  
Cl //选择所有氯原子  
cl //设为GAFF力场的cl原子类型  
1 //对未设定类型的原子用UFF原子类型  
0 //进入下一步  
4 //用预置的力场参数，缺失的自动猜  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

屏幕上提示的缺失力场项如下，很正常  
Missing bond types (equilibrium length comes from current geometry, while force  
constant is arbitrary guessed):  
1 cl-UF_Fe

Missing angle types (equilibrium angle comes from current geometry, while force  
constant is arbitrary guessed):  
1 cl-UF_Fe-cl  
2 UF_Fe-cl-UF_Fe

Missing dihedral types (rotational barriers are set to zero):  
1 cl-UF_Fe-cl-UF_Fe

前述的FeCl2_5x5x1.pdb里有晶胞信息，Z方向真空层足够大，不做修改就可以直接用于跑动力学。现将FeCl2_5x5x1.pdb、FeCl2_5x5x1.itp、FeCl2_5x5x1.top以及examples\md_PBC.mdp相结合，跑动力学模拟：  
gmx grompp -f md_PBC.mdp -c FeCl2_5x5x1.pdb -p FeCl2_5x5x1.top -o md.tpr -maxwarn 3  
gmx mdrun -v -deffnm md  
gmx trjconv -s md.tpr -f md.xtc -o md_new.xtc -ur tric -pbc atom，选system  
gmx trjconv -s md.tpr -f md.gro -o md_new.gro -ur tric -pbc atom，选system  
上面用trjconv处理是为了让新得到的xtc和gro文件里原子坐标的周期性记录方式满足当前FeCl2的三斜晶胞的情况。基于md_new.gro/xtc观看轨迹，可见FeCl2二维结构维持得非常好，刚性很强。  

**2 较严格方法：基于CP2K周期性DFT计算的Hessian得到参数**

首先用Multiwfn载入FeCl2.cif，参考《使用Multiwfn非常便利地创建CP2K程序的输入文件》（[http://sobereva.com/587](http://sobereva.com/587)）创建一个对FeCl2原胞的变胞几何优化任务的CP2K输入文件，用5\*5\*1 k点，优化过程中保持晶胞夹角和空间群不变，输入文件是examples\FeCl2\exact\opt.inp。跑完后，用Multiwfn载入优化任务产生的restart文件，在创建CP2K输入文件的界面里扩成5\*5\*1的超胞，再创建CP2K振动分析的输入文件，见examples\FeCl2\exact\freq.inp。之后退回到Multiwfn主菜单（如果你已经把Multiwfn关了也没事，此时载入freq.inp即可），用主功能100的子功能2将当前超胞结构保存成pdb文件opted_5x5x1.pdb。用CP2K跑freq.inp，从其输出文件freq.out中搜Hessian的话会看到里面确实记录了笛卡尔Hessian矩阵。

启动Sobtop，然后输入  
opted_5x5x1.pdb  
-1 //修改基于Hessian计算力常数的方法  
3 //m2Seminario。当前体系里有大量等价的键、键角、二面角，用默认的mSeminario的话得到的力常数会严重违背等价性。DRIH对于当前体系不理想故不考虑  
1 //产生拓扑文件  
6 //手动设置原子类型  
Cl //选择所有氯原子  
cl //设为GAFF力场的cl原子类型  
1 //对未设定类型的原子用UFF原子类型  
0 //进入下一步  
2 //所有参数皆基于Hessian计算产生  
examples\FeCl2\exact\freq.out //CP2K振动分析输出文件  
\[回车\] //用默认的top文件产生路径  
\[回车\] //用默认的itp文件产生路径

现在当前目录下就有了opted_5x5x1.itp和opted_5x5x1.top。当前目录下还产生了FFderiv.txt，里面记录了基于Hessian计算的每种类型的bond、angle、dihedral项的计算次数、所得参数的平均值/最小值/最大值。虽然当前用了m2Seminario方法计算力常数，但由于CP2K靠有限差分算的Hessian有一定数值误差，因此等价的力场项的力常数仍可能多多少少有点差异（但至少远小于用mSeminario的情况）。

顺带一提，对于Sobtop对当前体系算出来的最小值和最大值相差很小的bonded参数，可以考虑将它的平均几何参数和平均力常数添加到bonded_param.dat里，以供今后对类似体系直接使用。例如在FFderiv.txt里可见的如下所示的UF_Fe-cl-UF_Fe项就是这种情况，对当前体系总共算了150次，其键角和力常数的min和max值都比较相近，因此可以挪到bonded_param.dat里。  
2 Type: UF_Fe-cl-UF_Fe Times of evaluations: 150  
Avg, min, max of k: 675.30 664.43 695.20 kcal/mol/rad^2  
Avg, min, max of a0: 94.548 94.507 94.576 degree  
但FFderiv.txt里比如cl-UF_Fe-cl型的键角项的最小键角为85.437，最大键角为179.990，差异太大，因此不适合将此类键角项的平均参数放到bonded_param.dat里。

为检验拓扑文件合理性，用下面的命令跑动力学  
gmx grompp -f md_PBC.mdp -c opted_5x5x1.pdb -p opted_5x5x1.top -o md.tpr -maxwarn 3  
gmx mdrun -v -deffnm md  
gmx trjconv -s md.tpr -f md.xtc -o md_new.xtc -ur tric -pbc atom，选system  
gmx trjconv -s md.tpr -f md.gro -o md_new.gro -ur tric -pbc atom，选system  
从结果可见FeCl2的结构很好地维持住了。

别忘了，当FeCl2板和其它分子一起模拟时，需要给FeCl2赋予原子电荷，REPEAT电荷就不错。  

 

#### 例12：产生非标准残基的rtp文件字段

待写

 

 

### Skill

#### 技巧1：通过命令行方式使用Sobtop

Sobtop通常是以交互式方式使用，但也可以通过命令行方式使用，这可以很方便地将Sobtop嵌入shell脚本里，实现对大批量分子一键产生拓扑和gro文件。相关知识非常建议阅读《详谈Multiwfn的命令行方式运行和批量运行的方法》（[http://sobereva.com/612](http://sobereva.com/612)）。下面仅举个最简单的例子，通过命令行方式运行Sobtop产生examples\7-helicene.mol2的itp、top、gro，假设用户用的是Linux环境。

先创建一个文本文件，比如叫genGAFF.txt，内容是在Sobtop里要输入的所有命令，将之放到Sobtop目录下  
2  
1  
2  
4  
0

然后进入Sobtop目录，输入./Sobtop examples/7-helicene.mol2 \< genGAFF.txt \> 7-helicene.txt。之后当前目录下就有了7-helicene.itp、7-helicene.top、7-helicene.gro了。7-helicene.txt是Sobtop在屏幕上输出的那些信息，供检查用。

 

### FAQ

#### FAQ 1：我是初学者，我用Sobtop产生完了拓扑文件，然后怎么用GROMACS做模拟啊？

这个不是Sobtop的问题，而是GROMACS本身使用的问题，问出这种问题说明没有最基本的GROMACS常识性知识。怎么做模拟这种问题绝对不是三言两语就能说明白的，不懂分子动力学算法和分子力场的基础知识、不懂GROMACS的各种常见子程序的用法和拓扑文件的规则、不懂对于各类问题模拟的流程和应注意的要点，根本不可能开展模拟。零基础的话光是照着网上零七八碎、东一榔头西一棒子的教程（其中很多还有错误，或者是很过时的）去摸索效率极低，还容易被误导，还学得非常不系统，遇到问题也不知道怎么解决，也难以恰当地变通算自己的体系。我非常建议参加北京科音分子动力学与GROMACS培训班（[http://www.keinsci.com/KGMX](http://www.keinsci.com/KGMX)）特别系统性地循序渐进学一遍，就彻底全都明白了，在理解和使用Sobtop上也不会再遇到任何障碍。没机会到现场参加也没关系，往届的培训资料都可以随时购买自学，培训介绍页面里明确说了。

#### FAQ 2：为什么Sobtop直接支持的是GAFF和AMBER力场，会支持CGenFF、OPLS-AA、GROMOS么？

Sobtop支持的函数形式是GAFF/AMBER力场的，而且自带力场库包含的是GAFF/AMBER的参数，主要原因在于Sobereva很喜欢GAFF/AMBER力场，因为：  
(1)力场函数形式简单且标准  
(2)流行程度、被认可度极高  
(3)被分子模拟程序支持广泛，在GROMACS中完美支持  
(4)原子类型数目适中，而且名字非常简洁清楚，因此很便于管理（反观OPLS-AA的原子类型真是乱七八糟！）  
(5)基于RESP这种非常标准化的原子电荷计算方法，用Multiwfn可以方便地计算  
(6)GAFF（普通有机体系）、AMBER（蛋白质和核酸）、GLYCAM（糖类）、Lipid/Slipids（磷脂）、Merz（各类单原子离子）等高质量力场彼此兼容，组合使用可以描述无机以外的几乎各种体系

CGenFF、OPLS-AA、GROMOS力场能描述的体系用GAFF/AMBER也都能描述，GAFF/AMBER不能描述的那些力场也基本不能描述，因此我不觉得有任何必要去直接支持GAFF/AMBER以外的力场。

由于前面说了，Sobtop的力场库文件是完全开放的，所以如果其它力场里的力场项的函数形式与GAFF/AMBER的相同，也可以把它们的相应类型参数自己写到Sobtop的力场库里使用。因此，**Sobtop能创建的拓扑文件涉及的力场绝不仅限于GAFF/AMBER**，诸如例子里的二氧化硅、MOF-5、FeCl2体系都是完全脱离了GAFF/AMBER力场，过渡金属配合物的例子里对过渡金属也用了GAFF/AMBER以外的原子类型。

**附：AMBER和GAFF的关系**：我在答疑时经常发现有不少人搞不清楚GAFF和AMBER的关系，居然试图用AMBER描述小分子。这里顺带强调一下二者的联系。AMBER力场提出的目的是用于蛋白质和核酸的模拟，里面的原子类型、参数主要也是面向这类生物大分子的。虽然AMBER也不是不能描述有机小分子，但是很容易遇到缺适合的原子类型、缺需要的bonded参数的情况。后来提出的GAFF的全称是“广义化的AMBER力场”，开发的目的专门是用来描述各种杂七杂八的有机小分子，并且它和AMBER力场形式完全兼容，也有不少参数是直接从AMBER继承过来的，最适合搭配的都是RESP原子电荷（搭配后来的RESP2(0.5)也很好）。GAFF的原子类型都是小写，而AMBER是大写，所以二者一起用的时候不会有冲突。GAFF的原子类型比AMBER能更充分涵盖五花八门的有机小分子的情况，bonded参数也更丰富，**显然对于小分子体系没有任何理由用AMBER而不用GAFF**。而对于蛋白质和核酸，虽然比AMBER更普适的GAFF也能描述，但明显不如AMBER这样的对它们专一性的力场更合适。所以，对于诸如蛋白质+配体这种类型体系的模拟，蛋白质要用AMBER，配体要用GAFF。由于GAFF比较普适，所以只要不是像蛋白质、核酸这样有专门特别适合的力场的情况，都可以用GAFF。但也有很多情况有些元素不被GAFF支持，有些处于非典型电子结构状态的原子在GAFF里没有合适的原子类型能够描述，或者特殊的bonded参数在GAFF里没有，这时候就要考虑让Sobtop用UFF原子类型进行补充，以及用Sobtop基于Hessian矩阵计算力常数或者通过从文献搜索/自行拟合等其它方式补充bonded参数。

顺带一提，北京科音分子动力学与GROMACS培训班（[http://www.keinsci.com/KGMX](http://www.keinsci.com/KGMX)）专门有一节“分子力场”，里面超级全面系统介绍了所有主流力场和一切相关背景知识，十分推荐通过本培训完整系统学习一遍，这样就绝对不会在力场选择方面犯糊涂、犯错误了。

#### FAQ 3：Sobtop会支持AMBER、Lammps等程序么？

Sobtop没打算支持其它程序。我不用Lammps。AMBER我如今也很少用，因为GROMACS更快更灵活还完全免费，常用功能都有，还有gmx_mmpbsa、PLUMED等很多工具能扩展其功能。而且AMBER的拓扑文件相比于GROMACS过于复杂。

如果你是其它动力学程序的用户，也可以先借助Sobtop产生GROMACS的拓扑文件，然后再转成其它程序的。比如GROMACS拓扑文件转成AMBER、NAMD和CHARMM的可以用ParmED，转成Lammps的可以用GRO2LAM或InterMol。

#### FAQ 4：含阴、阳离子的体系的拓扑文件怎么产生？阴阳离子合在一起处理还是分开处理？

我强烈建议（这也是GROMACS的良好使用习惯），对体系中每种通过bond项（用于描述有显著共价特征的化学键，也包括配位键）连接到一起的片段，用Sobtop单独产生拓扑文件，并计算其原子电荷。比如离子液体，由于阴阳离子间是非共价作用，模拟过程中可以自发分离开，因此就应当对阳离子和阴离子部分分别照常产生拓扑文件，然后把二者的itp都include到主top文件里，并且把二者中的\[ atomtypes \]也都合并、去重后挪到主top的\[ defaults \]字段的后面去。再比如，你的体系里有苯甲酸钠，不应当对整个苯甲酸钠计算原子电荷和创建拓扑文件，因为钠离子和苯甲酸根在模拟过程中会自发分离。正确做法是对苯甲酸根计算原子电荷并使用sobtop创建拓扑文件，而Na离子用GROMACS自带的力场目录下的ions.itp里提供的\[moleculetype\]来描述。

有些零基础的GROMACS初学者对GROMACS的正确用法一无所知，居然试图用Sobtop产生整个模拟体系（含一大堆分子）的拓扑文件，然后直接用GROMACS跑，这种做法是极端野蛮粗暴不可理喻的！这么做可能在Sobtop里耗时很高，甚至完全产生不了而崩溃，而且所有分子的拓扑信息都搅合在一起作为一个\[ moleculetype \]出现时会特别难以管理和修改。

再顺带一提，在使用Packmol等程序构造离子液体凝聚相模型时，个人比较推荐把阴阳离子对作为一个整体来插入，而不建议阴、阳离子单独插入，否则产生的结构文件里可能恰好有的地方阳离子非常密集、有的地方阴离子非常密集。如果真出现了这种情况，模拟一开始，带相同电荷的离子间会产生强烈的静电互斥，可能造成动力学不稳定甚至崩溃。而阴阳离子作为一对来插入的话，至少保证了每个离子旁边有个相反电荷的离子，不至于出现局部静电互斥特别大的情况。别忘了top里的\[ molecules \]字段中离子出现顺序要和结构文件里相一致。

#### FAQ 5：Sobtop可以产生生物分子的拓扑文件么？

可以是可以，毕竟Sobtop是普适的，对这类体系可以用AMBER原子类型。但是对这类体系我不建议优先考虑Sobtop，因为GROMACS里自带的pdb2gmx是专门干这个的，它对蛋白质、核酸会自动修改质子化态、加氢、处理末端残基，这些对生物分子专一性的处理在Sobtop里是没有考虑的，而且pdb2gmx直接就会根据rtp文件里的定义去给氨基酸/核苷酸残基设置力场原文里定义的原子电荷。

Sobtop倒是可以帮助你去产生非标准残基的rtp文件。具体来说就是给标准残基两侧用ACE（乙酰）和NME（甲胺）封闭成模型分子，用量子化学程序做优化和振动分析。基于得到的波函数文件，用Multiwfn对非标准残基计算RESP电荷（将中间的残基的净电荷约束为整数）并得到chg文件。然后在Sobtop里载入模型分子的mol2文件，从chg文件里载入原子电荷，然后选产生rtp文件，其间让Sobtop自动指认AMBER原子类型，并要求从预置力场库文件里取合适的参数，缺的让Sobtop基于Hessian算出来。然后把得到的rtp里的字段恰当处理从分子状态变成为残基状态后，挪到GROMACS力场目录下的rtp里。

#### FAQ 6：Sobtop会支持二面角扭转势的拟合么？

早晚会。其实这个功能实现的复杂度完全看做到什么程度。最简单的情况，只是拟合一个二面角势函数而且不考虑优化phase参数，是非常简单的事。但如果同时考虑拟合多个二面角，还要优化phase参数，就是个非线性全局优化问题，这就很复杂了。

#### FAQ 7：我希望Sobtop能像MCPB.py那样产生金属蛋白的拓扑信息

做成MCPB.py那样原理上是不可能的，因为GROMACS产生蛋白质拓扑文件是靠pdb2gmx，其逻辑和AMBER的leap程序截然不同。

实际上目前的Sobtop就能对付金属蛋白体系，只不过手动操作较多。比如蛋白质中有个铁硫簇和几个残基结合，那就把铁硫簇以及与之配位的残基抠出来并饱和边缘作为一个簇模型，冻结边缘原子，用量子化学程序做优化和振动分析，参考《要善用簇模型，不要盲目用ONIOM算蛋白质-小分子相互作用问题》（[http://sobereva.com/597](http://sobereva.com/597)）里的讨论。然后对这个簇模型照常用Sobtop产生拓扑文件、计算RESP电荷，其间要求Sobtop完全基于Hessian矩阵获得力常数。然后，用Sobtop对铁硫簇部分产生参数为空的itp文件。之后，用pdb2gmx对纯蛋白质部分产生\[ moleculetype \]，将之和铁硫簇部分的\[ moleculetype \]都引入主top里，把铁硫簇和配位残基的原子电荷替换为前面计算的，把铁硫簇部分的参数替换为簇模型中铁硫簇部分的。然后在top里加入\[ intermolecular_interactions \]字段，这个字段里可以设置跨越不同\[ moleculetype \]的bonded项，其中加入\[ bonds \]、\[ angles \]、\[ dihedrals \]字段，在里面手动写入铁硫簇和配体残基两部分之间的bond、angle、dihedral项和之前对簇模型计算的相应的力场参数。注意这里写的原子序号是全局序号，即整个模拟的结构文件里对应的序号。

以上过程手动操作的地方较多，以后笔者可能会写辅助工具，给出个尽量自动化的方案，减少手动操作量。

#### FAQ 8：为什么我基于Sobtop产生的拓扑文件，在动力学模拟过程中GROMACS报错/崩溃？

mdrun跑计算期间不稳定乃至崩溃时会在屏幕上显示LINCS warning、segmentation fault、1-4 interaction not within cut-off、water can not be settled、Listed nonbonded interaction between particles ... larger than the table limit其中的一种或多种提示，还可能产生一大堆step\*\*\*\*.pdb文件。这是超级老生常谈的问题。为什么出现、怎么解决和Sobtop没直接关系，纯粹是GROMACS使用层面上的问题。既然出现崩溃，自然得试图搞清楚为什么崩溃，必须得基于GROMACS和分子动力学的常识性知识一点点排查，包括初始结构合理性、拓扑文件里的项和参数的合理性、mdp设置的合理性，都合理了自然就不崩溃了。下面就全面地谈一下，以下文字无论你是否用Sobtop产生拓扑文件都是适用的。PS：如果你欠缺GROMACS和分子模拟基本理论知识的话，光看以下文字可能也很难理解和解决问题，这种情况我强烈建议参加北京科音分子动力学与GROMACS培训班（[http://www.keinsci.com/workshop/KGMX_content.html](http://www.keinsci.com/workshop/KGMX_content.html)）从头非常系统性地学一遍，问题就全都明白了，也不会因为犯各种低级错误导致模拟老也没法顺利跑起来。

**检查mdp**：从mdp角度排查来说，首先确保设置的合理性。如果你觉得原本是合理的，在合理的范畴内可尝试不同的参数，比如原先模拟的温度较高就先试试低温、原本加的电场较大就把电场改小点、调节压浴设置（例如把nstpcouple改小，2023版开始nstpcouple默认值可能偏大，可改小到10试试。也可以尝试不同的压浴，如Parrinello-Rahman改成更稳且更普适的C-rescale），等等。还找不到原因就把能去掉的设置一点点去掉，比如用了控压就把控压去掉、用了冻结就把冻结去掉（或改用位置限制基本等效地实现）、用了约束就把约束去掉、用了电场/pull/外力设置就将它们去掉、用了能量-压力色散校正就把它去掉，等等，修改设置后重新跑，反复对比找原因，看是否是哪些设置造成的问题。

动力学步长太大是导致动力学不稳定的常见因素，如果原先用的2 fs步长结合氢有关的键的约束，应当改成1 fs乃至0.5 fs不加约束再试，如果此时能顺利跑下去，等跑一段时间体系弛豫了、相对平稳了，续跑时候可再切换回2 fs步长+约束照常跑。顺带一提，用约束时绝对不要用某些误人子弟的教程里的constraints = all-bonds。

产生初速度、控温方式是特别要注意的，温度和原子速度分布关系密切，若有原子速度过大可能造成崩溃。如果你用了gen_vel = yes结合默认的gen-temp = 300要求程序产生对应300 K时Maxwell分布的原子初速度，建议把温度设低点，比如50或100 K，否则可能有个别原子初速度太大造成崩溃。关于控温，我一般都建议设置退火，从较低温度（0或100K）经过100~200 ps线性、平缓地升温到实际研究的温度。如果不设退火，而且热浴时间常数tau-t比较小的话，可能由于温度变化太快导致出现有的原子速度瞬间过大而崩溃。

**检查结构文件**：从结构文件（给grompp用的gro或pdb）角度来说，一定要注意结构文件里的分子顺序和top文件里的\[ molecules \]里记录的顺序必须一致，且结构文件里各个分子里原子的顺序和拓扑文件里相应的\[ moleculetype \]中的\[ atoms \]里的顺序必须一致，否则用的参数就乱套了，就算不崩溃结果也毫无意义。

还要确保动力学初始结构中没有明显不合理的原子间接触。如果之前没做能量极小化的话记得先做能量极小化以消除不合理的接触、过大的斥力，否则动力学一开始由于有的原子受力太大导致之后速度太大，很容易崩溃。如果之前做过能量极小化，而mdp里emtol设得较大，比如500，可以设得更小点（如100或50），让能量极小化做得更充分一些再试。也注意nsteps的设置，这个控制的是能量极小化的步数上限，如果设得不够大的话，可能斥力还没充分释放时能量极小化任务就自动停掉了。

**检查拓扑文件**：从拓扑文件角度来说，要注意检查\[ bonds \]、\[ angles \]、\[ dihedrals \]、\[ pairs \]字段，是否该有的项都有，而且里面的参数都是合理的。把分子结构连同原子序号显示出来，对照着一个一个看，基于分子力场和GROMACS拓扑文件的基本知识来判断合理性并不困难。如果参数是你自己照着文献里的值填进去的，或者从其它力场/程序里挪过来的，注意原本的地方用的力场函数形式是否和当前相同、单位转换是否弄对了。还要注意检查\[ atoms \]里的原子电荷是否都是合理的。如果里面涉及到了你额外补充的原子类型，也检查\[ atomtypes \]里的范德华参数的合理性，注意函数形式、单位等问题。

**注意看grompp的提示**：记得在用grompp产生tpr文件时，一定要仔细看屏幕上的NOTE和Warning，理解是什么含义，能忽略的就忽略（出现N个warning时可以grompp加-maxwarn N来忽略），如果是可能导致动力学出问题的因素则要想办法解决，不能简单地无视。

**仔细观察轨迹**：通过在VMD里看动力学轨迹，经常从肉眼上就能发现结构变化不合理的地方，进而判断出崩溃的原因。比如拓扑文件里少了个bond项，自然会导致动力学过程中该维持住的地方散架；再比如某个键角参数的平衡值或力常数严重不合理，很容易造成结构严重扭曲，这显然从轨迹里是能看出来的。如果动力学模拟刚一开始就崩溃，为了便于找原因，可以把nstxout设为1（或很小的值），这样每一步的结构都会输出到轨迹文件里便于细致分析结构变化，这对于一些特殊情况很有用。比如曾经我用某个程序产生带磺酸基的分子的拓扑文件，看似拓扑文件没任何毛病，但跑起来就是会崩。后来一帧帧地观看模拟开始后的结构变化，发现是磺酸基上的氢在一瞬间跑到距离氧很近的地方去了。分析发现是由于这个基团上的氢带的电荷很正，氧的电荷很负，它们彼此间有1-4静电作用项因此有很强的静电吸引，再加上氢的质量很小、很容易运动，导致了上述看到的问题。像这种情况，可以把1-4作用项去了（从\[ pairs \]中删除对应的），也可以把氢改成质量更大的重氢（在\[ atoms \]里改原子质量）减缓其运动，或者用很小的模拟步长。显然，从拓扑文件和参数中找出原因必须对拓扑文件里的各种项、力场的函数形式都理解得很清楚才行。

当怀疑一个分子的拓扑文件有问题时，应当先对分子在真空下进行模拟，只有一个分子时比较容易观看；而如果带着其它分子一起跑，或者模拟的是某种分子的凝聚相，显然就不方便观看结构了。但也有时候在真空下模拟时没问题，仅当其它分子存在，因而涉及到分子间相互作用时问题才会暴露出来。

**简化体系**：如果你模拟的是复杂体系，遇到动力学过程报错时应想到到不断简化体系进行测试，体系越简单越容易找出报错的原因。比如，模拟一个蛋白质+配体+纳米管+水的体系遇到报错，对这样复杂的体系显然很难直接排查出问题出在哪里，因此应当分别尝试蛋白质+水、纳米管+水、配体+水能否模拟。如果发现只有配体+水不能模拟，那再看看真空中跑一个配体分子能不能模拟。如果还不能，那自然就应当着重分析是不是配体的拓扑文件存在问题。这种把复杂问题简化是遇到计算报错问题最基本的逻辑。

**并行计算方式**：mdrun通常默认会使用多个thread-MPI来并行计算，此时会使用域分解策略进行计算。但对于个别情况，可能由于不当的域分解策略造成崩溃。可以给mdrun加上-ntmpi N和-ntomp M，分别指定thread-MPI并行进程数和每个下属的OpenMP并行线程数，反复调节N和M。对于非GPU加速的情况，N和M的乘积应等于CPU的物理核心数以最大程度利用CPU运算性能。遇到崩溃问题，建议先尝试只写-ntmpi 1，这样的话相当于不会利用域分解，可以由此判断是否是域分解造成的崩溃问题。

该说的上面都说了，没什么可补充的了。以后问我为什么GROMACS动力学崩溃时，不要就说个崩溃了，没有信息量的问题不可能回答。先尽自己最大可能按上面说的自己排查、分析、解决，如果花费两天时间还解决不了，届时把问题描述详细并发到计算化学公社论坛（[http://bbs.keinsci.com](http://bbs.keinsci.com)）的分子模拟板块，必须上传mdp、拓扑和结构文件（别就传个mdp文件，别人都不知道你跑的结构是什么。而且前面说了，mdp里设置不合理仅仅是可能导致出现问题的众多原因之中的一个），我总会看到，在有空的时候会回答。

#### FAQ 9：为什么Sobtop调用OpenBabel计算MMFF94原子电荷时失败？

首先要知道，MMFF94是面向普通有机体系构造的力场，此力场定义的计算原子电荷的方法也只适合普通有机体系。如果你的体系里有比如金属、硼等普通有机体系里不存在的元素，或者你的体系里有一些很特殊的成键方式，显然就没法成功计算MMFF94原子电荷了。而且就算能计算出来，结果也可能不靠谱（至少应当结合理论化学常识判断一下）。

如果安装OpenBabel的方式不当，也可能由于OpenBabel的功能不正常而得不到MMFF94原子电荷。切勿用一些古灵精怪的方法安装OpenBabel。如果你用的是Windows，应当去OpenBabel官网上下载Windows版安装包并安装，不建议用conda等特殊方式安装（除非你安装完了后通过手动用命令行方式使用OpenBabel时能确保功能是正常的），而且安装时不要装到默认的带空格的Program Files目录下。

mol2文件格式不标准也可能导致OpenBabel没法正常载入而失败，应当自己检查mol2文件内容。

#### FAQ 10：使用Sobtop必须提供Hessian矩阵么？

**当 然 不 是！！！**我很难理解为什么经常有人有这种误解。明明本页面里的一些例子诸如“产生苯甲酸甲酯的GROMACS的拓扑和gro文件：参数完全基于GAFF的”就根本没有利用用户提供的Hessian矩阵。看教程一定要一个字一个字认真看完整，**绝对不要断章取义！**教程里写得很清楚，Sobtop有bonded_param.dat力场库文件，如果你要求Sobtop用的参数全都直接来自于力场库文件，当然就用不着提供Hessian。仅当你要求Sobtop基于Hessian计算力常数的情况才必须提供振动分析任务产生的Hessian。

#### FAQ 11：什么时候才需要Sobtop基于Hessian算力常数？

对那些适合谐振势描述的bonded项（键长、键角、不可周期性旋转的刚性二面角），而且GAFF力场里没有适合参数，而且文献里也找不到合适的参数的情况，才有必要自己算力常数。最典型的就是诸如《使用Sobtop超级方便地创建二茂铁的GROMACS的拓扑文件》 （[http://sobereva.com/635](http://sobereva.com/635)）所示的过渡金属配合物，通常涉及过渡金属配位键的相关力场项都适合当做刚性的，因而可以用谐振势描述，但GAFF里却没有适用的参数，文献里也很难找到能用的参数，所以才明显有必要让Sobtop基于Hessian计算它们的力常数并写到拓扑文件里。

我之前看到有人计算柔性有机分子（比如多巴胺）居然也让Sobtop计算力常数，这明显是费力不讨好。这种分子有柔性的可旋转的二面角，若计算力常数而把这样的二面角用谐振势来描述，二面角还怎么旋转？分子的柔性特征还怎么体现？而且GAFF对于普通有机分子就已经描述得挺好，直接让Sobtop按照苯甲酸甲酯的例子指认GAFF的参数就完了，这还免得你去用量子化学程序事先做结构优化再做振动分析。

#### FAQ 12：基于Hessian算的力常数产生周期性体系的拓扑文件时，振动分析必须用超胞么？

做周期性体系动力学模拟时，往往涉及大量的重复单元，甚至能达到好几千原子，而直接对这么大体系用CP2K做振动分析得到力常数耗时极高，或者根本不可能算得动。

对于这种情况，你可以取一个合适大小的晶胞（如果单胞就已经够大了，比如MOF-5，用单胞即可。如果单胞很小，必须先平移复制到足够大，以确保得到的力常数靠谱，参考FeCl2的例子的做法），对它做振动分析，并用Sobtop得到体系中涉及的各种力常数。然后将这些力常数连同平衡几何参数写入到bonded_param.dat里，并且在assign_AT.dat里定义原子类型判断规则。之后当前体系的任意大的超胞结构都可以迅用Sobtop速产生拓扑文件了，产生的时候让Sobtop根据assign_AT.dat的规则判断原子类型，并基于原子类型直接从力场库文件里取合适的参数。

对原子电荷也是如此，绝对不是说实际要模拟多大的超胞就必须对多大的超胞体系用CP2K计算。也是取一个算得动大小的模型体系，算出来原子电荷后写入assign_AT.dat的原子类型判断规则里即可。之后Sobtop按照此文件里的规则指认原子类型时，原子电荷也就一并指认了。

#### FAQ 13：为什么Sobtop载入mol2文件时元素不识别？为什么识别出的元素和实际不符？

这都是因为你提供的mol2文件不规矩所致。给Sobtop用的mol2文件不能太不规矩，然而有些来源、有些程序产生的mol2文件相当不规矩。用文本编辑器打开.mol2文件，可看到在@\<TRIPOS\>ATOM字段下面记录了原子的信息，比如  
7 H7 -4.0563 -0.4333 -0.0000 H  
第一个数字是原子序号。H7是这个原子的原子名。然后是原子的XYZ坐标。再往后是atom type（这和实际Sobtop指认的原子类型是两码事）。当前atom type是H，因此此原子会被Sobtop解析为是氢原子。在mol2标准格式中，atom type也可以是诸如N.am、S.O2、O.3等形式，可见共性都是圆点前面是元素名，因此Sobtop如果发现atom type中有圆点的时候会根据圆点前的字符判断元素。

根据以上规则，通过检查你的mol2文件，自然就能明白为什么有的原子没有被Sobtop正确识别了。原子信息不规矩的话自然需要自己手动修改，或者换其它程序产生mol2文件。推荐阅读《谈谈记录化学体系结构的mol2文件》（[http://sobereva.com/655](http://sobereva.com/655)）了解mol2格式的具体信息。

#### FAQ 14：为什么sobtop产生的周期性体系的拓扑文件里面有平衡键长很大（如几nm）的bond项？

这是因为你用GaussView产生的mol2当做sobtop一开始的输入文件，而且要求sobtop自动猜或者基于Hessian矩阵计算bonded参数。即便GaussView载入的是cif这样含晶胞信息的文件，它产生的mol2文件也不包含晶胞信息，因此sobtop会以为当前体系是孤立体系，那些本来是跨越晶胞的键就成了孤立体系内长得离谱的键了。有两个解决办法：  
(1)用记录了晶胞信息的pdb文件作为输入文件，sobtop会根据原子间距离（考虑周期性）和元素半径判断连接关系。此做法的缺点是没法保证sobtop判断的连接关系和GaussView图形界面里看到的键完全一致  
(2)在mol2文件里写入晶胞信息，使得sobtop把此体系视为周期性体系。在mol2文件末尾加入一行@\<TRIPOS\>CRYSIN，在下一行写晶胞的a、b、c三个边长（埃）以及alpha、beta、gamma夹角（度），每个值之间以逗号分隔。例如：  
@\<TRIPOS\>CRYSIN  
3.785,3.785,9.514,90,90,90

#### FAQ 15：为什么sobtop对巨大体系指认原子类型花费时间极长？

如果体系非常大，比如几千个原子，指认原子类型那一步不要选“Assign GAFF atom types...”或“Assign AMBER atom types...”，否则程序通过分析化学环境来判断GAFF或AMBER原子类型花的时间极多，甚至好几个小时也完成不了。这种情况应当用其它方式指认原子类型，比如按照assign_AT.dat文件定义的规则指认原子类型，或者手动通过输入原子序号指认原子类型。

#### FAQ 16：我对很大的固体表面用sobtop产生拓扑文件，但生成二面角的过程耗时极高，或者产生出的itp文件尺寸极大，怎么解决？

要求不产生二面角项就行了，即把sobtop.ini里的iskipgendih设为1。很大的体系二面角项巨多，考虑二面角项的话必定导致产生拓扑文件耗时非常高，以及产生出的itp文件巨大。对于研究固体表面类型的体系通常二面角项没有什么用处，因为靠bond和angle项就能维持住结构。固体表面大多是呈高度刚性的，或者其可变形特征对于实际研究的问题可忽略不计，这种情况就连bond和angle项都可以不必考虑（如果手动从itp里删掉的话可以减小itp的体积），动力学模拟时把原子坐标冻结或者加上位置限制势固定就够了。

#### FAQ 17：sobtop产生的gro文件和输入文件里的坐标不一样是怎么回事？

sobtop不会无缘无故修改你的输入文件里的坐标。但如果你让sobtop从chg文件里载入原子电荷，那么坐标也会被替换成chg文件里的坐标，此时导出的gro文件里的坐标和chg文件里的一致。如果你不想让坐标自动被替换成chg文件里的，把sobtop.ini里的ichggeom设为0。

如果chg文件是Multiwfn载入诸如fch、molden等波函数文件之后计算原子电荷后导出的，那么chg文件里的坐标和波函数文件里的坐标严格一致。

如果chg文件是通过比如《[RESP2原子电荷的思想以及在Multiwfn中的计算](http://sobereva.com/531)》、《[ORCA结合Multiwfn计算RESP、RESP2和1.2*CM5原子电荷的懒人脚本](http://sobereva.com/637)》里的脚本得到的，由于脚本自动会做几何优化（除非用的是带noopt后缀的脚本），显然得到的chg文件里的坐标不会和脚本的输入文件里的坐标精确一致。

哪怕你是只用Gaussian算单点（而非优化）任务产生fch文件然后用于Multiwfn产生chg文件，chg里的坐标也不会和Gaussian输入文件里的一致，因为Gaussian默认会把体系摆到标准朝向下，即fch文件里的坐标是标准朝向下的。只有写nosymm关键词才能避免Gaussian自动平移、旋转体系，不懂的话看《[谈谈Gaussian中的对称性与nosymm关键词的使用](http://sobereva.com/297)》。

对于sobtop载入chg文件的情况，若你总是想确保sobtop产生的gro文件里的坐标和给sobtop的输入文件里的完全一致，可以直接把输入文件里的坐标通过Ultraedit的列模式替换到chg文件里（区区十秒钟的事。chg文件里的坐标是自由格式，替换方便。虽然自行替换到gro文件里也行，但gro文件是固定格式，自己替换的话容易弄错）。

#### FAQ 18：sobtop里怎么用GAFF2力场？

由于目前GAFF2还没有正式发表，所以sobtop里用GAFF2目前需要按下面说的改一下。等以后GAFF2正式发表了，sobtop就会直接以GAFF2完全代替GAFF了。

先备份sobtop目录下的ATOMTYPE_GFF.DEF、bonded_param.dat、LJ_param.dat（比如可以建立个GAFF目录，把它们都挪进去）。然后把sobtop目录下的examples\GAFF2\子目录中的ATOMTYPE_GFF2.DEF、bonded_param.dat、LJ_param.dat都放到sobtop目录下，把ATOMTYPE_GFF2.DEF改名为ATOMTYPE_GFF.DEF。  
注：这里的CORR_NAME_TYPE.DAT和ATOMTYPE_GFF2.DEF取自AmberTools 24，bonded_param.dat和LJ_param.dat里面的GAFF2的参数对应AmberTools 24带的GAFF2参数文件（gaff2.dat）。

然后在sobtop里照常指认GAFF原子类型和参数，就等价于指认GAFF2的原子类型和参数了。

#### FAQ 19：sobtop产生的拓扑文件能结合CHARMM、OPLS-AA等力场使用么？

不能。在我网上回答问题时，看到好多次有人试图用sobtop产生的基于GAFF力场的配体的拓扑文件和OPLS-AA或CHARMM力场描述的蛋白质相结合做蛋白质-配体复合物的动力学模拟，这真是匪夷所思的事！首先，蛋白质用AMBER力场描述非常理想、和GAFF完美兼容，干嘛蛋白质不用AMBER力场？其次，GAFF和OPLS-AA、CHARMM根本不能兼容，因为获得原子电荷的方法、LJ参数混合规则、对1-4项的考虑都不一样。所有CHARMM、OPLS-AA能模拟的体系，靠AMBER+GAFF都能很好地模拟，至少不会输于它们。此外，糖类还可以用专门的GLYCAM力场、磷脂可以用Slipids或Lipid力场、乱七八糟的AMBER/GAFF不支持的单原子离子可以用KBFF或Merz力场，这都与AMBER/GAFF完全兼容。而碳纳米、石墨烯管之类，CHARMM/CGenFF、OPLS-AA和GAFF都一样并未做特殊的考虑。可见根本没有任何理由非要把sobtop产生的拓扑文件和CHARMM或OPLS-AA结合使用。至于GROMOS就更不可能和GAFF兼容了，前者是联合原子力场后者是全原子力场。

总之，做动力学模拟和正确使用sobtop都需要有基本的分子力场的知识，这样才不会胡算瞎算、胡用瞎用。北京科音分子动力学与GROMACS培训班（[http://www.keinsci.com/KGMX](http://www.keinsci.com/KGMX)）里专门有一节“分子力场”把各种力场讲得十分全面系统，十分建议缺乏相关知识的人参加系统学一遍，免得犯常识性错误。

#### FAQ 20：什么物质不适合用sobtop产生拓扑文件？

- 虽然sobtop非常普适，但绝不是所有情况都适合用sobtop产生拓扑文件，因为对一些体系有更好、更专一性的选择，以下是典型的例子：

- 蛋白质（包括普通的小肽）、核酸：这些生物分子应当用pdb2gmx产生专门的力场的拓扑文件。因为pdb2gmx会恰当加氢、对末端残基进行特殊考虑、对力场支持的残基指认专门定义的原子电荷，明显处理得更为周到（但不少没常识的初学者乱用pdb2gmx也是个常见问题，甚至居然以为什么拓扑文件都能靠pdb2gmx产生。始终记得pdb2gmx能产生拓扑文件的体系仅仅限于体系中的残基都是在力场目录下的rtp文件里定义过的情况）。

- 水：必须用现成的水模型。水分子极其重要，已有的水模型都有好几十种了，如SPC/E、TIP4P-Ice、OPC3、OPC等。北京科音分子动力学与GROMACS培训班（[http://www.keinsci.com/KGMX](http://www.keinsci.com/KGMX)）里专门有一节“溶剂模型”对此讲得极其全面详细。通用程序产生的水的参数远没有专门的水模型（往往是通过尽可能重复各种已知实验数据来优化的参数）理想。

- 单原子离子：直接用GROMACS自带的力场或第三方力场包（如KBFF，[http://kbff.chem.k-state.edu](http://kbff.chem.k-state.edu)）的力场目录下的ions.itp就完了。或者基于文献里的参数（如Merz的离子力场）自己直接手写\[ moleculetype \]并在\[ atomtypes \]里添加额外的原子类型的定义来使用

- CO<sub>2</sub>、N<sub>2</sub>、H<sub>2</sub>等微型分子：合理描述它们的特征对参数的准确度要求很高，而且也都有广泛的文章对它们做过模拟，故应当用文献里专门优化、验证的参数并手写\[ moleculetype \]、在\[ atomtypes \]里添加原子类型定义。在网上也能找到一些微型分子现成的GROMACS用的拓扑文件，如TRAPPE-small力场的[http://bbs.keinsci.com/thread-36352-1-1.html](http://bbs.keinsci.com/thread-36352-1-1.html)。

- 磷脂：用Sobtop产生拓扑文件没有问题，但如果是常见的磷脂，像是DPPC等，知名的磷脂力场都对其有定义，显然用专门的力场更好。比如知名的Slipids以及Lipid磷脂力场都和AMBER/GAFF完全兼容，前者的GROMACS拓扑文件见[http://www.fos.su.se/~sasha/SLipids/Downloads.html](http://www.fos.su.se/~sasha/SLipids/Downloads.html)，后者的GROMACS拓扑文件可以在[http://bbs.keinsci.com/thread-43852-1-1.html](http://bbs.keinsci.com/thread-43852-1-1.html)直接下。

#### FAQ 21：自动指认GAFF原子类型的时候报错Unrecognized atomic name ( 并自动退出/崩溃

- 出现这个问题常见有以下可能：
- mol2文件格式不规矩。应首先确保载入的mol2结构文件格式合理，照着《谈谈记录化学体系结构的mol2文件》（[http://sobereva.com/655](http://sobereva.com/655)）检查元素名。如果查不出什么毛病，载入GaussView并保存成新的mol2文件再试。
- 有某原子成键数目多得离谱、极为反常，应手动在GaussView里删掉多余的键保存成新的mol2再试，一个解决例子见[http://bbs.keinsci.com/thread-52295-1-1.html](http://bbs.keinsci.com/thread-52295-1-1.html)。
- 可能mol2文件里的@\<TRIPOS\>BOND字段有诸如34 20 52 Wk这样的行，代表第34个键是20-52之间的Weak（Wk）作用，这是sobtop不支持的，如果20-52确实是弱相互作用，把这行删掉，而如果是共价键，则把Wk改成实际的形式键级（如1代表单键）。
- 一个mol2里同时包含了多个分子或离子，比如同时包含离子液体的阳离子和阴离子。如FAQ4所述，不应当让Sobtop试图直接处理这样的体系的拓扑文件。要记住Sobtop产生拓扑文件的对象是靠共价键连接成的一个整体。

 

### TODO list

Supporting fitting dihedral parameters based on scanning curve obtained by quantum chemistry calculation.

Designing an convenient and ideal protocol to prepare topology file of metalloprotein.

Designing an convenient protocol to prepare .rtp file of non-standard residue.

Facilitating assignment of RESP charges for polymers

### Update History

**Version 2026.1.16:** Limit of atomic indices has been extended to 999999.

**Version 1.0(dev5):** 2024-Sep-15. Fixed a bug of reading atomic indices when manually assigning atomic charges.

**Version 1.0(dev4):** First release: 2024-Jun-5, Last update: 2024-Jun-7

**Version 1.0(dev3.1):** First release: 2022-May-18, Last update: 2022-Aug-9

**Version 1.0(dev3):** 2022-Mar-26

**Version 1.0(dev2):** 2022-Mar-14

**Version 1.0(dev):** 2022-Feb-16

### Published papers that utilized Sobtop

Shermo has been utilized by more and more computational chemists in their daily research due to its unique value. The following publications have employed and cited Shermo (incomplete list):

1.  Ziyi Wang , Ruimin Song, Weigen Chen, et al., Vibrational Spectra and Molecular Vibrational Behaviors of Dibenzyl Disulfide, Dibenzyl Sulphide and Bibenzyl, Int. J. Mol. Sci., 23, 1958 (2022) https://www.mdpi.com/1422-0067/23/4/1958/htm
2.


## Sobtop 下载包文件索引

- 下载地址：<http://sobereva.com/soft/Sobtop/sobtop_2026.1.16.zip>
- SHA256：`d8a6726ad80a930d45bbcc34f5d32ea47ecca201aacd34ce1a870680d45c3c38`
- 文件数：74

| 路径 | 大小(bytes) |
| --- | ---: |
| `assign_AT.dat` | 2235 |
| `atomtype` | 192208 |
| `atomtype.exe` | 232208 |
| `ATOMTYPE_AMBER.DEF` | 7057 |
| `ATOMTYPE_GFF.DEF` | 16851 |
| `bondcrit.dat` | 434 |
| `bonded_param.dat` | 267053 |
| `CORR_NAME_TYPE.DAT` | 1445 |
| `examples/AMBER.itp` | 4836 |
| `examples/CNT/CNT.itp` | 806731 |
| `examples/CNT/CNT.pdb` | 45765 |
| `examples/CNT/CNT.top` | 331 |
| `examples/diamond_3x3x3/diamond_3x3x3.itp` | 1872660 |
| `examples/diamond_3x3x3/diamond_3x3x3.pdb` | 17398 |
| `examples/diamond_3x3x3/diamond_3x3x3.top` | 361 |
| `examples/exercise/7-helicene.mol2` | 2845 |
| `examples/exercise/COBH3.mol2` | 444 |
| `examples/exercise/PTZ.mol2` | 2971 |
| `examples/FeCl2/exact/FFderiv.txt` | 1075 |
| `examples/FeCl2/exact/freq.inp` | 7241 |
| `examples/FeCl2/exact/freq.out` | 5364970 |
| `examples/FeCl2/exact/opt.inp` | 4162 |
| `examples/FeCl2/exact/opt.out` | 72087 |
| `examples/FeCl2/exact/opted_5x5x1.itp` | 213990 |
| `examples/FeCl2/exact/opted_5x5x1.pdb` | 6118 |
| `examples/FeCl2/exact/opted_5x5x1.top` | 355 |
| `examples/FeCl2/FeCl2.cif` | 1177 |
| `examples/FeCl2/FeCl2_5x5x1.pdb` | 6118 |
| `examples/FeCl2/lazy/FeCl2_5x5x1.gro` | 3563 |
| `examples/FeCl2/lazy/FeCl2_5x5x1.itp` | 258999 |
| `examples/FeCl2/lazy/FeCl2_5x5x1.top` | 355 |
| `examples/GAFF.itp` | 6655 |
| `examples/GAFF2.itp` | 7858 |
| `examples/GAFF2/ATOMTYPE_GFF2.DEF` | 17916 |
| `examples/GAFF2/bonded_param.dat` | 468740 |
| `examples/GAFF2/LJ_param.dat` | 16679 |
| `examples/md_PBC.mdp` | 692 |
| `examples/md_vac.mdp` | 570 |
| `examples/Methyl_benzoate/Methyl_benzoate.fchk` | 1921447 |
| `examples/Methyl_benzoate/Methyl_benzoate.gro` | 945 |
| `examples/Methyl_benzoate/Methyl_benzoate.itp` | 13358 |
| `examples/Methyl_benzoate/Methyl_benzoate.mol2` | 1110 |
| `examples/Methyl_benzoate/Methyl_benzoate.top` | 367 |
| `examples/MOF-5/CP2K_REPEAT-RESP_CHARGES.resp` | 13222 |
| `examples/MOF-5/CP2K_REPEAT.inp` | 26625 |
| `examples/MOF-5/CP2K_REPEAT.out` | 31210 |
| `examples/MOF-5/MOF-5.cif` | 34813 |
| `examples/MOF-5/MOF-5.itp` | 462850 |
| `examples/MOF-5/MOF-5.mol2` | 26479 |
| `examples/MOF-5/MOF-5.pdb` | 34038 |
| `examples/MOF-5/MOF-5.top` | 337 |
| `examples/MOF-5/MOF-5_fragment.gjf` | 5510 |
| `examples/MOF-5/MOF-5_fragment.mol2` | 5186 |
| `examples/polymer/Neoprene_10_cross.itp` | 91361 |
| `examples/polymer/Neoprene_10_cross.mol2` | 5669 |
| `examples/polymer/Neoprene_10_cross.top` | 373 |
| `examples/polymer/Neoprene_40.gro` | 18605 |
| `examples/polymer/Neoprene_40.itp` | 371338 |
| `examples/polymer/Neoprene_40.mol2` | 23807 |
| `examples/polymer/Neoprene_40.top` | 355 |
| `examples/SF6/SF6.fchk` | 2147167 |
| `examples/SF6/SF6.gro` | 427 |
| `examples/SF6/SF6.itp` | 4681 |
| `examples/SF6/SF6.mol2` | 500 |
| `examples/SF6/SF6.top` | 331 |
| `examples/SiO2_3x3x3/SiO2_3x3x3.itp` | 419392 |
| `examples/SiO2_3x3x3/SiO2_3x3x3.pdb` | 25997 |
| `examples/SiO2_3x3x3/SiO2_3x3x3.top` | 354 |
| `examples/UFF.itp` | 8336 |
| `libiomp5md.dll` | 2047000 |
| `LJ_param.dat` | 19763 |
| `sobtop` | 17804208 |
| `sobtop.exe` | 14447104 |
| `sobtop.ini` | 964 |

## Sobtop 下载包关键文本文件摘录

### sobtop.ini

```text
  nthreads= 4  // Number of threads used for parallel calculation
  iskipgendih= 0  // 1: Skip generating dihedral terms, 0: Do not skip
  ioutatminfo= 0  // 1: Output atomic coordinates and connectivities when to atminfo.txt in current folder when loading input file, 0: Do not output to file but shown on screen
  ichggeom= 1  // 1: When loading .chg file, replace current geometry with that in .chg file, 0: Do not replace
  k_method= 2  // Default method of determining k. 1: Seminario, 2: mSeminario, 3: m2Seminario, 4: DRIH
  bondcrit= 1.15  // When pdb/pqr is used as input, two atoms are considered as bonded if their distance is smaller than sum of their covalent radii multiplied by this factor. Priority is lower than the criteria defined in bondcrit.dat
  Multiwfn_cmd= "D:\CM\my_program\Multiwfn\Multiwfn.exe" // Path of executable file of Multiwfn
  OpenBabel_cmd= "D:\study\OpenBabel-3.1.1\obabel.exe"  // Path of executable file of OpenBabel
```

### assign_AT.dat

```text
;This file defines rule of determining atom types according to bondings and distances
;The lines beginning with semicolon are comment lines
;
;Each atom type starts with $ symbol, then optionally followed by atomic charge. &
;Specific definitions are given in the next line(s), the following constraint(s) can be used, each one occupies a line
;  nbond: The number of bonds the atom must form
;  element: The element of the atom must be
;  bond: The bonding relationship criteria. The number of terms can be less than nbond. &
;For example, "bond -1 C 2 O 1 H -2 N" means the atom must simultaneously bond to a carbon with aromatic bond (denoted by -1), &
;to an oxygen with double bond, to a hydrogen with single bond, and to a nitrogen with arbitrary bond (denoted by -2).
;  dist: Distance criteria. The number of terms can be less than nbond. &
;For example, "dist 1.05-1.1 C 1.05-1.1 C 1.19-999 O" means there must be two carbons bonding to this atom &
;both with bond length of 1.05-1.1 A. At the same time, there must be an oxygen bond to this atom &
;with bond length of 1.19-999 A (i.e. at least 1.19 A).
;  angc: Angle criteria (present atom is in center). The number of terms can be less than actual number of angles of this atom type. &
;For example, "angc 115.5-124 C H 100-110 C H 120-122.3 O H" means there must be two C-X-H angles (X is present atom), &
;one within 115.5-124 and another one within 100-110 degree. Also this atom should has a O-X-H angle within 120-122.3 degree.
;  angt: Angle criteria (present atom is in terminal). The number of terms can be less than actual number of angles of this atom type. &
;For example, "angt 115.5-124 C N 100-110 C N 120-122.3 O H" means there must be two X-C-N angles (X is present atom), &
;one within 115.5-124 and another one within 100-110 degree. Also this atom should has a X-O-H angle within 120-122.3 degree.
;See http://bbs.keinsci.com/thread-43186-1-1.html for more example of using angc and angt
;
;Examples:
;$C_ar
;nbond 3
;element C
;bond -1 C -1 C 1 H
;
;$C_CH3
;nbond 4
;bond 1 H 1 H 1 H
;
;$H_CH3 0.1
;nbond 1
;dist 1.05-1.1 C

$Ctest
nbond 4

$Si_bulk 1.1
nbond 4
element Si

$O_bulk -0.55
nbond 2
element O
```

### bondcrit.dat

```text
; You can define lower and upper limits for determining existence of bond between
; specific two elements in this file. For example, if you add the
; following lines to this file, then if distance (Angstrom) between Fe and Cl is
; >= 2.0 and <=2.4, then they will be regarded as bonded. While if a pair of Fe and C atoms
; has distance short than 2.1 Angstrom, they will be regarded as bonded.
;
;Fe Cl 2.0 2.4
;Fe C  0.0 2.1
```

### CORR_NAME_TYPE.DAT

```text
C.3 C 	4
C.2 C 	3
C.1 C 	2
C.ar C 	3
C.cat C	3
N.3 N	3	
N.2 N	2
N.1 N	1
N.ar N	2
N.pl3 N	3
N.4 N	4
O.3 O	2	
O.2 O	1
O.co2 O	1
O.spc O	2
O.t3p O	2
S.3 S	2
S.2 S	1
S.O S	3
S.O2 S	4
P.3 P	-1 (2,3,4,5)
H H	1
H.spc H	1
H.t3p H	1
F F	1
Cl Cl	1
Br Br	1
I I	1
Si Si	4
LP LP	0
du du	-1	
Du Du	-1	
DU DU	-1	
Na Na	0
K K	0
Ca Ca	0
Li Li	0
Al Al	0
Any Any	-1
Hal Hal	1
Het Het	-1
Hev Hev -1
hc H	1
ha H	1
hn H	1
ho H	1
hp H	1
hs H	1
hw H	1
hx H	1
h1 H	1
h2 H	1
h3 H	1
h4 H	1
h5 H	1
f  F	1
cl Cl	1
br Br	1
i  I	1
c3 C	4
c2 C	3
c1 C	2
c  C	3
ca C	3
cc C	3
cd C	3
ce C	3
cf C	3
cg C	2
ch C	2
cp C	3
cq C	3
cu C	3
cv C	3
cx C	4
cy C	4
cz C	3
ns N	3
nt N	3
n  N	3
n1 N	-1 (1 or 2)	
n2 N	2
n7 N	3
n8 N	3
n9 N	3
n3 N	3
nx N	4
ny N	4
nz N	4
n+ N	4
n4 N	4
na N	3
nb N	2
nc N	2
nd N	2
ne N	2
nf N	2
ni N    3
nj N    3
nk N    3
nl N    3
nm N    3
nn N    3
n5 N    3
n6 N    3
np N    3
nq N    3
nu N	3
nv N	3
nh N	3
no N	3
o  O	1
oh O	2
op O	2
oq O	2
os O	2
ow O	2
s  S	1
s2 S	2
s4 S	3
s6 S	4
sp S	2
sq S	2
ss S	2
sh S	2
sx S	3
sy S	4
p2 P	1
p3 P	3
p4 P	3
p5 P	4
pb P	2
pc P	2
pd P 	2
pe P	2
pf P	2
px P	3
py P	4
C  C	3
CA C	3
CB C	3
CC C	3
CD C 	3	
CK C 	3
CM C 	3
CN C 	3
CQ C 	3
CR C 	3
CT C 	4	
CV C 	3
CW C 	3
C* C 	3
CY C 	2
CZ C 	2
C1 C 	2
H  H	1 
HO H	1 
HS H	1 
HP H	1 
HA H	1
HC H	1
H1 H	1
H2 H	1
H3 H	1
H4 H	1
H5 H	1
N  N	3
NA N	3	
NB N	2
NC N	2
N1 N	1
N2 N	3
N3 N	4
NT N	3
N* N	3
NY N	1
O  O	1
O2 O	1
OW O	2
OH O	2
OS O	2
P  P	-1
S  S	2
SH S	2
SO S	4
```

### LJ_param.dat

```text
;This file contains LJ parameters that can be assigned by Sobtop
;The lines beginning with semicolon are comment lines
;Meaning of each column:
;Column 1: Atom type. Should be no more than 10 characters, no - symbol
;Column 2: vdW nonbond radius (half of r0) in Angstrom
;Column 3: Well depth (epsilon) in kcal/mol
;The content after semicolon is description of atom type

;Your own atom type may be added here
Ctest    1.9255      0.105   ;My carbon
Si_bulk  2.329       0.093   ;Si in bulk SiO2
O_bulk   1.947       0.054   ;O in bulk SiO2

;The following ones are UFF atom types
UF_H      1.4430      0.044   ;UFF atom type of H 
UF_He     1.1810      0.056   ;UFF atom type of He
UF_Li     1.2255      0.025   ;UFF atom type of Li
UF_Be     1.3725      0.085   ;UFF atom type of Be
UF_B      2.0415      0.180   ;UFF atom type of B 
UF_C      1.9255      0.105   ;UFF atom type of C 
UF_N      1.8300      0.069   ;UFF atom type of N 
UF_O      1.7500      0.060   ;UFF atom type of O 
UF_F      1.6820      0.050   ;UFF atom type of F 
UF_Ne     1.6215      0.042   ;UFF atom type of Ne
UF_Na     1.4915      0.030   ;UFF atom type of Na
UF_Mg     1.5105      0.111   ;UFF atom type of Mg
UF_Al     2.2495      0.505   ;UFF atom type of Al
UF_Si     2.1475      0.402   ;UFF atom type of Si
UF_P      2.0735      0.305   ;UFF atom type of P 
UF_S      2.0175      0.274   ;UFF atom type of S 
UF_Cl     1.9735      0.227   ;UFF atom type of Cl
UF_Ar     1.9340      0.185   ;UFF atom type of Ar
UF_K      1.9060      0.035   ;UFF atom type of K 
UF_Ca     1.6995      0.238   ;UFF atom type of Ca
UF_Sc     1.6475      0.019   ;UFF atom type of Sc
UF_Ti     1.5875      0.017   ;UFF atom type of Ti
UF_V      1.5720      0.016   ;UFF atom type of V 
UF_Cr     1.5115      0.015   ;UFF atom type of Cr
UF_Mn     1.4805      0.013   ;UFF atom type of Mn
UF_Fe     1.4560      0.013   ;UFF atom type of Fe
UF_Co     1.4360      0.014   ;UFF atom type of Co
UF_Ni     1.4170      0.015   ;UFF atom type of Ni
UF_Cu     1.7475      0.005   ;UFF atom type of Cu
UF_Zn     1.3815      0.124   ;UFF atom type of Zn
UF_Ga     2.1915      0.415   ;UFF atom type of Ga
UF_Ge     2.1400      0.379   ;UFF atom type of Ge
UF_As     2.1150      0.309   ;UFF atom type of As
UF_Se     2.1025      0.291   ;UFF atom type of Se
UF_Br     2.0945      0.251   ;UFF atom type of Br
UF_Kr     2.0705      0.220   ;UFF atom type of Kr
UF_Rb     2.0570      0.040   ;UFF atom type of Rb
UF_Sr     1.8205      0.235   ;UFF atom type of Sr
UF_Y      1.6725      0.072   ;UFF atom type of Y 
UF_Zr     1.5620      0.069   ;UFF atom type of Zr
UF_Nb     1.5825      0.059   ;UFF atom type of Nb
UF_Mo     1.5260      0.056   ;UFF atom type of Mo
UF_Tc     1.4990      0.048   ;UFF atom type of Tc
UF_Ru     1.4815      0.056   ;UFF atom type of Ru
UF_Rh     1.4645      0.053   ;UFF atom type of Rh
UF_Pd     1.4495      0.048   ;UFF atom type of Pd
UF_Ag     1.5740      0.036   ;UFF atom type of Ag
UF_Cd     1.4240      0.228   ;UFF atom type of Cd
UF_In     2.2315      0.599   ;UFF atom type of In
UF_Sn     2.1960      0.567   ;UFF atom type of Sn
UF_Sb     2.2100      0.449   ;UFF atom type of Sb
UF_Te     2.2350      0.398   ;UFF atom type of Te
UF_I      2.2500      0.339   ;UFF atom type of I 
UF_Xe     2.2020      0.332   ;UFF atom type of Xe
UF_Cs     2.2585      0.045   ;UFF atom type of Cs
UF_Ba     1.8515      0.364   ;UFF atom type of Ba
UF_La     1.7610      0.017   ;UFF atom type of La
UF_Ce     1.7780      0.013   ;UFF atom type of Ce
UF_Pr     1.8030      0.010   ;UFF atom type of Pr
UF_Nd     1.7875      0.010   ;UFF atom type of Nd
UF_Pm     1.7735      0.009   ;UFF atom type of Pm
UF_Sm     1.7600      0.008   ;UFF atom type of Sm
UF_Eu     1.7465      0.008   ;UFF atom type of Eu
UF_Gd     1.6840      0.009   ;UFF atom type of Gd
UF_Tb     1.7255      0.007   ;UFF atom type of Tb
UF_Dy     1.7140      0.007   ;UFF atom type of Dy
UF_Ho     1.7045      0.007   ;UFF atom type of Ho
UF_Er     1.6955      0.007   ;UFF atom type of Er
UF_Tm     1.6870      0.006   ;UFF atom type of Tm
UF_Yb     1.6775      0.228   ;UFF atom type of Yb
UF_Lu     1.8200      0.041   ;UFF atom type of Lu
UF_Hf     1.5705      0.072   ;UFF atom type of Hf
UF_Ta     1.5850      0.081   ;UFF atom type of Ta
UF_W      1.5345      0.067   ;UFF atom type of W 
UF_Re     1.4770      0.066   ;UFF atom type of Re
UF_Os     1.5600      0.037   ;UFF atom type of Os
UF_Ir     1.4200      0.073   ;UFF atom type of Ir
UF_Pt     1.3770      0.080   ;UFF atom type of Pt
UF_Au     1.6465      0.039   ;UFF atom type of Au
UF_Hg     1.3525      0.385   ;UFF atom type of Hg
UF_Tl     2.1735      0.680   ;UFF atom type of Tl
UF_Pb     2.1485      0.663   ;UFF atom type of Pb
UF_Bi     2.1850      0.518   ;UFF atom type of Bi
UF_Po     2.3545      0.325   ;UFF atom type of Po
UF_At     2.3750      0.284   ;UFF atom type of At
UF_Rn     2.3825      0.248   ;UFF atom type of Rn
UF_Fr     2.4500      0.050   ;U
... [truncated in knowledge source; see Sobtop package for full file]
```

### bonded_param.dat

```text
;This file contains bonded parameters that can be assigned by Sobtop
;There are following fields in sequence: $BOND, $ANGLE, $DIHEDRAL, $HARM_DIH, $IMPROPER
;The lines beginning with semicolon are comment lines
;Between atom types there must be a - symbol
;GAFF parameters come from gaff.dat (Version 1.81, May 2017) in AmberTools 21
;AMBER parameters come from parm19.dat in AmberTools 21, corresponding to AMBER19SB with parmbsc0 and OL3


;Content between $BOND ... $end are parameters of bond terms
;Parameters should be given in AMBER/GAFF form: E_bond = k*(r-r0)^2
;Column 1: Two atom types
;Column 2: Force constant (k) in kcal/mol/A^2
;Column 3: Equilibrium bond distance (r0) in Angstrom
;Note that in GROMACS the potential is (1/2)*k*(r-r0)^2, so the k given below is half of that used in GROMACS
;To convert to k in GROMACS convention, the k in this section should be multiplied by 4.184*100*2
$BOND
Ctest-Ctest   300.9    1.5375
Si_bulk-O_bulk  285  1.65
ow-hw  553.0    0.9572
hw-hw  553.0    1.5136
br-br  123.2    2.5420
br-c1  352.7    1.7870
br-c2  272.3    1.8928
br-c   240.3    1.9460
br-c3  223.4    1.9779
br-ca  262.7    1.9079
br-cc  277.4    1.8850
br-cx  245.4    1.9370
br-i     0.0    2.6710
br-n1  330.4    1.8600
br-n2  219.0    2.0380
br-n   320.2    1.8730
br-n3  265.9    1.9520
br-n4  282.4    1.9260
br-na  237.3    2.0020
br-nh  270.9    1.9440
br-no  191.0    2.1010
br-o   278.9    1.8000
br-oh  237.2    1.8660
br-os  225.6    1.8870
br-p2  174.3    2.2100
br-p3  167.0    2.2310
br-p4  188.8    2.1710
br-p5  179.3    2.1960
br-s   170.6    2.2200
br-s4  134.3    2.3410
br-s6  172.7    2.2140
br-sh  174.4    2.2090
br-ss  176.6    2.2030
c1-c1  923.7    1.1983
c1-c2  625.0    1.3070
c1-c3  371.6    1.4671
c1-ca  404.1    1.4400
c1-ce  607.4    1.3153
c1-cg  865.1    1.2159
c1-ch  854.0    1.2194
c1-cl  419.7    1.6310
c1-cx  398.0    1.4450
c1-f   469.4    1.2700
c1-ha  374.7    1.0668
c1-hc  385.6    1.0600
c1-i   318.8    1.9890
c1-n1  954.6    1.1535
c1-n2  807.8    1.1971
c1-n3  474.3    1.3475
c1-n4  378.2    1.4170
c1-n   503.0    1.3300
c1-na  452.0    1.3620
c1-ne  792.2    1.2023
c1-nf  792.2    1.2023
c1-nh  482.6    1.3423
c1-no  393.0    1.4050
c1-o   758.1    1.1724
c1-oh  435.6    1.3260
c1-os  447.5    1.3181
c1-p2  289.3    1.7700
c1-p3  275.1    1.7900
c1-p4  275.1    1.7900
c1-p5  302.2    1.7530
c1-s2  410.0    1.5950
c1-s   400.6    1.6032
c1-s4  272.9    1.7460
c1-s6  290.4    1.7220
c1-sh  324.5    1.6800
c1-ss  316.2    1.6898
c2-c2  569.4    1.3343
c2-c3  326.8    1.5095
c2-ca  482.1    1.3846
c2-cc  523.8    1.3593
c2-cd  523.8    1.3593
c2-ce  547.3    1.3461
c2-cf  547.3    1.3461
c2-cl  321.3    1.7308
c2-cu  590.0    1.3240
c2-cx  352.0    1.4850
c2-cy  325.6    1.5110
c2-f   370.6    1.3385
c2-h4  344.6    1.0868
c2-h5  338.4    1.0912
c2-ha  343.1    1.0879
c2-hc  344.3    1.0870
c2-hx  350.1    1.0830
c2-i   215.4    2.1701
c2-n1  546.0    1.3060
c2-n2  594.1    1.2817
c2-n3  486.3    1.3400
c2-n   400.1    1.3994
c2-n4  282.0    1.5125
c2-na  397.4    1.4015
c2-nc  533.0    1.3130
c2-nd  533.0    1.3130
c2-ne  574.1    1.2915
c2-nf  574.1    1.2915
c2-nh  416.2    1.3872
c2-no  343.0    1.4481
c2-o   622.9    1.2247
c2-oh  417.6    1.3385
c2-os  389.2    1.3596
c2-p2  377.3    1.6686
c2-p3  246.6    1.8340
c2-p4  254.0    1.8220
c2-p5  230.0    1.8626
c2-pe  357.6    1.6886
c2-pf  357.6    1.6886
c2-s2  393.1    1.6100
c2-s   281.5    1.7340
c2-s4  263.2    1.7600
c2-s6  263.2    1.7600
c2-sh  248.9    1.7820
c2-ss  280.0    1.7360
c3-c3  300.9    1.5375
c3-ca  321.0    1.5156
c3-cc  334.8    1.5015
c3-cd  334.8    1.5015
c3-ce  320.7    1.5159
c3-cf  320.9    1.5157
c3-cl  266.3    1.8045
c3-cu  353.1    1.4840
c3-cv  335.4    1.5010
c3-cx  315.1    1.5220
c3-cy  304.2    1.5340
c3-f   356.9    1.3497
c3-h1  330.6    1.0969
c3-h2  331.7    1.0961
c3-h3  333.3    1.0949
c3-hc  330.6    1.0969
c3-hx  338.7    1.0910
c3-i   197.8    2.2117
c3-n1  359.6    1.4330
c3-n2  324.5    1.4661
c3-n   328.7    1.4619
c3-n3  325.9    1.4647
c3-n4  283.3    1.5110
c3-na  327.7    1.4629
c3-nc  334.7    1.4560
c3-nd  334.7    1.4560
c3-nh  326.6    1.4640
c3-no  265.1    1.5334
c3-o   449.9    1.3165
c3-oh  316.7    1.4233
c3-os  308.6    1.4316
c3-p2  234.3    1.8550
c3-p3  232.5    1.8582
c3-p4  243.8    1.8387
c3-p5  243.3    1.8395
c3-px  249.9    1.8286
c3-py  243.2    1.8397
c3-s   212.9    1.8450
c3-s4  220.6    1.8305
c3-s6  233.5    1.8075
c3-sh  213.7    1.8435
c3-ss  215.9    1.8392
c3-sx  214.6    1.8418
c3-sy  232.8    1.8087
ca-ca  461.1    1.3984
ca-cc  385.1    1.4555
ca-cd  385.1    1.4555
ca-ce  361.3    1.4763
ca-cf  361.3    1.4763
ca-cg  413.3    1.4328
ca-ch  413.3    1.4328
ca-cl  305.6    1.7502
ca-cp  450.2    1.4058
ca-cq  450.2    1.4058
ca-cx  340.5    1.4960
ca-cy  320.8    1.5160
ca-f   357.8    1.3490
ca-h4  341.5    1.0890
ca-h5  343.2    1.0878
ca-ha  345.8    1.0860
ca-i   234.9    2.1288
ca-n1  494.6    1.3350
ca-n2  551.6    1.3030
ca-n   384.2    1.4121
ca-n4  307.0    1.4842
ca-na  420.5    1.3840
ca-nb  488.0    1.3390
ca-nc  467.7    1.3517
ca-nd  467.7    1.3517
ca-ne  389.3    1.4079
ca-nf  389.3    1.4079
ca-nh  417.9    1.3859
ca-no  321.7    1.4689
ca-o   598.1    1.2358
ca-oh  384.0    1.3637
ca-os  376.6    1.3696
ca-p2  243.0    1.8400
ca-p3  251.7    1.8257
ca-p4  264.3    1.8060
ca-p5  271.5    1.7952
ca-pe  249.6    1.8290
ca-pf  249.6    1.8290
ca-px  252.1    1.8250
ca-py  257.7    1.8162
ca-s   277.9    1.7390
ca-s4  245.2    1.7880
ca-s6  258.7    1.7669
ca-sh  249.6    1.7809
ca-ss  249.8    1.7806
ca-sx  223.6    1.8251
ca-sy  243.4    1.7909
c -c1  379.8    1.4600
c -c2  449.9    1.4060
c -c   291.7    1.5482
c -c3  313.0    1.5241
c -ca  345.9    1.4906
c -cc  371.0    1.4676
cc-cc  419.8    1.4278
cc-cd  500.9    1.3729
cc-ce  386.9    1.4540
cc-cf  513.0    1.3656
cc-cg  422.6    1.4257
cc-ch  420.9    1.4270
cc-cl  317.5    1.7354
cc-cx  369.6    1.4690
c -cd  371.0    1.4676
c -ce  354.5    1.4825
c -cf  354.5    1.4825
cc-f   367.8    1.3407
c -cg  390.2    1.4512
c -ch  390.2    1.4512
cc-h4  352.0    1.0817
cc-h5  351.7    1.0819
cc-ha  349.1    1.0837
c -cl  267.4    1.8029
cc-n2  576.1    1.2905
cc-n   425.1    1.3807
cc-n4  299.0    1.4930
cc-na  425.8    1.3802
cc-nc  441.1    1.3694
cc-nd  525.4    1.3172
cc-ne  428.0    1.3786
cc-nf  560.3    1.2985
cc-nh  435.2    1.3735
cc-no  364.2    1.4289
cc-oh  405.9    1.3470
cc-os  386.1    1.3620
cc-pd  318.2    1.7330
cc-sh  257.1    1.7693
cc-ss  265.8    1.7562
cc-sx  231.7    1.8107
cc-sy  247.7    1.7839
c -cu  441.4    1.4120
c -cx  333.4    1.5030
c -cy  288.6    1.5520
cd-cd  419.8    1.4278
cd-ce  513.0    1.3656
cd-cf  386.9    1.4540
cd-cg  420.9    1.4270
cd-ch  422.6    1.4257
cd-cl  317.5    1.7354
cd-cx  357.4    1.4800
cd-cy  331.4    1.5050
cd-h4  352.0    1.0817
cd-h5  351.8    1.0818
cd-ha  349.1    1.0837
cd-n2  576.1    1.2905
cd-n   425.1    1.3807
cd-na  425.8    1.3802
cd-nc  525.4    1.3172
cd-nd  441.1    1.3694
cd-ne  560.3    1.2985
cd-nh  435.2    1.3735
cd-oh  405.9    1.3470
cd-os  386.1    1.3620
cd-pc  318.2    1.7330
cd-ss  265.8    1.7562
cd-sy  247.7    1.7839
ce-ce  382.8    1.4574
ce-cf  538.6    1.3509
ce-cg  420.9    1.4270
ce-ch  415.6    1.4310
ce-cl  294.9    1.7641
ce-cx  333.4    1.5030
ce-cy  319.8    1.5170
ce-h4  337.8    1.0916
ce-ha  342.5    1.0883
ce-n1  536.5    1.3111
ce-n2  582.4    1.2874
ce-n   369.7    1.4242
ce-na  373.6    1.4209
ce-ne  406.9    1.3942
ce-nf  564.4    1.2964
ce-nh  412.3    1.3901
ce-oh  401.6    1.3502
ce-os  374.9    1.3710
ce-p2  259.1    1.8140
ce-pe  256.5    1.8180
ce-px  254.6    1.8210
ce-py  264.5    1.8056
ce-s   324.5    1.6800
ce-ss  249.3    1.7814
ce-sx  227.2    1.8185
ce-sy  245.1    1.7881
c -f   387.9    1.3250
cf-cf  382.8    1.4574
cf-cg  415.6    1.4310
cf-ch  420.9    1.4270
cf-h4  337.8    1.0916
cf-ha  342.5    1.0883
cf-n1  536.5    1.3111
cf-n2  582.4    1.2874
cf-n   369.7    1.4242
cf-ne  564.4    1.
... [truncated in knowledge source; see Sobtop package for full file]
```

### ATOMTYPE_GFF.DEF

```text
# Please go to the end to see rules of defining an atom  

============================================================================================
                        Defination begin
============================================================================================
--------------------------------------------------------------------------------------------
WILDATOM XX C N O S P
WILDATOM XA O S
WILDATOM XB N P
WILDATOM XC F Cl Br I
WILDATOM XD S P
-------------------------------------------------------------------------------------------- 
 f1  f2    f3  f4  f5  f6  f7  f8      		f9          
-------------------------------------------------------------------------------------------- 
//3-membered ring atom
ATD  cx    *   6   4   *   *   [RG3]            &
//4-membered ring atom
ATD  cy    *   6   4   *   *   [RG4]            &
//other sp3 C
ATD  c3    *   6   4   &
//C=O or C=S
ATD  c     *   6   3   *   *   [2DL]   		(XA1) 	&
ATD  c     *   6   3   *   *   [1DB,0DL]  	(XA1)	&
ATD  c     *   6   3   *   *   [3sb]   		(XA1)	&
ATD  cz    *   6   3   *   *   *                (N3,N3,N3)  &
//pure aromatic atom that can form an aromatic single bond 
ATD  cp    *   6   3   *   *   [AR1,1RG6]       (XX[AR1],XX[AR1],XX[AR1]) &
//pure aromatic atom 
ATD  ca    *   6   3   *   *   [AR1]    &
// sp2 C of conjugated ring systems
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (C3(C3))	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (C3(C2))	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (C3(XB2))	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (XB2(XB2))	& 
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (XB2(C2))	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (XB2(C3))	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (C3[sb'])	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (XB2[sb'])	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (XD3[sb',db])	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       (XD4[sb',db])	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (C3(C3))	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (C3(C2))	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (C3(XB2))	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (XB2(XB2)) 	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (XB2(C2))	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (XB2(C3))	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (C3[sb'])	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (XB2[sb'])	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (XD3[sb',db])	&
ATD  cc    *   6   3   *   *   [sb,db,AR3]       (XD4[sb',db])	&
ATD  cc    *   6   3   *   *   [sb,db,AR2]       &
ATD  cc    *   6   3   *   *   [sb,db,AR3]       &
// sp2 C of conjugated chain systems
ATD  ce    *   6   3   *   *   [sb,db]          (C3[SB'])	&
ATD  ce    *   6   3   *   *   [sb,db]          (C2[SB'])	&
ATD  ce    *   6   3   *   *   [sb,db]          (XB2[SB'])	&
ATD  ce    *   6   3   *   *   [sb,db]          (XD3[SB',db])	&
ATD  ce    *   6   3   *   *   [sb,db]          (XD4[SB',db])	&
//sp2 carbon in a 3-membered ring
ATD  cu    *   6   3   *   *   [RG3]            &
//sp2 carbon in a 4-membered ring
ATD  cv    *   6   3   *   *   [RG4]            &
//other sp2 C
ATD  c2    *   6   3   &
// sp C of conjugated systems
ATD  cg    *   6   2   *   *   [sb,tb]          (C2[SB'])	&
ATD  cg    *   6   2   *   *   [sb,tb]          (C3[SB'])	&
ATD  cg    *   6   2   *   *   [sb,tb]          (N1[SB'])	&
ATD  cg    *   6   2   *   *   [sb,tb]          (XB2[SB'])	&
// other sp C 
ATD  c1    *   6   2   &
ATD  c1    *   6   1   &
ATD  hn    *   1   1   *   *   *       		(N)         	& 
ATD  ho    *   1   1   *   *   *       		(O)         	&
ATD  hs    *   1   1   *   *   *       		(S)     	& 
ATD  hp    *   1   1   *   *   *       		(P)     	& 
ATD  hx    *   1   1   *   *   *       		(C(N4)) 	& 
ATD  hw    *   1   1   *   *   *       		(O(H1))  	&
ATD  h3    *   1   1   *   3   *       		(C4)     	&
ATD  h2    *   1   1   *   2   *       		(C4)     	&
ATD  h1    *   1   1   *   1   *       		(C4)     	& 
ATD  hc    *   1   1   *   *   *       		(C4)    	& 
ATD  h5    *   1   1   *   2   *       		(C3)	&     
ATD  h4    *   1   1   *   1   *       		(C3)   	& 
ATD  ha    *   1   1   &
ATD  f     *   9   &
ATD  cl    *   17  &
ATD  br    *   35  &      
ATD  i     *   53  & 
// sp2 P of conjugated ring systems
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (C3(C3))	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (C3(C2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (C3(XB2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (XB2(C3))	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (XB2(C2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (XB2(XB2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (C3[sb'])	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (C2[sb'])	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (XB2[sb'])	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (XD3[sb',db])	&
ATD  pc    *   15  2   *   *   [sb,db,AR2]       (XD4[sb',db])	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (C3(C3))	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (C3(C2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (C3(XB2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (XB2(C3))	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (XB2(C2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (XB2(XB2))	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (C3[sb'])	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (C2[sb'])	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (XB2[sb'])	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (XD3[sb',db])	&
ATD  pc    *   15  2   *   *   [sb,db,AR3]       (XD4[sb',db])	&
// sp2 P of conjugated chain systems
ATD  pb    *   15  2   *   *   [AR1]            &
ATD  pe    *   15  2   *   *   [sb,db]          (C3[sb'])	&
ATD  pe    *   15  2   *   *   [sb,db]          (C2[SB'])	&
ATD  pe    *   15  2   *   *   [sb,db]          (XA1[SB'])	&
ATD  pe    *   15  2   *   *   [sb,db]          (XB2[SB'])	&
ATD  pe    *   15  2   *   *   [sb,db]          (XD3[SB',DB])	&
ATD  pe    *   15  2   *   *   [sb,db]          (XD4[SB',DB])	&
ATD  p2    *   15  2   &  
ATD  p2    *   15  1   &  
ATD  px    *   15  3   *   *   [db]    		(XB2[sb'])      & 
ATD  px    *   15  3   *   *   [db]    		(C3[sb'])       &
ATD  px    *   15  3   *   *   [db]    		(XD3[sb',db])   &    
ATD  px    *   15  3   *   *   [db]    		(XD4[sb',db])   &    
ATD  p4    *   15  3   *   *   [db]    		(XA1)      	& 
ATD  p3    *   15  3   &  
ATD  py    *   15  4   *   *   [db]    		(XB2[sb'])      &
ATD  py    *   15  4   *   *   [db]    		(C3[sb'])      	&
ATD  py    *   15  4   *   *   [db]    		(XD3[sb',db])  	&    
ATD  py    *   15  4   *   *   [db]    		(XD4[sb',db])  	&    
ATD  p5    *   15  4   &  
ATD  p5    *   15  5   &  
ATD  p5    *   15  6   &  
ATD  ni    *   7   3   *   *   [RG3]       	(C3(XA1))  	& 
ATD  nj    *   7   3   *   *   [RG4]       	(C3(XA1))  	& 
ATD  n     *   7   3   *   *   *       		(C3(XA1))  	& 
ATD  nk    *   7   4   *   *   [RG3]       	& 
ATD  nl    *   7   4   *   *   [RG4]       	& 
ATD  n4    *   7   4   &
ATD  no    *   7   3   *   *   *       		(O1,O1)		& 
ATD  na    *   7   3   *   *   [AR1.AR2.AR3]    &
ATD  nm    *   7   3   *   *   [RG3]    	(XX[AR1.AR2.AR3]) & 
ATD  nm    *   7   3   *   *   [RG3]    	(C3[DB]) 	& 
ATD  nm    *   7   3   *   *   [RG3]    	(N2[DB])	& 
ATD  nm    *   7   3   *   *   [RG3]    	(P2[DB])	& 
ATD  nn    *   7   3   *   *   [RG4]    	(XX[AR1.AR2.AR3]) & 
ATD  nn    *   7   3   *   *   [RG4]    	(C3[DB]) 	& 
ATD  nn    *   7   3   *   *   [RG4]    	(N2[DB])	& 
ATD  nn    *   7   3   *   *   [RG4]    	(P2[DB])	& 
ATD  nh    *   7   3   *   *   *       		(XX[AR1.AR2.AR3]) & 
ATD  nh    *   7   3   *   *   *       		(C3[DB]) 	& 
ATD  nh    *   7   3   *   *   *       		(N2[DB])	& 
ATD  nh    *   7   3   *   *   *       		(P2[DB])	& 
ATD  np    *   7   3   *   *   [R
... [truncated in knowledge source; see Sobtop package for full file]
```

### ATOMTYPE_AMBER.DEF

```text
# Please go to the end to see rules of defining an atom  

============================================================================================
                        Definition begin
============================================================================================
--------------------------------------------------------------------------------------------
WILDATOM XX C N O S P
WILDATOM XA O S
WILDATOM XB N P
WILDATOM XC F Cl Br I
-------------------------------------------------------------------------------------------- 
 f1  f2    f3  f4  f5  f6  f7  f8      			f9         	f10 
-------------------------------------------------------------------------------------------- 
ATD  CT    *   6   4   &                                    
ATD  C     *   6   3   *   *   *       	      	 	(XA1)			&
ATD  CN    *   6   3   *   *   [RG5,RG6,AR1.AR2.AR3]   	(C3,C3,N3(H))		&
ATD  CB    *   6   3   *   *   [RG5,RG6,AR1.AR2.AR3]    &
ATD  CR    *   6   3   *   *   [RG5,AR1.AR2.AR3]        (N3,N3)			&
ATD  CR    *   6   3   *   *   [RG5,AR1.AR2.AR3]        (N2,N3(H))		&
ATD  CK    *   6   3   *   *   [RG5,AR1.AR2.AR3]        (N2,N3) 		&	 
ATD  CC    *   6   3   0   *   [RG5,AR1.AR2.AR3]        (C3,N3(C3,H))		&
ATD  CC    *   6   3   0   *   [RG5,AR1.AR2.AR3]        (C3,N2(C3))		&
ATD  CW    *   6   3   *   *   [RG5,AR1.AR2.AR3]        (C3,N3(H))		&
ATD  CV    *   6   3   *   *   [RG5,AR1.AR2.AR3]        (C3,N2)			&
ATD  C*    *   6   3   *   *   [RG5,AR1.AR2.AR3]        (C3,C3)			&
ATD  CQ    *   6   3   *   *   [RG6,AR1.AR2.AR3]        (N2,N2)			&
ATD  CM    *   6   3   *   *   [RG6,AR1.AR2.AR3]        (C3,C3(N2(C3(N3(C3))))) &
ATD  CM    *   6   3   *   *   [RG6,AR1.AR2.AR3]        (C3,C3(N3(C3(N3(C3))))) &
ATD  CM    *   6   3   *   *   [RG6,AR1.AR2.AR3]        (C3,N3(C3(N2(C3(C3))))) &
ATD  CM    *   6   3   *   *   [RG6,AR1.AR2.AR3]        (N3,C3(C3(N3(C3(N3))))) &
ATD  CA    *   6   3   *   *   [AR1.AR2.AR3]             &	
ATD  CA    *   6   3   *   *   *                	(N3,N3,N3)  		&
ATD  CD    *   6   3   *   *   *                        (C3,C3)			& 
ATD  CM    *   6   3   &
ATD  CZ    *   6   2   &
ATD  H     *   1   1   *   *   *                        (N)			&
ATD  HO    *   1   1   *   *   *                        (O)			&
ATD  HS    *   1   1   *   *   *                        (S)			&
ATD  HP    *   1   1   *   *   *                        (C(N4))			&
ATD  HW    *   1   1   *   *   *                        (O(H1))			&
ATD  H3    *   1   1   *   3   *                        (C4)			&
ATD  H2    *   1   1   *   2   *                        (C4)			&
ATD  H1    *   1   1   *   1   *                        (C4)			&
ATD  HC    *   1   1   *   *   *                        (C4)			&
ATD  H5    *   1   1   *   2   *                        (XX[AR1.AR2.AR3])	&
ATD  H4    *   1   1   *   1   *                        (XX[AR1.AR2.AR3])	&
ATD  HA    *   1   1   *   *   *                        (XX[AR1.AR2.AR3])	&
ATD  HA    *   1   1   &
ATD  F     *   9   1   &
ATD  Cl    *   17  1   &
ATD  Br    *   35  1   &
ATD  I     *   53  1   &
ATD  P     *   15  &
ATD  N1    *   7   1   &   
ATD  NB    *   7   2   *   *   [RG5,AR1.AR2.AR3]         & 
ATD  NC    *   7   2   *   *   [RG6,AR1.AR2.AR3]         & 
ATD  N2    *   7   *   *   *   *                         (C3(N3,N3))		&
ATD  N2    *   7   *   *   *   *                         (C3(N3,N3))		&
ATD  NO    *   7   3   *   *   *                         (O1,O1)		&
ATD  NA    *   7   3   1   *   [RG5.RG6,AR1.AR2.AR3]     & 
ATD  N2    *   7   3   *   *   [NR]                      (XX[AR1.AR2.AR3]) 	&
ATD  N*    *   7   3   *   *   [AR1.AR2.AR3]             &
ATD  N     *   7   3   *   *   *                         (C3(XA1))		&
ATD  NT    *   7   3   &   
ATD  N3    *   7   4   &   
ATD  O2    *   8   1   *   *   *                         (C(O1))		&
ATD  O2    *   8   1   *   *   *                         (P)			&
ATD  O     *   8   1   *   *   *                         (C)			&
ATD  O     *   8   1   *   *   *                         (S)			&
ATD  OH    *   8   2   1   & 
ATD  OW    *   8   2   2   & 
ATD  OS    *   8   2   & 
ATD  SH    *   16  2   1   &
ATD  SH    *   16  2   2   &
ATD  S     *   16  2   & 
ATD  SO    *   16  4   & 
ATD  LP   *    0   &
ATD  DU  &
--------------------------------------------------------------------------------------------
============================================================================================




============================================================================================
			Field descriptions
============================================================================================
(1)  ATD, which stands for atom type definition, ATD should always in the first three columns 
(2)  Atom type name, can be letters or numbers   
(3)  Residue names, which means this description is only applied to atoms in special residues
(4)  Atomic number 
(5)  Number of attached atoms 
(6)  Number of attached hydrogen atoms
(7)  For hydrogen, number of the electron-withdrawal atoms connected to the atom that the 
     hydrogen attached
(8)  atomic property
(9)  Chemical environment definitions


============================================================================================
			Specific symbols
============================================================================================
*  Ignore this field
&  End of definition 
.  "or" operation in the ring and aromatity descriptions 


============================================================================================
			Predefined words
============================================================================================
EW   Electron-withdraw atom
AA   Amino acid residue
NA   Nucleic acid
BIO  AA + NA

AR1  Pure aromatic atom (benzene and pyridine)
AR2  Atom in a planar ring, usually the ring has two continuous single bonds
AR3  Atom in a planar ring, which has one or several double bonds formed between outside atoms
     and ring atoms
AR4  Atom other than AR1, AR2, AR3 and AR5. 
AR5  Pure aliphatic atom in a ring, which is made of sp3 carbon

RG   Ring (from 3-membered to nine-membered)
RG3  3-membered ring 
RG4  4-membered ring 
RG5  5-membered ring 
RG6  6-membered ring 
RG7  7-membered ring 
RG8  8-membered ring 
RG9  9-membered ring 
NR   non-ring atom 

SB   Single bond
DB   Double bond
TB   Triple bond
AB   Aromatic bond
sb   Single bond, including aromatic single
db   Double bond, including aromatic double
tb   Triple bond
 
============================================================================================
			Miscellaneous
============================================================================================
1. maximum line length is 500 characters
2. no space in the atomic property string
3. no space in the chemical environment string 
4. no filed missing before &
5. the definition order is crucial, special atom types should defined before the more general 
   ones
6. Bonds in COO- and -NO2 are considered as double bonds
```

### examples/md_vac.mdp

```text
define =
integrator = md
dt         = 0.001   ; ps
nsteps     = 100000
comm-grps  = system
comm-mode  = Angular
;
nstxout = 0
nstvout = 0
nstfout = 0
nstlog  = 500
nstenergy = 500
nstxout-compressed = 100
compressed-x-grps  = system
;
pbc = no
nstlist = 0
rlist = 0
cutoff-scheme = group
coulombtype   = cut-off
rcoulomb      = 0
vdwtype       = cut-off
rvdw          = 0
;
Tcoupl  = V-rescale
tau_t   = 0.2
tc_grps = system
ref_t   = 300
;
gen_vel  = no
gen_temp = 20
gen_seed = -1
;
freezegrps  = 
freezedim   = 
constraints = none
```

### examples/md_PBC.mdp

```text
define =
integrator = md
dt         = 0.001   ; ps
nsteps     = 100000
comm-grps  = system
;
nstxout = 0
nstvout = 0
nstfout = 0
nstlog  = 100
nstenergy = 100
nstxout-compressed = 100
compressed-x-grps  = system
periodic-molecules = yes
;
pbc = xyz
cutoff-scheme = verlet
rlist = 0.5
coulombtype   = PME
rcoulomb      = 0.5
vdwtype       = cut-off
rvdw          = 0.5
DispCorr      = no
;
Tcoupl  = V-rescale
tau_t   = 0.2
tc_grps = system
ref_t   = 300
;
Pcoupl     = berendsen
pcoupltype = isotropic
tau_p = 1.5
ref_p = 1.0
compressibility = 4.5e-5
;
gen_vel  = yes
gen_temp = 100
gen_seed = -1
;
freezegrps  = 
freezedim   = 
constraints = hbonds
```
