---
thread_id: 428
source_id: forum_thread:428
title: "几种生成有机分子GROMACS拓扑文件的工具"
url: http://bbs.keinsci.com/thread-428-1-1.html
date: "2014-10-01T00:00:00+08:00"
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: wsl2_chrome_cdp_verified_session
source_crawled_at: "2026-06-05T10:05:00.952Z"
original_reply_count: 163
page_count: 11
views: 226287
software_tags:
- GROMACS
- AMBER
- Sobtop
topic_tags:
- 分子动力学
- 结构与文件格式
- 综述/教程/投稿经验
authority_level: A
confidence: 0.97
classification_reason: sobereva原创教程，22万浏览，介绍生成有机分子GROMACS拓扑文件的各类工具。
---

# 几种生成有机分子GROMACS拓扑文件的工具

- 原帖 URL：<http://bbs.keinsci.com/thread-428-1-1.html>
- 论坛板块：分子模拟
- 作者：**sobereva**
- 浏览量：226287 | 回复数：163 | 共11页
- 完整性：**全部内容已完整抓取**。

## 楼层正文

### 1 楼（楼主）｜sobereva

几种生成有机分子GROMACS拓扑文件的工具

Several tools for generating GROMACS topology files of organic molecules

文/Sobereva@北京科音First release：2014-Dec-9  Last update: 2024-Nov-5



本文把各种可以产生GROMACS拓扑文件的工具进行汇总。具体细节和实际使用例子笔者在相关分子动力学与 GROMACS 教程里会详细讲（[已省略培训课程链接]）。



值得一提的是，这些程序有很多不能产生原子电荷，或者产生的原子电荷质量较差。RESP电荷是最适合分子动力学模拟使用的电荷之一，AMBER、GAFF、GLYCAM等力场将之作为御用的原子电荷，将RESP电荷与UFF力场结合使用也是得当的。Multiwfn是计算RESP电荷最简单、最好、最灵活而且完全免费的工具，原理、用法和实例见《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（http://sobereva.com/441）、《计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）》（http://sobereva.com/476）、《RESP2原子电荷的思想以及在Multiwfn中的计算》（http://sobereva.com/531）。另外，OPLS-AA力场很适合结合1.2*CM5电荷使用，用Multiwfn的主功能7的子功能16直接就能计算出CM5电荷，将之手动乘以1.2即是1.2*CM5电荷，可以用Gaussian、ORCA等程序产生的fch/wfn/wfx/molden等格式作为Multiwfn的输入文件，详见《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（http://sobereva.com/379）。如果你完全不会用Gaussian的话，可以直接用这个傻瓜式脚本，一行命令就能算出来：《计算适用于OPLS-AA力场做模拟的1.2*CM5原子电荷的懒人脚本》（http://sobereva.com/585）。另有专门结合ORCA用的傻瓜式脚本，见《ORCA结合Multiwfn计算RESP、RESP2和1.2*CM5原子电荷的懒人脚本》（http://sobereva.com/637）。





• Sobtop（http://sobereva.com/soft/Sobtop）

这是我开发的GROMACS拓扑文件产生工具，主要产生GAFF/GAFF2、AMBER力场的拓扑文件，但由于其力场库可以自行非常方便地修改和扩充，因此Sobtop本质上是完全普适、通用的。Sobtop可谓是最理想、最灵活、最易用的产生GROMACS拓扑文件的工具。此程序用起来超级简单，什么额外的程序以及特殊的运行环境都不需要装，解压即用。Sobtop使用极其方便，照着屏幕上的提示敲几下键盘，itp、top和gro文件就产生了，另外也可以要求产生rtp文件。Sobtop的主页有非常详细的产生各类体系拓扑文件的例子，并给出了详细的相关要点的说明。从例子中你会体会到Sobtop的设计特别注重兼顾便利和灵活，初级用户会体会到它极其便利，而高级用户则会体会到通过Sobtop构建复杂体系拓扑文件特别灵活好用。



Sobtop可以产生任意体系的拓扑文件，有机和无机小分子、过渡金属配合物、聚合物、共价团簇、晶体、二维材料等等全都可以产生，孤立体系和周期性体系都支持。Sobtop可以用于包含任意元素的体系，那些GAFF/GAFF2/AMBER不支持的元素可以自动让Sobtop用UFF的，或者自己定义额外原子类型。对于GAFF/GAFF2/AMBER力场里缺失的成键相关参数，可以直接让Sobtop基于量子化学程序产生的Hessian矩阵通过不同方法自动算出来，也可以自己把其它方式得到的（如自己单独拟合、文献中找的）添到力场库文件里让Sobtop直接用。Sobtop运行效率特别高，甚至对于几千原子体系的拓扑文件都可以搞。



Sobtop极度灵活，提供许多不同的指认原子类型的方式，可以自动指认GAFF/GAFF2/AMBER原子类型，也可以手动指认，也可以自定义判断规则让Sobtop结合实际化学环境和成键关系判断，等等。Sobtop还提供了丰富的指认力场成键相关参数的方式，比如可以都用力场库文件里的，都用直接基于Hessian算出来的参数，或者一部分作为刚性（里面的参数都基于Hessian算出来的）而其余部分作为柔性（参数用力场库里的，可以考虑二面角的可旋转性），等等。Sobtop还可以调用Multiwfn或OpenBabel自动指认EEM、Gasteiger、MMFF94原子电荷，还可以载入Multiwfn计算RESP/RESP2等电荷产生的chg文件来获得原子电荷。Sobtop的设计在各方面都特别贴心，比如在产生的拓扑文件里非常详细地注释各个力场项的参数来源、是否是缺失的，在自己手动改和补参数时很方便。



有了Sobtop，下面介绍的acpype就没有任何使用价值了。acpype只适合产生GAFF能描述的那些有机和极少数无机体系，有特殊成键方式、有GAFF不支持的元素、周期性体系都没法搞；对很大体系耗时非常高；容易出现莫名其妙又不好解决的报错；还得有Python运行环境、安装臃肿的AmberTools...



• acpype

这是一个Python脚本，可以在https://github.com/alanwilter/acpype下载。使用前必须在机子里安装AmberTools（免费），acpype会调用其中的Antechamber先产生Amber格式的拓扑文件然后再转成GROMACS的。acpype用法很简单，要处理xxx.mol2就执行./acpype.py -i xxx.mol2，算完后会新产生一个xxx目录，里头有_GMX后缀的.gro、.itp、.top，直接在GROMACS里用即可。默认情况下，产生的拓扑文件是基于GAFF力场的，另外也会输出_OPLS后缀的基于OPLS力场的文件，但属于实验性质不建议用。.mol2文件用常用的GaussView就可以产生（但必须确保在gview里看到的分子结构中没有诡异的成键方式），也可以通过OpenBabel或Antechamber将其它格式转成.mol2。默认情况下acpype分配的原子电荷是Antechamber产生的AM1-BCC，虽然能用，但明显不如RESP/RESP2电荷理想。建议大家按前述做法用Multiwfn计算出RESP或RESP2电荷，自行写入分子拓扑信息的[atoms]的原子电荷那一列。



如果你懒得为了用acpype而装臃肿庞大的AmberTools，可以用在线版http://bio2byte.be/acpype/，不过可能排队要排很久。所以如果你要快速处理较多小分子，还是建议用离线版acpype。



对于稍大的体系，用独立的acpype时强烈建议加上-c user选项以避免acpype自动算AM1-BCC原子电荷，否则在处理期间acpype所调用的Antechamber会先调用SQM程序用半经验方法进行优化然后再算这个电荷。然而SQM不仅慢，做优化还容易不收敛，导致半天也无法成功产生拓扑文件。更何况最后也是要替换为Multiwfn算的RESP/RESP2电荷，故计算AM1-BCC电荷没实际意义。同理，用在线版acpype也是建议把charge method设为user。



• Automated Topology Builder（ATB，http://atb.uq.edu.au）：生成GROMACS拓扑文件的在线工具，可以生成基于ATB开发者自行修改的GROMOS96 G54A7力场（扩充了原子类型）的GROMACS或GROMOS程序的拓扑文件。比PRODRG2更先进更可靠，解决了PRODRG2没法自动确定质子化态和charge group指认不准的问题以保证原子电荷可靠，并且能利用对称性保证电荷等价，另外没有PRODRG2那样对于每日提交的数目有限制。ATB虽然设计得不错，可以作为产生小分子GROMOS力场的GROMACS拓扑文件的首选，但它生成的原子电荷、确定的参数的可靠性也只是一般，不能保证总是很理想。如果要做很严谨的模拟研究，还是建议自行计算RESP电荷并且手动检查ATB给出的拓扑文件的合理性，有必要时适当调节。ATB网站上也有个分子库，包含巨量事先搞好的小分子的参数和拓扑文件，其中有的是别人之前提交过的分子，有的是经过专人手工处理过的分子，显然后者可靠程度更高。对于比较常见的分子，提交到ATB之前建议先搜索一下分子库，如果已经有的话就直接用。



• LigParGen（http://zarbi.chem.yale.edu/ligpargen/）：生成GROMACS, NAMD, CHARMM, LAMMPS等程序OPLS-AA力场的拓扑文件的工具。毕竟这是OPLS力场开发者自己搞的，因此原则上比MKTOP、TPPmktop更靠谱。可以通过SMILES字符串、.mol、.pdb文件进行输入（用pdb格式时老是报错，我建议用.mol），原子上限200个，可以顺带着让服务器对分子在OPLS-AA力场下做几何优化。分配的原子电荷是1.14*CM1A或1.14*CM1A-LBCC，前者是把CM1A电荷数值乘上1.14得到的，后者是在1.14*CM1A基础上再引入LBCC校正得到的，在J. Phys. Chem. B, 121, 3864 (2017)中已证明这两种原子电荷结合OPLS-AA模拟有机体系凝聚相可以得到不错结果。此服务器还可以输出PQR文件。



本文开头所述的Multiwfn可以计算的1.2*CM5电荷比LigParGen直接给出的电荷在多数情况下更适合做动力学模拟，特别是对于密度、蒸发焓的精度方面而言，这点在J. Phys. Chem. B, 121, 3864 (2017)的测试中充分体现了。而且对于一些分子，LigParGen给出的原子电荷加和不精确为0，而是比如0.0001，这导致此类分子数目较多时体系总电荷对整数有不可忽视的偏离，对模拟造成不良影响。因此建议大家将LigParGen给出的itp文件里的原子电荷部分替换为Multiwfn得到的1.2*CM5电荷。



• MKTOP：是个Perl脚本，可以在https://github.com/aar2163/MKTOP/blob/master/mktop.pl下载。支持OPLS-AA和AMBER03力场，电荷没法自动生成而必须自己提供。使用之前需要确保已经安装了Perl运行环境，并且要把mktop.pl脚本开头的GROMACS拓扑文件目录改成当前机子里实际的，比如$gromacs_dir="/sob/gmx2018.8/share/gromacs/top";。之后可以比如这样运行：./mktop.pl -i new.pdb -o new.top -ff opls -conect no。这代表处理当前目录下的new.pdb，产生名为new.top的拓扑文件，使用OPLS-AA力场，并且不使用.pdb里的CONECT字段记录的连接关系而是根据原子之间距离猜测连接关系。之后需要自行把原子电荷填到new.top的[atoms]字段里。我发现有时候此脚本指认的OPLS-AA原子类型是错误的，所以建议按照力场目录下的atomtypes.atp仔细看看指认的原子类型到底是否合理。

注：以前MKTOP是有在线服务器的（http://www.aribeiro.net.br/mktop/），但是如今已经失效。



• OBGMX（http://software-lisc.fbk.eu/obgmx/）：生成UFF力场的gromacs拓扑文件的在线工具。由于UFF几乎涵盖整个周期表，因此不光有机分子，也可以使得Gromacs能够处理无机物、周期性体系，比如MOF。由于UFF的力场形式和Gromacs所支持的不完全兼容，此程序给出的参数实际上是对原UFF力场的近似。个别原子类型识别可能有误。电荷必须自己提供。

