---
post_id: 490
title: 详谈Multiwfn产生ORCA量子化学程序的输入文件的功能
url: http://sobereva.com/490
date: '2019-06-17T06:47:00+08:00'
source_categories:
- Multiwfn
- 量子化学
- ORCA
primary_topic: Multiwfn
secondary_topics:
- ORCA
- 结构与文件格式
- 量子化学
academic_relevant: true
classification_reason: 标题是 Multiwfn 生成 ORCA 输入文件的功能，属于软件联用教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**注：本文内容对应的总是目前Multiwfn官网上最新的版本，不要用老版本Multiwfn**

**详谈Multiwfn产生ORCA量子化学程序的输入文件的功能**

On the function of generating ORCA input file in Multiwfn

文/Sobereva@[北京科音](http://www.keinsci.com/)

First release: 2019-Jun-23  Last update: 2025-Jun-17

## 1 简介

ORCA量子化学程序如今的用户越来越多，用户数仅次于Gaussian，不仅免费，而且有很多优点，例如支持很多Gaussian不支持的较重要方法，如wB97M-V和DLPNO-CCSD(T)，并且由于充分利用了RI技术，使得DFT、TDDFT的效率很高，这点在《大体系弱相互作用计算的解决之道》（http://sobereva.com/214）和《使用ORCA在TDDFT下计算旋轨耦合矩阵元和绘制旋轨耦合校正的UV-Vis光谱》（http://sobereva.com/462）我都已经说过。ORCA的安装方法见《量子化学程序ORCA的安装方法》（http://sobereva.com/451）。  
  
最强大的波函数分析程序Multiwfn也可以产生ORCA常见任务的输入文件，这个功能实用性极高。产生的关键词对于ORCA最新版都是合适的。随着ORCA的更新、用法的变动，Multiwfn也会相应地更新。最新版Multiwfn可以从主页http://sobereva.com/multiwfn免费获取。  
  
Multiwfn的这个功能并不是那种类似GaussView产生Gaussian输入文件的界面那样可以充分指定各种各样的选项，我觉得这种创建输入文件的工具对于ORCA用户而言并没什么实际意义。实际上有很大一批人用ORCA只是冲着ORCA的那些长处、特色功能去的，把ORCA作为Gaussian的补充，特别常用的任务类型就那么些，他们没精力也不需要把ORCA的所有细节都摸清楚。Multiwfn的这个产生ORCA输入文件的功能更像是把当前载入的体系的坐标套入特定类型任务的关键词模板里，之后用户只需把内存使用量、核数等参数简单地改一下，马上就可以跑，这显著拉低了ORCA的使用门槛，也使得ORCA用起来方便不少。  
  
如果你的研究中使用了Multiwfn创建了ORCA输入文件并给你带来了便利，希望在写文章的时候提及诸如The input files of ORCA program were prepared with the help of Multiwfn code并引用Multiwfn程序在刚启动时显示的Multiwfn原文，这是对Multiwfn此功能开发最好的支持。  
  
**特别注意**：本文介绍的功能仅仅能让你用ORCA做一些最最简单、最最常见的计算，以及在使用上提供一些便利。而正经用ORCA做计算的话是*必须*要花时间专门具体学习ORCA的用法和各种相关理论背景知识的，而*绝对*不能稀里糊涂把ORCA当黑箱用！否则一定会踩坑！非常推荐参加**北京科音高级量子化学培训班（**[**http://www.keinsci.com/KAQC**](http://www.keinsci.com/KAQC)**）**，里面专门有一节用300多页幻灯片对ORCA的使用进行极度系统的讲解并给出大量实例和各种我长期总结的使用经验，并且还在其它不同小节中还对于以下提到的RI/密度拟合/辅助基组、COSX、DLPNO、F12显式相关、STEOM、3c系列方法、sTD-DFT等关键知识有极为详细、具体的介绍和示例。只有完全掌握了这些知识才可能把ORCA用得得心应手、游刃有余，并且避免各种犯错误！

## 2 产生ORCA输入文件的界面

可以用任意Multiwfn支持的含有结构信息的文件作为Multiwfn的这个功能的输入文件，比如fch、molden、wfn、mol、mol2、pdb、xyz、gjf等。然后进入主功能100的子功能2中的选项12（更快速进入的方法是在主菜单里直接输入oi），输入要产生的ORCA输入文件的文件名，之后就会看到以下界面。注意随着Multiwfn的版本更新，这个界面也可能会有所变化，届时笔者也会相应地更新本文。

-100 Use template input file provided by user to generate new input file  
-11 Choose ORCA version compatibility, current: >ORCA 5.0  
-10 Set computational resources, core:   8 memory/core:  1000 MB  
-2 Toggle adding diffuse functions, current: No  
-1 Toggle employing implicit solvation model, current: No  
 0 Select task, current: Single point  
 1 B97-3c      1b r2SCAN-3c  
 2 RI-BLYP-D3(BJ)/def2-TZVP  
 3 RI-B3LYP-D3(BJ)/def2-TZVP(-f)     4 RI-B3LYP-D3(BJ)/def2-TZVP  
 5 RI-wB97M-V/def2-TZVP  
 6 RI-PWPB95-D4/def2-TZVPP       7 RI-PWPB95-D4/def2-QZVPP  
 6b RI-wB97X-2-D3(BJ)/def2-TZVPP     7b RI-wB97X-2-D3(BJ)/def2-QZVPP  
 6c RI-revDSD-PBEP86-D4/def2-TZVPP   7c RI-revDSD-PBEP86-D4/def2-QZVPP  
 8 DLPNO-CCSD(T)/def2-TZVPP with normalPNO and RIJCOSX  
 9 DLPNO-CCSD(T)/def2-TZVPP with tightPNO and RIJCOSX  
 10 CCSD(T)/cc-pVTZ  
 11 CCSD(T)-F12/cc-pVDZ-F12 with RI  
 12 Approximated CCSD(T)/CBS with help of MP2 (cc-pVTZ->QZ extrapolation)  
 13 DLPNO-CCSD(T)/CBS with RIJCOSX & tightPNO (def2-TZVPP->QZVPP extrapolation)  
 14 CCSD(T)/CBS (cc-pVTZ->QZ extrapolation)  
 20 sTD-DFT based on RI-wB97X-D3/def2-SV(P) orbitals  
 22 TDDFT RI-PBE0/def2-SV(P)  
 23 TDDFT RI-RSX-QIDH/def2-TZVP     231 TDDFT RI-DSD-PBEP86/def2-TZVP  
 24 EOM-CCSD/cc-pVTZ                 25 STEOM-DLPNO-CCSD/def2-TZVP(-f)

上述选项里，从1开始都是最常用的ORCA计算级别，20之前的都是基态计算任务，从20开始的都是激发态计算任务，都是序号越大精度越高但耗时也越高。选了之后就会生成ORCA输入文件，关键词是相应级别计算时最恰当的。之后用户可以再根据实际需要把输入文件里的基组、核数（%pal nprocs后面的值）、内存使用量（%maxcore后面的值）改成实际情况。

由于ORCA不同大版本的情况不同，某些关键词写法相差甚大，为了兼容性考虑，界面里专门留了个选项-11可以用来切换ORCA版本。默认对应的是最新的ORCA版本。

选择计算级别前，可以先用选项0选择任务类型。默认是单点，也可以选优化极小点、振动分析、优化极小点+振动分析、优化过渡态+振动分析、分子动力学、考虑counterpoise校正算结合能。对于振动分析任务，关键词会自动加上tightSCF来使用更严格的SCF收敛限（而对于优化任务ORCA默认就是用tightSCF）。分子动力学任务默认设置对应的是控温在298.15 K下用0.5 fs步长模拟500步。

默认不使用溶剂，如果想用SMD溶剂模型表现溶剂环境，可以选择选项-1，然后输入溶剂名，之后导出的输入文件里就带着溶剂模型关键词了。ORCA直接支持的SMD溶剂名详见手册（一搜1-HEXANOL就可以跳到对应的页）。若在这个选项里输入c，也可以用CPCM溶剂模型、自定义溶剂。

如《谈谈弥散函数和“月份”基组》（<http://sobereva.com/119>）中所述，很多情况用弥散函数是必须的，比如阴离子体系的单点等。如果你想把基组改成带弥散函数的版本，就选择一次选项-2将其状态切换为Yes。此时cc-pVnZ系列基组都会被改为aug-cc-pVnZ，def2系列基组都会被改为ma-def2系列，不熟悉此基组的话见《给ahlrichs的def2系列基组加弥散的方法》（<http://sobereva.com/340>）。与此同时，辅助基组也会改成恰当的。对于ma-def2系列，由于没有标配的辅助基组，所以会自动用autoaux关键词来自动构建。仅B97-3c、r2SCAN-3c和CCSD(T)-F12/cc-pVDZ with RI没法加弥散函数。

如果你载入进Multiwfn的文件是比如fch、wfn、molden这样带有波函数信息的，那么原本波函数对应的电荷和自旋多重度是多少，则产生的ORCA输入文件里的值也是多少。如果载入的是诸如xyz、pdb这样只含有结构信息的文件，那么别忘了需要根据实际情况自己改一下电荷和自旋多重度。

注意有些方法和任务类型之间不兼容，比如对于ORCA 5.0版而言，PWPB95-D3(BJ)没有解析梯度而无法直接用于几何优化任务。也有些方法本身可以用于优化，比如TDDFT，但使用了SMD溶剂模型后就不再支持。这种情况请大家自行手动调整输入文件里的关键词，比如需要改用数值梯度、数值Hessian的自己分别写上numgrad、numfreq

输入文件里的%maxcore控制ORCA并行计算时每个进程用的内存量（MB）的上限。因此比如你想8核并行，机子有32GB物理内存，若扣除操作系统、后台任务占的内存，假设剩30GB（约30000MB），那么maxcore不应超过30000/8=3750，但鉴于ORCA计算时进程实际使用的内存量上限往往会超过maxcore，因此为保险起见此时maxcore建议设为3000。计算使用的CPU核数、maxcore设置既可以自己编辑Multiwfn产生的ORCA输入文件，也可以直接在当前界面里用选项-10修改，默认的核数与Multiwfn的settings.ini里的nthreads参数等同。

Multiwfn产生的ORCA输入文件里都带着noautostart miniprint关键词。ORCA会自动试图从当前目录下与当前任务同名的gbw里读取结构和波函数作为初猜，noautostart代表要求不这样干。miniprint代表避免输出一些对普通用户没什么意义的中间信息，且也不自动做布居分析，因为ORCA默认做的布居分析的输出会导致输出文件的信息量巨大，而这些信息没太大意义而且格式还不好读。真想要做布居分析讨论电子结构，随时可以用Multiwfn基于ORCA产生的molden文件来实现，又快又方便信息又容易读，见《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）以及Multiwfn手册4.7节的布居分析例子。

此界面里有个选项-100，选了之后用户要提供一个ORCA模板文件，其中包含实际计算要用的所有设置，只不过坐标部分写成[geometry]，Multiwfn会将这部分替换为当前体系的坐标来产生ORCA输入文件。通过这个功能可以完全自定义地创建ORCA输入文件，还可以通过自写简单的脚本实现诸如把一大批xyz文件转化为带有特殊关键词的ORCA输入文件。一个模板文件的例子如下，用来产生DSD-BLYP双杂化泛函级别的自然轨道（算完后产生的以.mp2nat为后缀的文件可自行改成.gbw后缀，然后就可以用orca_2mkl转成.molden输入文件，之后可以载入Multiwfn做波函数分析）。  
! DSD-BLYP def2-TZVP tightscf miniprint  
%maxcore  6000  
%pal nprocs   10 end  
%mp2  
density relaxed  
NatOrbs true  
end  
* xyz   0   1  
[geometry]  
*

## 3 使用Multiwfn产生ORCA输入文件的简单例子

此例我们要用ORCA对甲醇在B97-3c级别下优化，之后用wB97M-V/def2-TZVP算单点，算单点时使用SMD模型表现乙醇环境。

首先用GaussView（或其它建模程序）画个甲醇，保存为gjf或mol或mol2或pdb文件，然后载入启动Multiwfn，载入此文件，依次输入  
100  //其它功能，Part 1  
2   //导出文件、产生量化程序输入文件  
12  //产生ORCA输入文件  
opt.inp   //输出的文件名  
0  //选择任务类型  
2  //优化  
1  //B97-3c  
现在当前目录下出现了opt.inp，恰当设置里面的maxcore和nprocs，然后用ORCA运行之。

算完后当前目录下出现了opt.xyz，此为优化后的结构文件，将之载入Multiwfn，依次输入  
100  //其它功能，Part 1  
2   //导出文件、产生量化程序输入文件  
12  //产生ORCA输入文件  
SP.inp   //文件名  
-1  //启用SMD溶剂模型  
ethanol  //溶剂名  
5  //RI-wB97M-V/def2-TZVP  
然后将当前目录下得到的SP.inp再次用ORCA运算即可。

在《Simulating UV-Vis and ECD spectra using ORCA and Multiwfn》（<http://sobereva.com/485>）一文中，笔者还演示了使用了Multiwfn创建ORCA输入文件，然后通过ORCA做TDDFT计算，最后用Multiwfn产生电子光谱的全过程。在《基于ORCA量子化学程序对分子做优化、振动分析、观看红外光谱、观看轨道的简单演示》（<https://www.bilibili.com/video/av59599938>）视频中，笔者演示了利用ORCA结合Multiwfn等程序，对有机小分子做一系列最常见的计算任务的基本操作。

## 4 计算级别简介和关键词解读

下面解释一下前述计算级别的特点以及解读一下相关的关键词，以便于读者准确地认识这些计算级别的特点、什么时候适合用什么级别、为什么笔者令Multiwfn支持这些级别，以及理解为什么关键词是那样定义的。

注意采用的基组没有一个是Pople系列基组，因为如《谈谈量子化学中基组的选择》（<http://sobereva.com/336>）提到的，这套基组对于较好精度的计算没有一个是划算的，而对于便宜的级别，这套基组又没有标配的给RI用的辅助基组，因此Pople系列基组在ORCA中几乎是摆设。DFT相关的计算笔者配的都是def2系列，这非常适合DFT，而对于后HF类型计算用的都是Dunning相关一致性基组，但实际上改用档次相当的def2系列基组也完全可以。

从ORCA 5.0开始，对于杂化泛函默认就会用RIJCOSX，因此下面关键词里面RIJCOSX对于ORCA >=5.0版做杂化泛函计算其实是多余的，但为了与老版本的兼容性考虑还是留着了。

### 4.1 基态计算

• B97-3c。关键词：B97-3c  
这是Grimme提出来的一个又便宜又快的组合式方法，用的是纯泛函，基组是方法直接内定的，还带了DFT-D3、SRB校正项。对于主族和过渡金属体系都适用。在ORCA里的耗时仅略高于RI-BLYP/def2-SVP一点点，但结果肯定整体更好。更详细介绍见《盘点Grimme迄今对理论化学的贡献》（<http://sobereva.com/388>）。我建议使用此方法去优化、计算大体系能量，或者粗略计算小体系用于初步筛选的目的，比如笔者在《gentor：扫描方式做分子构象搜索的便捷工具》（<http://bbs.keinsci.com/thread-2388-1-1.html>）的实例中就是这样做的。根据笔者自己的一些研究，用Intel 36核机子用B97-3c在真空下优化一个160原子的弱相互作用显著的有机体系，用了75步收敛，总共耗时才不到三个小时，比起在Gaussian下用算这种体系常用的B3LYP-D3(BJ)/6-311G*耗时低得多得多。之后在同样条件下用B97-3c对这个体系做振动分析，耗时三个半小时，也完全可以接受。使用B97-3c时不需要写与RI相关的关键词和指定辅助基组，因为默认就会用RIJ和恰当的辅助基组加速计算。

• r2SCAN-3c。关键词：r2SCAN-3c  
这是B97-3c的后继者，基于2020年末提出的r2SCAN泛函弄的-3c方法。耗时比之高了百分之几十，但精度全面提升了不少。因此如果不是特别穷的话，建议总是用r2SCAN-3c代替B97-3c。

• RI-BLYP-D3(BJ)/def2-TZVP。关键词：BLYP D3 def2-TZVP def2/J  
BLYP泛函平时用得不多，毕竟算有机体系精度远不如杂化泛函，但是BLYP这样的纯泛函在ORCA下利用RIJ方式加速库仑部分的计算后（记为RI-BLYP），对于稍大点的体系，速度能比Gaussian快一个数量级以上（振动分析除外）！。因此以BLYP为典型代表的纯泛函还是很有存在意义的。关键词里D3代表加上DFT-D3(BJ)色散校正，详见《DFT-D色散校正的使用》（<http://sobereva.com/210>）。对于算弱相互作用，根据GMTKN55测试集的测试，BLYP加上DFT-D3(BJ)后，在所有的“纯泛函-D3”里是顶尖的。def2-TZVP虽然是一个中等偏上的基组，在Gaussian里算是偏贵的，但是在ORCA里利用RIJ加速后其实挺便宜的。使用RIJ技术加速需要指定辅助基组，关键词中def2/J就代表使用对def2系列基组通用的用于RIJ目的的辅助基组。不需要特意写RIJ关键词，因为对纯泛函默认会使用RIJ。注意BLYP-D3(BJ)/def2-TZVP的耗时比B97-3c稍高，但精度未必比B97-3c好。特别是从ORCA 5.0开始支持了r2SCAN-3c后，RI-BLYP-D3(BJ)/def2-TZVP这个组合其实就没什么任何使用价值了。

• RI-B3LYP-D3(BJ)/def2-TZVP(-f)。关键词：B3LYP D3 def2-TZVP(-f) def2/J RIJCOSX  
由于B3LYP便宜、稳健、被支持广泛，虽然算热化学方面的精度已经严重落伍，但即便到现在还是被使用得最多的泛函，结合DFT-D色散校正后又令它的生命周期进一步延长，相关信息看《简谈量子化学计算中DFT泛函的选择》（<http://sobereva.com/272>）。对于B3LYP这样的杂化泛函，ORCA里可以用RIJK或RIJCOSX来加速，后者在ORCA里能用的特征更多，而且对于二、三十个原子以上的情况，通常RIJCOSX比RIJK明显更快，RIJCOSX关键词代表启用之。def2-TZVP(-f)是在def2-TZVP基组的基础之上把f极化函数阉割掉的结果，这可以显著节约时间，而对精度损失不算特别严重，此时尺寸与6-311G(2d,p)相仿佛。杂化泛函结合RIJCOSX的耗时显著高于纯泛函结合RIJ，因此RI-B3LYP即便结合def2-TZVP(-f)，耗时也比RI-BLYP/def2-TZVP高得多，且速度远胜于在Gaussian里的计算速度（Gaussian对杂化泛函不支持RI）。对于主族体系各方面计算以及弱相互作用计算而言，B3LYP-D3(BJ)比上述的BLYP-D3(BJ)好是肯定的，因此是否适合使用B3LYP-D3(BJ)应当自行掂量。

• RI-B3LYP-D3(BJ)/def2-TZVP。关键词：B3LYP D3 def2-TZVP def2/J RIJCOSX  
同上，只不过基组变成了完整的def2-TZVP

• RI-wB97M-V/def2-TZVP。关键词：wB97M-V def2-TZVP def2/J RIJCOSX strongSCF  
根据Phys. Chem. Chem. Phys., 19, 32184 (2017)、Mol. Phys., 115, 2315 (2017)、J. Chem. Theory Comput., 15, 3610 (2019)等测试，ωB97M-V在除了双杂化泛函以外的泛函中，无论算主族还是含过渡金属的体系，无论算反应能、势垒还是弱相互作用，性能都是顶级的，在《简谈量子化学计算中DFT泛函的选择》我也提到了。虽然从ORCA 5.0开始支持了ωB97M-V的解析梯度，但没有解析Hessian，因此不便于做振动分析检验虚频情况，所以我不建议用这个泛函做优化，而且本身这个泛函也比B3LYP等更贵一些。另外，众所周知，几何优化耗时远高于单点计算，而几何优化用的级别可以比单点要低，因为几何优化结果对计算级别敏感度远低于能量计算，这点在《浅谈为什么优化和振动分析不需要用大基组》（<http://sobereva.com/387>）专门提了，因此推荐大家用相对便宜的B97-3c或比它更好也更贵的RI-B3LYP-D3(BJ)/def2-TZVP(-f)来优化结构，最后用RI-wB97M-V/def2-TZVP来算单点。对于ωB97M-V这样的非双杂化泛函而言，对于一般问题用def2-TZVP就已经够用了，要求更高的话也可以考虑def2-QZVPP。如果你要算弱相互作用能的话也推荐用def2-QZVPP，若结合counterpoise校正还能更好一点。由于ORCA的默认的SCF收敛限相对于wB97M-V的精度水平来说过于宽松了些，因此同时用了strongSCF来让能量收敛到更高精度。

值得一提的是虽然M06-2X很流行，很适合算主族体系，但在上面只字未提。这是因为M06-2X做几何优化方面比B3LYP-D3(BJ)优势并不明显，而耗时明显更高，对积分格点要求也高，还更难收敛。虽然M06-2X用于算主族体系的能量很不错，但是和ωB97M-V比又明显逊色，在速度上也没优势，故M06-2X在当前的ORCA中没多大用武之地。

• RI-PWPB95-D4/def2-TZVPP。关键词：PWPB95 D4 def2-TZVPP def2/J def2-TZVPP/C RIJCOSX tightSCF  
PWPPWPB95-D4在《简谈量子化学计算中DFT泛函的选择》中专门说了，是很稳健且精度很好的双杂化泛函，精度介于ωB97M-V和CCSD(T)档次之间。当前关键词令PWPB95-D4泛函的杂化泛函部分做SCF的过程中通过RIJCOSX加速来降低耗时，而在之后计算类似MP2部分的时候RI来显著降低耗时（只要用了RIJCOSX关键词，默认就会在MP2部分也用RI），这一步使用def2-TZVPP/C辅助基组。为了让SCF部分尽量准确从而得到数值层面较准确的PWPB95-D4的结果，因此用了tightSCF。笔者用Intel 36核服务器做过测试，对于168个原子的有机体系的单点，这样的计算级别耗时不到三个小时，耗硬盘也不多，而如果用Gaussian的话根本没戏，差不多80个原子就封顶了，还特别耗硬盘。对于66个原子的有机体系的单点，ORCA下用这个级别仅需六分钟就能算完。总的来说，RI-双杂化/def2-TZVPP用Intel三、四十核的服务器跑200原子以内的单点毫无压力。另外，如果你希望耗时更低的话，可以手动加上float关键词，代表通过单精度变量而非默认的双精度变量储存中间数据，耗时能节约一小半，而且还能省一倍硬盘。

• RI-PWPB95-D4/def2-QZVPP。关键词：PWPB95 D4 def2-QZVPP def2/J def2-QZVPP/C RIJCOSX tightSCF  
我之前在《谈谈量子化学中基组的选择》（<http://sobereva.com/336>）中说过，后HF、双杂化泛函对基组的要求显著高于普通泛函，因此为了充分发挥PWPB95-D4的潜力，如果你能接受更大计算量的话，推荐结合def2-QZVPP。对于66个原子的有机体系的单点，在Intel 36核服务器下ORCA下用这个级别用了30分钟算完。

• RI-wB97X-2-D3(BJ)/def2-TZVPP（RI-wB97X-2-D3(BJ)/def2-QZVPP与之类似）  
关键词：wB97X-2 D3 def2-TZVPP def2/J def2-TZVPP/C RIJCOSX tightSCF  
%method  
D3S6 0.547  
D3A1 3.520  
D3S8 0.0  
D3A2 7.795  
end  
ωB97X-2-D3(BJ)在PCCP, 20, 23175 (2018)的双杂化泛函横测当中表现出众（不过在算分子间弱相互作用的测试上表现一般）。ωB97X-2从ORCA 5.0开始支持，但支持的只是2009年当时提出的原版，其搭配的DFT-D3(BJ)色散校正参数在PCCP, 20, 23175 (2018)的补充材料里才给出，没有在ORCA里内置。因此Multiwfn产生的输入文件里如上所示自动用%method ... end字段补充了色散校正参数。

• RI-revDSD-PBEP86-D4/def2-TZVPP（RI-revDSD-PBEP86-D4/def2-QZVPP与之类似）  
关键词：revDSD-PBEP86-D4/2021 def2-TZVPP def2/J def2-TZVPP/C RIJCOSX tightSCF  
revDSD-PBEP86-D4在计算有机反应能以及弱相互作用能方面在现有的双杂化泛函里都是顶级的，建议对这类问题使用。

• DLPNO-CCSD(T)/def2-TZVPP with normalPNO and RIJCOSX。关键词：DLPNO-CCSD(T) normalPNO RIJCOSX def2-TZVPP def2/J def2-TZVPP/C tightSCF  
CCSD(T)普遍被认为是计算静态相关不是特别强的体系的金标准。DLPNO-CCSD(T)是ORCA中的黑科技，是一种对CCSD(T)的数值近似，可以把原本最多只能算得动不超过30原子的CCSD(T)的方法扩展到好几十甚至上百原子，精度和耗时通过此方法中的一些阈值参数来控制。ORCA里有LoosePNO、NormalPNO、TightPNO三种标准，越往后越贵，但结果也越接近CCSD(T)。LoosePNO就太烂了，不建议用，而NormalPNO较有实用价值。用NormalPNO的时候精度就已经显著超过revDSD-PBEP86-D4了，相对于CCSD(T)的误差通常在1 kcal/mol以内。DLPNO-CCSD(T)的HF计算部分可以用RIJCOSX方法来加速，这是为什么关键词里写了RIJCOSX，并且指定了def2/J辅助基组。def2-TZVPP/C辅助基组是用于DLPNO-CCSD(T)的电子相关部分计算的。顺带一提，在北京科音高级量子化学培训班（<http://www.keinsci.com/workshop/KAQC_content.html>）中专门有一节“低标度耦合簇方法”很详细讲授DLPNO相关方法以及LNO-CCSD(T)等其它低标度方法。

• DLPNO-CCSD(T)/def2-TZVPP with tightPNO and RIJCOSX。关键词：DLPNO-CCSD(T) tightPNO RIJCOSX def2-TZVPP def2/J def2-TZVPP/C tightSCF  
DLPNO-CCSD(T)结合tightPNO的时候，根据J. Chem. Theory Comput., 11, 4054 (2015)的测试（注意此文里有很多在耗时方面的严重误导性说法），与CCSD(T)的误差在1 kJ/mol的程度，几乎可认为没有差别。tightPNO的耗时比NormalPNO通常高几倍。在笔者的Intel 36核机子上，用当前级别计算66个原子的有机体系耗时约8小时，耗硬盘最多时候为120GB。如果你还想要更好的精度，建议将基组提升至def2-QZVPP，但也会贵非常多。如果不用RIJCOSX，即去掉RIJCOSX def2/J关键词，精度会有很轻微改进，但对较大的体系，SCF部分的耗时会增加许多。

• CCSD(T)/cc-pVTZ。关键词：CCSD(T) cc-pVTZ tightSCF  
这就是原版的CCSD(T)/cc-pVTZ，没什么好说的。

注：上述几个计算级别中，如果有cc-pVTZ不支持的元素，把cc-pVTZ替换为质量差不多的def2-TZVPP。如果提示某些元素没有对应的辅助基组，把cc-pVTZ cc-pVTZ/JK cc-pVTZ/C替换为def2-TZVPP def2/JK def2-TZVPP/C。

• CCSD(T)-F12/cc-pVDZ-F12 with RI。关键词：CCSD(T)-F12/RI cc-pVDZ-F12 cc-pVDZ-F12-CABS cc-pVTZ/C tightSCF  
F12是显式相关方法，可以结合到CCSD(T)、MP2等方法上。CCSD(T)-F12结合cc-pVDZ-F12基组时，耗时显著低于CCSD(T)/cc-pVQZ，但精度则与之接近。因此如果你需要CCSD(T)/cc-pVQZ档次的数据但算得很吃力的话，当前级别是个很好的选择。计算过程中利用RI可以进一步显著节约时间，所以写了/RI。顺带一提，北京科音高级量子化学培训班（<http://www.keinsci.com/workshop/KAQC_content.html>）专门有一节“显式相关计算”用30多页幻灯片非常完整深入讲F12这类计算。

• Approximated CCSD(T)/CBS with help of MP2 (cc-pVTZ->QZ extrapolation)。关键词：ExtrapolateEP2(3/4,cc,MP2) tightSCF  
我在《谈谈能量的基组外推》（<http://sobereva.com/172>）中专门介绍过基组外推的概念，这也叫CBS外推，即假定外推到了完备基组极限(CBS)。CCSD(T)档次下最常用的外推就是基于cc-pVTZ和cc-pVQZ来外推，可以免费地得到更高一个档次基组的结果，即大约cc-pV5Z的结果，这种计算方式常见于各种高精度小体系的研究文章当中。直接利用CCSD(T)结合cc-pVTZ和cc-pVQZ能量进行外推的话，后者耗时非常高，往往很难承受，因此可以借助MP2来进行“近似的外推”，即利用MP2/cc-pVTZ和QZ先外推出MP2/CBS相关能，然后CCSD(T)/CBS的相关能就近似可以估计为CCSD(T)/cc-pVTZ + MP2/CBS - MP2/cc-pVTZ，这就避免了直接做非常昂贵的CCSD(T)/cc-pVQZ计算了。这个近似精度很好，一般也就带来0.1 kcal/mol左右程度的误差，笔者在《各种后HF方法精度简单横测》（<http://sobereva.com/378>）中专门做过测试，有兴趣可以看看。ORCA提供了ExtrapolateEP2关键词，可以直接实现上述CCSD(T)结合MP2的CBS外推。

其实如果将这里的CCSD(T)改为tightPNO的DLPNO-CCSD(T)，能以相近的精度算明显更大体系，但可惜这没法在目前的ORCA里通过一套关键词直接实现。

• DLPNO-CCSD(T)/CBS with RIJCOSX & tightPNO (def2-TZVPP->QZVPP extrapolation)。关键词DLPNO-CCSD(T) tightPNO Extrapolate(3/4,def2) def2-QZVPP/C RIJCOSX tightSCF  
• CCSD(T)/CBS (cc-pVTZ->QZ extrapolation)。关键词：CCSD(T) Extrapolate(3/4,cc) tightSCF  
ORCA里可以用Extrapolate关键词对任意后HF方法进行外推，以上两个级别就用了这点。一个是直接用CCSD(T)，算十个原子都已经极度吃力；另一个是便宜得多但结果也糙一些的DLPNO-CCSD(T) with tightPNO，同时为了节约SCF时间而用了RIJCOSX，之所以改用了def2，是因为辅助基组层面的原因

### 4.2 激发态计算

• sTD-DFT based on RI-wB97X-D3/def2-SV(P) orbitals  
关键词：wB97X-D3 def2-SV(P) def2/J RIJCOSX  
%tddft  
Mode sTDDFT  
Ethresh 7.0  
PThresh 1e-4  
PTLimit 30  
maxcore 6000  
end  
对于好几百个原子的很大体系的电子光谱计算，往往要算几百个态才够覆盖感兴趣的波长范围。用wB97X-D3/def2-SV(P)对这样大小的体系算单点能往往算得动，但是用TDDFT算这么多态往往太困难。此时可以用Grimme提出的sTD-DFT方法，此方法基于DFT计算求解的轨道，通过对TDDFT矩阵元进行高度近似，只需要非常少的计算量就可以算出大量激发态（sTDDFT与TDDFT的耗时关系有点像半经验方法与DFT的耗时关系）。但代价是精度有所降低，不过对于很大体系的粗放式研究来说够用了。sTD-DFT功能已被内置于ORCA中，上面的关键词就是先做RI-wB97X-D3/def2-SV(P)单点计算，再基于其轨道做sTD-DFT，可以算出激发能为7 eV以内的所有态（这是一般感兴趣的电子光谱能量范围）。用wB97X-D3泛函是因为根据Phys.Chem.Chem.Phys.,16,14408(2014)的测试，将它结合sTD-DFT来用对于大体系（通常有显著电子共轭）结果较理想。PThresh和PTLimit用于控制纳入考虑的组态函数的范围，不写它们的话会考虑所有组态函数，这对于大体系可能耗时较高，当前的PThresh和PTLimit设置可以避免这个问题，对精度的牺牲可忽略不计。注意sTD-DFT目前只能对单个结构做电子激发计算，而不能用于激发态优化、振动分析等目的。顺带一提，北京科音高级量子化学培训班（<http://www.keinsci.com/workshop/KAQC_content.html>）专门有一节“使用sTDA方法快速计算大体系电子光谱”用约40页幻灯片非常全面完整详细讲这类计算。

• TDDFT RI-PBE0/def2-SV(P)  
关键词：PBE0 def2-SV(P) def2/J RIJCOSX tightSCF  
%tddft  
nroots 10  
TDA false  
end  
这是用PBE0结合大小与6-31G*差不多的def2-SV(P)做TDDFT计算。PBE0是TDDFT计算激发态常用的泛函，但碰见大共轭体系建议改为CAM-B3LYP等，详见《乱谈激发态的计算方法》（<http://sobereva.com/265>）。def2-SV(P)对于计算中、大体系的电子光谱是很适合的，既不贵，精度也基本够用，如果有余力且希望结果更好建议把def2-SV(P)改为def2-TZVP(-f)或def-TZVP（关键词写为TZVP）。关键词里nroots 10代表计算10个激发态，当然需要根据实际情况进行调节，同Gaussian的TDDFT计算中的nstates，详见《Gaussian中用TDDFT计算激发态和吸收、荧光、磷光光谱的方法》（<http://sobereva.com/314>）。用tightSCF是为了降低数值层面的误差。

• TDDFT RI-DSD-PBEP86/def2-TZVP  
关键词：DSD-PBEP86 def2-TZVP def2/J def2-TZVP/C RIJCOSX tightSCF  
（用TDDFT RI-RSX-QIDH/def2-TZVP则把上面的DSD-PBEP86改为RSX-QIDH）  
%tddft  
nroots 10  
TDA false  
end  
ORCA是为数不多的支持双杂化泛函下做TDDFT的程序，此级别精度比普通泛函做TDDFT更高，但代价是耗时也明显更高。计算时应当同时指定/C辅助基组。根据JCTC, 17, 4211 (2021)的测试，在ORCA能用的双杂化泛函中DSD-PBEP86算局域激发和分子内电荷转移激发最好，在JCTC, 18, 1646 (2022)的图5和表2中体现RSX-QIDH是算分子间CT激发的首选，所以Multiwfn给了两个选项。用上述关键词用对一个47原子的有机体系做TDDFT计算，笔者在Intel 2*2696v3 36核机子上用不到20分钟算完，可见耗时毫不夸张，算稍大一些的体系也能算得动。

• EOM-CCSD/cc-pVTZ  
关键词：EOM-CCSD cc-pVTZ tightSCF  
%mdci  
nroots 3  
end  
EOM-CCSD计算激发态的精度算是很不错了，比TD-双杂化精度更高，也更稳健和普适，但耗时颇高，而且随算的态数增加总耗时迅速增加，因此主要适合的是小体系的低阶激发态的较高精度的研究。RI在EOM-CCSD计算时派不上用场，和Gaussian相比也没有显著优势。

• STEOM-DLPNO-CCSD/def2-TZVP(-f)  
关键词：STEOM-DLPNO-CCSD RIJCOSX def2-TZVP(-f) def2/J def2-TZVP/C tightSCF  
%mdci  
nroots 3  
end  
STEOM-CCSD方法的初衷是降低EOM-CCSD的耗时，但不应将STEOM-CCSD视为是EOM-CCSD的近似，而应当视为两种不同方法。二者精度差不多，而STEOM-CCSD对CT激发的结果往往比EOM-CCSD更好。EOM-CCSD明显算不动的体系STEOM-CCSD照样算不动，结合像样的基组时一般顶多也就用于二十多个原子。DLPNO技术与STEOM-CCSD的结合诞生的STEOM-DLPNO-CCSD则可以用于大得多的体系，在def2-TZVP(-f)这样的基组下甚至对超过60个原子的体系也能算（但注意超级耗硬盘，没有好几个TB的剩余空间就别指望了）。
