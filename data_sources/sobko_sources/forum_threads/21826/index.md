---
thread_id: 21826
source_id: forum_thread:21826
title: "使用Multiwfn做aNCI分析图形化考察动态过程中的蛋白-配体间的相互作用"
url: http://bbs.keinsci.com/thread-21826-1-1.html
date: "2021-01-01T00:00:00+08:00"
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: wsl2_chrome_cdp_verified_session
source_crawled_at: "2026-06-05T09:57:27.805Z"
original_reply_count: 8
page_count: 1
views: 28295
software_tags:
- Multiwfn
topic_tags:
- 波函数分析
- 弱相互作用
- 可视化
- 综述/教程/投稿经验
authority_level: B
confidence: 0.97
classification_reason: sobereva教程，使用Multiwfn的aNCI方法分析动力学中的蛋白-配体相互作用。
---

# 使用Multiwfn做aNCI分析图形化考察动态过程中的蛋白-配体间的相互作用

- 原帖 URL：<http://bbs.keinsci.com/thread-21826-1-1.html>
- 论坛板块：分子模拟
- 作者：**sobereva**
- 浏览量：28295 | 回复数：8 | 共1页
- 完整性：**全部内容已完整抓取**。

## 楼层正文

### 1 楼（楼主）｜sobereva

后记：笔者于2025年提出的amIGM方法比aNCI好太多，完全取代了aNCI，因此aNCI分析已经完全没必要再使用了，本文已经没有任何意义了！强烈建议阅读《使用amIGM方法图形化直观展现动态过程中的平均弱相互作用》（http://sobereva.com/759）了解amIGM方法的特点以及在Multiwfn中的使用方法！





使用Multiwfn做aNCI分析图形化考察动态过程中的蛋白-配体间的相互作用Using Multiwfn to perform aNCI analysis to graphically study protein-ligand interactions in dynamic process



文/Sobereva@北京科音First release: 2021-Mar-4  Last update: 2022-Feb-22



1 前言



《使用Multiwfn图形化研究弱相互作用》（http://sobereva.com/68）介绍的NCI方法是如今用得非常普遍、广为流行的图形化研究弱相互作用的方法，后来我又在《使用Multiwfn研究分子动力学中的弱相互作用》（http://sobereva.com/186）中介绍了averaged NCI（aNCI）方法，可以把动态过程中的平均化的相互作用予以直观展现。aNCI对于研究蛋白和配体间的相互作用非常有价值，但那篇文章里我没给出具体例子，估计有用户实现起来会遇到一些技术上的困难，不过也有不少用户已经很好地用Multiwfn做了这种分析讨论了蛋白-配体结合问题，比如PLoS ONE, 13, e0196651 (2018)。本文的目的是详细演示如何在Multiwfn中做aNCI分析来清晰直观地展现蛋白和配体之间的弱相互作用，让所有用户都可以顺利地运用这种分析研究实际问题。aNCI的原理在本文就不再累述了，请先仔细阅读《使用Multiwfn研究分子动力学中的弱相互作用》了解相关背景知识。并且非常推荐阅读《一篇最全面介绍各种弱相互作用可视化分析方法的文章已发表！》（http://sobereva.com/667）介绍的笔者的综述文章，其中含有对aNCI的详细介绍并给出了典型的应用例子。



PS：虽然ligplot和ProteinPlus中的PoseView等程序也能以二维图的方式展现配体与蛋白各残基的相互作用，但那种展现方式过于抽象，不能体现三维空间关系，而且也不能体现实际动态环境的情况，局限性极大。用aNCI则严格得多、给出的信息丰富得多。



读者请使用2021年3月4日及以后更新的Multiwfn版本，否则有的地方和本文所述不符。Multiwfn可以在http://sobereva.com/multiwfn免费下载。本文用的VMD是1.9.3版，可以在http://www.ks.uiuc.edu/Research/vmd/免费下载。本文的例子是相关分子动力学与 GROMACS 教程（[已省略培训课程链接]）中我讲蛋白质-配体复合物模拟的3ATL那个例子，此体系结构如下










