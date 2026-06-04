---
post_id: 340
title: 给Ahlrichs的def2系列基组加弥散的方法
url: http://sobereva.com/340
date: '2016-06-08T10:52:00+08:00'
source_categories:
- 量子化学
primary_topic: 量子化学
secondary_topics:
- Gaussian
- ORCA
- 结构与文件格式
academic_relevant: true
classification_reason: 核心是基组构建与加弥散函数的方法，属于量子化学方法讨论。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**给Ahlrichs的def2系列基组加弥散的方法**Method of adding diffuse functions to Ahlrichs' def2 series of basis sets  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2016-Jun-8  Last update: 2023-Apr-24

 Ahlrichs等人2005年搞的def2系列基组（PCCP,7,3297）如今比较流行，构建得比较理想，比较普适，前六周期完全覆盖（锕系除外），对于3-zeta级别的版本在同等计算量下精度比Pople系列基组强不少，比Dunning相关一致性基组明显更适合DFT计算，还有对应的密度拟合辅助基组，在ORCA程序中能跑得很快，因而是DFT计算的首选基组之一。但是开发者并没专门提出def2系列带弥散的版本，而有些问题又必须有弥散函数（讨论见《谈谈弥散函数和“月份”基组》<http://sobereva.com/119>），经常有人问怎么给def2系列基组加弥散，这里就简单说一下。此文涉及的所有带弥散的def2基组在Gaussian里都没内置，而必须靠自定义基组方式使用，不知道具体怎么做的话仔细阅读和理解此文：《详解Gaussian中混合基组、自定义基组和赝势基组的输入》（<http://sobereva.com/60>）。  
   
**1 借用弥散函数**

Dunning相关一致性基组的弥散函数可以直接挪到Alhrichs基组上，例如加到def2-QZVP上可以称为aug-def2-QZVP，例如Phys. Chem. Chem. Phys., 13, 6670-6688 (2011)就这么用。也可以按照月份基组的思路，砍掉aug上不重要的高角动量弥散函数以降低耗时。另外，Frank Jensen搞的aug-pc-n系列基组的弥散函数也可以借到def2上，由于aug-pc-n基组是专给DFT计算优化的，故对于DFT计算来说可能结果比借用aug-cc-pVnZ的弥散效果更好。  
  
**2 带D后缀的def2系列**

在J. Chem. Phys., 133, 134105 (2010)中作者提出def2-SVPD、TZVPD、TZVPPD、QZVPD、QZVPPD，分别是对def2-SVP、TZVP、TZVPP、QZVP、QZVPP加上弥散函数，弥散函数的指数是通过优化原子的HF极化率得到（同样适合DFT下极化率计算）。这些基组用于其它需要弥散函数的任务，比如算弱相互作用，预期也能起到不错效果，但未必比本文其它的加弥散方式做法更好。这些带D的def2基组可以在BSE（<https://www.basissetexchange.org>）上获得。  
  
**3 ma-方式添加弥散函数**

Truhlar等人提出一种通用的给出原本不含弥散函数的基组以最低限度的弥散函数的策略，这样的基组以ma-开头，含义是minimal augmentation，详见J. Chem. Theory Comput., 7, 3027、Theor. Chem. Acc., 128, 295。也就是将原先基组中指数最小的s和p的指数除以3作为弥散函数的指数，但不对氢加弥散函数。这种处理后的def2基组可以直接从这里获得Gaussian格式的定义：<http://comp.chem.umn.edu/basissets/basis.cgi>。如ma-def2-TZVP在里面被简写为ma-TZVP。对于大多数需要弥散函数的问题，实际上像这样只给重原子加一层s和p弥散就已经解决绝大部分问题了，因此如果想给def2加弥散但又不想花费过高代价的话，这种ma-方式加弥散是比较理想的。  
2019-Aug-28补充：上面这个基组库里的ma-def2系列基组包含的元素不全（即远少于def2系列原本支持的），由于ma-def2又很常用，因此我专门制作了一套元素完整的ma-def2系列基组的Gaussian格式的定义，用起来很方便，见《给def2以ma-方式加弥散函数的Gaussian格式的基组定义文件（含所有def2支持的元素）》（<http://sobereva.com/509>），同时给出了自动基于原有基组定义文件以ma-方式添加弥散函数的程序。  
   
**4 Even-tempered方法**

若当前基组中某个角动量函数中指数最小的是ζ(n)，第二小的是ζ(n-1)，则这个角动量的弥散函数的指数应当为ζ(n)*[ζ(n)/ζ(n-1)]。这称为Even-tempered方法，见Int. J. Quantum Chem., 113, 21-34 (2013)式3，类似于靠几何级数关系来确定更弥散的函数的指数。这是比较普适的“自助”方式给原本没弥散函数的基组加各角动量弥散的做法。  
  
  
顺带一提，在Int. J. Quantum Chem., 116, 1084 (2016)中，作者提出了R-ORP基组，是在def2基础上加了一层s和p弥散同时调节了指数，目的是让基组大小在aug-cc-pVDZ的级别但计算（超）极化率性能有明显提升。实际测试表明此基组算极化率效果一般，但算第一超极化率比较碉，根据作者的测试达到>=daug-cc-pVDZ的水准。不过此基组目前只对C、H、O、N、F有定义。如果想在Gaussian中使用，见《适合超极化率计算的R-ORP基组在Gaussian下的格式》（<http://sobereva.com/338>）。  
  
另外，def2系列基组对弥散函数的要求低于pople系列基组。特别是在3-zeta级别，def2加ma后改进远比pople系列基组加+后的改进要小。所以像计算势垒这种加弥散有益但不是必须的情况，如果对精度要求不是很高的话def2不加弥散也无大碍。