2020-Dec-26注：此在线服务器目前已无法使用，但可以下载离线程序使用，见http://bbs.keinsci.com/thread-21015-1-1.html。



• SwissParam（http://swissparam.ch）：输入有机小分子mol2文件，生成用于CHARMM/NAMD和GROMACS模拟的拓扑、参数文件。力场参数基于MMFF，但只保留谐振项部分，因此只是MMFF的近似。原子电荷通过MMFF方法获得。范德华参数采用CHARMM22中最接近的原子类型。这样的参数比较粗糙，有优化的余地。



• ztop：计算化学公社论坛（http://bbs.keinsci.com）上钟成开发的拓扑文件产生工具，请在论坛首页搜索框里搜索ztop看他发的相关帖子了解此程序的特点和使用。



• CGenFF（https://cgenff.com）：能够生成CGenFF力场的GROMACS拓扑文件的在线工具，学术用户必须用edu邮箱才能注册。





以下在线程序已失效：



• PRODRG2（http://davapc1.bioch.dundee.ac.uk/cgi-bin/prodrg）：历史非常悠久很有名的生成Gromacs拓扑文件的在线工具。只支持GROMOS87/96力场，生成gromacs和其它一些程序的拓扑文件。原子电荷是根据基团指认的，如果基团识别不对那么电荷也不可靠。有在线版和离线版。可以选择自动优化分子结构。此工具在J. Chem. Inf. Model., 50, 2221 (2010)被曝光往往不能正确指认charge group，导致原子电荷分配也很不合理。而且又由于有了更好的ATB，因此如今强烈不推荐使用



• CGenFF（https://cgenff.paramchem.org）：先注册，上传有机小分子的mol2文件，即可生成基于CGenFF力场的CHARMM的拓扑文件。如果mol2是gview建的，一定要事先把里面的Ar替换成ar。上传文件的时候不要选Guess bond orders from connectivity和Include parameters that are already in CGenFF。如果文件处理正常，会立刻产生str文件，点击其链接之后把里面内容拷到比如Actos.str里面。进入网页里的More Info & Tools - Utilities，点击GROMACS conversion program，可下载把str文件转换为GROMACS格式的Python脚本cgenff_charmm2gmx.py。对于CentOS 7.2，应运行yum install numpy和yum install python-networkx把这个脚本所需的包装上。去http://mackerell.umaryland.edu/charmm_ff.shtml#gromacs里面下载用于GROMACS的CHARMM36力场文件，解压得到比如charmm36-nov2016.ff文件夹，将它和Actos.str、cgenff_charmm2gmx.py都放到当前目录，另外也把此文件夹拷到gromacs的top目录下。假设Actos.str里RESI后面的词是Molecu，最初上传的是Actos.mol2，则运行./cgenff_charmm2gmx.py Molecu Actos.mol2 Actos.str charmm36-nov2016.ff。在当前目录会产生molecu.top、molecu.prm、molecu.itp、molecu.pdb（从mol2转换过来的），适当调整itp和top里的分子名，调整itp里的残基名和结构文件相对应后，即可用于模拟。str文件里的力场参数有penalty指标，数值越大说明此参数可靠性越低，详见网页里的说明。



• TPPmktop（http://erg.biophys.msu.ru/tpp/）：在线工具，提供pdb文件，能产生OPLS-AA力场参数的GROMACS拓扑文件。速度比较快，但得到的拓扑文件里有时候会缺参数，或者出现额外的原子类型，需要再手工处理（需要引入额外的力场文件，但是笔者发现在网上下载不到）。此服务器有时候有其它任务在跑，此时无法提交任务，只能等过一阵服务器没任务时再提交。







另外说两个有关的程序



• YASARA AutoSMILES Server（http://www.yasara.org/autosmilesserver.htm）是在线版程序，离线的话得买YASARA（建模+可视化+动力学模拟工具）。可以计算AM1-BCC电荷、指认amber94/96/99力场参数。但是产生的文件只能用YASARA View打开，也就是说，拓扑文件相当于YASARA专用的。



• RED（RESP ESP charge Derive，http://q4md-forcefieldtools.org/REDServer-Development/）：专门生成RESP电荷的，也能搞力场参数。页面做得不是一般的糟糕，结构十分混乱，令我摸不到头绪，因此笔者也没怎么仔细研究。由于Multiwfn已经完美支持RESP电荷计算了，RED已没有必要使用了。





这里把各种程序做一下总结，是笔者讲授的相关分子动力学与 GROMACS 教程中的一页幻灯片










1.png (81.54 KB, 下载次数 Times of downloads: 625)

下载附件 Download



2024-11-5 00:53 上传 Uploaded

### 2 楼

太谢谢你了

### 3 楼

本帖最后由 yaochuang 于 2014-12-18 17:44 编辑 



@sobereva 

sob老师，请问用这些软件产生的top文件和用pdb2gmx 这个命令产生的有什么关系吗？



我可以直接用gaussianview产生pdb文件，然后用pdb2gmx这个命令来生成top文件吗？我试了一下总是报错（报错信息在下图中），是文件的格式问题呢，还是就不能用这种方法呢？



我主要想做的是模拟一下我们自己合成的一个有机分子在水和四氢呋喃中形成particle的过程，以及控制这个过程的作用力是什么。

谢谢了！

### 4 楼

自己找的小分子不要用pdb2gmx来产生拓扑文件，用我文中的途径产生.itp文件然后include到主.top文件是最好的作法。



pdb2gmx主要是对于力场已经自带的残基或者小分子产生拓扑文件的，并且可以处理残基间的拼接过程，比如产生蛋白、DNA等。用pdb2gmx之前必须把要载入的pdb文件里所有类型的分子拓扑信息写进相应力场的rtp文件里面。即便你已经把小分子的拓扑信息都写进了rtp里能够用它来生成体系的拓扑文件，但仍有一点很不好，就是所有分子的拓扑文件是连在一起的。比如说，你模拟20000个A分子，本来include一次A分子的.itp文件就够了，但你要如果先把A分子的拓扑信息写进rtp里用pdb2gmx来产生拓扑文件，则20000个A分子会成为一个“分子”，出现在同一个[ moleculetype ]里，这使得拓扑文件冗长且不容易修改。

### 5 楼

本帖最后由 yaochuang 于 2014-12-19 17:27 编辑 



@sobereva 

谢谢sob老师，



根据你的提示，我在ATB网站上提交了我的小分子，得到了WVQC.itp和WVQC.pdb文件.（如图ATB）

但是我在操作时还是出现了一些问题，我把我的过程写一下请你帮我看看。



1:我利用 WVQC.pdb产生一个盒子并添加了水:

editconf -f WVQC.pdb -bt dodecahedron -d 0.5 -o box.gro



2:按照manul中的介绍我写了一个WVQC.top文件。（如图top）

之后运行 gmx solvate -cp box.gro -cs spc216.gro -p WVQC.top solvated.gro

产生的solvated.gro在VMD中观看也是正常的。



3.做energy minimization，自己按手册写了em.mdp文件。 （如图em）



然后运行 grompp -f em.mdp -p WVQC.top -c solvated.gro -o em.tpr 时就出现了错误。（如图 error）



此时的top文件在最后多了一行sol   1467 （如图top2）





请老师帮我看看，自己弄了一天了也没有弄出来！ 谢谢！

### 6 楼

yaochuang 发表于 2014-12-19 17:22

@sobereva 

谢谢sob老师，

给你两个完整的基于ATB产生的拓扑文件做小分子+水模拟的例子。对照对照估计就明白了。对应的是gmx 4.6.7。

文中用到的mdp文件：





em.mdp

(447 Bytes, 下载次数 Times of downloads: 217)



2014-12-19 18:58 上传 Uploaded
点击下载
Click to download












md.mdp

(896 Bytes, 下载次数 Times of downloads: 181)



2014-12-19 18:58 上传 Uploaded
点击下载
Click to download












1 MD simulation for solvated cholesterol



Go to ATB homepage, select "Existing Molecules", input "Cholesterol" in "Search string" box, click "Search ATB", you will find the ATB library already contains cholesterol and thus we don't need to submit it as a new molecule. The first entry in the list is what we need, and its "Curation" is "Manual", that means its topology file is manually prepared and thus highly reliable. Click "Link" to enter to the molecular page. Then select "GROMACS G53A6FF United-Atom (ITP file)" to save it as cholesterol.itp, and select "United-Atom PDB (optimised geometry)" to save it as cholesterol.pdb.



Write a new topology named system.top with below content:

#include "gromos54a7.ff/forcefield.itp"

#include "gromos54a7.ff/spce.itp"

#include "cholesterol.itp"



[ system ]

Cholesterol+Water



[ molecules ]

CLR               1





Then build box and solvate it:

editconf -bt triclinic -f cholesterol.pdb -o cholesterol_box.gro -d 2

genbox -cp cholesterol_box.gro -cs spc216.gro -o system.gro -p system.top



Start simulation:

grompp -f em.mdp -c system.gro -p system.top -o em.tpr

mdrun -v -deffnm em

grompp -f md.mdp -c em.gro -p system.top -o md.tpr

mdrun -v -deffnm md





2 MD simulation for solvated perylene



Search "perylene" in ATB library, enter the entry 22654 (in fact this is the one I submitted), its "Curation" is "ATB", that means topology file of this molecule was generated automatically by ATB. In the new page click "Show MD", and click "GROMACS G54A7FF United-Atom (ITP file)" and save it as perylene.itp, click "United-Atom PDB (optimised geometry)" and save it as perylene.pdb.



Write a new topology named system.top with below content:

#include "gromos54a7.ff/forcefield.itp"

#include "gromos54a7.ff/spce.itp"

#include "perylene.itp"



[ system ]

perylene+Water



[ molecules ]

OVOF               1



The method for building box, adding solvents and running MD are exactly identical to the cholesterol case.

### 7 楼

sobereva 发表于 2014-12-19 18:58

给你两个完整的基于ATB产生的拓扑文件做小分子+水模拟的例子。对照对照估计就明白了。对应的是gmx 4.6.7 ...

谢谢sob老师！

### 8 楼

yaochuang 发表于 2014-12-20 16:01

谢谢sob老师！

    给你两个完整的基于ATB产生的拓扑文件做小分子+水模拟的例子。对照对照估计就明白了。对应的是gmx 4.6.7 ...





谢谢sob老师！



还有一个问题想请教你，如果我想向水盒子放5个这样的分子应该怎么做呢？

我直接在.top文件中将molecules后面的数字改为了5

[ molecules ]

;molecule name nr.

 WVQC       5



但是在计算 grompp -f em.mdp -c system.gro -p system.top -o em.tpr的时候出现这样的错误：

Fatal error:

number of coordinates in coordinate file (system.gro, 91625)

             does not match topology (system.top, 91750)



我查看了一下ststem.gro中最前面好像也只有一个WVQC的坐标。

这个应该怎么做呢？

谢谢！

### 9 楼

谢谢分享！

### 10 楼

yaochuang 发表于 2014-12-20 16:32

给你两个完整的基于ATB产生的拓扑文件做小分子+水模拟的例子。对照对照估计就明白了。对应的是gmx 4. ...

你也得相应地在结构文件里放5个分子才能对应上。

可以用packmol来生成初始结构，要放几个分子，在什么位置放都可以方便地设定。也可以建立个空盒子，然后用genbox添加分子，-nmol可以设定放几个。

### 11 楼

Sob老师您好，您提到了可以利用Packmol构建初始构型，我想请教一下那个resnumbers这个命令应该怎样使用（手册已看）？？我在构型的2侧分别加入15个Ca原子，但是它默认将这个2侧Ca离子看成了不同的残基序列号。我想让Ca离子是同一序列号应该怎样处理。附上我的inp文件



tolerance 2.0 

filetype pdb

output 7_7_Ca_Cl.pdb



structure Ca.pdb 

  number 15

  resnumbers 1

  inside box 0. 0. 0. 46. 46. 24.

end structure





structure Ca.pdb 

  number 15

  resnumbers 1

  inside box  0. 0. 42. 46. 46. 66.

end structure

### 12 楼

ruanyang 发表于 2014-12-20 22:01