1.png (157.85 KB, 下载次数 Times of downloads: 245)

下载附件 Download



2021-3-4 04:01 上传 Uploaded










对这类蛋白-配体复合物体系做aNCI分析总流程是：

(1)将配体位置冻结，做一段动力学模拟

(2)将配体连同与之作用的残基保存成xyz轨迹

(3)用Multiwfn计算aNCI的格点数据

(4)对格点数据进行适当屏蔽以得到最佳的效果

下面依次介绍这些步骤怎么做。涉及到动力学程序的部分我用的是GROMACS，其它动力学程序的用户也可以以类似的方式实现。本文用到的所有文件都可以在这里下载（cub文件太大就不提供了）：http://sobereva.com/attach/591/file.rar。





2 动力学模拟



对于aNCI分析蛋白-配体相互作用，我建议先做NPT模拟，使得体系达到充分平衡的状态，然后再做NVT模拟，此时将配体的坐标冻结。冻结配体很重要，如果在动力学过程中允许配体乱动的话，aNCI图可能会变得一团糟。注意如果在真实环境中，配体就是在多种构象之间反复切换，那么正确的考虑方式是对NPT轨迹的配体部分做簇分析，取容量较大的几个簇各自的最有代表性的结构，然后冻结配体再做动力学和aNCI分析，也即aNCI分析是对配体处于不同典型的构象分别来做、分别讨论的。本文的例子的配体是苄脒阳离子，并没有多种构象的问题。



跑3ATL这个体系的冻结配体坐标的NVT动力学用的tpr和mdp文件，以及跑出来的xtc和gro文件都可以在本文的文件包里下载。为避免轨迹太大不好下载，这里给出的轨迹md_fix_nowat.xtc以及对应的最终结构的md_fix_nowat.gro是去水之后的。md_fix.mdp是这个过程用的mdp文件，可见里面有freezegrps = MOL和freezedim = Y Y Y，这是用来将配体（MOL残基）固定用的。这个NVT动力学跑了1ns，每500步（1ps）保存一次轨迹，一共1001帧。通常来说有1000帧足够得到能说明问题的aNCI图了。注意aNCI分析耗时是和考虑的帧数成正比的。





3 获得用于aNCI分析的xyz轨迹文件



注意绝对不要直接把整个蛋白+配体体系给Multiwfn用于aNCI分析，这样会耗时极高，几乎根本算不动。正确做法是只把配体以及与配体距离较近的残基原子保存为xyz轨迹文件。



启动VMD，载入md_fix_nowat.gro，删除仅有的一帧，然后再载入md_fix_nowat.xtc。然后我们测试一下看看用什么样的VMD选择语句可以选中合适的区域，不了解语法的话看《VMD里原子选择语句的语法和例子》（http://sobereva.com/504）。把轨迹切换到第0帧，然后在Graphics - Representation里把选择范围设置为resname MOL or protein same resid as within 3.5 of resname MOL，这样就把配体以及有任何一个原子在距离配体3.5埃范围以内的残基都选中。把显示方式设为CPK，此时的图像如下（我把配体加了个透明的表面以突出显示）










2.png (135.11 KB, 下载次数 Times of downloads: 268)

下载附件 Download



2021-3-4 04:01 上传 Uploaded










可见当前用的选择语句很合适，如果发现不合适的话可以再调节within后面的值。现在选择File - Save coordinate，selected atoms填resname MOL or protein same resid as within 3.5 of resname MOL，保存的文件类型选xyz，然后点Save按钮，将这个局部区域保存为cluster.xyz。



