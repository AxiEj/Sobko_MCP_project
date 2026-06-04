---
post_id: 601
title: Multiwfn可以计算的分子描述符一览
url: http://sobereva.com/601
date: '2021-06-22T05:22:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 波函数分析
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 Multiwfn 可计算的分子描述符一览。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**Multiwfn可以计算的分子描述符一览**

List of molecular descriptors that Multiwfn can calculate

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2021-Jun-22  Last update: 2024-Apr-17

## 0 前言

做QSAR（定量结构活性关系）和QSPR（定量结构属性关系）需要提供分子的描述符（molecular descriptor）作为输入信息，从而根据拟合的经验关系预测分子的生物活性以及物理化学性质。特别是随着基于（深度）神经网络的机器学习方式的兴起，分子描述符更是受到了高度的关注。产生丰富且有不同物理意义的描述符对于化学领域的机器学习尤为重要。

强大、易用、免费的波函数分析程序Multiwfn（<http://sobereva.com/multiwfn>）可以基于不同原理计算许多分子以及原子的描述符，其中有不少都是通过其它公开的程序无法直接计算的。鉴于时不时有做QSAR/QSPR的人问及相关的事情，笔者觉得有必要写一个文章对Multiwfn能算的繁多的描述符做一个简要的汇总，供相关研究者了解Multiwfn在这方面能起到的用处。本文提到的描述符简单来说就是指一个分子一个值，或者一个原子一个值的那种量。构建预测模型中适合考虑哪些，应根据被预测的量与这些值的物理意义以及实际展现出的重要程度进行定夺。这些描述符除了用来预测分子性质外，也可以构建关系用来预测或解释特定问题，比如某种反应的难易或势垒的高低、分子间作用的强弱、各类实验现象等等。

目前已经有一些基于Multiwfn计算的描述符通过机器学习预测分子性质的文章，例如Phys. Chem. Chem. Phys. (2021) DOI: 10.1039/D1CP05072A利用Multiwfn计算的一些描述符建立了很好的预测分子亲核性的模型。

Multiwfn可以基于命令行运行，因此可以非常方便地通过脚本调用Multiwfn对大批体系自动进行计算、提取数据和处理数据，笔者专门写过文章进行详细说明，非常建议一读：《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>）。如果对Multiwfn不了解的话，务必看《Multiwfn入门tips》（<http://sobereva.com/167>）、《Multiwfn FAQ》（<http://sobereva.com/452>）、《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）以了解相关知识。

下面根据描述符的类型依次进行介绍。本文只是Multiwfn能算的描述符的一个不完整罗列，还有很多零零碎碎的相对次要的就没有提及。

## 1 静电势相关的描述符

如果对于静电势不了解的话，强烈建议看《静电势与平均局部离子化能相关资料合集》（<http://bbs.keinsci.com/thread-219-1-1.html>）里的资料了解基本知识。分子表面的静电势与分子间静电相互作用的关系特别密切，也因此Politzer等人提出了general interaction properties function (GIPF)的概念。GIPF描述符可以视为基于分子表面静电势做统计分析得到的描述符的统称。常见的GIPF包括分子表面静电势最大值和最小值、分子表面静电势正值/负值/所有部分的平均值/方差、分子表面静电势为正和为负的面积、电荷平衡度等等，详细介绍和公式见Multiwfn手册3.15节。Multiwfn的主功能12定量分子表面分析功能可以计算这些描述符，参考《使用Multiwfn的定量分子表面分析功能预测反应位点、分析分子间相互作用》（<http://sobereva.com/159>）以及Multiwfn手册4.12.1节的例子。GIPF描述符在预测分子性质上已有特别广泛的应用，在《使用Multiwfn预测晶体密度、蒸发焓、沸点、溶解自由能等性质》（<http://sobereva.com/337>）里我给了大量应用例子。由于GIPF是极其重要的一类分子描述符，物理意义很强，千万不要忽视。实际上基于GIPF预测的很多分子性质本身也可以再进一步作为描述符来用。

笔者在《谈谈如何衡量分子的极性》（<http://sobereva.com/518>）和Carbon, 171, 514 (2021)中提出了分子极性指数（molecular polarity index, MPI）的概念，可以衡量任意分子的等效极性，也是基于分子表面静电势定义的，同样可以用Multiwfn的主功能12计算。