Sob老师您好，您提到了可以利用Packmol构建初始构型，我想请教一下那个resnumbers这个命令应该怎样使用（手 ...

想不起来了，就用ultraedit之类的工具用列模式手动编辑一下就行了

### 13 楼

我也是这样处理的！  我不清楚这个resnumbers怎么用！在UltraEdit中编辑有点麻烦！谢谢Sob l老师

### 14 楼

本帖最后由 yaochuang 于 2014-12-22 11:13 编辑 

sobereva 发表于 2014-12-20 20:32

你也得相应地在结构文件里放5个分子才能对应上。

可以用packmol来生成初始结构，要放几个分子，在什么位 ...

谢谢sob老师，



我还有一个问题就是gromacs中可不可以把水盒子换成其他的溶剂盒子呢，比如说甲醇之类的。 我直接利用genbox把甲醇插入到盒子中，利用甲醇的密度来算盒子中插入的甲醇分子的个数。 这样可以吗？

我计算的一个6*6*6的盒子中要插入19224个甲醇分子，感觉和水比起来太多了，跑不完就死掉了。这样算可能是太多了，那要怎样计算分子的数量呢？

有没有其他的办法呢？

### 15 楼

不用设个数，genbox自动就会把盒子填满，能填多少填多少。

### 16 楼

sobereva 发表于 2014-12-22 11:15

不用设个数，genbox自动就会把盒子填满，能填多少填多少。

谢谢sob老师，终于搞定了！

### 17 楼

sobereva 发表于 2014-12-22 11:15

不用设个数，genbox自动就会把盒子填满，能填多少填多少。

sob老师

我在使用packmol建立一个蛋白一半在有机小分子内，一半在水分子内的时候。有了很大的问题。

1 packmol中两相体系中使用的输入文件是xyz。经过这样建模出来的xyz再通过VMD转换回gro时，原子序号都是乱的，用ultraedit编辑也无从下手。一是工作用量太大，2000个有机小分子光是序号就要编很久。但更严重的是这样生成的gro，并没有可以对应的top文件。。不知如何解决。已经尝试过gro2xyz和xyz2gro脚本。xyz文件默认把残基序号打乱了。和gro对不上。

2 尝试使用pdb建模。但是有机层分子通过pdb建立的模型。总体上应用了amber力场后，就不知道怎么怎么把GAFF力场应用到有机层上。amber力场下的坐标和GAFF力场下的坐标不同。itp进去之后，也对不上吧？对于gro和top的一一对应关系仍然很模糊。

3 通过gmx的editconf无法实现蛋白一半溶解在水里，蛋白会呈现周期性。穿过比它小的盒子（穿到底部），使得体系底部附近的水无法填充。尽管使用了-pbc 取消周期性的命令。仍然会出现。

请老师指点指点！

### 18 楼

kunkun 发表于 2015-1-21 22:52

sob老师

我在使用packmol建立一个蛋白一半在有机小分子内，一半在水分子内的时候。有了很大的问题。

1  ...

top文件自己写就行了，不管有多少个分子，只要include一次那个分子的.itp文件就行了，很简单。



你的做法都不是很理想。最简单的做法就是像一般情况那样，先用editconf围着蛋白建立一个盒子，把里面用genbox全填上水。 然后用VMD读取gro文件，用位置选择功能把一半的水都给去掉，保存成pdb文件（与此同时，把top文件里的水分子数改成相应的）。然后再用genbox对这个pdb文件填满有机分子即可。

### 19 楼

sobereva 发表于 2015-1-21 23:24

top文件自己写就行了，不管有多少个分子，只要include一次那个分子的.itp文件就行了，很简单。



你的做 ...

谢谢sob老师 我等等再去研究下怎么具体操作vmd。

我还有一个问题，如果在amber+gaff力场下，完成了蛋白的构变，此时如果需要脂类对接。脂的力场，貌似只有amber和charmm有，那我这样选择amber合适么。对接autodock都说自由能很粗糙，那肯定还要做一个蛋白复合物的动力学，此时amber和charmm是两个不兼容的力场。。实验结果也不可靠吧。（这个是gromacs mannal list论坛那里得知，不知是否正确），我看justin的教程也用了dppc的力场，但是做了力场的修改（我猜是应为dppc的参数就是用gromos来拟合的）

还是说我选择gromos力场更合适？（对整体的实验来说）

### 20 楼

kunkun 发表于 2015-1-21 23:42

谢谢sob老师 我等等再去研究下怎么具体操作vmd。

我还有一个问题，如果在amber+gaff力场下，完成了蛋白 ...




磷脂力场非常多。要考虑两个问题，一个是兼容什么力场，一个是兼容什么程序（否则得自己编写参数或拓扑文件，略麻烦点）。以下是我以前随便写的磷脂力场的总结（如果你在gmx里用amber力场模拟，用slipids为宜）：



Gromos96：rtp本身自带了DPPC参数，结果不好。

CHARMM27及改进版CHARMM36c：专门且常用的膜力场。

Glycam06：支持了少数磷脂分子，非主流。

GAFF：GAFF力场没有膜的参数，直接用在膜模拟效果不好。



Lipid11(2012)：Skjevik提出的膜力场，作为amber系列力场的扩展，参数来自GAFF，几种头部（PC,PE,PS,PH,P2,PGR,PGS,PI）和几种尾部可以自由搭配（模块化）组成磷脂，还支持胆固醇，完全兼容amber力场，leap已支持。非主流。Dickson(2012)的GAFFlipid力场只是一个阶段性的膜力场，将会被融合进Lipid11。



Berger(1997)：联合原子膜力场。成键参数基于GROMOS87，LJ参数基于OPLS-UA，适合搭配Gromos87，很常用也很好，几乎是唯一致命的问题在于不直接兼容Gromos96，若搭配OPLSAA需要很留神。虽然也有一些人结合Gromos96来模拟膜蛋白，但终究比较古怪，需谨慎。原文只给出了DPPC的参数，后来又有人基于此弄了其它磷脂的。Berger本身没直接提供参数和拓扑文件，Peter Tieleman基于Berger的参数制作了DPC、POPC、DPPC、DMPC、DLPC、DOPC、PLPC、POPE的itp文件，都需要lipid.itp中的参数，可以在这里下载：http://wcm.ucalgary.ca/tieleman/downloads



G43A1-S3 (2006)：Chiu弄的兼容Gromos43A1的膜力场。支持PC/PE/sphingomyelin和cholesterol。此力场的POPC不建议使用。



*Kukol(2009)：完全兼容Gromos96 G53A6的膜力场，烷烃链是联合原子，结果很好，和Berger相仿佛，弥补了它不支持Gromos96的遗憾。拓扑文件从原文的补充材料里得到。包含DPPC、DMPC、POPG、POPC、DMPC的参数。此力场的POPC不建议使用。



*DAVID POGER(2010)：完全兼容gromos96 G53A6的膜力场。JCC的文章中只提出了DPPC的参数，JCTC的文章中还提出了DLPC、DMPC、DOPC、POPC的参数。网址和gmx的拓扑文件：http://compbio.chemistry.uq.edu.au/~david/research/lipids.htm



Stockholm lipids (Slipids) (2012)：Jambeck弄的全原子膜力场。兼容amber。支持DPPC、DLPC、DMPC、POPC、DOPC、SOPC、POPE、DOPE、sphingomylin、PG和PS头部集团、胆固醇。gromacs的拓扑文件和预平衡的结构从这里下：http://people.su.se/~jjm/Stockholm_Lipids/Downloads.html



MARTINI：粗粒化。网址和gmx的拓扑文件：http://md.chem.rug.nl/cgmartini/index.php/downloads



====



Lipidbook汇总了各种膜力场的参数：http://lipidbook.bioch.ox.ac.uk



ATB带了几十种兼容gromos96的膜参数（可能对应的gromos96版本不同），ATB也能自动生成新的磷脂的参数。ATB网址和gmx的拓扑文件：http://compbio.biosci.uq.edu.au/atb/

### 21 楼

本帖最后由 kunkun 于 2015-1-22 10:42 编辑 

sobereva 发表于 2015-1-21 23:59

磷脂力场非常多。要考虑两个问题，一个是兼容什么力场，一个是兼容什么程序（否则得自己编写参数或拓扑 ...