有一个重点需要注意，aNCI分析必须知道各个原子对应什么元素，否则没法构建准分子密度。因此，用于aNCI分析的xyz轨迹文件里应该包含各个原子的元素名（规范的xyz文件都应当如此），否则Multiwfn会根据原子名去猜，这样很容易猜错，比如CA就到底是钙还是alpha碳就没法区分。由于md_fix_nowat.gro里记录的是GROMACS跑动力学时候的原子名，而此格式并不记录元素信息，所以像上面这样保存出的cluster.xyz里也是用的原子名。那么怎么让Multiwfn能正确获得元素信息呢？一个做法是手动把cluster.xyz里的原子名都替换成元素名，对于水盒子这种简单的情况还好办，原子名就三种因此就替换三次就可以，而对于当前体系显然这么替换太费劲了。因此Multiwfn设计了一个特殊规则，也就是如果当前目录下如果有和载入的xyz文件名相同但后缀是pdb的文件，就会优先从pdb文件记录元素的那一列里读取元素名。不过如果pdb里对某些原子没有提供元素名，对这些原子Multiwfn仍会根据xyz文件里的原子名去猜，原子名里如果有数字会被事先自动去掉。所以，现在要做的是产生一个对应局部区域的含有元素信息的pdb文件，具体做法如下。



运行gmx editconf -f md_fix.tpr -o md_fix.pdb，将当前动力学的tpr文件转化成pdb文件。因为tpr里有蛋白的元素信息，所以得到的pdb文件的蛋白部分也有元素信息，即新产生的md_fix.pdb的最后一列。但打开md_fix.pdb并找到MOL残基的位置，会看到这样得到的pdb中的配体部分是没有元素信息的。不过对于此例这倒不是问题，因为cluster.xyz里配体部分的原子名都是比如C1、N8、H13这样，除去数字后的字符和元素名直接相符，所以此例既不需要在md_fix.pdb里把配体部分的元素名再手动补上，也不需要把cluster.xyz里的配体的原子名都改为元素名（但对于其它体系的情况，二者最好改其一以求稳妥）。

注：顺带在这里说一下什么情况pdb是记录元素信息的。在[ atomtypes ]里，如果原子类型名后面记录了元素在周期表里的序号，那么tpr里使用这种原子类型的原子就是有元素信息的，因而转成pdb后也有元素信息。GROMACS自带的蛋白质力场的ffnonbonded.itp中的[ atomtypes ]里都定义了元素序号，因此转出来的pdb里蛋白质部分总是有元素的。而对于小分子部分，就看你用的拓扑文件产生工具在拓扑文件里给的[ atomtypes ]里是否包含元素序号了，和程序有关，没给的话也可以自己手动添加。



用VMD打开md_fix.pdb，然后选择保存文件，选择的范围还是resname MOL or protein same resid as within 3.5 of resname MOL。这样保存出的文件是本文文件包里的cluster.pdb，一共161个原子。



强调一下，前面保存cluster.xyz的时候我提了一句“把轨迹切换到第0帧”，千万别漏了这个。因为不同结构下，用上述选择语句选择的原子序号、原子数可能是不同的。按照上述操作，cluster.xyz里记录的原子是根据第0帧结构按照选择语句判断的那些原子，这些原子和cluster.pdb里是相同的，因为cluster.pdb的结构来自md_fix.tpr，这里面的坐标正是轨迹第0帧的。





4 计算aNCI格点数据



把cluster.xyz和cluster.pdb放到相同目录下，然后启动Multiwfn，输入cluster.xyz的路径，程序载入cluster.xyz里的坐标时也会把cluster.pdb里的元素信息载入。然后可以留意一下载入文件后Multiwfn在屏幕上输出的化学组成信息，当前为Formula: H72 C53 N16 O18 S2，明显是合理的，没有不该出现的元素。也可以进入主功能0看一眼当前的结构有无异常的地方（此时显示的结构是cluster.xyz里第一帧结构）。检查没问题后，就接着输入

20  //图形化分析弱相互作用

3  //aNCI分析

1,1001  //考虑的轨迹帧号范围，从1到1001帧（注意Multiwfn的帧号从0开始计）

11  //设置格点。这里选的模式11专门适合aNCI分析，即选择一批原子，然后往周围扩展一定距离定义盒子范围

144-161  //配体的原子序号（打开cluster.pdb，可见MOL残基第一个原子和最后一个原子的原子序号分别是144和161）

3 A  //往配体周围扩展3埃定义盒子

0.15  //格点间距。数值越小要算的点数越多，耗时越高，而aNCI等值面会越光滑