Multiwfn的主功能12还可以计算不同静电势区间的分子表面积。默认就会输出静电势大于0、小于0的面积，还会输出笔者定义的非极性和极性表面积，即静电势绝对值<=10 kcal/mol和>10 kcal/mol的表面积。读者还可以用Multiwfn做分子表面静电势面积统计得到静电势在各个区间面积的具体值，可以分别作为不同的描述符，详见《使用Multiwfn结合VMD分析和绘制分子表面静电势分布》（<http://sobereva.com/196>）。

用Multiwfn主功能12对分子表面静电势统计后会得到分子表面上各个静电势极大点和极小点的位置以及数值，位于特定原子附近的极值点的数值有特殊意义，比如卤原子的sigma-hole区域对应的表面静电势极大点数值和卤键强度关系非常密切，而氮原子附近的表面静电势极小点可以用来预测碱性（例如J. Chem. Inf. Model., 60, 1445 (2020)用Multiwfn算的这个量预测胺类物质的pKb）。

Multiwfn还可以计算整个三维空间中静电势极小点位置及其静电势的具体数值，这也被用于一些文献提出的QSAR/QSPR方程中。计算方法见《绘制静电势全局极小点+等值面图展现孤对电子位置的方法》（<http://sobereva.com/493>）。

Multiwfn中独家支持笔者提出的局部分子表面分析，可以得到暴露在分子表面的每个原子在各自表面上的静电势统计指标，比如每个原子局部范德华表面的静电势平均值。Multiwfn手册4.12.3节给出了通过这个量预测亲核反应位点的例子。

Multiwfn的定量分子表面分析（主功能12）极为普适，能分析的绝不仅限于静电势，对于任意实空间函数都可以做定量统计分析，比如平均局部离子化能（ALIE）、局部电子附着能（LEAE）、局部电子亲和能（LEA）、电子离域范围函数（EDR）等，可以得到它们的极大/极小值、平均值、方差等等。Multiwfn手册4.12.2节给了分子表面ALIE定量统计的实例。ALIE体现局部位置电子被电离的难易程度，它在分子表面的分布被大量文章所分析讨论，对于预测亲电反应活性很重要，见前述的《静电势与平均局部离子化能相关资料合集》中的资料，并且建议参看《使用Multiwfn和VMD绘制平均局部离子化能(ALIE)着色的分子表面图（含视频演示）》（<http://sobereva.com/514>）来对这个函数有个直观的认识。ALIE在预测分子性质上也很有用，比如在J. Chem. Phys., 98, 4305 (1993)中Politzer发现分子体积除以分子表面ALIE的平均值与分子的极化率有极好的相关性。在《使用Multiwfn通过局部电子附着能(LEAE)考察亲核反应位点、难易及弱相互作用》（<http://sobereva.com/676>）中介绍的LEAE对ALIE有重要互补性，它可以预测亲核反应的优先位点和反应速率常数，而且和卤键的相互作用能有非常密切的相关性。

## 2 与概念密度泛函理论、反应性有关的描述符

在概念密度泛函理论框架中有许多与分子、原子的反应性存在密切联系的描述符。相关知识见《概念密度泛函综述和重要文献合集》（<http://bbs.keinsci.com/thread-384-1-1.html>）。在Multiwfn中可以非常方便地计算这些量，见《使用Multiwfn超级方便地计算出概念密度泛函理论中定义的各种量》（<http://sobereva.com/484>）和《通过轨道权重福井函数和轨道权重双描述符预测亲核和亲电反应位点》（<http://sobereva.com/533>）。能算的有下面这些，具体公式在Multiwfn手册3.25节都给了。  
• 分子描述符：垂直电离能、垂直电子亲和能、Mulliken电负性、化学势、电子硬度（等同于fundamental gap）、电子软度、亲电指数（Parr定义的原始形式和后来定义的更严格的ωcubic）、亲电描述符ε、亲核指数  
• 原子描述符：简缩福井函数、简缩双描述符、简缩局部软度、相对亲电指数、相对亲核指数、简缩局部亲电指数、简缩局部亲核指数、简缩局部ωcubic亲电指数 、超离域度（superdelocalizability）

Multiwfn还可以算所谓的FED（前线电子密度），利用Multiwfn算分子轨道成份的功能就可以很容易地手动得到，见<http://bbs.keinsci.com/thread-11679-1-1.html>。还可以算RSC Adv., 3, 1486 (2013)中提出的所谓的Parr函数，对于原子来说其实就是分子在+1和-1电荷状态下原子的自旋布居，自旋布居的计算见《谈谈自旋密度、自旋布居以及在Multiwfn中的绘制和计算》（<http://sobereva.com/353>）。