sob老师，我在vmd中按照您所说的，用位置选择y平面以下的范围（在graphic>represatation>create Rep>select atoms (y 27 to 71 and water)，但是会出现平面内残缺的氢原子和氧原子...把这两个部分分别保存为pdb还是gro.。然后cat之后结构完全错乱(我看justin的教程，做蛋白底物复合也是这个思路，我把水当成了底物，蛋白还是蛋白）不知这里哪里错了。

而且因为我填充水分子时，我观察到水是沿着z轴添加（按序号），但是我需要是沿着y轴切割，那我选择水分子的序号就不是顺序的...还是说我对老师您说的位置选择功能理解错了...还请老师稍微再指点下,,对水分子删除那里理解还不是很对。



补充：刚才发现了原来正确的命令应该是water y 27.xxxxx to 71.xxxxxx or protein 这样才能解决，

但是sob老师，这样选择出来的水 在pdb中看还是会有残留的氧原子....

### 22 楼

kunkun 发表于 2015-1-22 09:46

sob老师，我在vmd中按照您所说的，用位置选择y平面以下的范围（在graphic>represatation>create Rep>sele ...

写成same residue as { xxx }  这里xxx是之前你写的选择语句，这样每个分子都会保留完整

### 23 楼

本帖最后由 kunkun 于 2015-1-22 13:47 编辑 

sobereva 发表于 2015-1-22 10:51

写成same residue as { xxx }  这里xxx是之前你写的选择语句，这样每个分子都会保留完整

感谢sob老师

问题都解决了！

### 24 楼

谢谢分享！

### 25 楼

sob 老师，请问以上几种生成拓扑文件的方法中有没有可以用来生成含有Ir原子的配合物的拓扑文件的方法呢？

我用ATB时失败了，显示Ir原子用不了。

### 26 楼

yaochuang 发表于 2015-1-24 20:16

sob 老师，请问以上几种生成拓扑文件的方法中有没有可以用来生成含有Ir原子的配合物的拓扑文件的方法呢？

 ...

ATB是基于gromos力场的，处理范围只限于有机分子，过渡金属只支持很少几种。

无机体系你可以按帖子里说的用UFF力场来模拟。

### 27 楼

sob老师，我想请问一下GROMOS力场下小分子的resp电荷计算除了用高斯之外，还有什么其他的软件推荐呢？(没有版权）

老师说的网站是计算amber和charmm力场的。按照老师说的antechamber的应该也是对应amber力场吧..?

### 28 楼

kunkun 发表于 2015-1-31 14:19

sob老师，我想请问一下GROMOS力场下小分子的resp电荷计算除了用高斯之外，还有什么其他的软件推荐呢？(没有 ...

高斯本身也产生不了RESP电荷，只不过是提供antechamber计算RESP要用的静电势数据。有没有高斯版权无所谓，不用提它，只说RESP电荷是antechamber算的就够了。

antechamber产生的RESP电荷用在任何力场下的模拟都可是可以的。就用它单纯作为产生RESP电荷的工具，和用什么力场没关系。

### 29 楼

sobereva 发表于 2015-2-1 02:47

高斯本身也产生不了RESP电荷，只不过是提供antechamber计算RESP要用的静电势数据。有没有高斯版权无所谓 ...

感谢 sob老师，我在使用antechamber时有点疑问，在计算RESP电荷时，有一个flag   -at（原子类型）好像manual上选项只有amber和gaff，若是使用gromos力场，是否此选项跳过，还是它会默认生成一个gaff类型，只需要把电荷部分修改至ATB产生的itp电荷部分即可？



还有一个问题，我看文献上有同学使用高斯来制作小分子（比如甘油三酯等，但ATB中只有磷脂部分），那我使用ATB画出甘油三酯后，自行计算RESP，不知该方法可靠度如何呢？还是说这类分子的制作方法是需要自己优化其他参数？望老师不吝解答

### 30 楼

kunkun 发表于 2015-2-1 11:26

感谢 sob老师，我在使用antechamber时有点疑问，在计算RESP电荷时，有一个flag   -at（原子类型）好 ...

不用设-at，用默认即可



直接把RESP电荷写进ATB给出的.itp里即可。不过，ATB某些时候自动确定的力场参数有点问题，比如我以前用ATB做磷脂的拓扑文件，一般来说烷烃链的二面角的k应该是5.9，ATB貌似给指认成其它类型的二面角力场参数了，成了3.7。prodrg貌似没这个问题。反正，用ATB的话，建议还是自行看一下每个原子的原子类型是否指认得合理，二面角参数是否确实给得合适。

### 31 楼

sobereva 发表于 2015-2-1 11:46

不用设-at，用默认即可



直接把RESP电荷写进ATB给出的.itp里即可。不过，ATB某些时候自动确定的力场参 ...

明白了，我再去检查研究，感谢sob老师指点

### 32 楼

本帖最后由 kunkun 于 2015-2-3 01:41 编辑 

sobereva 发表于 2015-2-1 11:46

不用设-at，用默认即可



直接把RESP电荷写进ATB给出的.itp里即可。不过，ATB某些时候自动确定的力场参 ...

sob老师，我用高斯09计算ESP 用antechamber拟合resp电荷的过程中，根据网上的说法，在gjf指令文件里面添加了antechamber-ini.esp 

antechamber.esp

但是产出的结果却无此两文件（混存文件夹内也无），我有安装ambertools（一开始还以为是学校机子没有安装的缘故）

我使用的参数是opt hf/6-31g* pop=MK iop(6/50=1) 应该是设置了高斯计算静电势的。但是在antechamber中使用gout文件生成mol2文件时，却提示我需要添加iop（6/50=1）的提示，说无ESP参数....  



-------------

后来看了老师的帖子发现 iop（3/33)和（6/42）才是关于esp的拟合的，但是为何网上那么多教程推荐高斯09计算esp用的是6/50=1呢...-------------

原来高斯09b1之后6/50取代了3/33..

我后来看了生成的mol2 发现resp拟合后的电荷和ATB拟合出来的差挺多的..(十六碳烷基),ATB的电荷计算出来还是不够准确。也不知道自己算的是不是更准确

grompp之后发现..antechamber经过拟合和优化的resp的均值精确到6位数，最终整体还是带负电的。。尽管我添加了-nc 0

最后只能自己用ultraedit，算均值，然后手动微调

### 33 楼

kunkun 发表于 2015-2-2 21:07

sob老师，我用高斯09计算ESP 用antechamber拟合resp电荷的过程中，根据网上的说法，在gjf指令文件里面添 ...

IOp指令和高斯版本有关，早期高斯09比较恣睢，乱改输出。



ATB直接给出的电荷不算理想，只能说自己懒得算的话可以勉强用。

实际上AM1-BCC也是很好的选择，虽然是对RESP的近似，但实际模拟结果往往更好。而且直接靠antechamber自身就能给出，免得借用Gaussian了，方便很多。

### 34 楼

sobereva 发表于 2015-2-3 04:17

IOp指令和高斯版本有关，早期高斯09比较恣睢，乱改输出。



ATB直接给出的电荷不算理想，只能说自己懒得 ...

感谢sob老师，我两种电荷分布都试试，看看哪个更适合我的体系

之前的ATB模拟出来的跟实验不太相符

### 35 楼

本帖最后由 kunkun 于 2015-2-6 15:01 编辑 

sobereva 发表于 2015-2-3 04:17

IOp指令和高斯版本有关，早期高斯09比较恣睢，乱改输出。



ATB直接给出的电荷不算理想，只能说自己懒得 ...

sob老师，我用antchamber计算的resp和bcc电荷，我仔细观察了下，有以下区别，resp电荷的每个charge group电荷有正有负，但总和为0。bcc计算的电荷每个charge group的电荷都为0..这个是正常的么。（ps都是经过手动微微调整的，antchamber计算的总电荷，grompp时不为0）而且antchamber -j 5 和不用-j 5 产出的电荷是不同的..不知老师为何说AM1-BBC的计算更好。是否就在于charge group上的总电荷有关？

### 36 楼

kunkun 发表于 2015-2-6 15:00

sob老师，我用antchamber计算的resp和bcc电荷，我仔细观察了下，有以下区别，resp电荷的每个charge group ...

并非am1-bcc比RESP好，只是说它虽然计算简单，但不一定比RESP差。

charge group没多大意义，其中电荷之和也并不需要非得为整数。只要从直觉上看各个原子电荷都合理就行了。

-j 5和默认的4可能在判断键的类型上有区别，导致处理时用的参数不同。就用默认的就行了。

### 37 楼

sobereva 发表于 2015-2-6 16:12

并非am1-bcc比RESP好，只是说它虽然计算简单，但不一定比RESP差。

charge group没多大意义，其中电荷之 ...

原来如此，感谢sob老师。

老师 我还有问题...

1 我在分析轨迹能量的时候，一般就只用到几个判断参数，总能 势能 温度 压力和密度。还有些参数不知道代表的具体作用，G96angle、coulomb(SR)、LJ(SR)、LJ-14的意义何在？感觉文献上很少有提及这部分的参数。（或则说，对于体系平衡的判断），而且总能的波动也是上千个RMSD。。不知以老师的经验来说多少范围以内可以判断是波动比较小的（针对蛋白体系），并且在在他们后面的总流失数值那块的判断不是很到位。我看手册上的流失总数的大小是以比值来计算的，不知流失的比值占总值多少比较合适？



2 老师认为在正式md的时候，控温和空压是使用速度矫正berendsen和berendsen好，还是nose-hoover配合Parrinello-Rahman更稳定？我看手册上是推荐berendsen来迅速平衡，而nose+par-Rahman来MD。但是文献很多人都直接用berendsen就完事了...不知偶联的方式对总流失方面的数值影响如何？

### 38 楼

kunkun 发表于 2015-2-6 19:43

原来如此，感谢sob老师。

老师 我还有问题...

1 我在分析轨迹能量的时候，一般就只用到几个判断参数， ...




1 那些都是构成势能的具体能量项，一般不单独分析。我不清楚你说的流失数值是指什么。波动大小无所谓，只要平均值比较平稳，没有明显起伏就行。实际上，对于蛋白体系，靠势能、温度、密度等等这些量衡量不出什么来，因为只要占模拟体系的主体的溶剂平衡了，这些量也就差不多平衡了，反映不出蛋白是否平衡了。蛋白的平衡一般看蛋白的RMSD曲线。



2 虽然原理上是nose-hoover配合Parrinello-Rahman好，但实际上对大体系用berendsen不会有什么问题，用不着过度讲究，一些人把berendsen的问题夸大了

### 39 楼

sobereva 发表于 2015-2-6 20:46

1 那些都是构成势能的具体能量项，一般不单独分析。我不清楚你说的流失数值是指什么。波动大小无所谓， ...

谢谢sob老师，看来我之前的设置还是可行的！



另外我说的流失值就是 

Energy                      Average   Err.Est.       RMSD  Tot-Drift

-------------------------------------------------------------------------------

Temperature                 307.814       0.13    2.91965   0.994645  (K)

Pressure                   -394.035         57    313.621    319.475  (bar)



此处的Tot-Drift的值..我看手册貌似是这么解释的..流失值

另外不知是否Err.Est是误差值..

### 40 楼

kunkun 发表于 2015-2-6 23:49

谢谢sob老师，看来我之前的设置还是可行的！



另外我说的流失值就是 

这些并不重要，平均值基本和期望的一致就行了。

### 41 楼

sobereva 发表于 2015-2-7 08:56

这些并不重要，平均值基本和期望的一致就行了。

谢谢sob老师指导！ 我就不继续纠结这些小问题了

### 42 楼

@sobereva

Sob老师， 我根据回复中的两个ATB生成拓扑文件的例子试了，但是ATB或者PRODRG中生成的itp都把烷基上的氢去掉了



[ atoms ]

;   nr      type  resnr resid  atom  cgnr   charge     mass

     1       CH3     1  S28     CEZ     1   -0.084  15.0350

     2       CH2     1  S28     CFA     1    0.133  14.0270

     3        OA     1  S28     OFB     1   -0.224  15.9994

     4       CH2     1  S28     CEW     1    0.133  14.0270

     5       CH2     1  S28     CEX     1    0.133  14.0270

     6        OA     1  S28     OEY     1   -0.224  15.9994

     7       CH2     1  S28     CET     1    0.133  14.0270

     8       CH2     1  S28     CEU     2    0.117  14.0270

     9        OA     1  S28     OEV     2   -0.235  15.9994



在计算 grompp -f em.mdp -c system.gro -p system.top -o em.tpr的时候出现这样的错误：

Fatal error:

number of coordinates in coordinate file (system.gro, 827830)

             does not match topology (system.top, 827653)

我试了PRODRG的ADDHYD atomname，但还是不行，纠结了一天都搞不定。求问老师这个要这么解决啊



谢谢

### 43 楼

shanshan 发表于 2015-2-27 10:46

@sobereva

Sob老师， 我根据回复中的两个ATB生成拓扑文件的例子试了，但是ATB或者PRODRG中生成的itp都把烷 ...

你的top中的分子数和gro文件的分子数不一致，检查一下top和gro，对应修改好top的分子数量就ok了

### 44 楼

kunkun 发表于 2015-2-27 11:24

你的top中的分子数和gro文件的分子数不一致，检查一下top和gro，对应修改好top的分子数量就ok了

谢谢。 然后还有一个问题， 如果是大分子长链的话是不是就不能用这个方法了呀，因为我看PRODRG在线的server不能算大分子。 那我是不是就就能自己写残基rtp加到gromacs的database里？ 小白表示有点小难度。

### 45 楼

shanshan 发表于 2015-2-28 03:13

谢谢。 然后还有一个问题， 如果是大分子长链的话是不是就不能用这个方法了呀，因为我看PRODRG在线的serv ...

如果长链大分子是由building block有规律地组成的，像是蛋白质、DNA，应该把building block写进rtp，而不是由ATB/prodrg直接生成大分子的拓扑信息。每个bulding block的.itp可以由ATB/prodrg产生，转换为rtp后，需适当处理一下边界。

### 46 楼

太感谢了，找到转换成CHARMM文件格式的地方

### 47 楼

本帖最后由 diaok 于 2015-11-20 16:58 编辑 



我可以补充一个工具吗？



对于新手可能会有所帮助

主要是oplsaa力场的

opls力场的好处是电荷参数完全指定，只要确定了原子类型，剩余参数都可以查表找到

对比文献就能知道结构是否正确



gromacs的Other software页面上还提供了一个topolbuild

http://www.gromacs.org/Downloads ... ions/Other_software



和mktop类似，也需要自己添加电荷

支持 tripos, gaff, glycam，amber，gmx，oplsaa力场（尝试glycam未成功，不同力场路径设置不一致，其他力场对比报错的路径很容易使用）

遇到不识别的键会直接报错退出，这点比不上mktop

运行后会生成*.gro  ff*.itp  *.log  *.top  posre*.itp文件

参数保存在*.top中，其中键、键角都带有连接信息注释，便于检查

我尝试的纤维素结果中原子类型定义比mktop稍准点，不过依然需要检查手动修改

### 48 楼

更新：添加了用CGenFF做gromacs拓扑文件的说明

### 49 楼

更新：增加了LigParGen（http://zarbi.chem.yale.edu/ligpargen/）的介绍

### 50 楼

sobereva 发表于 2014-12-19 18:58

给你两个完整的基于ATB产生的拓扑文件做小分子+水模拟的例子。对照对照估计就明白了。对应的是gmx 4.6.7 ...

太赞啦！Sob老师总是能够深入浅出地传授技能！

### 51 楼

更新：在文中加入了一张不同程序对比图

### 52 楼

请问acpype.py产生的gaff 力场中 CHARRMM格式的文件 （lig.cHARRMM.inp, lig.CHARMM.prm, lig.CHARMM.rtf) 能否用于NAMD?

### 53 楼

xpyp 发表于 2018-8-28 21:47

请问acpype.py产生的gaff 力场中 CHARRMM格式的文件 （lig.cHARRMM.inp, lig.CHARMM.prm, lig.CHARMM.rtf)  ...够呛，我没试过。

