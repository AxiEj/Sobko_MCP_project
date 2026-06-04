---
post_id: 486
title: Multiwfn 3.6正式版隆重发布！
url: http://sobereva.com/486
date: '2019-05-21T15:53:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 Multiwfn 3.6 正式版发布，属于软件发布信息。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**Multiwfn 3.6正式版隆重发布！**

The official version of Multiwfn 3.6 is grandly released!

文/Sobereva @[北京科音](http://www.keinsci.com)  2019-May-21

Multiwfn的上个正式版3.5是2018年4月16日发布的，经过近一年有余的不断改进和完善，Multiwfn 3.6正式版终于正式发布！目前已经可以在官网上<http://sobereva.com/multiwfn>下载。

近一年来Multiwfn更新极度频繁，带(dev)后缀的开发版在Multiwfn官网上甚至有时候一天就能更新两次。各种最新改进始终体现在官网上的update history页面里，到今日3.6正式版发布为止，各种新功能和改进合计已经有约一百条，可以说有了飞跃性的进步。强烈所有Multiwfn用户立刻更新到3.6版！

随着程序的进步，手册也在不断地扩充、完善，为此花费了极大的精力，3.5版手册是522页，而3.6正式版的手册已达717页。由于手册已经很庞大，为了让新用户可以快速从中找到做自己需要的分析对应的章节，特意在可执行文件包里增加了quick start文档，用户可以迅速从中查到自己要做的分析在哪一节有详细介绍、在哪一节有具体例子。还专门撰写了《Multiwfn FAQ》（<http://sobereva.com/452>），汇总了所有Multiwfn用户常见问题。

相对于3.5版，完整的更新列表在此文末尾给出了。所有更新中，意义比较大的和值得一提的，我在下面罗列一下。

• 增加了超级方便的一次性把几乎所有概念密度泛函理论里定义的量一次性全都输出的功能，比如福井函数、双描述符、软度、电负性、亲电指数等等，把需要算这些量的研究者从繁重的手工操作中大为解放，还避免了算错的可能。详见《使用Multiwfn超级方便地计算出概念密度泛函理论中定义的各种量》（<http://sobereva.com/484>）  
• 支持了RESP电荷计算。Multiwfn的RESP电荷计算功能在我来看已经做得完美了，非常灵活，操作步骤极为简单，结合cubegen计算RESP电荷非常快，远比antechamber，尤其是R.E.D好用得多，算是称作RESP电荷计算的革命我觉得也不为过。相关文章：《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）、《计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）》（<http://sobereva.com/476>）  
• 支持了基于力场的能量分解，可以用于非常大的体系的能量分解，还能随意定义片段、图形化展现原子对作用能的贡献，是很有用的功能。见《使用Multiwfn做基于分子力场的能量分解分析》（<http://sobereva.com/442>）  
• Multiwfn已可以在做静电势相关分析的时候调用Gaussian里的cubegen，这对大体系的静电势分析的耗时甚至能降低一个乃至两个数量级，对于常做静电势相关分析的用户至关重要。见《Multiwfn现已可以调用cubegen使静电势分析耗时有飞跃式的下降！》（<http://sobereva.com/435>）  
• Multiwfn支持了对非限制性开壳层波函数做双正交化，使得这类波函数在讨论的时候能够像RO波函数一样方便，不再需要考虑alpha和beta两套轨道，在讨论双自由基特征等场合也非常有用。详见《用于非限制性开壳层波函数的双正交化方法的原理与应用》（<http://sobereva.com/448>）  
• 支持了core-valence bifurcation (CVB)指数，对于研究氢键很有帮助，见《使用Multiwfn计算CVB指数考察氢键强度》（<http://sobereva.com/461>）  
• 在轨道定域化分析功能上做了很多扩展。可以给出所有轨道质心的位置，从图上一看就知道哪个LMO出现在哪，非常直观，省得一个一个看轨道了。而且还可以给出LMO的偶极矩、研究键的极性，见更新后的《Multiwfn的轨道定域化功能的使用以及与NBO、AdNDP分析的对比》（<http://sobereva.com/380>），以及《Multiwfn支持的分析化学键的方法一览》（<http://sobereva.com/471>）。在做完轨道定域化之后自动输出轨道成份时，计算成份的方法改为了可靠得多的Hirshfeld方法  
• 考察氧化态的LOBA方法用的轨道成分分析方法改为了比原先用的SCPA可靠得多的Hirshfeld方法，由于SCPA方法不可靠而导致的原先个别计算不理想的体系如OsO4的结果已经完全合理，见更新后的《使用Multiwfn通过LOBA方法计算氧化态》（<http://sobereva.com/362>）  
• 增加了绘制光电子谱的功能，见《使用Multiwfn绘制光电子谱》（<http://sobereva.com/478>），是很多研究者急需的功能  
• 给Multiwfn增加了脚本，可以极其方便快捷地获得效果绝佳的分子轨道图，见《使用Multiwfn+VMD快速绘制高质量分子轨道等值面图（含视频演示）》（<http://sobereva.com/447>），特别是《用VMD绘制艺术级轨道等值面图的方法（含演示视频）》（<http://sobereva.com/449>）  
• 给Multiwfn增加了脚本，可以非常简单快速地获得效果十分理想的静电势着色的分子表面图，见《使用Multiwfn+VMD快速地绘制静电势着色的分子范德华表面图和分子间穿透图（含视频演示）》（<http://sobereva.com/443>）  
• Multiwfn已支持了Grimme的xtb程序输出的波函数，这开启了巨大体系波函数分析的大门，这在此文里已经体现出来了：《巨大体系的范德华表面静电势图的快速绘制方法》（<http://sobereva.com/481>）  
• 显著改进了态密度（DOS）绘制功能。支持了基于Hirshfeld和Becke方式计算轨道成份。对非限制性波函数已可以将alpha和beta轨道一起考虑。在绘图效果方面做了不少改进，还增加了不少选项可以更灵活地设定作图参数。目前在定义片段时可以直接根据角动量来定义。见《使用Multiwfn绘制态密度(DOS)图考察电子结构》（<http://sobereva.com/482>）  
• Multiwfn的自动识别pi轨道的功能有了质的飞跃，现已可以对非平面体系识别定域化的pi轨道，从而非常方便地考察pi电子的各种特征，详见《在Multiwfn中单独考察pi电子结构特征》（<http://sobereva.com/432>）。另外，此功能还可以计算任意轨道的pi成份，实际意义很大，见《Multiwfn已支持计算任意轨道的pi成份》（<http://bbs.keinsci.com/thread-13110-1-1.html>）  
• 可以导出pqr格式的文件，使得结合VMD时可以根据Multiwfn计算的各种原子属性进行着色，见《使用Multiwfn+VMD以原子着色方式表现原子电荷、自旋布居、电荷转移、简缩福井函数》（<http://sobereva.com/425>）  
• 支持了计算分子长宽高和直径的功能，见《使用Multiwfn计算分子的长宽高以及显示分子的主轴》（<http://sobereva.com/426>）  
• Multiwfn绘制光谱的模块得到了改进。已经可以绘制拉曼光学活性光谱（ROA），见《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（<http://sobereva.com/224>）。还支持基于ORCA的SOC-TDDFT输出文件绘制考虑旋轨耦合的光谱，见《使用ORCA在TDDFT下计算旋轨耦合矩阵元和绘制旋轨耦合校正的UV-Vis光谱》（<http://sobereva.com/462>）。基于Gaussian非谐振计算的输出文件绘制光谱时已可以包含合频和泛音。结合新添加的脚本可以超级容易地批量绘制光谱，见《使用Multiwfn一键批量产生各类光谱图（含演示视频）》（<http://sobereva.com/479>）  
• Multiwfn已支持了超过20种动能泛函，详见手册2.7节  
• Multiwfn的MK和CHELPG计算模块现已可以考察任意读入的原子电荷对静电势的重现性，还可以借助VMD图形化展现，见手册4.7.8节。这对于关注原子电荷的研究者挺有帮助  
• 支持了在ACS Omega, 3, 18370 (2018)新提出的基于信息理论定义的芳香性指数，见手册3.18.11节  
• 球对称平均的ELF和LOL现已可以计算，这可以用于做J. Comput. Chem., 38, 2258 (2017)和J. Phys. Chem. C, 123, 4407 (2019)中提出的DFT泛函的ELF调控、LOL调控。见3.100.4节  
• 支持了刘述斌教授在J. Chem. Phys., 126, 244103 (2007)中提出的能量分解方法，见3.24.2节的介绍和4.21.2节的例子  
• 结合VMD已可以绘制漂亮的填色Hirshfeld/Becke表面图，对于研究弱相互作用，特别是晶体分子中的弱相互作用极其有用，见《使用Multiwfn结合VMD绘制Hirshfeld surface图分析分子晶体中的弱相互作用》（<https://www.bilibili.com/video/av35738671/>）  
• Multiwfn绘制平面图的功能已经支持对绘制内容平移和旋转，详见<http://bbs.keinsci.com/thread-11037-1-1.html>  
• 在很多显示三维结构的界面上增加了设置光源、标签类型、字体颜色等设定的选项，图像效果不好、标签看不清楚等问题得到了极大的避免  
• Multiwfn的显示效果得到了不少改进，保存出的图像的字体明显比原先舒服了很多  
• 拓扑分析的键径产生功能做了并行化，速度有了飞跃  
• 支持了将某个点（比如可以是AIM分析的BCP位置）的实空间函数值分解为任意类型轨道贡献的功能，如果结合定域化轨道，有点类似于NBO的NBCP分析。见手册4.2.4节的例子  
• 扩充了域分析功能使之更为灵活，比如可以用来考察分子孔洞的特征，见《使用Multiwfn可视化分子孔洞并计算孔洞体积》（<http://sobereva.com/408>）  
• 改进了拓扑分析功能，使之变得灵活得多。产生键径后，可以要求只保留特定片段间的键径和BCP而删除其它的。选项-1设定临界点搜索参数的界面里增加了子选项10，可以要求搜索临界点时只考虑特定原子构成的区域。选项-4中的删除临界点功能可以根据类型和与分子片段的距离进行删除。手册4.2.6节的例子对这些改进有所体现。  
• 通过脚本可以将Multiwfn与VMD联用，非常简单快速地绘制出效果特别理想的临界点+拓扑路径图，见《使用Multiwfn+VMD快速地绘制高质量AIM拓扑分析图（含视频演示）》（<http://sobereva.com/445>）  
• 用主功能1里计算原子核位置的属性时，会直接给出扣除这个原子的核对静电势贡献后的静电势，这对于研究很多问题有用，比如预测和解释pka、基于单体和二聚体状态下原子核位置静电势的改变量预测结合能（见手册4.1.2节）  
• mol、gjf和chk文件现在都可以直接作为输入文件，省得载入前还得转换。关于chk的情况见<http://bbs.keinsci.com/thread-12912-1-1.html>  
• 支持了非正交格子的cube文件，但仅限于通过主功能13做格点数据间相互运算以及导出cube文件的功能  
• 支持了对ORCA常见类型任务产生输入文件的功能，详见《Multiwfn已经可以产生ORCA中最常用计算级别的输入文件》（<http://bbs.keinsci.com/thread-13109-1-1.html>）。一个实际应用例子见《Simulating UV-Vis and ECD spectra using ORCA and Multiwfn》（<http://sobereva.com/485>）  
• 对一些功能显著提升了效率，比如大体系的CDA分析

在电子激发分析方面，3.6版可以说是有了翻天覆地的改进！功能总量是原先的约三倍，原有代码也大幅度改写。相关重要新功能和改进实在太多，就不逐一说明了，请阅读《Multiwfn支持的电子激发分析方法一览》（<http://sobereva.com/437>）。

在下一个Multiwfn大版本中，预计加入自然布居分析（NPA）功能，届时Multiwfn依赖于NBO程序输出信息的那些功能，比如基于NAO做轨道成分分析、AdNDP分析、Wiberg键级分解为原子轨道作用等，也预计将能够独立使用而不再依赖于NBO。

Multiwfn的开发离不开广大用户的支持，希望继续用户们积极关注Multiwfn的开发，多向周围研究者推广，使得Multiwfn的价值能更充分地发挥出来。

## NEW FUNCTIONS

- A very powerful and easy-to-use RESP module is added into main function 7 (Population analysis). It can calculate the well-known ElectroStatic Potential (RESP) charge proposed in J. Phys. Chem., 97, 10269 (1993), and can also calculate ESP fitting charges under various customized conditions such as atomic equivalence constraint and fragment charge constraint. Multiple conformation is fully supported. See Section 3.9.16 for detailed introduction and Section 4.7.7 for examples. This module should be able to bring a revolution in the field of RESP charge derivation.
- Energy decomposition analysis based on UFF/AMBER/GAFF molecular forcefield is supported as subfunction 1 of main function 21. See corresponding introduction in Section 3.24.1 and examples in Section 4.21.1 of the manual.
- A new parameter "cubegenpath" is introduced into settings.ini file. If the parameter is set to actual path of cubegen utility of Gaussian package and the input file is .fch/fchk type, for most analyses of electrostatic potential (ESP), such as plotting plane map of ESP, molecular surface analysis of ESP, the ESP data will be calculated using cubegen instead of internal code of Multiwfn, the overall computational time will be significantly reduced, especially for large systems (since speed of calculating ESP by cubegen is evidently faster than current version of Multiwfn). See Section 5.7 of manual for detail.
- If .chg file is used as input file, now it can be converted to .pqr file using subfunction 2 of main function 100. The .pqr file can be directly loaded into VMD. This feature is very useful if you want to vividly exhibit atomic properties (e.g. atomic charges, atomic spin populations, condensed Fukui function) calculated by Multiwfn by means of coloring atoms. See Section 4.A.10 of the manual for illustration.
- Subfunction 21 of main function 100 is extended, now it can easily calculate molecular length/width/height and diameter. See Section 4.200.21 of the manual for example.
- Raman optical activity (ROA) spectrum now can be plotted via main function 11 based on Gaussian output file, see Section 3.13 for detail and Section 4.11.7 for example.
- Almost all kinds of kinetic energy density (more than twenty) have been supported by Multiwfn as user-defined function 1200. See corresponding part of Section 2.7 of the manual for detail.
- Option -3 is added to MK and CHELPG charges calculation module, by using it, it is able to examine electrostatic potential reproducibility of given atomic charges around the whole system or around specific region, see Section 4.7.8 for example.
- Biorthogonalization between alpha and beta orbitals is supported as subfunction 12 of main function 100. For UHF or UKS wavefunction, after applying this transformation, alpha orbitals will be almost perfectly paired with beta orbitals, so that you no longer need to separately discuss two set of spin orbitals, this makes analysis of orbitals much easier. See Section 3.100.12 for introduction and 4.100.12 of example.
- The aromaticity index defined based on information-theoretic quantities in *ACS Omega*, **3**, 18370 (2018) has been supported as subfunction 12 of main function 15. See Section 3.18.11 for detail.
- The core-valence bifurcation (CVB) index, which is a useful quantity of distinguishing strength and classifying H-bonds, now is supported as subfunction 1 of main function 200, see Section 3.200.1 for introduction and example.
- In main function 19, center position of localized molecular orbitals (LMOs) can be given and directly visualized, see updated Section 4.19.1 for example. In addition, dipole moment of LMOs and bond polarity now can be studied, see Section 4.19.4 for example. Introduction of related theories have been added to Section 3.22.
- The spherically symmetric average ELF and LOL now can be calculated by subfunction 4 of main function 100, see Section 3.100.4 for detail. These quantites are key ingredient of the ELF-tuning and LOL-tuning, which were proposed in J. Comput. Chem., 38, 2258 (2017) and J. Phys. Chem. C, 123, 4407 (2019), respectively.
- A "quick start" document has been added into binary package, it should be particularly useful for new Multiwfn users, since via this they can quickly find needed information for performing common analyses.
- The energy decomposition method proposed by Shubin Liu in J. Chem. Phys., 126, 244103 (2007) has been supported as subfunction 2 of main function 21. Please check Section 3.24.2 for introduction and Section 4.21.2 for example.
- The density-of-states (DOS) plotting module now has a special interface aiming for easily plotting photoelectron spectrum (PES) based on (generalized) koopmans theorem, see Section 3.12.4 for introduction and Section 4.10.4 for example.
- Subfunction 22 of main function 100 has been significantly extended, now it can automatically detect pi orbitals based on localized molecular orbitals for both planar and non-planar systems; moreover, pi composition of any kind of orbitals can be evaluated. This feature makes separate study of sigma and pi electrons extremely easy for any system. See Section 3.100.22 of the manual for detail and Section 4.100.22 for illustrative application.
- Subfunction 16 has been added to main function 100, it can automatically calculate all important quantities defined in the framework of conceptual density functional theory via minimal steps (including Fukui function and dual descriptor as well as their condensed form, Mulliken electronegativity, hardness, electrophilicity and nucleophilicity index, softness, local softness, relative electrophilicity and nucleophilicity, etc.)

# UPDATES ABOUT ELECTRON EXCITATION ANALYSIS MODULE

Numerous improvements and changes have been made for main function 18, they are summarized as follows. At the meantime, the corresponding sections of the manual have been significantly rewritten.

- Hole-electron analysis module has been significantly rewritten. Definition of some indices have been changed and the result will be different to older version. This module now supports a new definition for measuring overlap between hole and electron, it is named as Sr, while the old one is named as Sm. Basis function, atom and fragment contribution to hole and electron distribution now can be directly printed. In addition, atom and fragment contribution can be vividly plotted as heat map. See Section 3.21.1 for introduction and Section 4.18.1 for example.
- The Λ (Lambda) index proposed in J. Chem. Phys., 128, 044118 (2008) has been supported as subfunction 14 of main function 18, it has been prevalently employed in literatures to determine type of electron excitations. See Section 3.21.14 for introduction.
- By newly added subfunction 13 of main function 18, natural orbitals for a batch of selected excited states can be generated and exported to .molden file. See Section 3.21.13 for detail and Section 4.18.13 for example.
- The transition density matrix plotting function (subfunction 2 of main function 18) now can plot fragment based TDM map. In addition, this function now can automatically generate TDM between ground state and selected excited state and thus becomes much easier to use. See Section 3.21.2 for introduction and Section 4.18.2 for example.
- The function of generating transition density matrix (TDM) has been moved to subfunction 9 of main function 18. At the meantime, this function now supports generating TDM between two selected excited states.
- Definition of some quantites outputted by subfunction 3 of main function 18 (Analyze charge-transfer based on density difference grid data) has been modified to make the result more meaningful, see Section 3.21.3 for detail.
- Delta_r index now can be calculated for a batch of excited states at one time (subfunction 4 of main function 18).
- Speed of calculating transition electric dipole moment between excited states (subfunction 5 of main function 18) has been remarkably improved.
- In the function "Calculate interfragment charge transfer in electron excitation via IFCT method" (subfunction 8 of main function 18), a batch of fragments now can be simultaneously defined and the result between all fragments are outputted together. Notice that the equation used in this function in older version is incorrect, this problem has been fixed. See Section 3.21.8 for introduction of this method and Section 4.18.8 for example.
- The function "Generate transition density matrix" has been moved to subfunction 9 of main function 18 from hole-electron analysis module. At the meantime, speed of this function was significantly improved.
- The function "Decompose transition electric dipole moment as molecular orbital pairs contribution" has been moved to subfunction 10 of main function 18 from hole-electron analysis module. At the meantime, speed of this function was significantly improved, and the terms can be sorted and outputted according to contribution to transition dipole moment.
- The function "Decompose transition dipole moment as basis function and atom contributions" has been moved to subfunction 11 of main function 18 from hole-electron analysis module.
- The function "Check, modify and export configuration coefficients of an excitation" has been moved to subfunction -1 of main function 18 from hole-electron analysis module. In addition, this function now can export user-modified configuration coefficients to an external file, which can then be directly used as input file for all subfunctions in main function 18.
- Output files of TDDFT task of Firefly and GAMESS-US programs are fully supported as input file for all kinds of electron excitation analyses, see beginning of Section 3.21.
- Option 4 is added to subfunction 5 of main function 18. This option is able to calculate dipole moment for all excited state at once.
- Generating transition density and transition dipole moment density between two excited states is available now, see Section 4.18.2.3 for example.

## IMPROVEMENTS AND CHANGES

- Calculation speed of charge decomposition analysis for large systems has been significantly improved.
- Section 4.A.13 has been added to manual, it describes how to very easily plot pretty ESP colored molecular vdW surface map as well as penetration map of monomer vdW surface in VMD program based on output file of Multiwfn.
- Section 4.2.5 has been added to the manual, it describes how to very easily plot pretty AIM critical points and topology paths in VMD program based on output file of Multiwfn.
- In the MK and CHELPG module, if option 6 as been chosen once, then after calculation, fitting points with exact ESP value or absolute difference between the exact ESP and the ESP evaluated by atomic charges can be exported to .pqr file, which can be directly render in VMD. The example in Section 4.7.8 utilized this feature.
- Algorithm detail of ADCH atomic charge has been changed, see Section 3.9.9 of the manual for detail. If the system has local planar (or almost planar) regions, the ADCH charges in these regions obtained via the new version may be different to those obtained via older versions. The result produced by the new version should be more reasonable. Similarly, the result of atomic dipole moment corrected Becke charges is also different to the older versions.
- .pqr file is supported as input file. For Multiwfn, the information provided by .pqr and .chg is the same, namely atom information as well as atomic charges, see Section 2.5 of the manual.
- Output file of Firefly has been experimentally supported. After changing the suffix of output file of Firefly to .gms, the file can be directly loaded into Multiwfn to provide wavefunction information.
- Molden input file produced by NWChem has been formally supported. See beginning of Chapter 4 of the manual on how to properly generated it.
- Option 8 is added to post-process menu of main function 4 for most kinds of plane maps. Using this option, chemical bonds can be drawn on the graph as straight lines.
- When using Independent Gradient Model (IGM) anaylsis, if your input file contains wavefunction information, the program will let you choose the kind of the sign(lambda2)rho to be used, the first one is that based on actual electron density, the second one is that based on promolecular density.
- Section 4.7.6 is added to the manual, in which I discussed how to easily determine correspondence between basis functions and atomic orbitals via Mulliken population analysis.
- Section 4.4.9 is added to the manual to illustrate how to plot LOL-pi map for porphyrin to reveal favorable electron delocalization path.
- Section 4.2.4 is added to the manual to illustrate how to decompose properties at a critical point or given point as orbital contributions.
- Interface of Mulliken population analysis (MPA) is improved, meantime Section 4.7.0 is added to the manual to illustrate the use of MPA.
- When outputting vtx.pdb in post-process menu of quantitative molecular surface analysis, for electrostatic potential analysis, if value at any surface vertex exceeded recording limit of B-factor field of .pdb file, eV will be used instead of kcal/mol.
- Content of Section 4.12.7 of the manual has been replaced, now it corresponds to a newly added example, namely illustrating how to predict density of molecular crystal based on result of quantitative molecular surface analysis
- Section 4.17.1 of the manual is extended to illustrate how to carry out AIM basin analysis for the systems containing pseudoatoms (non-nuclear attractors of electron density)
- After integrating specific domain in domain analysis module (subfunction 14 of main function 200), minimum and maximum X/Y/Z of points belonging to the domain, as well as span distance in X/Y/Z will be outputted. In addition, option 11 is added to post-process menu, which is used to export boundary grids of specific domain to a .pdb file, so that you can easily use such as VMD program to measure size of the domain. These updates are quite useful for characterizing molecular cavity (see Section 4.200.14.2 of the manual)
- In the interface of defining fragments for plotting PDOS and OPDOS, the fragments now can be directly defined according to angular moment of atomic orbital. Meantime, the DOS plotting example in Section 4.10 has been extended to reflect this improvement
- Subfunction 28 is added to wavefunction modification module (main function 6), it is used to modify orbital energies. This function is useful when you want to rectify the orbital energies using a given relationship (e.g. J. Am. Chem. Soc., 121, 3414 (1999)) before plotting density-of-states (DOS) map.
- Section 4.A.7 has been added to the manual to show how to study polarizability and hyperpolarizability densities by Multiwfn. This method is important for studying local contribution to (hyper)polarizability.
- Section 4.9.5 has been added to the manual to illustrate the usefulness of decomposition analysis of Mulliken bond order.
- The atomic radii used in MK and CHELPG charge fitting now can be set via option 10 in corresponding interface. The default radii of Na, Mg, Al, Si used in MK fitting have been modified (the older ones are not quite reasonable).
- Options 7 and 8 are added to post-process menu of IGM module. They are used to set delta_g and delta_g_inter where sign(lambda2)rho is out of specific range. Obviously, by these options you can screen unwanted regions from isosurface map of delta_g and delta_g_inter map.
- "imodlayout" in settings.ini now can be set to 2, the layout of all GUI will be very suitable for 1024*768 resolution.
- The option "2 Delete some CPs" in subfunction -4 of topology analysis module has been significantly extended, now it can also delete CPs according to type and distance to a given molecular fragment.
- Using the newly added option "10 Set the atoms to be considered in searching modes 2, 3, 4, 5" in subfunction -1 of topology analysis module, one can only search CPs in a given molecular region.
- Subfunction 9 of main function 100 now can evaluate and print index for measuring interatomic connectivity.
- When calculating AdNDP and LMO orbital energies, Fock matrix now can be directly loaded from $FOCK field of NBO .47 file.
- Generation of path in topology analysis module has been parallelized, the speed is improved significantly!
- New parameter "plotwinsize3D" has been added to settings.ini, it controls the size of the plotting region for 3D objects in GUI
- The .fchk files generated by PSI4 since 1.2 have been formally supported, and the way of analyzing CCSD(T) wavefunction generated by PSI4 has been changed, see Section 4.A.8 for detail.
- When showing orbital list in console window via "Orbital info." option of main function 0, for beta orbitals, now the index counted from the first beta orbital is also shown.
- Main function 11 now is able to plot spin-orbit coupling corrected (SOC) UV-Vis and ECD spectra based on SOC-TDDFT calculation of ORCA 4.1. See Section 3.13.2 of detail and Section 4.11.6 for example.
- In main function 1, when you request Multiwfn to print properties at nuclear position of an atom, the electrostatic potential without contribution of nuclear charge of this atom now is simultaneously printed (this quantity at hydrogen site is useful in pKa studies, because it measures binding strength between this proton and rest of the system). Due to this update, the procedure of the example in Section 4.1.2, which introduces how to predict intermolecular interaction energy based on ESP at nuclear position, has been significantly simplified.
- Thickness of lines/curves/axes/texts in spectrum plotting module (main function 11) now can be set by the newly added option 22.
- The molden input file generated by Grimme's xtb code has been supported.
- In the GUI windows showing 3D objects, now one can zoom in and zoom out the perspective by rotating mouse wheel on the drawing region.
- In the GUI of showing structure and orbitals (main function 0), the "Other settings" in the menu bar has been extended significantly. Its options now is able to choose atomic label type, atomic label color, set lighting and select predefined drawing style (CPK, vdW, line)
- In the GUI of topology analysis, label color of critical points and atoms now can be set via "Set label color" in the menu bar.
- Section 4.A.11 is added to the manual, this section presents an overview of all methods supported by Multiwfn that can be used to discuss chemical bonds.
- .gjf is now supported as input file, it can provide atomic coordinate information to Multiwfn.
- Magnitude of electric field is added as the 103th user-defined function.
- .mol2 is supported as input file.
- .chk file can be directly loaded as long as you have set "formchkpath" in settings.ini to actual path of formchk executable file in Gaussian package.
- Section 4.11.8 is added to the manual, it describes how to extremely easily plot spectrum for a batch of files via shell script
- For unrestricted wavefunction, now one can plot various kinds of DOS maps for alpha and beta spin simultaneously. The spin can be chosen via option 6 in DOS plotting interface.
- cube file with non-rectangle grid now can be loaded, however, in this case only the grid data calculation function in main function 13 could be normally used.
- In the AdNDP module, the option used to export cube files has been improved.
- The rarely used subfunction 7 of main function 100 is removed. Instead, when user export Gaussian .gjf using the subfunction 2 of main function 100 and meantime wavefunction is presented, the wavefunction can be written into the .gjf as initial guess.
- The interface of outputting ORCA input file (option 12 of subfunction 2 of main function 100) now is able to specify commonly used level and type of task.
- The function for calculating intermolecular orbital overlap integral is no longer limited for Gaussian users, see updated Section 3.100.15 of manual for detail.
- The default integration grid for computing orbital composition via Hirshfeld/Hirshfeld-I/Becke has been slightly changed to make result evidently more accurate for orbitals showing Rydberg character
- In the orbital localization module (main function 19), now Hirshfeld is employed as the default method to automatically compute composition of the resulting LMOs, it is more robust than the Mulliken+SCPA method used in earlier verison and compatible with diffuse functions.
- The method of calculating orbital composition for LOBA analysis has been changed to Hirshfeld, which is more robust than the SCPA method used in earlier version.
- In the DOS plotting module (main function 10), Hirshfeld and Becke methods have been supported for calculating orbital compositions, which are more robust than the Mulliken/SCPA method used in earlier version and compatible with diffuse functions. See Part 6 of Section 4.10.1 for example.
- More options have been added to the post-process menu of DOS plotting module to make it more flexible, and many improvements have been made to make graphical effect better.
- A section 4.A.14 has been added to manual, it introduces a way of very easily rendering cube files produced by Multiwfn as state-of-the-art isosurface map via VMD script.
- Option 13 has been added to post-process menu of quantitative molecular surface analysis module. Via this new option one can easily plot pretty color-mapped Hirshfeld/Becke surface isosurface via VMD program to illustrate intermolecular interactions, see updated Section 4.12.6 for example.
- Overband and combination band of IR, VCD and Raman spectra now can be plotted by main function 11 based on output file of corresponding Gaussian anharmonic tasks.
- Option -1 has been added to the plotting plane definition interface of main function 4. By this option you can set translation and rotation of the plotting plane. This point has been mentioned in Section 3.5.2 of the manual, a practical instance of using this option was posted on http://bbs.keinsci.com/thread-11037-1-1.html.
- Subfunction 8 is added to option -5 of topology analysis module, it is used to only retain bond paths (and corresponding BCPs) connecting two fragments but remove all other bond paths, so that one can more easily study interfragment interactions via AIM method. See Section 4.2.6 for illustration this option.

## BUG FIXED

- Fixed a fatal bug in the calculation of beta, gamma and delta via sum-over-states (SOS) method. This bug was introduced since version 3.5.
- Due to some bugs in EDFlib library, (3,+3) rather than (3,-3) type of AIM critical points are located at nuclear position for some elements when pseudopotential is employed. This problem has been fixed via updating EDFlib.
- When drawing spectra for multiple systems based on .dat file outputted by Grimme's sTDA program, Multiwfn crashes. This problem has been fixed.
- When custom operation involves "+" operator, the program doesn't work. This problem has been fixed, thanks jimkress for reporting.
- GAMESS-US output file cannot be loaded properly when pseudopotential is used, this problem has been solved, thanks PedroS for reporting.
- The sign of Coulomb attractive energy (exciton binding energy) outputted by hole-electron analysis module has been inverted, now this quantity is always positive to in line with literature convention.
- Local DOS map for beta part of unrestricted wavefunction is incorrect, this problem has been fixed.
