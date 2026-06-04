---
post_id: 309
title: 在线基组和赝势数据库一览
url: http://sobereva.com/309
date: '2015-11-11T01:21:00+08:00'
source_categories:
- 量子化学
primary_topic: 综述/教程/投稿经验
secondary_topics:
- 结构与文件格式
- 量子化学
academic_relevant: true
classification_reason: 文章是基组和赝势数据库的汇总，属于资源整理。
topic_family: 资源经验
exclude_reason: ''
confidence: 0.94
image_count: 0
local_assets_dir: assets
---

**在线基组和赝势数据库一览**  
Overview of online basis set and pseudopotential databases

文/Sobereva @[北京科音](http://www.keinsci.com)

First release: 2015-Nov-11   Last update: 2025-Jul-14  
 

量子化学程序都自带了基组或赝势库，但是显然是很难做到全面。缺的基组可以从其它程序自带基组库中借过来，但更常用的做法还是从网上的基组数据库上直接找定义。此文不完整地汇总一下在线基组、赝势数据库，都是免费开放的。如果其中有网站在大陆无法访问或者功能不正常，绝对不要以为是网站有问题，是什么原因导致的、怎么解决，懂的都懂。

**1 Basis Set Exchange (BSE)基组数据库**  
地址：<https://www.basissetexchange.org>  
原文：J. Chem. Inf. Model., 47, 1045-1052 (2007)  
简介：西北太平洋国家实验室（PNNL）的人搞的最重要、最全面的基组+赝势数据库，已把绝大多数（特别是常用的）目前已经发表的基组和赝势都已经纳入进去了，并且不断更新，已经成为搞量化的人必不可少的网站。输出格式支持很多程序。但注意极个别元素的个别不常用的基组的定义可能有误，所以如果得到奇怪结果别忘了检查下拷来的基组定义是否合理。据说此基组库以后会把旋轨势也加进去。

注：值得一提的是Optimized General Contractions这个选项，如果点了它，那么显示出的Dunning相关一致性基组就会比不选这个选项时要少一些GTF壳层。因为这类基组的GTF间有一些线性相关性（见CPL,260,513），对于片段收缩的程序去掉这些壳层不会影响结果还使得计算加快。（但对于Gaussian，选不选它都一样，因为Gaussian会自动按照CPL那篇Davidson提出的方法去掉多余GTF，而且在不影响结果前提下比Optimized General Contractions这个选项去得更彻底）。

**2 Turbomole程序的基组库**  
地址：<https://basissets.turbomole.org>  
简介：Turbomole那伙人搞的，包含的也都是他们搞出来的基组，包括def、def2系列基组（也包括给极化率计算优化的末尾带D的带有弥散的版本）、在def2基础上把赝势从MWB改成MDF后重新优化的dhf-系列基组，以及专给用于结合MDF的旋轨势做二分量计算的dhf-2c系列基组。除了普通基组，还可以获得/J、/JK、/C密度拟合基组。目前输出格式支持Gaussian、Turbomole、molpro、Dalton。输出格式选Turbomole或molpro的时候dhf-系列基组的条目中会有旋轨势。

**3 明尼苏达基组数据库**  
地址：<http://comp.chem.umn.edu/basissets/basis.cgi>  
简介：Truhlar一伙人弄的一个小基组库，包含Truhlar他们弄出来的一些非主流基组，诸如MIDI、MG3之类，其中相对来说有用的是ma-开头的，比如ma-TZVP，这是以最小方式给def2系列相应基组加上弥散函数的版本，即minimally augmented，也就是给非氢原子加上一层s和p弥散函数。在某些需要弥散函数的计算时如果嫌def2基组没弥散函数，又懒得自己手动修改定义，不妨直接来这里拷定义。支持的输出格式也不多，Gaussian、GAMESS、ACESII和已经被遗忘的HONDO。

**4 Stuttgart赝势参数数据库**  
地址：<http://www.tc.uni-koeln.de/PP/clickpse.en.html>  
简介：搞Stuttgart系列赝势的Dolg他们弄的Stuttgart赝势+赝势基组数据库，重元素的MDF版本除标量势外也有旋轨势（输出格式选molpro才能看到）。虽然BSE上也有Stuttgart赝势和配套基组的定义，Gaussian等程序也自带了，但都比较老，只有这里的才是最新、最全的。输出格式支持Molpro、Gaussian、Turbomole、Crystal。

**5 相关一致性基组数据库**  
有两个地址，分别是两个相关一致性基组的开发者课题组下属的页面  
Hill组：<http://www.grant-hill.group.shef.ac.uk/ccrepo/index.html>  
Peterson组：<http://tyr0.chem.wsu.edu/~kipeters/basis.html>  
简介：把Dunning最初开发，Peterson和Hill等人进一步发展的相关一致性基组做了最全面的汇总，包括cc-pVnZ、cc-pCVnZ、cc-pwCVnZ系列，带aug-前缀的，带-DK、-PP、-F12等后缀的版本都有。赝势基组没有同时给出赝势部分，需要自己去Stuttgart赝势库中下载相应的MDF型赝势结合使用。Hill组提供的页面可以按照周期表来查询，比较方便，而Peterson组那个是按照文献来查询，比较麻烦。

**6 Clarkson大学相对论有效势数据库**  
地址：<http://people.clarkson.edu/~pac/reps.html>（已失效）  
简介：包含的是CRENB（Christiansen-Ross-Ermler-Nash-Bursten）赝势和相应的赝势基组，并且包含对应的旋轨势，覆盖整个周期表。CRENB具体分CRENBL（小核赝势）和CRENBS（大核赝势），在BSE上都有，没必要来这里下，而且这种赝势精度也不咋地没什么人用。这个主页价值也就在于但这里提供了旋轨势，这在BSE上是没有的。

**7 ADF的STO基组数据库**  
地址：<http://www.scm.com/Downloads/zorabasis/Welcome.html>  
简介：这是仅有的STO基组的数据库，基组是ADF御用的，包括DZ、TZP、TZ2P、QZ4P，冻核和全电子版本的都有，1-118号元素都齐了。

**8 Crystal程序的基组数据库**  
地址：<https://www.crystal.unito.it/basis-sets.php>  
简介：为数不多的基于高斯函数的第一性原理程序Crystal的基组库，适当改格式也可以用于其它程序。值得一提的是其中的pob-TZVP是基于def2-TZVP修改的专门适合固体计算的版本，比用其它的3-zeta基组可得到更好结果，其定义也同样可以从这里得到<https://www.chemie.uni-bonn.de/bredow/de/software/basis_sets>。

**9 CASINO程序的基组和赝势库**  
地址：<http://www.tcm.phy.cam.ac.uk/~mdt26/casino2_pseudopotentials.html>  
简介：做量子蒙特卡罗计算的CASINO程序的相对论标量势、旋轨势、核极化势和基组库，元素从H到Ba，以及Lu到Hg都有。Gaussian、GAMESS、Crystal格式都支持。

**10 PSI-4程序的基组库**  
地址：<http://www.psicode.org/psi4manual/master/basissets_byfamily.html>  
简介：PSI-4程序的基组库，大部分是从BSE上或者molpro程序中搞出来的，少量是私有的。每种基组对应的密度拟合基组都明确列上了。格式就是Gaussian的格式。

**11 Hirao等人的DKH3全电子相对论计算的基组库**  
地址：<http://www.riken.jp/qcl/publications/dk3bs/periodic_table.html>  
简介：这是Hirao等人提出的专供DKH3相对论计算的基组库，参数通过最小化原子DKH3标量相对论计算得到的能量得到，对应的文章是JCP,115,4463(2001)，覆盖1-103号元素。可惜没法选择输出格式。

**12 Sapporo全电子相对论基组库**  
地址：<http://sapporo.center.ims.ac.jp/sapporo/Order.do>  
简介：提供了DZ、TZ、QZ级别的用于非相对论和DKH3相对论计算的基组，强调是片段收缩。输出格式支持Gaussian、GAMESS、molpro、molcas、turbomole、NWChem、Dirac等主流程序。另外提供的TK/NOSec是适合非相对论电子相关计算的基组，MCP/NOSec是结合相对论模型势(MCP)用的适合电子相关级别下计算的基组，可以在支持MCP的GAMESS-US、molcas等程序中用。

**13 RAGBS、RPF-4Z全电子相对论基组库**  
地址：<http://basis-sets.iqsc.usp.br/basis-sets/>  
简介：可以获得RPF-4Z（一种性价比很高的4-zeta级别用于相对论计算的基组）和RAGBS（Relativistic Adapted Gaussian Basis Sets，号称是相对论计算中没有变分塌陷问题的基组中最小的一种）的基组定义。

**14 Dyall全电子相对论基组库**  
地址：<http://dirac.chem.sdu.dk/basisarchives/dyall/>  
简介：这是专门做相对论计算的Dirac程序御用的Dyall基组的基组库，专适合四分量、二分量或标量相对论计算计算，是非收缩的，从第四周期开始都有定义（但是目前没3d金属）。

**15 Sadlej基组库**  
地址：<http://www.qch.fns.uniba.sk/Baslib/>和<http://www.chem.uni.torun.pl/zchk/basis-sets.html>  
简介：在撰文时BSE上只有Sadlej POL、Sadlej+基组的定义。Sadlej还提出了其它的适合计算（超）极化率的基组，在这两个网页里有。但是网页里是他们私有的格式，笔者为了方便广大研究者把这倆网页上的基组文件转换成了Gaussian格式，见《各种Sadlej基组的Gaussian格式的定义》（<http://sobereva.com/345>）。 在撰文时BSE上只有Sadlej POL、Sadlej+基组的定义。Sadlej还提出了其它的适合计算（超）极化率的基组ZPolX和LPolX，在原文里没给定义，但在这个网页上能下载到定义，但可惜没有Gaussian格式的，得自己转换。

**16 Jorge基组库**  
地址：<http://qcgv.ufes.br/downloadbasis.html>  
简介：包含巴西Jorge课题组开发的DZ到6Z级别的基组，优点并不鲜明，但好处是涵盖了周期表大部分，且有用于普通计算和专为DKH2计算优化的两类基组，前者也有带弥散的版本，以A开头（比如ADZ。A代表augmented）。能导出大部分主流量化程序支持的格式，实际上这些基组在BSE上也能找到。