NAMD、charmm的用户，建议考虑用和charmm兼容的CGenFF力场，用CGenFF工具

### 54 楼

sob老师您好，我用MS构建了一个分子，想要生成其itp文件，用MS导出pdb格式后PRODRG报错如下：

PRODRG> Starting up PRODRG version AA100323.0717

PRODRG> Parameter set 'pd/gromos96' (fftype=2).

PRODRG> PDB mode detected.

PRODRG> WARNING: deleted hydrogen(s) from your input.

PRODRG> WARNING: duplicate atom name C   .

PRODRG> WARNING: duplicate atom name N   .

PRODRG> WARNING: duplicate atom name O   .

PRODRG> WARNING: atoms with same name found. Auto-renaming.

PRODRG> WARNING: more than one fragment.

ERRDRG> PRODRG does not deal with mono/di-atomic molecules.

PRODRG> Program terminated unsuccessfully, sorry!



由于MS导出的pdb文件原子名称全是按原子符号显示的，所以有大量重复。但是我不知道该怎么修改，把文件通过gromacs的editconf重新导出pdb后原子名称也不变，请问一下有什么解决的方法

### 55 楼

Lacrimosa 发表于 2018-11-17 11:49

sob老师您好，我用MS构建了一个分子，想要生成其itp文件，用MS导出pdb格式后PRODRG报错如下：

PRODRG> Sta ...

prodrg早过时了，甭用。而且也被证明电荷组划分不合理，现在都用ATB

### 56 楼

sobereva 发表于 2018-11-17 15:54

prodrg早过时了，甭用。而且也被证明电荷组划分不合理，现在都用ATB

感谢您的回复，ATB功能还挺多的~谢谢指教~

### 57 楼

在文中开头增加了对原子电荷生成方式的说明

### 58 楼

sobereva 发表于 2014-12-18 05:09

自己找的小分子不要用pdb2gmx来产生拓扑文件，用我文中的途径产生.itp文件然后include到主.top文件是最好的 ...

sob老师好，如果为聚合物用pdb2gmx的话，是需要自己编辑冗长且不容易修改的pdb文件吗？怎样能让这个过程变得简洁呢？谢谢。

### 59 楼

yihanxu 发表于 2019-2-26 15:43

sob老师好，如果为聚合物用pdb2gmx的话，是需要自己编辑冗长且不容易修改的pdb文件吗？怎样能让这个过程 ...

pdb是否符合要求、是否容易修改得满足pdb2gmx的要求完全看创建pdb的程序

### 60 楼

sobereva 发表于 2019-2-26 02:33

pdb是否符合要求、是否容易修改得满足pdb2gmx的要求完全看创建pdb的程序

老师好，我是用gview画聚合物链然后保存成pdb，觉得格式不是很好。请问能创建满足pdb2gmx的格式要求的pdb的程序有什么呢？谢谢。

### 61 楼

本帖最后由 yihanxu 于 2019-2-26 12:40 编辑 

sobereva 发表于 2019-2-26 02:33

pdb是否符合要求、是否容易修改得满足pdb2gmx的要求完全看创建pdb的程序

请老师删除此楼。实在对不起，又重发了，下次一定注意。

### 62 楼

yihanxu 发表于 2019-2-27 02:33

老师好，我是用gview画聚合物链然后保存成pdb，觉得格式不是很好。请问能创建满足pdb2gmx的格式要求的pdb ...

不可能有恰好合要求的，免不了得自己改，或者自己写程序处理

你得保证每个单体内的原子名不同，而且和rtp里的匹配

### 63 楼

本帖最后由 naoki 于 2019-3-23 00:03 编辑 

sobereva 发表于 2019-2-27 02:44

不可能有恰好合要求的，免不了得自己改，或者自己写程序处理

你得保证每个单体内的原子名不同，而且和rt ...

Sob老师，我想请教一个问题~我用TPPmktop生成有机小分子的itp拓扑文件，但是文件里没有[ atomtype ]，一开始就是[ moleculetype ]。我该如何获取[ atomtype ]呢？谢谢您~






tpp.png (55.05 KB, 下载次数 Times of downloads: 206)

下载附件 Download



2019-3-22 23:50 上传 Uploaded

### 64 楼

naoki 发表于 2019-3-22 23:50

Sob老师，我想请教一个问题~我用TPPmktop生成有机小分子的itp拓扑文件，但是文件里没有[ atomtype ]，一 ...

gmx自己的oplsaa目录下的ffnonbonded.itp里就已经有atomtype了，你把这力场的forcefield.itp引入了，程序自动就会用这些信息

### 65 楼

本帖最后由 naoki 于 2019-3-23 13:18 编辑 

sobereva 发表于 2019-3-23 03:35

gmx自己的oplsaa目录下的ffnonbonded.itp里就已经有atomtype了，你把这力场的forcefield.itp引入了，程序 ...

谢谢Sob老师的解答！老师我还想问一下，就是TPPmktop和LigParGen生成同一个分子的拓扑文件里面有些参数，如原子电荷，差别很大，哪个更可靠呢？而且LigParGen生成的itp里面atomtype感觉不太对，不管换什么分子都是opls_8XX这样子，以至于我用GMX生成tpr的时候提醒“WARNING 1 [file mpd.itp, line 7]:  Overriding atomtype opls_810”。我去看了一下oplsaa的atp文件，里面并没有8开头字段的原子类型，这是为什么呢，好困惑。

下面是间苯二胺分子分别用TPPmktop和LigParGen生成的itp文件截图：








itp1.png (86.41 KB, 下载次数 Times of downloads: 213)

下载附件 Download



2019-3-23 13:11 上传 Uploaded













itp2.png (44.05 KB, 下载次数 Times of downloads: 226)

下载附件 Download



2019-3-23 13:11 上传 Uploaded








下图是oplsaa的atp文件截图，编号从7XX直接跳到了9XX…








atp.png (13.56 KB, 下载次数 Times of downloads: 230)

下载附件 Download



2019-3-23 13:15 上传 Uploaded

### 66 楼

naoki 发表于 2019-3-23 13:15

谢谢Sob老师的解答！老师我还想问一下，就是TPPmktop和LigParGen生成同一个分子的拓扑文件里面有些参数， ...

OPLS-AA力场本身没有定义标准的计算原子电荷的方法，因此不同程序给的拓扑文件里电荷不同也很正常

合理的做法是使用1.20*CM5电荷，在J. Phys. Chem. B, 121, 3864 (2017)里证明适合结合OPLS-AA使用，计算方式如下








Clipboard01.png (57.65 KB, 下载次数 Times of downloads: 225)

下载附件 Download



2019-3-23 15:10 上传 Uploaded












这俩产生拓扑文件的程序我都不怎么用，平时也很少用OPLS-AA，主要原因之一是我很讨厌它对原子类型的名字定义得太混乱。LigParGen是专门搞OPLS-AA的人弄的，所以理应更合理。如果整个拓扑文件里对同一种原子类型定义了多次，会自动用最后一次定义的。如果新产生的小分子的itp文件里自己带了opls_810的atomtype定义，这种提示没有问题。

### 67 楼

装好了最新版Ambertools，用acpype.py处理.mol文件获得gmx拓扑文件。发现凡是带苯环的分子都不能运行，报错如下






QQ截图20190328154248.jpg (56.6 KB, 下载次数 Times of downloads: 211)

下载附件 Download



2019-3-28 15:47 上传 Uploaded








而其它的分子都能正常运行，几个不能运行的带苯环分子已上传。很费解，难道是程序BUG?

### 68 楼

h840473807 发表于 2019-3-28 15:48

装好了最新版Ambertools，用acpype.py处理.mol文件获得gmx拓扑文件。发现凡是带苯环的分子都不能运行，报错 ...

自行把mol2里的Ar改写为ar

### 69 楼

@sobereva 谢谢卢老师解答，我在用acpype.py处理一个较大的分子时又遇到了问题（与之前不同的是这次若把Ar改成ar,则开始就报错，报错内容同67#, 而用Ar则运算半小时后报错，报错内容如图） 






QQ截图20190331183422.jpg (127.4 KB, 下载次数 Times of downloads: 224)

下载附件 Download



2019-3-31 18:35 上传 Uploaded






，文件已上传。请问这该怎么解决呢？

### 70 楼

h840473807 发表于 2019-3-31 18:39

@sobereva 谢谢卢老师解答，我在用acpype.py处理一个较大的分子时又遇到了问题（与之前不同的是这次若把Ar ...

acpype加上-c user代表不自动计算原子电荷。如果你也修改acpype不让它自动优化结构，这个体系瞬间就能搞完。（本身让acpype自动添加AM1-BCC电荷也没什么实际意义，一般都建议用Multiwfn算更好的RESP电荷手动添加到[atoms]里面）

### 71 楼

sobereva 发表于 2019-4-1 04:11

acpype加上-c user代表不自动计算原子电荷。如果你也修改acpype不让它自动优化结构，这个体系瞬间就能搞 ...

好的，谢谢社长

### 72 楼

prodrg2的在线网址好像一直在维护，http://www.ccl.net/chemistry/res ... 2005/01/17.002-dir/这个是prodrg2.5的页面

### 73 楼

sobereva 发表于 2019-4-1 04:11

acpype加上-c user代表不自动计算原子电荷。如果你也修改acpype不让它自动优化结构，这个体系瞬间就能搞 ...

sob老师我想请教您一下如何不让acpype自动优化结构，谢谢~

### 74 楼

naoki 发表于 2019-11-4 09:47

sob老师我想请教您一下如何不让acpype自动优化结构，谢谢~

用我改过的这个







acpype_noopt.py

(143.37 KB, 下载次数 Times of downloads: 20)



2019-11-4 10:03 上传 Uploaded
点击下载
Click to download

### 75 楼

sobereva 发表于 2019-11-4 10:03

用我改过的这个

感谢Sob老师！我还想请教一下不让acpype几何优化，构建的拓扑文件有什么问题吗，谢谢！

### 76 楼

naoki 发表于 2019-11-4 12:24

感谢Sob老师！我还想请教一下不让acpype几何优化，构建的拓扑文件有什么问题吗，谢谢！

没有问题，只要输入文件里的键的连接关系正确就够了

### 77 楼

sobereva 发表于 2019-11-5 08:37

没有问题，只要输入文件里的键的连接关系正确就够了

谢谢Sob老师的回复~

### 78 楼

sob老师，我想做小分子穿膜的练习，查了很多资料，准备用charmm36力场来做，软件版本是gromacs5.7，所以在小分子的力场获取上，我有一些不明白，我应该用SwissParam来做，还是CGenFF来做呢？我对您的Multiwfn结合Gauss算RESP挺感兴趣，觉得这样的原子电荷更准确，想放到小分子参数里，谢谢

### 79 楼

Jack_Jun 发表于 2020-2-4 10:34

sob老师，我想做小分子穿膜的练习，查了很多资料，准备用charmm36力场来做，软件版本是gromacs5.7，所以在 ...

gmx根本就没有5.7版



我个人不喜欢charmm力场

建议用GAFF描述小分子（通过acpype产生拓扑信息，结合Multiwfn算的RESP电荷），用slipid描述磷脂（兼容AMBER力场。拓扑文件在这里有现成的http://www.fos.su.se/~sasha/SLipids/Downloads.html）

### 80 楼

sobereva 发表于 2020-2-6 02:46

gmx根本就没有5.7版



我个人不喜欢charmm力场

谢谢sob老师

### 81 楼

sob老师，我在用pdb2gmx命令生成拓扑文件时，在官网上下载下来蛋白质的PDB文件，和我力场中的PDB文件中氢原子名称不对应，我应该怎么加氢是其对应起来呢。非常感谢sob老师

### 82 楼

weiyi8061225 发表于 2020-3-2 16:15

sob老师，我在用pdb2gmx命令生成拓扑文件时，在官网上下载下来蛋白质的PDB文件，和我力场中的PDB文件中氢原 ...