## 3 与分子结构有关的描述符

Multiwfn能计算许多跟分子结构特征有关的描述符。

在Multiwfn主功能100的子功能21里，可以计算特定一批原子的回转半径、转动常数、转动惯量、原子间最大和最小距离，见Multiwfn手册3.100.21节的说明。

Multiwfn能计算分子的长、宽、高，见《使用Multiwfn计算分子的长宽高以及显示分子的主轴》（<http://sobereva.com/426>）。

Multiwfn可以基于不同方式计算分子的半径，见《谈谈分子半径的计算和分子形状的描述》（<http://sobereva.com/190>）和《使用Multiwfn计算分子的动力学直径》（<http://sobereva.com/503>）。

Multiwfn可以以不同方式计算分子体积，见《谈谈分子体积的计算》（<http://sobereva.com/102>）。

Multiwfn可以计算笔者在J. Mol. Model., 27, 263 (2021) DOI: 10.1007/s00894-021-04884-0中提出的分子平面性参数（molecular planarity parameter, MPP）和偏离平面跨度（span of deviation from plane, SDP），这俩是彼此互补的而且特别理想的定量衡量分子或体系局部平面性的参数。详细介绍和例子见《使用Multiwfn定量化和图形化考察分子的平面性（planarity）》（<http://sobereva.com/618>）。

Multiwfn可以计算整个分子或者特定一批原子对应的面积，见《使用Multiwfn和VMD计算分子表面积和片段表面积》（<http://sobereva.com/487>）。

Multiwfn可以计算分子的球形度来定量衡量分子轮廓接近球形的程度，见《使用Multiwfn计算分子的球形度（sphericity）》（<http://sobereva.com/661>）。

Multiwfn能够计算含有孔洞的分子的孔洞体积《使用Multiwfn可视化分子孔洞并计算孔洞体积》（<http://sobereva.com/408>）。对于周期性体系也可以计算自由体积，见《使用Multiwfn图形化展示分子动力学模拟体系中的孔洞、自由区域》（<http://sobereva.com/539>）和《使用Multiwfn计算晶体结构中自由区域的体积、图形化展现自由区域》（<http://sobereva.com/617>）。

Multiwfn可以计算BLA衡量环状或者链状体系中的键交替变化情况，见《使用Multiwfn计算Bond length/order alternation (BLA/BOA)和考察键长、键级、键角、二面角随键序号的变化》（<http://sobereva.com/501>）。

Multiwfn可以一次性导出分子所有内坐标数据，见<http://bbs.keinsci.com/thread-23029-1-1.html>。

Multiwfn可以根据原子间距离和原子半径根据特殊公式计算原子的配位数，见手册3.100.9节的介绍。

## 4 与原子有关的描述符

除了前面提到的以外，还有很多其它Multiwfn可以算的与原子有关的描述符，可以用于预测和解释局部特征，如局部反应能力、局部作用强度、局部酸/碱度等。

原子电荷有广泛的用处，也与很多问题关系密切，比如与静电作用强度密切相关、与NMR化学位移密切相关、与反应难易密切相关（J. Phys. Chem. A, 119, 8216 (2015)、J. Phys. Chem. A, 118, 3698 (2014)）、与反应位点密切相关（物理化学学报, 30, 628 (2014)、Sci. China Chem., 58, 1845 (2015)）。Multiwfn可以计算种类十分丰富的原子电荷，包括ADCH、Hirshfeld、Hirshfeld-I、VDD、Mulliken、修改的Mulliken（SCPA、Stout & Politzer、Bickelhaupt三种）、Löwdin、CM5、1.2*CM5、CHELPG和Merz-Kollmann拟合静电势、RESP、RESP2、AIM（也叫Bader电荷）、EEM、PEOE、MBIS。具体原理在Multiwfn手册3.9节有详细的介绍，在手册3.7节有许多例子。有一些原子电荷的计算也有专门的文章，AIM电荷计算见《使用Multiwfn做电子密度、ELF、静电势、密度差等函数的盆分析》（<http://sobereva.com/179>）；1.2*CM5电荷计算有快速的脚本，见《计算适用于OPLS-AA力场做模拟的1.2*CM5原子电荷的懒人脚本》（<http://sobereva.com/585>）；RESP/RESP2电荷有专门的文章和快捷脚本，见《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）、《计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）》（<http://sobereva.com/476>）、《RESP2原子电荷的思想以及在Multiwfn中的计算》（<http://sobereva.com/531>）。

