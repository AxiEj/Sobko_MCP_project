---
post_id: 566
title: Multiwfn 3.7正式版隆重发布！
url: http://sobereva.com/566
date: '2020-08-14T15:55:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 波函数分析
academic_relevant: true
classification_reason: 标题是 Multiwfn 3.7 正式版发布消息，属于软件更新信息。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**Multiwfn 3.7正式版隆重发布！**

The official version of Multiwfn 3.7 is grandly released!

文/Sobereva @[北京科音](http://sobereva.com/multiwfn)  2020-Aug-14

## 1 前言

Multiwfn是极为流行、功能最全面的的量子化学波函数分析程序，被学术文章引用得越来越多（目前已被近70个国家的研究者共引用5600多次），用户数越来越庞大。Multiwfn的上个正式版3.6是2019年5月21日发布的，经过近一年有余的不懈发展、改进和完善，Multiwfn 3.7正式版终于正式发布！目前已经可以在官网上<http://sobereva.com/multiwfn>下载。如果下载速度太慢，大陆地区用户可以通过百度网盘下载：<http://pan.baidu.com/s/1dFgeghF>，大陆地区以外用户可以通过MEGA网盘下载：<https://mega.nz/#F!HVcjECZS!rGG6dCO57AwpdCgYaQ3apg>。

近一年来Multiwfn更新极度频繁，带(dev)后缀的开发版在Multiwfn官网上甚至有时候一天就更新两、三次。各种最新改进始终体现在官网上的update history页面里，到今日3.7正式版发布为止，相对于3.6版的各种新功能和改进合计已经有近140条，可以说再次有了飞跃性的进步。强烈建议所有Multiwfn用户立刻更新到3.7版！不仅功能更多，而且很多功能变得更易用、效率更高，还修正了不少bug。

随着Multiwfn程序的进步，手册也在不断地扩充、完善，为此花费了极大的精力。3.6版手册是717页，而3.7正式版的手册已达900页！虽然手册很庞大，但新用户可以从可执行文件包里的Multiwfn quick start.pdf文档中快速找到学习自己要做的分析应当查看的手册的章节号。

3.7版的可执行文件包里加入了How to cite Multiwfn.pdf文档，特意详细说明了使用Multiwfn发表文章时应当引用的文章。Multiwfn程序永远免费，恰当引用Multiwfn及其作者的相关工作是对Multiwfn程序发展最大的支持。另外，专门介绍使用Multiwfn做刘述斌教授提出的各种信息论相关的量的文档已发布，见《使用Multiwfn计算各种与信息论相关的量（information-theoretic quantities）》（<http://sobereva.com/537>）。

顺带一提，Multiwfn的入门非常容易，不熟悉Multiwfn者建议参看《Multiwfn FAQ》（<http://sobereva.com/452>）和《Multiwfn入门tips》（<http://sobereva.com/167>）。预计今年11月左右，将会在北京举办“第六届量子化学波函数分析与Multiwfn程序培训班”，具体通知会在培训前一个月发布在北京科音官网（<http://www.keinsci.com>）和Multiwfn程序主页上，欢迎关注！通过这个5天的培训，参加者可以一次性彻底学懂各种波函数分析方法的思想、原理、应用以及在Multiwfn、NBO等程序中实现相应分析的操作，将会量子化学研究如虎添翼，明显更容易做出更高档次的研究成果。培训内容见此链接：<http://www.keinsci.com/workshop/WFN_content.html>。

预计Multiwfn下个大版本(3.8)中主要将加入的一个功能是比较流行的自然布居分析（NPA），与此同时自然原子轨道（NAO）也将可以由Multiwfn直接产生。届时，诸如AdNDP、Wiberg键级分解为原子轨道相互作用、NAOMO轨道成分分析、基于NAO的AV1245指数和多中心键级等各种依赖于NAO的功能将可以不依赖于NBO程序而独立运行，这将给广大用户带来极大的便利，尤其是对于使用Gaussian以外程序的量子化学研究者而言。

如果在使用Multiwfn中遇到问题、发现bug，欢迎在计算化学公社论坛论坛下属的Multiwfn分区（<http://bbs.keinsci.com/wfn>）或Multiwfn英文论坛（<http://sobereva.com/wfnbbs>）中反馈。

## 2 主要的新功能和改进

## 2.1 新功能

相对于3.6版新加入的功能如下：

支持了NMR谱的绘制，直接支持Gaussian和ORCA的NMR任务的输出文件，对于其它程序也可以自行写为通用的输入文件形式，见手册3.13.5节的介绍和4.11.10节的例子。远比GaussView绘制NMR灵活强大得多。

支持了卢天提出的IGM under Hirshfeld partition of actual molecular density （IGMH，待发表）方法可视化和定量研究弱相互作用。此方法比起IGM图像效果好得多，而且物理意义更严格，而且基于真实电子密度。见手册3.23.6节的介绍以及4.20.11节的例子。

支持了隧道扫描显微镜(STM)的绘制功能，见《使用Multiwfn模拟扫描隧道显微镜(STM)图像》（<http://sobereva.com/549>）。

支持了单位球面表示法和矢量表示法展现（超）极化率，对于研究（超）极化率的各向异性极为有益，介绍和应用实例见《使用Multiwfn通过单位球面表示法图形化考察（超）极化率张量》（<http://sobereva.com/547>）。

支持了轨道权重福井函数和双描述符的计算，对于考察前线轨道（近）简并体系的反应位点极有价值，见《通过轨道权重福井函数和轨道权重双描述符预测亲核和亲电反应位点》  
（<http://sobereva.com/533>）。

支持了J. Phys. Chem. A, 124, 339 (2020)提出的键级密度（BOD）和自然适应性轨道（NAdO）分析，可以将离域化指数对应的共价作用区域图形化展现出来，以及以轨道方式进行展现，对于研究化学键很有帮助。详见《使用键级密度(BOD)和自然适应性轨道(NAdO)图形化研究化学键》（<http://sobereva.com/535>）。

支持了卢天提出的基于力场的范德华势分析方法，对于考察分子间相互作用极为有益。见《谈谈范德华势以及在Multiwfn中的计算、分析和绘制》（<http://sobereva.com/551>）。

支持了卢天提出的interaction region indicator（IRI，待发表）。此函数可以将化学键作用区域和弱相互作用区域同时展现出来，比具有同类功能的DORI函数明显图像效果更好，而且定义还简单得多。见手册3.23.8节的介绍和4.20.4节的例子。

支持了J. Phys. Chem. A, 124, 2090 (2020)中新提出的比常用的Parr亲电指数更严格的亲电指数ωcubic。介绍和计算方法见已更新的《使用Multiwfn超级方便地计算出概念密度泛函理论中定义的各种量》（<http://sobereva.com/484>）。

支持了卢天提出的轨道离域指数（ODI，待发表）定量衡量轨道离域程度，见《通过轨道离域指数(ODI)衡量轨道的空间离域程度》（<http://sobereva.com/525>）。

在空穴-电子分析功能中加入了卢天提出的两个新指数“空穴离域指数”和“电子离域指数”，这对于定量衡量空穴和电子的空间分布广度很有益。见更新过的《使用Multiwfn做空穴-电子分析全面考察电子激发特征》（<http://sobereva.com/434>）。

支持了可视化周期性体系中的孔洞的功能，还能计算自由体积，见《使用Multiwfn图形化展示分子动力学模拟体系中的孔洞、自由区域》（<http://sobereva.com/539>）。

支持了将原子径向电子密度非常精确、容易地拟合为一批Slater函数或一批Gauss函数的线性组合。看手册3.300.2节的介绍和4.300.2节的例子。

可以解析地计算体系的电偶极矩、四极矩、八极矩，输出信息非常丰富。见手册3.300.5节的介绍和4.300.5节的例子。

支持了计算特定片段的偶/多极矩，应用例子见《使用Multiwfn计算分子片段的偶极矩和复合物中单体的偶极矩》（<http://sobereva.com/558>）。

盆分析模块（主功能17）支持了轨道成份计算的功能。例如可以计算AIM盆、ELF盆等各种类型的盆对轨道的贡献，见手册4.8.6节的例子。

支持了卢天提出的分子极性指数（MPI，待发表）衡量分子的极性，极性和非极性表面积也可以一同给出。见《谈谈如何衡量分子的极性》（<http://sobereva.com/518>）。此方法已被应用于讨论18碳环的极性，见《一篇最全面、系统的研究新颖独特的18碳环的理论文章》（<http://sobereva.com/524>）。

支持了卢天提出的IBSIW (intrinsic bond strength index for weak interactions，待发表) 指数定量衡量弱相互作用强度，可基于IGM和IGMH分析计算，见手册3.23.5节的介绍。也支持了J. Phys. Chem. A, 124, 1850 (2020)中提出的intrinsic bond strength index (IBSI)定量衡量化学键强度。

支持了ChemPhysChem, 14, 3714 (2013)中提出的high ELF localization domain population and volume (HELP and HELV)方法表征孤对电子特征，见手册4.17.8节的例子。

支持了非常适合用于分子动力学模拟的RESP2原子电荷的计算。见《RESP2原子电荷的思想以及在Multiwfn中的计算》（<http://sobereva.com/531>）。

支持了Phys. Chem. Chem. Phys., 18, 11839 (2016)中提出的AV1245指数，以及J. Phys. Chem. C, 121, 27118 (2017)中提出的AVmin指数衡量大环的芳香性，见《使用Multiwfn计算AV1245指数研究大环的芳香性》（<http://sobereva.com/519>）和《衡量芳香性的方法以及在Multiwfn中的计算》（<http://sobereva.com/176>）。

支持了将Gaussian等程序做TDDFT电子激发计算中涉及的主要轨道跃迁和贡献百分比以非常简洁、紧凑的格式输出，便于考察电子激发特征、将数据放到文章补充材料中。见《使用Multiwfn便利地查看所有激发态中的主要轨道跃迁贡献》（<http://sobereva.com/529>）。

支持了PEOE（也称Gasteiger）原子电荷计算功能，可以瞬间对大体系完成计算，见手册3.9.17节的介绍和4.7.9节的例子。

AdNDP模块中加入了选项15，用于以NAO方式计算搜索出的AdNDP轨道的成份。

绘制光谱的功能（主功能11）中，极小点和极大点的具体位置、数值都可以自动在图上进行标注，见更新过的《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（<http://sobereva.com/224>）。

支持了绘制MO-PDOS态密度曲线的功能，此曲线可以描绘不同分子轨道对DOS曲线的贡献。见《使用Multiwfn绘制态密度(DOS)图考察电子结构》（<http://sobereva.com/482>）第6节的应用介绍和手册4.10.5节的例子。此方法也被应用于卢天等人的18碳环的研究文章中：Carbon, 165, 461 (2020)。

新加入了用户自定义函数-3，对应于基于3D cubic spline方法对格点数据进行插值产生的函数，比用户自定义函数-1对应的三线性插值明显更为光滑。

主功能100的主功能2支持了导出.mkl文件功能，结合ORCA自带的orca_2mkl工具，使得其它量子化学程序产生的波函数都可以给ORCA程序当初猜用，对于解决ORCA中出现SCF不收敛很有价值，详见《将Gaussian等程序收敛的波函数作为ORCA的初猜波函数的方法》（<http://sobereva.com/517>）。

主功能0的菜单栏的Tools分类中加入了非常方便的批量绘制轨道的功能，见视频演示：《使用Multiwfn方便快速地批量绘制轨道图形》（<https://www.bilibili.com/video/av69765564/>）。

支持了解析Gaussian的polar=gamma关键词输出的第二超极化率的功能，将其输出信息整理为非常易读的格式，而且还顺带输出一些重要的相关的量。见更新过的手册 3.200.7节和《使用Multiwfn分析Gaussian的极化率、超极化率的输出》（<http://sobereva.com/231>）。

主功能11绘制光谱时可以在光谱下方通过不同颜色的竖线标示不同类型跃迁的位置，以及通过竖线高度体现简并度，这使得光谱图的信息明显更为丰富。见此文第8节的示例：《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（<http://sobereva.com/224>）。

支持了第一超极化率的双能级分析和卢天提出的三能级分析，对于解释影响第一超极化率的本质因素很重要，见《使用Multiwfn对第一超极化率做双能级和三能级模型分析》（<http://sobereva.com/512>）。

支持了J. Phys. Chem. A, 118, 1150 (2014)中提出的基于电子密度等值面计算小分子的动力学直径的功能，见《使用Multiwfn计算分子的动力学直径》（<http://sobereva.com/503>）。

支持了对指定的链计算键长交替（BLA）、键级交替（BOA）、键角交替和二面角交替情况，这对于研究寡聚物、大环的共轭路径特征很有益。见《使用Multiwfn计算Bond length/order alternation (BLA/BOA)和考察键长、键级、键角、二面角随键序号的变化》（<http://sobereva.com/501>）。

支持了将密度差分解为各种类型轨道贡献，例如可以将福井函数分解为NBO轨道的贡献。这对于了解密度差的本质、揭示其化学意义很有益。见《使用Multiwfn考察分子轨道、NBO等轨道对密度差、福井函数的贡献》（<http://sobereva.com/502>）。

支持了计算超瑞利散射（HRS）相关的数据，对于经常研究非线性光学的人很有价值。见《使用Multiwfn计算与超瑞利散射(HRS)实验相关的量》（<http://sobereva.com/499>）。

支持了计算两套不同波函数中的轨道的模之间的重叠积分，见手册3.200.6节的介绍和例子。这可以方便地衡量比如二聚体中的两个分子间各个轨道间的重叠程度。

支持了基于数值格点方式计算库仑和交换积分的功能。见手册3.200.17节。

主功能100的主功能2支持了将格点数据导出为ParaView的.vti文件、将分子结构导出为.cml文件的功能，从而可以令格点数据连同分子结构通过强大的体数据观看程序ParaView进行作图。ParaView在可视化体数据方面的强大之处可参考《考察分子磁感生电流的程序GIMIC 2.0的使用（含24分钟演示视频）》（<http://sobereva.com/491>）。.vti也被Multiwfn支持作为输入文件来读入格点数据信息。

RESP电荷拟合过程中允许加入额外的拟合中心，可以比如拟合在力场中用于增强描述sigma穴、孤对电子区域的非原子中心的电荷。在更新过的《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）一文的3.6节中已做了示例。

RESP电荷拟合功能支持了根据用户指定的体系局部区域（或整个体系）自动判断和设置原子等价性，见更新过的《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）一文的3.5节的示例。

盆分析功能的图形界面里支持了只观看盆的电子密度大于0.001 a.u.部分的功能，使得盆的主体特征明显更易于考察。见已更新的《使用Multiwfn做电子密度、ELF、静电势、密度差等函数的盆分析》（<http://sobereva.com/179>）。

定量分子表面分析功能（主功能12）中加入了选项14，用于计算特定表面极值点附近的特定函数值范围内的面积，这可以用于衡量诸如sigma穴、pi穴的面积，见手册3.15.2.2节的介绍和4.12.10节的实例。还加入了选项15，用于对分子表面根据被映射的函数进行类似盆分析的划分，每个局部表面对应一个极值点，这有助于认识分子表面的构成，见手册4.12.11节的实例。

支持了载入和导出卢天提出的.mwfn格式文件。详见《最理想的用于波函数分析的波函数文件格式mwfn已发表！》（<http://bbs.keinsci.com/thread-16363-1-1.html>）。

主功能11绘制UV-Vis和ECD光谱的功能支持了Gaussian的EOM-CCSD任务的输出文件。

绘制光谱的主功能11中，以及绘制态密度（DOS）图的主功能10中，现在都可以输入s将当前的绘图设置保存为文本文件，以后重新绘图时可以输入l从文本文件中读入作图设定，免得每次都得麻烦地重新修改一遍作图设置。

settings.ini中加入了iloadGaugeom选项，设为1后就可以从Gaussian输出文件中载入最后的结构。这个设计使得Multiwfn可以实现此文介绍的功能：《一键把所有gjf文件转成xyz文件、把所有Gaussian输出文件转成gjf文件的脚本》（<http://sobereva.com/530>）。

DOS绘制功能中加入了选项9，可以将轨道的简并度通过离散竖线高度直观地体现出来。

主功能100的主功能2加入了非常方便的产生PSI4的SAPT任务的输入文件的功能，见《使用PSI4做对称匹配微扰理论(SAPT)能量分解计算》（<http://sobereva.com/526>）。

Multiwfn计算出的键级已可以非常方便地直接通过GaussView标注在图上，见《将Multiwfn计算的键级直接标注在分子结构图上的方法》（<http://sobereva.com/523>）。

完全态求和（SOS）功能中加入了选项19，可以对beta(-(w1+w2);w1,w2)中的w1和w2进行扫描，从而绘制二维图直观展现体系可能具有的非线性光学特征，见《Multiwfn的SOS功能现已可以对动态超极化率beta(w1,w2)的频率做二维扫描》（<http://bbs.keinsci.com/thread-15455-1-1.html>）。

支持了非平面体系的pi电子轨道自动检测功能，这使得绘制任意体系的pi共轭路径非常方便。见《在Multiwfn中单独考察pi电子结构特征》（<http://sobereva.com/432>），以及卢天等人介绍此算法的论文Theoretical Chemistry Accounts, 139, 25 (2020)。

## 2.2 新改进和改变

相对于3.6版，意义比较大的或被较多人关注的新改进和改变将在下面罗列一下。完整的改进列表见下一节的IMPROVEMENTS AND CHANGES部分。

Multiwfn自身的静电势计算代码速度得到质的提升，见《Multiwfn的计算静电势的内部代码速度得到了巨幅提升！》（<http://sobereva.com/563>）。此部分的改进是基于张鋆提供的利用了他的libreta积分库的代码，在此表示感谢。

为了方便用户，使用命令行方式运行Multiwfn时现已可以添加一些选项。可以使用-nt、-uf分别指定并行核数、用户自定义函数（user-defined function）的编号。可以加用-silent要求使用silent方式运行。可以用-set直接指定settings.ini文件位置。例如可运行Multiwfn phenol.wfn -nt 12 -silent -set /sob/settings.ini。

平均局部离子化能着色的分子表面图已可以方便地绘制来考察亲电反应位点，见《使用Multiwfn和VMD绘制平均局部离子化能(ALIE)着色的分子表面图（含视频演示）》（<http://sobereva.com/514>）。

计算概念密度泛函理论定义的各种量的功能（主功能100的子功能16）加入了选项-1，选过一次之后，再选选项1，就可以产生ORCA的输入文件，自行运行之后就可以得到做分析所需的N.wfn、N-1.wfn等波函数文件。这使得没有Gaussian的人也能方便地用这个功能做概念密度泛函理论分析。此功能介绍见《使用Multiwfn超级方便地计算出概念密度泛函理论中定义的各种量》（<http://sobereva.com/484>）。

Hirshfeld-I电荷计算变得远比以往容易得多得多。由于Multiwfn现在已经自带了全周期表（稀土元素除外）的各种元素的不同电荷数的原子径向密度文件，因此目前计算过程已可以完全脱离Gaussian程序。见手册3.9.13节的说明和4.7.4节的例子。

轨道定域化功能现在可以通过选项3来要求只对部分轨道允许其相互混合来进行定域化。

载入较大.fch、.molden文件的耗时大幅降低。

主功能11绘制多个体系光谱的时候不再需要将跃迁数最多的体系放在输入的multiple.txt文件中的第一个，明显更为方便。

支持了ORCA和Dalton程序产生的含有h角动量基函数的.molden文件。

主功能18中的各种基于组态系数做电子激发分析的功能都已支持ORCA的sTDA和sTDDFT任务的输出文件，使得巨大体系电子激发分析成为可能，详见<http://bbs.keinsci.com/thread-17358-1-1.html>。

绘制平面图（主功能4）的后处理菜单中加入了选项-3，可以将当前作图设定导出到文本文件中，也可以从文本文件载入作图设定，免得每次作类似的图或者重作某张图时都需要重新敲一遍命令。

拓扑分析功能（主功能2）目前已支持对Multiwfn支持的所有实空间函数做拓扑分析。

IGM分析中计算delta-g指数的算法做了显著改进，计算耗时远低于上个版本，与此同时精度还得到了改进。

为了方便用户，导出轨道格点数据的功能（主功能200的主功能3）里可以通过输入诸如h选择HOMO、h-3选择HOMO-3、l+2选择LUMO+2。

观看体系结构和轨道的主功能0里的一些改进：加入了几何结构测量功能、高亮部分原子功能、基于特定原子编号获得其所在整个片段中原子序号的功能、切换是否显示氢原子的选项。另外，选择了某轨道后，保存图片文件时文件名将对应于轨道编号以便于管理和避免混淆。Tools下拉菜单里加入了Write settings to GUIsettings.ini和Load settings from GUIsettings.ini选项，分别用于将当前作图设置导出到GUIsettings.ini文件、从GUIsettings.ini文件中读入作图设置。

将以NAO为基的Wiberg键级分解为原子轨道间相互作用的功能已支持开壳层体系。

在定量分子表面分析功能（主功能12）中加入了选项18，用于删除不想要的表面极值点。还加入了选项19，可以将特定一批表面极值点合并为它们的平均位置，由此可以消除某些离得很近的影响视觉效果的多余的表面极值点。

主功能18中的电子激发分析模块（空穴-电子分析等）现已支持Gaussian和ORCA的激发态优化的输出文件作为输入文件，因此做这些分析前不必先把优化的最后一帧提取出来再单独做一次电子激发计算。

填色平面图、着色的地形图、热图等绘制功能中，都增加了Set color transition选项来设置色彩过渡方式，使得控制图像效果的灵活度比以前高得多，见手册4.4.1.2节的示例，以及此文中的例子的绘图过程：《谈谈18碳环的几何结构和电子结构》（<http://sobereva.com/515>）。

在《利用Multiwfn计算倾斜、扭曲环的NICS_ZZ》（<http://sobereva.com/261>）一文介绍的功能中，目前已经可以通过指定的一批原子拟合出的平面来定义平面（之前版本只能用三个原子定义平面，这样做有时不够合理）。

GROMACS的.gro文件已支持作为输入文件来提供结构信息。

绘制填色效果的RDG散点图变得更容易，见更新过的《绘制有填色效果的用于弱相互作用分析的RDG散点图的方法》（<http://sobereva.com/399>）。还支持了IGM填色散点图的绘制，见手册4.20.10.1节末尾。

已支持直接载入ORCA的gbw文件，前提是将settings.ini里的orca_2mklpath设为了ORCA目录下的orca_2mkl程序的实际路径。

EEM电荷计算已支持用.mol2作为输入文件，避免了之前需要用的.mol文件对原子数有999的严重限制。

大大扩展和完善了产生ORCA输入文件的功能。详见《详谈Multiwfn产生ORCA量子化学程序的输入文件的功能》（<http://sobereva.com/490>）。

之前《使用Multiwfn+VMD快速地绘制静电势着色的分子范德华表面图和分子间穿透图（含视频演示）》（<http://sobereva.com/443>）文中介绍了怎么在Windows下绘制，现在也提供了在Linux下绘制这种图的脚本，做法见手册4.A.13节的Part 9。

定量分子表面分析功能的后处理菜单加入了选项8，可以把表面顶点和极值点导出为pqr文件，既包含坐标也包含被映射的函数的数值，而且此格式可以直接被VMD载入。此改进便于用户做后处理分析。

需要读取NBO输出信息的功能中（如AdNDP模块等）已支持了NBO7的输出信息，并且改进了对其它NBO版本在特殊情况下的兼容性。

RESP电荷拟合时所做的电荷约束和原子等价性约束对于两步式拟合的第一步现在也生效了。

Hirshfeld surface分析中，支持了计算中心分子的特定原子与周围分子的特定原子之间的接触面积，见手册4.12.6节的例子。

支持了.dx格式作为输入文件载入格点数据。此文件可以通过诸如VMD的Volmap插件产生。利用这个特征，Multiwfn可以作为非主流的.dx向主流的.cub格式的转换器（主功能13可将已载入的格点数据导出为.cub）。

HOMA芳香性指数计算功能里加入了B-N和B-C的参数，从而令此方法能用于很多含硼的体系。

主功能100的基于几何结构的分析功能（子功能21）中，如果输入dist命令并且输入两个片段中的原子序号，就可以给出这两个片段之间最近和最远距离，以及它们之间的几何中心和质心距离。

拓扑分析（主功能2）的功能1现已可以将txt/pdb/pqr文件中记录的坐标作为初猜点。这使得拓扑分析模块可以对盆分析模块毫无遗漏地确定的各种函数的极值点位置进行精炼，见手册4.2.7节的盆分析+拓扑分析获得自旋密度极值点位置的例子。

## 3 完整的更新列表

方框里的日期是相应功能加入Multiwfn开发版(dev)的时间。

### NEW FUNCTIONS

•Functionality of quantitative molecular surface analysis module (main function 12) has been extended. A new option "14 Calculate area of the region around a specific surface extreme" is added to post-process menu, this is very useful for measuring local surface area (i.e. size) of sigma-hole or pi-hole. See corresponding introduction in Section 3.15.2.2 of manual and practical analysis example in Section 4.12.10. In addition, a new option "15 Basin-like partition of surface and calculate areas" is added, it is useful for unveiling how the whole molecular surface is composed of individual surface basins corresponding to various surface ESP extrema, see study example in Section 4.12.11.  
•Exporting loaded or calculated grid data to .vti file is supported by subfunction 2 of main function 100. .vti can be visualized by the very powerful volumetric data visualizer ParaView (freely available at <https://www.paraview.org>). This function now also supports exporting current structure to .cml file, which can be loaded by ParaView to show molecules.  
•Subfunction 17 is added to main function 200, it is used to calculate Coulomb and exchange integral between two orbitals based on uniform grid, see Section 3.200.17 of manual for detail and example. In the future version, evaluating these integrals via analytical method may be also available (in that case the cost will be significantly lower).  
•Subfunction 6 of main function 200 now is also able to calculate overlap integral between norm of orbitals of two sets of wavefunctions, this quantity is useful for measuring orbital superposition. See Section 3.200.6 of manual for detail.  
•Many data related to Hyper-Rayleigh scattering (HRS) now can be computed via subfunction 7 of main function 200. See Section 3.200.7 of manual for introduction and 4.200.7 for example.  
•[2019-Aug-9] Density difference now can be decomposed to orbital contributions. For example, one can use this function to study which NBO orbital(s) have evident contribution to Fukui function. See Section 3.200.13 of manual for introduction and Section 4.200.13 for example.  
•[2019-Aug-11] Bond length alternation (BLA), bond order laternation (BOA), bond angle and dihedral alterations for a given chain now can be very easily calculated via subfunction 18 of main function 200. This function is particularly useful for studying conjugated oligomers or conjugated paths. See Section 3.200.18 of manual for introduction and 4.200.18 for example.  
•[2019-Aug-20] The procedure of calculating kinetic diameter for small molecules using the method proposed in J. Phys. Chem. A, 118, 1150 (2014) has been illustrated in Section 4.12.12 of manual.  
•[2019-Sep-7] Two-level and three-level analyses of first hyperpolarizability have been supported in sum-over-states (SOS) module of Multiwfn. See Section 3.200.8.2 for detail and Section 4.200.8.2 for example.  
•[2019-Sep-11] Multiwfn now is able to parse second polarizability from "polar" task of Gaussian and print it in readible format and give relevant information. See updated Section 3.200.7 for introduction and Section 4.200.7 for example.  
•[2019-Sep-27] When plotting spectra via main function 11, user can use new option 23 to add spikes at bottom of the spectrum to clearly indicate position of transition energies, different colors can be used to highlight different types of transitions, the height can be used to reflect degree of degenerate. See example in Section 4.11.9 for illustration.  
•[2019-Sep-27] An option "Tools - Batch plotting orbitals" is added to menu bar of main function 0. This option can very conveniently save isosurface graphs for a batch of given orbitals.  
•[2019-Sep-27] A special form of PDOS, namely "MO-PDOS" now can be plotted by main function 10. MO-PDOS map can clearly reveal contribution to DOS from different sets of MOs. See Section 4.10.5 for introduction and example.  
•[2019-Oct-11] Subfunction 2 of main function 100 now can export .mkl file (old Molekel input file). This is particularly useful for ORCA users if they want to use wavefunction generated by other quantum chemistry codes as initial guess of ORCA, namely using other codes to generate .fch or .molden file first, then use Multiwfn to convert it to .mkl, and finally use orca_2mkl test -gbw to convert test.mkl to test.gbw.  
•[2019-Oct-13] The real space function generated by 3D cubic spline interpolation based on the grid data in memory is supported as user-defined function with index of -3. This function is more smoother and usually more accurate than the function evaluated by trilinear interpolation (user-defined function -1) when grid spacing is relatively large.  
•[2019-Oct-14] In the spectrum plotting function (main function 11), minima and maxima of spectrum can be directly labelled on the spectrum, see updated Section 4.11.3 on how to do this. Exact values of spectrum extrema are now directly printed on screen when choosing option 0 to plot map; the use of option 16 has been completely changed, now it is used to set how to show extreme labels.  
•[2019-Oct-15] A new molecular descriptor "Molecular polarity index" (MPI) as well as polar and nonpolar surface areas are automatically outputted after performing quantitative molecular surface analysis for electrostatic potential via main function 12. See Section 3.15.1 for introduction of its definition. The larger the MPI, the higher the molecular polarity.  
•[2019-Oct-19] The RESP fitting module now supports generate equivalent constraint file based on point group symmetry of local regions or the entire system, see "Example 5" of Section 4.7.7 for illustration. This feature is particularly useful and convenient if you want to make resulting charges satisfy molecular global or local symmetry.  
•[2019-Oct-27] The AV1245 proposed in Phys. Chem. Chem. Phys., 18, 11839 (2016) has been supported as subfunction 11 of main function 9. This index is very useful in quantifying aromaticity of large ring (such as porphyrin). See Section 3.11.10 for introduction and 4.9.11 for example.  
•[2019-Nov-16] In the AdNDP module, option 15 is added, which is used to compute orbital composition based on natural atomic orbitals (NAOs) for picked AdNDP orbitals.  
•[2019-Nov-19] PEOE is a popular and very fast method of evaluating atomic charges, it has been supported as subfunction 19 of main function 7. This kind of charge is also known as Gasteiger charge. See Section 3.9.17 for introduction and Section 4.7.9 for example.  
•[2019-Dec-21] Orbital delocalization index (ODI) is supported to quantify extent of spatial delocalization of orbitals on the whole system or on specific fragment. See Section 4.8.5 for example.  
•[2020-Jan-5] Hole delocalization index (HDI) and electron delocalization index (EDI) have been supported in hole-electron analysis module, they are pretty useful in quantifying breadth of spatial distribution of hole and electron. See "Theory 3" of Section 3.21.1.1 for introduction and updated Section 4.18.1 for example.  
•[2020-Jan-24] Adding additional fitting center is supported by RESP charge calculation module. See Example 6 of Section 4.7.7 for illustrative application.  
•[2019-Jan-27] GUI (option 0) of basin analysis module now supports drawing basins within in rho=0.001 surface (via "Set basin drawing method" - "rho>0.001 region only" option in the menu bar). See updated Section 4.17 of manual for illustration. In addition, this video tutorial is highly suggested to have a look: "Drawing AIM basins (atomic basins) in Multiwfn and VMD" (<https://youtu.be/9D5do80XcbI>)  
•[2019-Jan-28] Subfunction 15 is added to main function 18. It is used to show major MO transitions for all excited states, so that you can quickly recognize basic characteristics of various excited states in terms of MOs  
•[2019-Jan-30] The RESP2 charge proposed in DOI: 10.26434/chemrxiv.10072799.v1 now can be easily calculated, see Section 4.7.7.9 for example. RESP2 is very suitable for molecular dynamics purpose.  
•[2020-Feb-9] Van der Waals potential and its two components (repulsion potential and dispersion potential) now can be visualized via subfunction 6 of main function 20. See Section 3.23.7 for introduction and Section 4.20.6 for example. This analysis method has been published in DOI: 10.26434/chemrxiv.12148572.v1  
•[2020-Feb-13] Bond order density (BOD) and natural adaptive orbital (NAdO) analyses proposed in J. Phys. Chem. A, 124, 339 (2020) has been supported. This is a useful method that can visualize contribution to delocalization index from various spatial regions. See Section 3.200.20 for introduction and 4.200.20 for example.  
•[2020-Feb-23] Orbital-weighted Fukui function and orbital-weighted dual descriptor not can be easily calculated, see Section 3.100.16.3 of manual for introduction and 4.100.16.2 for illustrative application. Compared to standard form of Fukui function and dual descriptor, they are able to reasonably applied to systems with (quasi-)degenerate frontier molecular orbitals, such as C60, coronene and cyclo[18]carbon.  
•[2020-Mar-5] Pores or free regions in a box (usually simulated by molecular dynamics) can be visualized by subfunction 1 of main function 300, volume of free regions can also be calculated. See Section 3.300.1 for introduction and 4.300.1 for example.  
•[2020-Mar-10] Sphericalized atomic radial density now can be easily fitted as multiple Slater type orbitals (STOs) or Gaussian type functions (GTFs) by subfunction 2 of main function 300. This module is quite robust and flexible. See Section 3.300.2 for introduction and Section 4.300.2 for practical examples.  
•[2020-Mar-13] The ωcubic electrophilicity index introduced in J. Phys. Chem. A, 124, 2090 (2020) now can be automatically calculated by subfunction 16 of main function 100, see Section 3.100.16 for detail. It is shown that condensed form of this index at halogen atom in halogen bond dimers has ideal linear relationship with binding energy.  
•[2020-Apr-3] The high ELF localization domain population and volume (HELP and HELV) defined in ChemPhysChem, 14, 3714 (2013) now can be calculated via basin analysis module. They can be used to study molecular properties that closely related to lone pair electrons. See the ChemPhysChem paper for detailed introduction and Section 4.17.8 of manual for illustration.  
•[2020-Apr-10] The unit sphere representation and vector representation of (hyper)polarizability proposed in J. Comput. Chem., 32, 1128 (2011) has been supported as subfunction 3 of main function 300. They are quite useful methods of visualizing (hyper)polarizability tensor, see Section 3.300.3 of manual for introduction and 4.300.3 for example.  
•[2020-Apr-19] The intrinsic bond strength index (IBSI) proposed in J. Phys. Chem. A, 124, 1850 (2020) has been supported. It was defined in the framework of IGM and demonstrated to be useful in characterizing strength for chemical bonds. See Section 3.11.9 for introduction and Section 4.9.6 for example.  
•[2020-Apr-19] The IGM under Hirshfeld partition of actual molecular density (IGMH) proposed by Tian Lu has been supported as subfunction 11 of main function 20. This new form of IGM purely relies on wavefunction to perform IGM analysis, the result is more physically meaningful and graphical effect is better, though the cost is higher than the original form of IGM, which employs promolecular approximation. See Section 3.23.6 for introduction of IGMH and Section 4.20.11 for example.  
•[2020-Apr-26] Scanning tunneling microscope (STM) image now can be well simulated by subfunction 3 of main function 300 of Multiwfn. Both constant height and constant current modes are supported, very nice image can be directly generated. See Section 3.300.4 of manual for introduction and 4.300.4 for example.  
•[2020-Apr-26] IBSIW (intrinsic bond strength index for weak interactions) now can be calculated by option 6 of IGM and IGMH analysis modules. See Section 3.23.5 for introduction.  
•[2020-Jun-3] Orbital composition now can be computed based on AIM partition by newly added subfunction 11 of main function 17. This function can also computes composition contributed by various kinds of basins, such as ELF basin and Fukui function basin. See Section 4.8.6 for example.  
•[2020-Jun-18] Molecular quadrupole and octopole moments now can be calculated via subfunction 2 of fuzzy atomic space analysis module. In addition, by defining fragment using option -5 in this module and then choose subfunction 2, you can calculate fragment dipole/quadrupole/octopole moments, see Section 4.15.3 for example of calculating fragment dipole moment.  
•[2020-Jun-27] Electric dipole, quadrupole and octopole moments of present system now can be evaluated analytically by subfunction 5 of main function 300, see Section 3.300.5 of manual for introduction and 4.300.5 for example.  
•[2020-Jul-3] The interaction region indicator (IRI) proposed by Tian Lu has been supported as subfunction 4 of main function 20. IRI is a function that able to equally well reveal chemical bond regions and weak interaction regions. See Sections 3.23.8 and 4.20.4 of manual for introduction and example, respectively. IRI is defined in a much simpler way than DORI, while graphical effect is found to be evidently better than DORI.  
•[2020-Jul-26] Plotting NMR has been supported in main function 11. Output file of NMR task of Gaussian and ORCA are supported. See Section 3.13.5 of manual for detail and 4.11.10 for example.

### IMPROVEMENTS AND CHANGES

 •In the menu bar of main function 0, "Measure geometry" is added, by which you can easily measure distance, angle and dihedral between selected atoms.  
•Option -2 of AdNDP module has been modified. Now it consists of a few suboptions, via "Set maximum number of candidate orbitals to be printed", one can customize the maximum number of candidate orbitals printed on screen during AdNDP searching.  
•The way of plotting electrostatic potential colored vdW surface via script under Linux platform has been described in part 9 of Section 4.A.13.  
•The interface for generating ORCA input file (option 12 of subfunction 2 of main function 100) now supports adding diffuse functions and generating input file of sTD-DFT task.  
•.vti file (ParaView VTK Image Data) containing scalar data now can be loaded to provide grid data. This makes Multiwfn able to deal with the magnetically induced ring current data calculated by GIMIC 2.0 code.  
•.mol2 file now can be used as input file for EEM charge calculation.  
•After using option 6/7/16/17 of sum-over-states module of Multiwfn (subfunction 8 of main function 200), variation of all components of beta/gamma with respect to number of considered states / external frequency will be exported to a text file with _comp suffix in current folder.  
•Subfunction 22 of main function 100 now is also able to detect pi-like delocalized orbitals for a not exactly planar system, see updated Section 3.100.22 for detail.  
•Multiwfn now is able to directly load .gbw file of ORCA program, the user should set "orca_2mklpath" in settings.ini to actual path of the orca_2mkl executable file in ORCA folder.  
•A new option "8 Export all surface vertices and surface extrema as vtx.pqr and extrema.pqr" is added to post-process menu of quantitative molecular surface analysis module. In the exported .pqr files, value of mapped function is recorded as the third last column in high precision and a.u.  
•[2019-Aug-8] GROMACS .gro format now can be used as input file to provide atomic information  
•[2019-Aug-24] The RDGmap.gnu in "examples" folder has been replaced with examples\scripts\RDGscatter.gnu. As described in the updated Section 3.23.1, before plotting sign(λ2)ρ colored RDG scatter map, the output.txt file is no longer needed to be manually processed.  
•[2019-Aug-30] In the function "Obtain NICSZZ value for non-planar or tilted system", the plane can be defined via fitting a given set of atoms (in old version you can only use three atoms to define the plane)  
•[2019-Sep-2] When input file contains connectivity information, such as .mol2 and .cml, the bonding in GUI will not be automatically determined but displayed according to known connectivity.  
•[2019-Sep-11] In main function 0, if an orbital has been selected, then the file name of saved picture will be the corresponding orbital index.  
•[2019-Sep-13] Electron excitation analysis modules (e.g. hole-electron analysis) now supports output file of excited state optimization task of Gaussian and ORCA as input file.  
•[2019-Sep-14] In the menu of plotting color-filled map, shaded relief map and colored matrix, now one can change color transition method via option "Set color transition", namely the default rainbow transition (Purple-Green-Red) is no longer the only choice. An illustration is given in Section 4.4.1.2 of the manual. At the meantime, the "inowhiteblack" parameter in settings.ini is removed, because the same effect can be equivalently realized by choosing other color transition method instead of the default one.  
•[2019-Sep-19] "iprintLMOorder" parameter is added to settings.ini, if it is set to 1, then after completing the generation of LMOs, composition of LMOs will be printed in the order of atoms and atom pairs instead of in order of LMO indices.  
•[2019-Sep-21] Output file of NBO7 now could be used for AdNDP, NAOMO, etc. analyses (Earlier versions only support NBO 3,5,6).  
•[2019-Sep-22] In the post-process menu, a new option 18 is added, by which you can remove unwanted surface extrema by inputting their indices. Another new option is 19, you can use it to merge some surface extrema, the average coordinate of selected extrema will be employed as the new position.  
•[2019-Sep-22] In the population analysis module, if fragment has been defined by option -1, then after population analysis or atomic charge evaluation, not only fragment charge will be given, but also fragment population will be shown.  
•[2019-Sep-24] In the post-process menu of hole-electron analysis, an option -1 is added, if its status is manually switch to "Yes", then the outputted cube files (e.g. hole.cub) will have index of currently loaded excited state as suffix.  
•[2019-Sep-28] "Toggle showing hydrogens" and "Set atom highlighting" options are added to "Other settings" menu of GUI of main function 0.   
•[2019-Oct-12] "isoRGB_same" and "isoRGB_oppo" parameters are added into settings.ini, they are used to set default red, green and blue components of isosurface with same sign and oposite sign as current isovalue, respectively.  
•[2019-Oct-19] Customized charge constraint and equivalent constraint now also take effect for the first stage of the standard two-stage RESP fitting procedure. This improvement make RESP charge fitting more flexible.  
•[2019-Oct-22] A new parameter "iMCBOtype" is added to settings.ini. If it is set to 1, then the calculated multi-center bond order will correspond to the average between positive and reversed input order of atom indices. If it is set to 2, then all possible permutations of atom indices will be taken into account in the multi-center bond order calculation. See Section 3.11.2 for detail.  
•[2019-Oct-29] The function "Decompose Wiberg bond order in NAO basis as atomic orbital pair contributions" introduced in Section 3.11.8 has supported open-shell wavefunction.  
•[2019-Oct-30] When outputting calculated Hirshfeld/ADCH/Becke/VDD/CM5 charges, normalized charges are also printed to eliminate the marginal error due to unavoidable inaccuracy of numerical integration  
•[2019-Nov-16] The orbital composition analysis function based on natural atomic orbitals (NAOs) now also prints contribution from NAO shells.  
•[2019-Nov-21] The sum-over-states module (subfunction 8 of main function 200) now has a new option 19, which is used for scanning w1 and w2 of beta(-(w1+w2);w1,w2), the resulting file can be used to plot "beta vs. w1,w2" relief map to identify possible non-linear optical effects. See Section 4.200.8.1.  
•[2019-Dec-2] In the Hirshfeld surface analysis, the area of contact surface between specific atoms in the central molecule and specific atoms in the peripheral molecules can be outputted. See updated Section 4.12.6 of Multiwfn manual for example.  
•[2019-Dec-4] The bond orders calculated by Multiwfn now can be easily labelled on molecular structure map by using Multiwfn in combination with GaussView. See updated Section 4.9.1 of manual on how to realize this.  
•[2019-Dec-23] A new option "Select fragment" is added to "Tools" submenu of the menu bar of main function 0. After selecting it and input an atom index, the whole fragment where the atom attributes to will be highlighted, and the indices of all atoms in the fragment will be returned. This is useful when you perform analysis based on fragment.  
•[2019-Dec-24] The function of generating PSI4 input file (see subfunction 2 of main function 100) now can very easily generate input file of SAPT task. See <http://sobereva.com/526> for introduction.  
•[2019-Dec-10] The functions for generating input file of PSI4 and MOPAC programs (corresponding options in subfunction 2 in main function 100) have been largely extended  
•[2019-Jan-19] Option 9 is added to DOS plotting module, it can be used to show orbital degeneracy in terms of height of discrete lines. See updated examples in Section 4.10.  
•[2019-Jan-23] DOS plotting module (main function 10) now support saving current status (plotting settings, fragment definition and orbital information) to a file and loading status from a file, so that you can quickly recover previously saved status. See end of Section 4.10.5 for example.  
•[2019-Jan-23] Spectrum plotting module (main function 11) now support saving current plotting settings to a file and loading plotting settings from a file. See updated Section 4.11.3 for example.  
•[2019-Jan-24] In MK and CHELPG calculation module, the unit of the coordinate in the file for providing additional fitting centers has been changed to Angstrom (the old version is Bohr)  
•[2019-Jan-28 & 2020-Apr-10] "iloadGaugeom" is added to settings.ini. When Gaussian output file is used as input file, if it is set to 1 and 2, then Multiwfn will load final geometry (input orientation and standard orientation, respectively) from this file to obtain atom coordinate information.  
•[2019-Jan-30] Spectrum plotting module (main function 11) has supported plotting UV-Vis and ECD spectra for EOM-CCSD task of Gaussian.  
•[2020-Feb-8] .dx format has been supported as input file, it is a volumetric data format that can be exported by e.g. Volmap plugin of VMD program.  
•[2020-Feb-11] A new option "6 Output orbital overlap matrix in atoms to AOM.txt in current folder" now is available in basin analysis module when electron density is selected as the function for partitioning the basins.  
•[2020-Feb-13] .mwfn file is supported as input file and can be exported by some functions (e.g. subfunction 2 of main function 100). This is a new and much better format than others (e.g. wfn/fch/molden) for exchanging wavefunction information. See Section 2.5 of manual for detail. The paper specifically introducing the .mwfn format has been published: ChemRxiv (2020) DOI: 10.26434/chemrxiv.11872524.v1  
•[2020-Feb-14] In main function 0, now one can select "Tools" - "Write settings to GUIsettings.ini" to save current visualization state to GUIsettings.ini. In the future, one can use "Tools" - "Load settings from GUIsettings.ini" to retrieve previous visualization state. See Section 3.2 of manual for detail.  
•[2020-Feb-21] After generating AIM basins via main function 17, if option 4 is selected, not only localization index and delocalization index matrix will be outputted based on basin indices (like earlier version), but also they will be outputted based on atomic indices.  
•[2020-Mar-1] B-N and B-C parameters have been added to HOMA calculation module. B-N parameter has been added to Bird calculation module  
•[2020-Mar-20] In the function of exporting orbital wavefunctions (subfunction 3 of main function 200), now one can use such as "h" to choose HOMO, "h-3" to choose HOMO-3, "l+2" to choose "LUMO+2". This improvement makes exporting cube file for frontier orbitals easier.  
•[2020-Mar-24] A new option "20 Set number of decimal places for axes" is added to post-process menu of DOS plotting module (main function 10).  
•[2020-Apr-18] A new algorithm is employed for calculating atom pair delta-g index in the IGM analysis module. The cost is much lower than before, and at the same time the numerical accuracy is evidently improved.  
•[2020-Apr-22] Color of critical points in plane map now can be set by "CP_RGB_2D" parameter in settings.ini.  
•[2020-Apr-23] Topology analysis function now can be applied for any real space function that supported by Multiwfn.  
•[2020-Apr-23] Option 1 in topology analysis module has been extended. Now a batch of starting points can be directly loaded from a .txt/.pdb/.pqr file, therefore this module now is able to be used to refine the positions of the attractors crudely located by basin analysis module based on evenly distributed grids.  
•[2020-Apr-23] Option -4 of basin analysis module is extended, now it can also export located attractors as .pqr file and .txt file, in which the function value at the attractors are recorded.  
•[2020-Apr-23&29] Option -3 has been added to post-processing menu of main function 4, in this option there are many suboptions used to adjust plotting settings. Option -4 is also added, it is used to save (load) all plotting settings to (from) an external file (.txt).  
•[2020-May-9] All electron excitation analyses related to configurational coefficients, such as hole-electron analysis, now support sTDA or sTDDFT task of ORCA. See updated Section 3.21.A of manual for detail. Due to this improvement and extremely fast speed of sTDA/sTDDFT method, electron excitation analyses are feasible for systems consisting of even more than 500 atoms.  
•[2020-May-21] Option 3 has been added to orbital localization analysis module (main function 19). This option can localize specific subset of molecular orbitals, making orbital localization more flexible.  
•[2020-May-30] In old versions, topology paths do not exactly reach the final critical point. In the new version, the finally nearly reached critical point is regarded as the final point of the path, and thus the reported length of topology paths becomes more reasonable.  
•[2020-May-31] AVmin index proposed in J. Phys. Chem. C, 121, 27118 (2017) has been supported for measuring aromaticity of large ring. See Section 3.11.10 of manual for detail.  
•[2020-Jun-2] Calculation of Hirshfeld-I charge becomes significantly easier!!! In the new version, "atmrad" folder is provided in the "examples" directory in Multiwfn binary package, it contains atomic radial densities for all elements in the periodic table (except for lanthanides and actinides) at all possible charged states. If this folder is copied to current folder, then the step of calculating atomic .wfn files will be directly skipped during Hirshfeld-I calculation. See Section 3.9.13 of manual for details and Section 4.7.4 for example.  
•[2020-Jun-6] The molden file generated by ORCA and Dalton containing h angular moment now has been perfectly supported.  
•[2020-Jun-6] Default extension distance of ICSS analysis has been changed from 6 Bohr to 12 Bohr, which is more reasonable for this kind of analysis.  
•[2020-Jun-7] In the RESP charge calculation module, maximum number of RESP iterations and charge convergence threshold now can be set by option 4 in this module.  
•[2020-Jun-27] Subfunction 7 of main function 6 now is able to export electric quadrupole and octopole integral matrix between basis functions.  
•[2020-Jun-27] In subfunction 21 of main function 100, now one can input "dist" command and then input atom indices for two fragments, then minimum and maximum distances between the fragments, as well as distances between their geometry centers or between their mass centers, will be outputted.  
•[2020-Jul-5] In the sum-over-states (SOS) calculation module (subfunction 8 of main function 200), user now can specify incident lights in negative frequencies to compute e.g. beta(-(w1-w2);w1,-w2).  
•[2020-Jul-11] Speed of calculating electrostatic potential (ESP) has been significantly improved!!! (faster than old version by more than 20 times) This new code of efficiently evaluating ESP was kindly provided by Jun Zhang and then adapted by Tian Lu.  
•[2020-Jul-21] Time spent in loading large .fch/.molden file is notably reduced.  
•[2020-Jul-24] When plotting spectra for multiple systems in main function 11, it is no longer need to place the system with maximal number of transitions as the first term in the multiple.txt.  
•[2020-Aug-13] The option 1 in conceptual density functional theory analysis module (subfunction 16 of mainfunction 100) now is able to generate ORCA input files for producing N.wfn, N+1.wfn and N-1.wfn. User should select option -2 to switch the program to ORCA before selecting option 1.  
•[2020-Aug-14] -nt and -uf arguments now can be added to command line of running Multiwfn to specify number of threads and index of user-defined function, respectively. -set can be used to specify position of settings.ini file. For example, Multiwfn phenol.wfn -nt 12 -set /sob/settings.ini. -silent argument can request Multiwfn run in silent mode. See Section 2.2 for more information.

### IMPROVEMENTS ON MANUAL

•[2019-Aug-8] Section 4.18.9 is added to the manual to illustrate how to transform transition density to natural orbitals and export them as .molden and .wfx files.  
•[2019-Aug-24] The way of plotting sign(λ2)ρ colored IGM scatter map has been described at the end of Section 4.20.10.1.  
•[2019-Sep-14] A new Section 4.4.1.2 is added to the manual to further illustrate skills of plotting plane map.  
•[2019-Sep-17] Average local ionization energy (ALIE) colored molecular surface map now can be very easily drawn based on VMD script, see updated Section 4.12 of manual on how to realize this. This kind of map is quite useful for studying possible sites of electrophilic attack.  
•[2019-Sep-28] Section 4.200.6.2 is added to the manual to show how to evaluate contribution of lone pair of an atom to various MOs by means of orbital localization analysis and orbital correspondence analysis.  
•[2020-Feb-21] Section 4.12.13 is added to the manual to illustrate how to analyze local electron affinity.  
•[2020-Feb-21] In the output of Mulliken, SCPA, Stout-Politzer and NAO orbital composition analysis, contribution of various angular moment of shells are directly printed.  
•[2020-Mar-1] A document "Calculating information-theoretic quantities and some relevant quantities by Multiwfn" is added to "Resources" page of Multiwfn website. This document briefly illustrates how to use Multiwfn to calculate the very valuable information-theoretic quantities proposed by Prof. Shubin Liu in recent years.  
•[2020-Mar-1] "Trick: Perform ESP analysis on molecular surface solely based on cube files" is added to end of Section 4.12.1.  
•[2020-Apr-22] A document "How to cite Multiwfn.pdf" is provided in Multiwfn binary package since this version.  
•[2020-Apr-23] Section 4.2.7 is added to the manual. This section illustrates how to use attractors determined by basin analysis module as initial guessing points for searching critical points by topology analysis module. This skill guarantees that all maxima of positive part and minima of negative part of a function with complicated distribution can be exactly located.

### BUG FIXED

•Fixed: For a molecule of very long chain, the main function 0 is unable to plot the system.  
•Fixed: When plotting DOS for beta spin, the vertical dash line does not correspond to beta-HOMO.  
•[2019-Aug-28] Fixed: Some functions are incompatible with output file of ORCA 4.2  
•[2019-Sep-11] Fixed: For some large systems, the Hirshfeld-I charge is completely wrong or the calculation will crash.  
•[2019-Sep-12] Fixed: Multiwfn crash during Hirshfeld surface analysis if atomic densities are evaluated based on atomic .wfn files.  
•[2019-Sep-24] Fixed: The outputted new.gjf by simple energy decomposition analysis function (subfunction 5 main function 21) does not work for Linux version of Gaussian16  
•[2019-Oct-24] Fixed: Output file of anharmonic analysis of Gaussian program for linear molecule cannot be loaded to plot vibrational spectrum by main function 11  
•[2019-Nov-4] Fixed: Cannot normally invoke cubegen to plot electrostatic potential by main function 3.  
•[2019-Nov-20] Fixed: The excited state dipole moments outputted by option 4 of subfunction 5 of main function 18 are wrong if the origin of the system is not placed at nuclear charge center.  
•[2020-Feb-20] Fixed: Molden file containing certain kinds of transition metals generated by Grimme's xtb code cannot be properly loaded.  
•[2020-May-28] Fixed: Unit conversion factor between eV and nm is marginally inaccurate.  
•[2020-Jun-28] Fixed: The unsymmetrized transition density matrix (TDM) between two excited states generated by subfunction 9 of main function 18 is incorrect. This bug does not affect symmetrized TDM