然后程序就开始计算了。aNCI的耗时是不低的，嫌慢可以找个比较好的服务器算，这部分代码做了充分并行化。在笔者的普通4核机子上经过不到半小时算完，而如果用36核服务器，3分钟就能算完。



之后选6，aRDG（平均的约化密度梯度）格点数据会被导出到当前目录下的avgRDG.cub，平均的sign(lambda2)rho会被导出到当前目录下的avgsl2r.cub。如果还想绘制热波动指数（Thermal fluctuation index, TFI)着色的aRDG等值面图，这里再选7来再计算TFI，之后TFI格点数据会被输出到当前目录下的thermflu.cub。





5 绘制aNCI图



把avgRDG.cub和avgsl2r.cub以及Multiwfn目录下的examples\aNCI\avgRDG.vmd脚本挪到VMD目录下。然后启动VMD，在文本窗口里输入source avgRDG.vmd执行此脚本绘制aNCI图，当前图像如下所示










3.png (213.35 KB, 下载次数 Times of downloads: 262)

下载附件 Download



2021-3-4 04:01 上传 Uploaded










当前图像已经不错地展现了配体和周围残基的相互作用，但其它地方有很多零碎的多余的等值面，特别是上图右下角那一坨很难看，所以需要对aRDG的格点数据进行屏蔽。在Multiwfn中，可以实现将距离某个片段较远区域的aRDG格点数据的数值设为一个比较大的值（比如100），之后再绘制等aRDG值面图的时候那部分区域就不会出现等值面了，下面就来这么处理一下。



这里先把原先avgRDG.cub改名为avgRDG_org.cub，然后启动Multiwfn，载入avgRDG_org.cub，输入

13  //处理格点数据

13  //设置远离或接近某些原子的格点的数值

1.6  //设置原子范德华半径乘的倍数，这个值可以反复试试直到效果满意

100  //满足条件的格点的数值设为100

2  //手动输入原子序号

144-161  //配体的原子序号

0  //将当前的格点数据导出

avgRDG.cub  //新的格点数据的文件名



之后将avgRDG.cub挪到VMD目录下替换掉原先的，再次用avgRDG.vmd脚本绘图。之后再做一些适当调节，在Graphics - Representation里把显示等值面的那个rep的isovalue稍微设大到0.3使得等值面更膨胀丰满一些，以令边缘的锯齿减弱。然后把显示当前几何结构的rep的选择范围设为serial 144 to 161，把Sphere Scale设小为0.7。然后点Create Rep按钮新建一个Rep，把选择范围设为not serial 144 to 161，Drawing Method设为licorice，bond radius设0.1，Material设Transparent。此时的图像效果如下。










4.png (302.09 KB, 下载次数 Times of downloads: 244)

下载附件 Download



2021-3-4 04:02 上传 Uploaded










上图的效果已经挺好了。大面积的绿色等值面展现出了苯环区域与周围残基形成的广阔的范德华作用。配体的每个氨基氢与与之接触的残基间都有蓝色等值面，体现出了与周围残基的较强的氢键作用。注：上图中在配体的C-H和N-H之间有一块蓝色区域，切勿把这个解释成分子内的强吸引作用。C-H和N-H之间并没强烈的吸引作用，实际上这部分只是范德华作用而已，由于aNCI是基于准分子密度近似的，所以有些弱相互作用区域的电子密度不够真实，可能偏高（没体现Pauli互斥导致作用区域密度的下降）。



avgRDG.vmd脚本用的色彩刻度是-0.025到-0.025，颜色变化是蓝-绿-红。其默认的色彩刻度范围比较窄，这令某些很弱作用的区域的等值面的颜色仍显得发青。想避免的话可以自行把脚本里的-0.025和0.025分别改为-0.04和0.04，也可以在Graphics - Representation里选中显示等值面的那个rep，然后点Trajectory标签页，手动输入色彩刻度下限和上限为-0.04和0.04。发文章时图中应附上的色彩刻度条，可以直接用Multiwfn自带的examples\RGB_bar.png文件。



还可以把md_fix_nowat.gro一同载入VMD，用New Cartoon方式显示其中蛋白质骨架结构，用Secondary structure着色，材质用Transparent，而之前的与配体作用的残基材质改为AOEdgy。此时图像如下，效果非常理想