Multiwfn可以计算原子的氧化态，见《使用Multiwfn通过LOBA方法计算氧化态》（<http://sobereva.com/362>）。Multiwfn在计算Mayer和Wiberg键级的时候会给出原子价和自由价，计算例子见手册4.9.1节。

Multiwfn可以计算原子的极化率、原子有效体积、原子和分子的C6色散系数，见《使用Multiwfn计算分子中的原子极化率》（http://sobereva.com/600）和《使用Multiwfn计算原子的C6色散系数》（<http://sobereva.com/709>）。

Multiwfn的AIM分析功能可以计算分子中原子的体积（以0.001 a.u.电子密度等值面为边界），见《使用Multiwfn做电子密度、ELF、静电势、密度差等函数的盆分析》（<http://sobereva.com/179>），在《使用Multiwfn和VMD绘制原子盆（AIM盆）》（<https://www.bilibili.com/video/av85202089>）视频里有直观的图形示意。

Multiwfn的模糊空间分析功能（主功能15）的主功能2可以计算原子的偶极矩、四极矩、八极矩。还可以对特定片段来算，参考《使用Multiwfn计算分子片段的偶极矩和复合物中单体的偶极矩》（<http://sobereva.com/558>）。模糊空间分析功能里的主功能1可以对Multiwfn支持的上百种实空间函数（见手册2.6、2.7节的介绍）在各个原子空间内积分，因此能得到原子的众多的描述符，比如可以在原子空间里积分局部温度、ELF、动能密度、能量密度、源函数等等。Multiwfn的模糊空间分析功能里支持Becke、Hirshfeld、Hirshfeld-I这些模糊式原子空间划分方式，Multiwfn也支持在AIM原子空间（也叫AIM原子盆）内积分这些函数，后者需要用主功能17盆分析模块来做，参考《使用Multiwfn做电子密度、ELF、静电势、密度差等函数的盆分析》（<http://sobereva.com/179>）以及手册4.17节的相关例子。

Multiwfn可以计算轨道成份，HOMO和LUMO轨道中各个原子以及原子轨道的成份尤为有意义，计算方法见《谈谈轨道成份的计算方法》（<http://sobereva.com/131>），另参考《利用布居分析判断基函数与原子轨道的对应关系》（<http://sobereva.com/418>）。

Multiwfn还可以计算各个原子核位置的任意实空间函数，有些有实际意义。比如原子电荷位置的自旋密度就和超精细耦合的费米接触项密切相关。原子核位置的静电势（扣除这个核产生的静电势的贡献）与pKa关系密切，见J. Comput. Chem., 39, 117 (2018)。在Multiwfn的子功能1里面输入诸如a4，就可以得到各种函数在4号原子核位置的值。

原子的能量指数（energy index, EI）在J. Phys. Chem., 94, 5602 (1990)中提出，后在J. Phys. Chem., 96, 157 (1992)中进行了进一步讨论。这个量体现的是某个原子上平均每个价电子的能量，和原子在分子中的电负性有密切联系。详细介绍见Multiwfn手册3.200.12节，在4.200.12节有计算例子。另外，基于两个原子的EI还可以计算它们间的键极性指数考察键的极性。

## 5 其它的描述符

分子的电荷分布特征可以通过电多极展开来描述。Multiwfn可以计算分子的偶极矩、四极矩、八极矩、十六极矩，见Multiwfn手册3.300.5节的介绍。

Multiwfn可以计算electronic spatial extent（电子空间范围） <r^2>，这是衡量分子的电子密度空间分布广度的一个很有用的量，而且与分子的（超）极化率有正相关性。Multiwfn不仅可以对这个体系计算这个量，还可以对原子计算它来衡量各个原子的电子空间分布广度的区别，详见《电子空间范围<r^2>和电子径向分布函数的含义以及在Multiwfn中的计算》（<http://sobereva.com/616>）。

量子化学计算完了就得到轨道信息，在里面可以读取HOMO、LUMO能级。在Multiwfn里提取HOMO、LUMO更为方便，载入诸如Gaussian的fch文件、ORCA的molden文件等，进入主功能0的时候屏幕上直接就显示了HOMO、LUMO能级，以及二者的差值，即HOMO-LUMO gap。