替老师回答一下试试，最省事的方法氢删了就行，反正测的氢也很不准，尤其是XRD的，动力学也不需要很准。

参数中国加入-ignh忽略掉所有氢，自动添加。

不然就得用正则表达式替换一点点改，非常麻烦，有些还得交互选择质子化程度。

### 83 楼

snljty 发表于 2020-3-2 16:46

替老师回答一下试试，最省事的方法氢删了就行，反正测的氢也很不准，尤其是XRD的，动力学也不需要很准。

 ...

谢谢回答，但是自动添加的时候，因为质子化的程度不一样，所以填的氢和原结构是有出入的，比如GLY，结构中只有7个原子，自动添加的时候就多填了两个氢原子，明显和原来的结构不一样了，这样我的蛋白质和锌离子形成的配合物就有问题了，这个时候有什么其他办法解决吗？

非常感谢！

### 84 楼

weiyi8061225 发表于 2020-3-2 17:57

谢谢回答，但是自动添加的时候，因为质子化的程度不一样，所以填的氢和原结构是有出入的，比如GLY，结构 ...

不可能多两个氢原子，GLY是标准结构，而且又不涉及质子化态问题（除非是在蛋白质两端），因此除非你用联合原子力场，否则实际是几个原子自动加氢后就必定是几个原子

### 85 楼

sob老师，PRODRG2（http://davapc1.bioch.dundee.ac.uk/cgi-bin/prodrg）这个网站好像无法打开，不知如何使用这个服务器或者软件？

### 86 楼

夏一天 发表于 2020-3-3 12:16

sob老师，PRODRG2（http://davapc1.bioch.dundee.ac.uk/cgi-bin/prodrg）这个网站好像无法打开，不知如何使 ...地址变了：

http://prodrg1.dyndns.org/

### 87 楼

sobereva 发表于 2020-3-3 11:00

不可能多两个氢原子，GLY是标准结构，而且又不涉及质子化态问题（除非是在蛋白质两端），因此除非你用联 ...

sob老师，就是我的体系里是锌指蛋白，锌离子和蛋白质结合的时候，相邻的两个CYS是去氢的，但是自动加上的会多一个氢，导致结构不对应，这个时候应该怎么解决，既能有正确的结构，又能有正确的拓扑文件呀？非常感谢sob老师

### 88 楼

weiyi8061225 发表于 2020-3-6 16:17

sob老师，就是我的体系里是锌指蛋白，锌离子和蛋白质结合的时候，相邻的两个CYS是去氢的，但是自动加上的 ...

你是指CYS之间有二硫键还是什么其它情况？

### 89 楼

请问是不是用gaussview画好分子以后直接保存为pdb就可以用TPPmktop生产拓扑文件了？我画了一个167个原子的分子试了几次都失败了，请问是什么原因？

### 90 楼

王寓于 发表于 2020-3-13 08:29

请问是不是用gaussview画好分子以后直接保存为pdb就可以用TPPmktop生产拓扑文件了？我画了一个167个原子的 ...

很久不用TPPmktop了，看返回来的具体提示。不过鉴于已经有了更靠谱的ligpargen了，不如用这个。

### 91 楼

gromacs新手求教一下sob老师，有在OPLS-AA力场下的CO2的itp文件么？ATB给出的如下，在grompp时，提示Atomtype CPos not found。也尝试过其他类型的itp文件，总是报错误，如NO default U-B types。



我是通过packmol建了CO2，水，表面活性剂的盒子后，grommpp时出错的，请问有相近的例子可以参考么？



[ moleculetype ]

; Name   nrexcl

F9IT     3

[ atoms ]

;  nr  type  resnr  resid  atom  cgnr  charge    mass

    1    OM    1    F9IT     O2    1   -0.376  15.9994

    2  CPos    1    F9IT     C1    2    0.752  12.0110

    3    OM    1    F9IT     O1    3   -0.376  15.9994

; total charge of the molecule:   0.000

[ bonds ]

;  ai   aj  funct   c0         c1

    1    2    2   0.1170   3.2508e+07

    2    3    2   0.1170   3.2508e+07

[ pairs ]

;  ai   aj  funct  ;  all 1-4 pairs but the ones excluded in GROMOS itp

[ angles ]

;  ai   aj   ak  funct   angle     fc

    1    2    3    2    180.00   500.00

[ dihedrals ]

; GROMOS improper dihedrals

;  ai   aj   ak   al  funct   angle     fc

[ dihedrals ]

;  ai   aj   ak   al  funct    ph0      cp     mult

[ exclusions ]

;  ai   aj  funct  ;  GROMOS 1-4 exclusions

### 92 楼

张一手大哥 发表于 2020-3-21 06:50

gromacs新手求教一下sob老师，有在OPLS-AA力场下的CO2的itp文件么？ATB给出的如下，在grompp时，提示Atomty ...

对CO2不建议用OPLS-AA，因为有很多成熟、流行的描述CO2的力场可以用










Clipboard01.png (56.86 KB, 下载次数 Times of downloads: 146)

下载附件 Download



2020-3-22 15:25 上传 Uploaded

### 93 楼

sobereva 发表于 2020-3-22 15:25

对CO2不建议用OPLS-AA，因为有很多成熟、流行的描述CO2的力场可以用

感谢sob老师指导！我去学习一下！

### 94 楼

本帖最后由 张一手大哥 于 2020-3-25 16:52 编辑 

sobereva 发表于 2020-3-22 15:25

对CO2不建议用OPLS-AA，因为有很多成熟、流行的描述CO2的力场可以用

请问 sob老师， 我在以epm2写CO2的itp时，有几个参数没搞明白，请您指教。

1. [bonds]里面的kb参数是多少呢？键的力常数, 单位kJ/mol/nm2。影响了能量最小化em和cg过程么？2. 我在ffnonbonded.itp中添加了C和O的参数，是不是也需要在ffbonded里面添加键的参数呢？

3. 构建EMP2的CO2模型，在gromacs中是这么操作么？4. 对构建CO2和水的体系，[bonds]和[constraints]有区别么

辛苦sob老师

### 95 楼

我写的








Clipboard01.png (35.01 KB, 下载次数 Times of downloads: 159)

下载附件 Download



2020-3-25 21:11 上传 Uploaded

### 96 楼

sobereva 发表于 2020-3-25 21:11

我写的

谢谢sob老师

### 97 楼

拓扑生成好全啊，收藏一下，备用。

### 98 楼

专业

### 99 楼

请问用LigParGen产生的力场参数里电荷不守恒该怎么办？我的分子是中性分子。（电荷加起来是0.0001）

### 100 楼

wasngsimin 发表于 2020-7-13 17:40

请问用LigParGen产生的力场参数里电荷不守恒该怎么办？我的分子是中性分子。（电荷加起来是0.0001）

你的贴图方式不正确，仔细看指定的新社员必读贴了解怎么贴图



另一个帖子里我刚回复完

http://bbs.keinsci.com/thread-18451-1-1.html



用Multiwfn算1.2*CM5电荷

### 101 楼

本帖最后由 吃西瓜的佩奇 于 2020-8-27 11:35 编辑 



请问sob老师，我在打开TPPmktop网页上传pdb以后出现了图片中的情况，是什么原因呢？而在打开Ligpargen网页时出现了无法加载的情况，pdb文件无法提交。

### 102 楼

sobereva 发表于 2015-1-21 23:24

top文件自己写就行了，不管有多少个分子，只要include一次那个分子的.itp文件就行了，很简单。



你的做 ...

