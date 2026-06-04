---
post_id: 613
title: 显著改进SMD溶剂模型描述Br和I元素精度的溶剂模型SMD18的介绍
url: http://sobereva.com/613
date: '2021-08-23T17:11:00+08:00'
source_categories:
- 量子化学
primary_topic: 量子化学
secondary_topics:
- 分子动力学
- 弱相互作用
academic_relevant: true
classification_reason: 文章介绍改进溶剂模型 SMD18，属于量化计算方法。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.93
image_count: 0
local_assets_dir: assets
---

**显著改进SMD溶剂模型描述Br和I元素精度的溶剂模型SMD18的介绍**

Introduction of the solvent model SMD18, which significantly improves the accuracy of the SMD solvent model in describing Br and I elements

文/Sobereva@[北京科音](http://www.keinsci.com)  2021-Aug-23

之前笔者在《谈谈隐式溶剂模型下溶解自由能和体系自由能的计算》（<http://sobereva.com/327>）中专门说过SMD溶剂模型，这是现阶段最适合算溶剂环境下体系能量的隐式溶剂模型。SMD模型需要通过原子球叠加来构建溶质的孔洞用于算溶剂-溶质相互作用的静电部分，定义原子球需要原子半径。在SMD原文里，仅对H、C、N、O、F、Si、P、S、Cl、Br专门优化了半径，对其它元素用的是Bondi范德华半径来凑合（如果Bondi范德华半径都没有，就用2.0埃凑合）。

SMD溶剂模型作者后来的一篇文章Chem. Eur. J., 24, 15983 (2018)是SMD18溶剂模型的原文。这篇文章根据涉及卤素的体系在乙腈中的反应自由能，发现对于碘用Bondi范德华半径1.98埃来凑合算的结果很不好，此半径值明显太小，于是改为了1991年SM1溶剂模型里对碘优化的半径2.74埃，这令计算结果与实验数据相符程度有了极大的提升。后来他们对Br的半径进行了专门优化，发现用2.60埃做半径的结果与实验数据最接近，这比SMD原文里专门给出的Br的半径3.06埃要小不少，这也令结果大有改进。将SMD里Br和I的半径分别改为2.60埃和2.74埃之后，就被此文称为SMD18溶剂模型。

对于溶液中的涉及卤键的形成或断裂的过程，与Br、I关系密切的化学过程（例如成键断键），或者算含有Br和I的体系的溶解自由能，都强烈建议使用SMD18代替SMD模型。

根据文中的测试，SMD18模型非常适合结合M06-2X使用，我也建议用SMD18时都用M06-2X泛函。为了最大程度地误差抵消，计算溶液中自由能（1M标准态浓度）用的流程也最好和原文一致，具体来说是：对溶质在M06-2X下做优化和振动分析，在这个过程就带着SMD18溶剂模型，直接取量子化学程序输出的自由能，然后再加上1.89 kcal/mol的1atm->1M标准态转变自由能变即可。对Cl、Br、I应当用def2-TZVPD（此时对I来说是赝势基组，需要结合相应的赝势），对其它元素用def2-TZVP。如果不清楚怎么在Gaussian中这么用基组，看《给ahlrichs的def2系列基组加弥散的方法》（<http://sobereva.com/340>）和《详解Gaussian中混合基组、自定义基组和赝势基组的输入》（<http://sobereva.com/60>）。按照SMD18原文所述，如果存在100cm^-1波数以下振动频率的情况，应当改用Grimme的准RRHO模型计算热力学量而非用Gaussian默认用的RRHO模型，这可以通过Shermo程序实现，详见《使用Shermo结合量子化学程序方便地计算分子的各种热力学数据》（<http://sobereva.com/552>），后文有例子。

PS：当然了，用def2-TZVP、def2-TZVPD做opt freq很昂贵，显然不是可取的做法，但无奈SMD18原文这么干的，为了和SMD18优化的半径尽可能实现误差抵消，自己计算时也只能忍着了。如果实在算着太吃力的话，也可以opt freq时候用便宜一些的基组比如def2-TZVP(-f)（这么做对于自由能热校正量和结构的影响很小），之后再用前述SMD18原文里用的基组算个单点，之后再把电子能量和自由能热校正量相加。另外，原理上考虑ZPE校正因子更好，但也为了与SMD18原文一致，就不去考虑这点了。

目前的Gaussian不支持SMD18溶剂模型，但只要在SMD溶剂模型计算时改一下Br和I的元素半径即可轻易实现。这需要写scrf(SMD,solvent=溶剂名,read)关键词，输入文件末尾空一行写modifysph，下面再空一行写以下内容即可  
I 2.74  
Br 2.60

下面给一个Gaussian的完整的计算例子输入文件。输入文件和Gaussian 16跑的输出文件可以在<http://sobereva.com/attach/613/file.zip>里得到。

#P M062X/genecp SCRF(SMD,solvent=acetonitrile,read) opt freq  
 [空行]  
 Title  
 [空行]  
 0 1  
  N                  2.53946200   -1.07717200   -0.01319200  
  C                  1.74543500    0.00000700   -0.00027500  
  N                  2.53948000    1.07717200    0.01885100  
  C                  3.85512000   -0.67530300   -0.00660900  
  H                  4.66037300   -1.38842900   -0.01940300  
  C                  3.85513000    0.67528200    0.00619900  
  H                  4.66038900    1.38840200    0.01901300  
  I                 -0.36464300    0.00000000    0.00004200  
  C                  2.13385200    2.47671900   -0.00046400  
  H                  1.05119700    2.53713200    0.26086500  
  H                  2.74614800    3.02347800    0.75566000  
  H                  2.31269200    2.89578200   -1.02444600  
  C                  2.13383000   -2.47671400   -0.00044100  
  H                  1.05117500   -2.53711700   -0.25836000  
  H                  2.74216300   -3.02400000   -0.75519100  
  H                  2.31661900   -2.89526100    1.02491500  
  Br                -3.43164200    0.00000200    0.00045300  
 [空行]  
 @/sob/SMD18.gbs/N  
 [空行]  
 @/sob/def2-ECP.txt/N  
 [空行]  
 modifysph  
 [空行]  
 I 2.74  
 Br 2.60  
 [空行]  
 [空行]

被引入的SMD18.gbs是BSE基组数据库的def2-TZVP基组文件，但是把Cl、Br、I替换成了def2-TZVPD之后的情况。def2-ECP.txt是def2系列基组标配的Stuttgart赝势基组的定义。即便你的体系里没有I，用上面的输入文件直接替换坐标部分后也可以算，只不过读取赝势的设定以及修改I的半径不生效而已。这两个文件可以在<http://sobereva.com/attach/613/SMD18.gbs>和<http://sobereva.com/attach/613/def2-ECP.txt>下载，上例放到了/sob目录下。

对于Gaussian 09，特别要注意对元素半径的修改没法在opt freq任务中传递给freq部分，因此必须opt和freq分别做，这是个bug，在Gaussian 16中得到了修正。

上面的例子的最低频率只有44.24 cm^-1，因此不建议直接读取输出文件里的基于RRHO模型算出来的Sum of electronic and thermal Free Energies，否则低频对熵的贡献很不准确，而应当用Shermo程序基于准RRHO模型算。把Shermo的settings.ini里的ilowfreq=后面的值设为2，启动Shermo并载入上例的输出文件，可看到结果Sum of electronic energy and thermal correction to G:       -3176.6090365 a.u.。将之加上标准态转换自由能变1.89/627.51=0.00301 a.u.后即得到1M浓度下的乙腈中的自由能-3176.60602 a.u.。

SMD18模型体现出隐式溶剂模型计算能量的准确度对原子半径是多么的敏感。顺带一提，J. Phys. Chem. A, 123, 9498 (2019)提出的SMD-B模型将SMD定义的原子半径都改为了Bondi范德华半径，发现对离子体系（特别是含硫的）的溶解自由能得到一定改进。既可以如上通过modifysph来对各个元素一一修改半径，也可以在scrf里写read的同时在输入文件末尾后面空一行直接加上Radii=Bondi来实现，当然后者省事得多。