对各种轨道，包括最重要的HOMO和LUMO，Multiwfn做轨道成份分析时可以计算衡量轨道离域程度的ODI指数，对整个体系以及特定片段都可以算，见《通过轨道离域指数(ODI)衡量轨道的空间离域程度》（<http://sobereva.com/525>）。

Multiwfn可以计算d带中心，这是广为使用的催化方面的描述符，见《用Multiwfn计算过渡金属的d-band center（d带中心）》（<http://sobereva.com/582>）。以文中类似方法也可以计算诸如p带中心。

Multiwfn可以计算十分丰富的定量衡量整体或者局部芳香性的指标，比如HOMA、多中心键级、AV1245/AVmin、PDI、FLU、FLU-pi、香农芳香性等等，详见《衡量芳香性的方法以及在Multiwfn中的计算》（<http://sobereva.com/176>）。

Multiwfn还能计算大量与键有关的描述符，比如各种键级的数值、AIM理论定义的键临界点（bond critical point, BCP）位置的各种实空间函数的值、基于BCP性质定义的一些的量（如键椭率、bond degree、eta index、键金属性等等）、原子重叠空间内各种实空间函数的积分（诸如笔者提出的拉普拉斯键级就是基于这种思想定义的，涉及重叠空间内积分电子密度拉普拉斯函数）、键偶极矩，等等。大部分在《Multiwfn支持的分析化学键的方法一览》（<http://sobereva.com/471>）里都有介绍。

当孤对电子与当前研究的问题关系密切时，可以用Multiwfn计算ChemPhysChem, 14, 3714 (2013)中提出的ELF localization domain population and volume (HELP and HELV)，这是孤对电子的布居数和体积的一种定义。在原文里发现HELP与分子的电离能有很好的相关性。HELP和HELV的计算例子看Multiwfn手册的4.17.8节。

Multiwfn对芳环可以计算Chem. Commun., 48, 9239 (2012)中提出的LOLIPOP指数，与分子的pi-pi堆积能力有密切关系。笔者认为这对于考察诸如多环芳烃体系通过pi-pi堆积插入DNA导致致癌的毒性有密切关系，因此也是个有用的描述符。LOLIPOP的计算看Multiwfn手册4.100.14节的例子。

Multiwfn可以可以基于Gaussian的输出文件提取和进一步计算一大堆与(超)极化率有关的量。它们体现体系对外电场的响应，也是重要的分子描述符。详见《使用Multiwfn分析Gaussian的极化率、超极化率的输出》（<http://sobereva.com/231>）和《使用Multiwfn计算与超瑞利散射(HRS)实验相关的量》（<http://sobereva.com/499>）。

Multiwfn的子功能100的子功能4可以利用Becke的多中心积分算法对Multiwfn支持的上百种实空间函数（看手册2.6、2.7节的介绍）在全空间进行积分，一些函数的积分结果可以作为分子描述符，这个功能的具体介绍看手册3.100.4节，例子见4.100.4节。而且用户还可以非常方便地自己修改源代码定义新的用户自定义的被积函数，做法见手册2.7节开头，然后使用功能100的子功能4时被积函数选择用户自定义函数，即可在全空间积分自己定义的新函数，可见极度灵活！

刘述斌等人将信息论和密度泛函理论中的概念相结合用于广泛的化学问题的研究，提出了Information-theoretic approach (ITA)的思想，并定义了许多定量指标，综述见Acta Phys. -Chim. Sin., 32, 98 (2016)（<http://dx.doi.org/10.3866/PKU.WHXB201510302>）和WIREs Comput Mol Sci., 10, e1461 (2019)（<https://doi.org/10.1002/wcms.1461>）。Multiwfn可以计算ITA中的各种对分子或整体定义的量，计算方法笔者汇总在了《Calculating information-theoretic quantities and some relevant quantities by Multiwfn》文档里（<http://sobereva.com/multiwfn/res/ITA.pdf>），这些量都可以作为描述符。

刘述斌在J. Chem. Phys., 126, 244103 (2007)提出了一种能量分解思想，将体系总能量拆分为steric、electrostatic、quantum三部分，并被用于诸多问题的研究，详见Multiwfn手册3.24.2节的介绍，在手册4.21.2节有这种分析的具体例子。Multiwfn做这个分析的时候还会把大量中间涉及到的能量成分都会输出出来，都可以考虑直接或间接（比如取比值）作为分子描述符。