老师，您好，我想请教一下在VMD中如何利用位置选择功能把一半的水去掉呢？我已经在VMD中（graphic>represation>create rep>Selected Atoms(same residue as { water z 40 to 80} ）选中了一半的水.

### 103 楼

五支折断的箭 发表于 2020-9-3 22:44

老师，您好，我想请教一下在VMD中如何利用位置选择功能把一半的水去掉呢？我已经在VMD中（graphic>repres ...

保存文件时选择另外一部分即可

### 104 楼

请问为什么LigParGen在生成阴离子的时候会出错，比如SO42- 三氟甲基磺酸根SO3CF3-

### 105 楼

更新了此文，主要是对MKTOP的离线perl脚本使用方法加入了说明

### 106 楼

请问，为啥gaff官方没有完整的gromacs格式立场包呢？既然提供了acpype……

### 107 楼

tjuptz 发表于 2020-12-8 20:46

请问，为啥gaff官方没有完整的gromacs格式立场包呢？既然提供了acpype……

GAFF本身是AMBER那些人搞的，从感情上也不会提供gmx的力场包

而且就算有其他人提供了也没实际用处，毕竟acpype都会给出相应的atomtypes定义。而且GAFF的特征也不像gmx自带的其它力场那样，比如也没有定义生物分子残基的rtp等文件，因此弄个目录显得也怪怪的

### 108 楼

sobereva 发表于 2020-12-8 23:15

GAFF本身是AMBER那些人搞的，从感情上也不会提供gmx的力场包

而且就算有其他人提供了也没实际用处，毕竟 ...

Soga，谢谢老师，这算是小小的情怀问题。感觉charmm的开发者就稍微open一些

### 109 楼

obgmx在线版也凉了-_-

### 110 楼

sobereva 发表于 2014-12-19 18:58

给你两个完整的基于ATB产生的拓扑文件做小分子+水模拟的例子。对照对照估计就明白了。对应的是gmx 4.6.7 ...

老师，你好。我想请问一下，ATB网站能够生成“ GROMACS G54A7FF All-Atom (ITP file)”和“GROMACS G54A7FF United-Atom (ITP file)”两种的itp文件，您举的例子都是选用的United atom的。两者有什么区别吗？选用all-atom的可不可以？

### 111 楼

黑择明 发表于 2021-1-6 16:15

老师，你好。我想请问一下，ATB网站能够生成“ GROMACS G54A7FF All-Atom (ITP file)”和“GROMACS G54A7 ...

标准GROMOS96力场是联合原子力场，all-atom下载下来如果发现确实是全原子的，那是利用了ATB作者自己的修改版GROMOS里的原子类型，合理性可靠性被检验得没那么充分

### 112 楼

老师，您好。我想请问下，输入高斯优化后的结构，再用LigParGen工具产生OPLS力场的top文件时，键长、键角的值都会和我的初始结构不一致，这时我应该相信哪一个呢？



另外中性小分子+阴阳离子+水体系中，中性分子原子电荷采用CM5*1.2，离子采用RESP电荷，水模型直接引入力场自带的itp文件，这样模拟可行么？

### 113 楼

rice 发表于 2021-2-3 14:44

老师，您好。我想请问下，输入高斯优化后的结构，再用LigParGen工具产生OPLS力场的top文件时，键长、键角的 ...

键长键角的平衡值是由力场参数决定的，和你输入结构无关



可以

### 114 楼

sobereva 发表于 2021-2-4 03:20

键长键角的平衡值是由力场参数决定的，和你输入结构无关



可以

好的，谢谢卢老师

### 115 楼

老师，对于镍卟啉用ATB计算显示目前该程序不支持该原子，但是我还想应用GROMOS96力场，想请问老师，还有没有其它方法可以获得镍卟啉的top与itp文件？

### 116 楼

xxzj 发表于 2021-5-8 20:12

老师，对于镍卟啉用ATB计算显示目前该程序不支持该原子，但是我还想应用GROMOS96力场，想请问老师，还有没 ...

google搜看有没有人基于gromos系列力场模拟过，有相应文章的话里面可能会提及用的参数

### 117 楼

请问老师SwissParam生成的itp文件然后自己计算电荷修改，是不是就是真正的基于charmm力场的。

还有通过CGenFF生成的力场时CGenFF+CHARMM是什么意思，两者混合的吗。

### 118 楼

sobereva 发表于 2021-2-4 03:20

键长键角的平衡值是由力场参数决定的，和你输入结构无关



可以

sob老师，在用packmol构建初始结构的时候，小分子的结构是直接使用ligpargen给的gro文件中的结构，还是使用自己用gauss结构优化后的？

### 119 楼

adong 发表于 2021-5-12 23:39

sob老师，在用packmol构建初始结构的时候，小分子的结构是直接使用ligpargen给的gro文件中的结构，还是使 ...

如果ligpargen没有修改原子顺序，就无所谓

### 120 楼

sun666 发表于 2021-5-12 21:33

请问老师SwissParam生成的itp文件然后自己计算电荷修改，是不是就是真正的基于charmm力场的。

还有通过CGe ...

显然不是。帖子里明确说了成键相关的参数是MMFF94的



我不知道在哪显示的CGenFF+CHARMM

### 121 楼

sobereva 发表于 2021-5-13 07:25

显然不是。帖子里明确说了成键相关的参数是MMFF94的



我不知道在哪显示的CGenFF+CHARMM

您帖子最下面的图里

### 122 楼

sun666 发表于 2021-5-13 15:56

您帖子最下面的图里

那个不对，我改了

单纯是CGenFF

### 123 楼

本帖最后由 牧生 于 2021-5-16 16:04 编辑 










QQ截图20210516152615.jpg (238.99 KB, 下载次数 Times of downloads: 175)

下载附件 Download



2021-5-16 15:30 上传 Uploaded






 

大佬在文中提及了如上的字句，我能理解。而且原则上，使用opls力场时，我都会用 LigParGen去得到拓扑信息。





我现在需要做硫化氢和水的接触，且希望使用opls力场。但是用 LigParGen生成硫化氢的拓扑，无论用pdb，还是mol，还是SMILES，都会出错。。

因为实在能力有限，不会自己手搓itp，于是想到了acpype，使用在线服务器得到硫化氢这样的小分子信息：



; HHS_GMX_OPLS.itp created by acpype (v: 2020-11-11T22:59:34CET) on Sun May 16 01:28:37 2021



; For OPLS atomtypes manual fine tuning

; AC_at:OPLS_at:OPLScode: Possible_Aternatives (see ffoplsaa.atp and ffoplsaanb.itp)

; sh:SH:opls_200: []

; hs:HS:opls_204: []



[ moleculetype ]

;name            nrexcl

 HHS              3



[ atoms ]

;   nr  type  resi  res  atom  cgnr     charge      mass       ; qtot   bond_type

     1 opls_200     1   MOL     S    1    -0.196000     32.06000 ; qtot -0.196  SH  

     2 opls_204     1   MOL     H    2     0.098000      1.00800 ; qtot -0.098  HS  

     3 opls_204     1   MOL    H1    3     0.098000      1.00800 ; qtot  0.000  HS  



[ bonds ]

;   ai     aj funct   r             k

     1      2   1 ;    1.3473e-01    2.4426e+05 ;      S - H          SH - HS    

     1      3   1 ;    1.3473e-01    2.4426e+05 ;      S - H1         SH - HS    



[ angles ]

;   ai     aj     ak    funct   theta         cth

     2      1      3      1 ;    9.3000e+01    3.1213e+02 ;      H - S    - H1       HS -   SH - HS  









请教一下，对于像硫化氢这样十分简单的小分子，acpype得到的针对opls力场的拓扑信息，算是可靠还是不可靠？

### 124 楼

牧生 发表于 2021-5-16 15:39

大佬在文中提及了如上的字句，我能理解。而且原则上，使用opls力场时，我都会用 LigParGen去得到拓扑信 ...

原子电荷应当替换成Multiwfn算的1.2*CM5电荷，否则默认的AM1-BCC和OPLS-AA不搭



并且自行检查指认的原子类型到底是否合理，并且检查键长、键角和量化优化出来的是否基本吻合



以上都没问题的话，跑个MD看看实际效果，如果结构维持得不错就可以用

### 125 楼

老师，我想获得金属卟啉的gromacs拓扑文件，金属包括铁和镍，从网上下载的晶体结构文件，然后使用哪种工具都会出现问题，中心没有引入金属的无论使用哪个工具都可以获得相应的参数文件。所以想问一下老师，对于含有过渡金属配位的情况应该如何去获取相应的参数文件？辛苦老师了

### 126 楼

xxzj 发表于 2021-6-17 21:21

老师，我想获得金属卟啉的gromacs拓扑文件，金属包括铁和镍，从网上下载的晶体结构文件，然后使用哪种工具 ...

模拟金属卟啉的文献一大堆，去搜，然后看计算细节的描述

### 127 楼

本帖最后由 牧生 于 2021-7-7 21:50 编辑 



请教一下，我使用LigParGen得到的两种物质的itp，然后做两种物质在水中混合的模拟，两种物质[ atomtypes ]字段里面有编号是重复的，但对应的原子不一样的情况下该怎么办？在模拟过程中，gromacs能区分的开吗？



比如下面这样的例子，以红色字体标出的部分， 当我将两种物质的[ atomtypes ]都剪切到ffnonbonded.itp里面以后，那么[ atomtypes ]里面就有了两个opls_801  C801 ，而且参数是不一样的

十六烷基三甲基溴化铵阳离子的字段如下：

; GENERATED BY LigParGen Server

; Jorgensen Lab @ Yale University 

;

[ atomtypes ]

  opls_857  H857     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_814  C814    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_855  H855     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_824  H824     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_815  C815    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_804  C804    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_818  C818    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_848  H848     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_843  H843     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_836  H836     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_834  H834     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_810  C810    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_828  H828     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_860  H860     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_851  H851     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_812  C812    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_802  C802    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_827  H827     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_809  C809    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_806  C806    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_822  H822     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_807  C807    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_859  H859     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_838  H838     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_830  H830     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_821  H821     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_842  H842     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_820  H820     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_837  H837     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_829  H829     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_831  H831     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_853  H853     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_856  H856     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_832  H832     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_858  H858     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_805  C805    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_846  H846     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_811  C811    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_823  H823     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_819  C819    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_861  H861     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_826  H826     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_835  H835     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_841  H841     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_825  H825     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_816  C816    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_833  H833     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_839  H839     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_817  C817    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_852  H852     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_801  C801    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_808  C808    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_850  H850     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_840  H840     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_849  H849     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_813  C813    12.0110     0.000    A    3.50000E-01   2.76144E-01

  opls_800  N800    14.0070     0.000    A    3.25000E-01   7.11280E-01

  opls_847  H847     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_844  H844     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_845  H845     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_854  H854     1.0080     0.000    A    2.50000E-01   1.25520E-01

  opls_803  C803    12.0110     0.000    A    3.50000E-01   2.76144E-01





水杨酸钠阴离子itp中[ atomtypes ]字段如下：



; GENERATED BY LigParGen Server

; Jorgensen Lab @ Yale University 

;

[ atomtypes ]

  opls_804  C804    12.0110     0.000    A    3.55000E-01   2.92880E-01

  opls_813  H813     1.0080     0.000    A    2.42000E-01   1.25520E-01

  opls_807  C807    12.0110     0.000    A    3.55000E-01   2.92880E-01

  opls_803  C803    12.0110     0.000    A    3.55000E-01   2.92880E-01

  opls_811  H811     1.0080     0.000    A    2.42000E-01   1.25520E-01

  opls_810  H810     1.0080     0.000    A    2.42000E-01   1.25520E-01

  opls_808  O808    15.9990     0.000    A    2.96000E-01   8.78640E-01

  opls_805  C805    12.0110     0.000    A    3.55000E-01   2.92880E-01

  opls_802  C802    12.0110     0.000    A    3.55000E-01   2.92880E-01

  opls_809  O809    15.9990     0.000    A    2.96000E-01   8.78640E-01

  opls_806  O806    15.9990     0.000    A    3.12000E-01   7.11280E-01

  opls_814  H814     1.0080     0.000    A    0.00000E+00   0.00000E+00

  opls_812  H812     1.0080     0.000    A    2.42000E-01   1.25520E-01

  opls_800  C800    12.0110     0.000    A    3.55000E-01   2.92880E-01

  opls_801  C801    12.0110     0.000    A    3.55000E-01   2.92880E-01

### 128 楼

牧生 发表于 2021-7-7 21:32

请教一下，我使用LigParGen得到的两种物质的itp，然后做两种物质在水中混合的模拟，两种物质[ atomtypes ] ...

最好直接问作者，按理说不应该如此

### 129 楼

牧生 发表于 2021-7-7 21:32

请教一下，我使用LigParGen得到的两种物质的itp，然后做两种物质在水中混合的模拟，两种物质[ atomtypes ] ...

本来就是随机分配原子类型和数据的，如果有两种不同的分子同时使用该服务器，必然有可能原子类型名称相同而后面的非键参数不同，甚至有时候像你这种原子类型相同元素不同的也会出现。所以如果多种分子都用该服务器产生top，就必须自己改原子类型名称区分

### 130 楼

本帖最后由 牧生 于 2021-7-9 13:39 编辑 

lyj714 发表于 2021-7-8 13:00

本来就是随机分配原子类型和数据的，如果有两种不同的分子同时使用该服务器，必然有可能原子类型名称相同 ...

非常感谢大佬的回答。

我已经重新修改了，这里以十六烷基三甲基溴化铵（CTAB）和对苯磺酸钠（STS）为例

将两种物质的opls_xxxx已经重新编号，确保二者里面不会有重复，如

CTAB中的原子编号，全部保持不变

opls_800        N800

opls_801        C801

opls_802        C802

……

opls_861        H861



但修改STS中的编号，将本来的以C800开始编号的，改成870开始

opls_800  C800    →     opls_870  C870

opls_801  C801    →     opls_871  C871

……

opls_817  H817    →     opls_887  H887

这样，既保证两种物质的opls_XXXXX不重复，也与ffnonbonded.itp里面本来已有的opls_XXXXX不重复。





现在有个小问题，就是atom这一列里面的如果重复，那么对结果有没有影响

如CTAB的[ atoms ]内容为

[ atoms ]

;   nr       type  resnr residue  atom   cgnr     charge       mass  

     1   opls_800      1    CTAB   N00      1    -0.0487    14.0070 

     2   opls_801      1    CTAB   C01      1    -0.1513    12.0110 

     3   opls_802      1    CTAB   C02      1    -0.1509    12.0110 

     4   opls_803      1    CTAB   C03      1    -0.1522    12.0110 

……



而修改后的STS的[ atoms ]内容为

nr       type  resnr residue  atom   cgnr     charge       mass

 1   opls_870      1    STS    C00    1    -0.0787    12.0110 

 2   opls_871      1    STS    C01    1    -0.1773    12.0110 

 3   opls_872      1    STS    C02    1    -0.0478    12.0110 

 4   opls_873      1    STS    C03    1    -0.2502    12.0110 



这个红色字体部分是重复的。如果我把STS中的[ atoms ]列修改了别的，



opls_870      1    STS   C00   →   C870

opls_871      1    STS   C01   →   C871  

opls_872      1    STS   C02   →   C872   





但最终在能量最小化的时候就会提示

Warning: atom name 6201 in CTAB.top and CTAB_solv.gro does not match (C870 - C00)

Warning: atom name 6202 in CTAB.top and CTAB_solv.gro does not match (C871 - C01)

Warning: atom name 6203 in CTAB.top and CTAB_solv.gro does not match (C872 - C02)

Warning: atom name 6204 in CTAB.top and CTAB_solv.gro does not match (C873 - C03)

……

程序会自动还是使用STS中的C00，C01，并不是识别我自己写的C870，C871



那么，我需要请教的问题在于，[ atoms ]列里面相同的字符，会对结果造成影响吗？

### 131 楼

牧生 发表于 2021-7-9 13:30

非常感谢大佬的回答。

我已经重新修改了，这里以十六烷基三甲基溴化铵（CTAB）和对苯磺酸钠（STS）为例

 ...

不同分子，原子名称可以一样啊，这又不影响md，只要分子顺序是对应的不就完事了。

### 132 楼

请问社长，LigParGen网站用.mol文件生成葫芦脲分子（原子数126个）的参数一直加载超时（尝试了不同的浏览器），不能成功生成，该怎样解决呢

### 133 楼

CGenFF生成的拓扑文件中原子电荷是怎么指定的呢？是否需要调整为其他形式的原子电荷

### 134 楼

喵星大佬 发表于 2021-8-9 15:06

CGenFF生成的拓扑文件中原子电荷是怎么指定的呢？是否需要调整为其他形式的原子电荷

CGenFF在线程序中，原子电荷是根据Automation of the CHARMM General Force Field (CGenFF) II-Assignment of Bonded Parameters and Partial Atomic Charges文中提出的类似MMFF94的extended bond-charge increment方法瞬间产生的。校正参数依赖于成键方式，是向CGenFF力场原文中参数化过的分子（昂贵的重现分子与水相互作用能）的原子电荷尽可能贴近来优化的。这种做法可以接受，但不如力场原文中重现分子与水相互作用能的那种方式理想，对于一些体系我看大概率不如替换成RESP2(0.5)电荷理想。

### 135 楼

liushu 发表于 2021-8-9 14:56

请问社长，LigParGen网站用.mol文件生成葫芦脲分子（原子数126个）的参数一直加载超时（尝试了不同的浏览器 ...

问作者，或者用其它产生拓扑文件的工具，或者干脆别用OPLS-AA力场，用acpype产生GAFF力场的

### 136 楼

"另外也会输出_OPLS后缀的基于OPLS力场的文件，但属于实验性质不建议用"

请教老师是OPLS力场不如GAFF精确吗。我看很多文献做离子液体都是用的opls而不是GAFF

### 137 楼

sun666 发表于 2021-9-10 14:10

"另外也会输出_OPLS后缀的基于OPLS力场的文件，但属于实验性质不建议用"

请教老师是OPLS力场不如GAFF精确 ...

这句话的意思是，acpype得到的_OPLS文件，属于acpype这个脚本的实验性质结果，不建议用。



如果要使用opls力场，当然首选Ligpargen来得到itp文件。

### 138 楼

请问acpype生成的原子上限是多少啊，谢谢~~

### 139 楼

一条君 发表于 2021-12-18 15:31

请问acpype生成的原子上限是多少啊，谢谢~~

没明确限制

只要让acpype不自动优化、不产生原子电荷，几百个原子没问题

### 140 楼

yaochuang 发表于 2014-12-20 16:01

谢谢sob老师！

GOOD

### 141 楼

其实最好用的是charmm-GUI，蛋白/膜/小分子复合物各种乱七八糟的可以一次性生成，还有Amber(包括19SB和各种相关力场，GAFF/GAFF2，lipid17等)，charmm36m/charmm36(同样包括CGenFF等)，OPLS-AA可选

### 142 楼

喵星大佬 发表于 2022-5-19 18:55

其实最好用的是charmm-GUI，蛋白/膜/小分子复合物各种乱七八糟的可以一次性生成，还有Amber(包括19SB和各种 ...

没有edu邮箱不给注册，是我甚不喜欢这东西的原因

### 143 楼

使用sobtop(linux版本)的几点意见:

系统: Centos 7.9

1. sobtop需要输入绝对路径,如/home/xxx/xxxx,如果装的位置路径很长,挺麻烦的,(尝试将sobtop添加至环境变量可以解决这问题)

2. sobtop添加到环境变量后,不能在任意环境下使用,提示缺乏sobtop文件夹中的其他几个文件;

3. 输入问题,按Tab键不能补全,按向上箭头不能返回历史输入;

### 144 楼

boqiang 发表于 2022-9-16 08:23

使用sobtop(linux版本)的几点意见:

系统: Centos 7.9

1. sobtop需要输入绝对路径,如/home/xxx/xxxx,如果 ...

2 网页里明确说了，当前版本必须在sobtop目录下运行

3 补全是shell提供的特性，不是Fortran提供得了的

### 145 楼

@sobereva 老师好，请问用Sobtop处理得到gro、top、itp文件后，怎么去选择力场和水模型并建立盒子呀

### 146 楼

深爱小李 发表于 2022-9-24 13:33

@sobereva 老师好，请问用Sobtop处理得到gro、top、itp文件后，怎么去选择力场和水模型并建立盒子呀

http://sobereva.com/soft/Sobtop#FAQ1

### 147 楼

各位老师好，想请问如何生成opls-ua力场的小分子拓扑结构用于gromacs？

### 148 楼

高处裹棉被 发表于 2022-9-27 11:59

各位老师好，想请问如何生成opls-ua力场的小分子拓扑结构用于gromacs？

OPLS-UA已经过时了，干嘛用这个

### 149 楼

sobereva 发表于 2022-9-28 09:00

OPLS-UA已经过时了，干嘛用这个

谢谢老师解答，



因为做的是超临界体系下模拟（比如超临界甲醇），搜到的文献有用OPLS-UA力场下模型的，



如果没有专门软件的话是不是得自己按照文献内容扣，然后主top文件规则用opls力场下的？

### 150 楼

高处裹棉被 发表于 2022-9-28 10:10

谢谢老师解答，



因为做的是超临界体系下模拟（比如超临界甲醇），搜到的文献有用OPLS-UA力场下模型的 ...

联合原子力场模型下的甲醇结构极其简单，自己手写itp也不费事

### 151 楼

请问sob老师，ATB生成带苯环的分子，苯环是不是没法用联合原子模型。

### 152 楼

GoldenBaby 发表于 2023-2-3 16:23

请问sob老师，ATB生成带苯环的分子，苯环是不是没法用联合原子模型。

如果没返回来联合原子模型的拓扑文件那就不行

### 153 楼

sobereva 发表于 2014-12-18 19:09

自己找的小分子不要用pdb2gmx来产生拓扑文件，用我文中的途径产生.itp文件然后include到主.top文件是最好的 ...

老师我是小白，我想通过MD计算锂离子电池电解液锂离子扩散系数还有模拟锂离子溶剂化结构。

目前我做的流程是1.分别把溶剂分子，锂离子，锂盐阴离子分别优化(锂离子直接计算单点)，频率，得到力常数。2.计算上述结构的RESP电荷。3.通过sobtop得到以上各结构的itp文件。4.通过packmol建立以上结构混合的盒子。

请问老师，接下来我怎样才能得到盒子对应的TOP文件和gro文件，并让MD跑起来呢

### 154 楼

Smes 发表于 2023-3-28 23:41

老师我是小白，我想通过MD计算锂离子电池电解液锂离子扩散系数还有模拟锂离子溶剂化结构。

目前我做的流 ...

一般没必要算力常数，仔细看http://sobereva.com/soft/Sobtop/#FAQ11



packmol构建模拟体系的结构的pdb文件，直接可以作为grompp的输入文件，不需要刻意转成gro



整个体系的top文件自己手写，很简单。注意[molecules]和整体结构文件里的分子数目和顺序必须对应。

### 155 楼

牧生 发表于 2021-7-9 13:30

非常感谢大佬的回答。

我已经重新修改了，这里以十六烷基三甲基溴化铵（CTAB）和对苯磺酸钠（STS）为例

 ...

老师好，根据你的做法，已经成功可以继续往下运行了，但是出现了好多warning，如图1所示，这些是不是可以直接用-maxwarn 跳过。

同时又出现了新的问题，如图2所示，请问这种问题老师有没有遇到过，该怎么解决？

### 156 楼

奥利给 发表于 2023-6-7 21:37

老师好，根据你的做法，已经成功可以继续往下运行了，但是出现了好多warning，如图1所示，这些是不是可以 ...

我以前用过opls，但现在已经不推荐opls力场了。amber+gaff力场才是我的首选了，用Multiwfn计算RESP电荷加入小分子里面，才是最最正规的做法。



你的提示里面，原子类型有重复，你自己看一下，是不是参数都一样的，如果一样，就可以忽略，如果不一样，就要自己改编号了。。电荷如果偏离实际的净电荷很少，可以忽略该提示，或者手动把这些电荷分配到别的原子上去。

### 157 楼

牧生 发表于 2023-6-8 06:46

我以前用过opls，但现在已经不推荐opls力场了。amber+gaff力场才是我的首选了，用Multiwfn计算RESP电荷加 ...

感谢老师的回复，我还有三个问题需要老师帮忙解答一下

1.“是不是参数都一样的”    这地方我不理解，我是根据你的做法，把两个分子都放在一块了，然后分别编号，分别为opls_800-opls_896（顺序没有重新排列），opls_900-opls_942，只修改了前两列，这样做的话有问题吗？

2.itp文件的内容是否要放到top文件里面

3.我这个净电荷是0.005，是不是可以忽略了？如何手动分配电荷呀！

### 158 楼

奥利给 发表于 2023-6-8 10:41

感谢老师的回复，我还有三个问题需要老师帮忙解答一下

1.“是不是参数都一样的”    这地方我不理解，我 ...

因为LigPargen每次会给opls力场的atomtype重新编号，所以两个分子的原子类型可能编号相同，但是表示的含义不一样，一种办法就是你手动把编号全部改掉，比如把OPLS_***改成你的CE_***。另一种办法就是干脆用我们写的AuToFF（https://cloud.hzwtech.com/web/personal-space/auto-ff/all-atom）来生成拓扑文件。

Ligpargen生成的净电荷不为0主要是因为浮点数的数值误差引起的，这个你可以手动把这个0.005的电荷平均分配到几个电荷数较大的原子上面。

### 159 楼

slxc920113 发表于 2023-6-8 12:04

因为LigPargen每次会给opls力场的atomtype重新编号，所以两个分子的原子类型可能编号相同，但是表示的含 ...

感谢老师，用了老师推荐的生成拓扑文件，之前的问题都不会出现了

### 160 楼

sobereva 发表于 2014-12-18 19:09

自己找的小分子不要用pdb2gmx来产生拓扑文件，用我文中的途径产生.itp文件然后include到主.top文件是最好的 ...

请问老师，我的体系是蛋白+小分子复合物（对接得到），如果想构建小分子的拓扑文件，是不是将对接后的小分子结构(mol2格式)提取出来，然后放到sobtop里面产生拓扑文件呢？ 我看您sobtop教程里面的例子使用的是小分子用高斯优化后的结构

### 161 楼

crush 发表于 2024-7-31 18:02

请问老师，我的体系是蛋白+小分子复合物（对接得到），如果想构建小分子的拓扑文件，是不是将对接后的小 ...

是

sobtop指认GAFF参数不依赖于几何结构，仅依赖于连接关系

算RESP电荷与几何结构有关，看下文末尾的讨论

RESP拟合静电势电荷的原理以及在Multiwfn中的计算

http://sobereva.com/441（http://bbs.keinsci.com/thread-10880-1-1.html）

### 162 楼

sobereva 发表于 2024-8-1 01:25

是

sobtop指认GAFF参数不依赖于几何结构，仅依赖于连接关系

算RESP电荷与几何结构有关，看下文末尾的讨 ...

好的，谢谢老师

### 163 楼

@sobereva 

sob老师，请问ATB网站提交小分子任务后一直显示“Gateway Timeout”，这个问题怎么解决？

最近在使用ATB网站（Automated Topology Builder，https://atb.uq.edu.au/）为自己的小分子配体生成GROMACS拓扑文件。



将小分子的PDB文件上传后，任务一直处于处理中状态，等待超过10分钟仍未完成。最终页面刷新后出现“Gateway Timeout”错误，提示全文为：

“The gateway did not receive a timely response from the upstream server or application.”



1. 多次重新提交任务，问题依旧

2. 更换不同网络环境和浏览器（Chrome/Edge）

3. 尝试过不同时间段提交（包括凌晨）

4. 检查过小分子结构，原子数为31个，应在可接受范围内



1. 这是ATB服务器近期的问题，还是我的文件有特殊之处？

2. 目前是否有可用的替代方案（在线工具或本地软件），可以生成类似ATB质量的GROMACS拓扑文件？

### 164 楼

clh@17685395256 发表于 2026-5-16 12:59

@sobereva 

sob老师，请问ATB网站提交小分子任务后一直显示“Gateway Timeout”，这个问题怎么解决？

最 ...

但凡你看了第一楼超过10秒钟，你都能看到以下文字










202605161528069882..png (234.13 KB, 下载次数 Times of downloads: 36)

下载附件 Download



2026-5-16 15:28 上传 Uploaded

## 入库完整性评估

- 主帖全文收录
- 全部回复完整收录