5.jpg (315.19 KB, 下载次数 Times of downloads: 246)

下载附件 Download



2021-3-4 04:02 上传 Uploaded










下面我们再来绘制一下热波动指数TFI着色的aRDG图。启动VMD，在文本窗口里输入source avgRDG_TFI.vmd，然后对显示方式稍作调节，即可看到下图（这里对配体用了AOEdgy材质，可以令轮廓比较清楚）










6.png (294.41 KB, 下载次数 Times of downloads: 236)

下载附件 Download



2021-3-4 04:02 上传 Uploaded










此图中越蓝的地方说明相互作用越稳定，在动力学过程中波动程度越低。由于苄脒阳离子在当前的蛋白环境中很稳定，所以大部分等值面都是蓝色的，尤其是上图右侧两个氨基附近的等值面都是蓝色的，体现出氢键稳定程度非常高。在上图左侧等值面颜色发绿，体现出这部分作用的稳定性相对差一些。





6 总结&其它



本文演示了如何利用GROMACS+Multiwfn+VMD绘制蛋白-配体相互作用的aNCI图。这种图非常清楚直观生动地展现了蛋白质和配体间的相互作用，能令这类问题分析的文章增色不少，鼓励大家在实际中使用。这种做法也可以用于研究分子在其它受限环境中与外界的相互作用。

### 2 楼

精品内容，社长威武！

### 3 楼

PS: gmx editconf这类工具转出的pdb一般都是不包括配体的元素名的，如果配体原子名也很特殊，可能混淆，劲量自己补全一下。

### 4 楼

lyj714 发表于 2021-3-4 08:31

PS: gmx editconf这类工具转出的pdb一般都是不包括配体的元素名的，如果配体原子名也很特殊，可能混淆，劲 ...

文章中相应部分已经做了修改以强调这一点

### 5 楼

卢老师，按照你的教程，试了一下两个蛋白间3个氨基酸残基的相互aIGM作用，以前我用IGM作是没问题的。 把MultiWFN生成的两个文件，拷贝到VMD文件夹，启动source IGM_inter.vmd，发现VMD里面显示只有两个Frames，原子数52个，也没有等值面显示出来。实际上， 我在作XYZ文件的时候是201个Frames,原子数54个。不知道是什么原因？

### 6 楼

Tonycjlu 发表于 2021-10-19 11:14

卢老师，按照你的教程，试了一下两个蛋白间3个氨基酸残基的相互aIGM作用，以前我用IGM作是没问题的。 把Mul ...

该用什么脚本，Multiwfn手册3.23.9节里明确说了








Clipboard01.png (36.6 KB, 下载次数 Times of downloads: 207)

下载附件 Download



2021-10-20 03:17 上传 Uploaded

### 7 楼

sobereva 发表于 2021-10-20 03:17

该用什么脚本，Multiwfn手册3.23.9节里明确说了

谢谢卢老师，我脚本用错了，现在做出来了。下一篇稿件就用aIGM啦！

### 8 楼

鉴于有今天有人问相关问题，在此文里加入了如下内容



注：顺带在这里说一下什么情况pdb是记录元素信息的。在[ atomtypes ]里，如果原子类型名后面记录了元素在周期表里的序号，那么tpr里使用这种原子类型的原子就是有元素信息的，因而转成pdb后也有元素信息。GROMACS自带的蛋白质力场的ffnonbonded.itp中的[ atomtypes ]里都定义了元素序号，因此转出来的pdb里蛋白质部分总是有元素的。而对于小分子部分，就看你用的拓扑文件产生工具在拓扑文件里给的[ atomtypes ]里是否包含元素序号了，和程序有关，没给的话也可以自己手动添加。

### 9 楼

提示：此文已经过时了，如今强烈建议用《使用amIGM方法图形化直观展现动态过程中的平均弱相互作用》（http://sobereva.com/759）介绍的amIGM代替aNCI方法

## 入库完整性评估

- 主帖全文收录
- 全部回复完整收录
