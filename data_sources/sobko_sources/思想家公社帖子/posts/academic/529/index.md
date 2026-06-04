---
post_id: 529
title: 使用Multiwfn便利地查看所有激发态中的主要轨道跃迁贡献
url: http://sobereva.com/529
date: '2020-01-28T04:17:00+08:00'
source_categories:
- Multiwfn
- 量子化学
primary_topic: Multiwfn
secondary_topics:
- 激发态与光谱
- 波函数分析
- 结构与文件格式
academic_relevant: true
classification_reason: 标题是用 Multiwfn 查看所有激发态的主要轨道跃迁贡献。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**使用Multiwfn便利地查看所有激发态中的主要轨道跃迁贡献**

Using Multiwfn to conveniently examine major orbital contributions to every excited state

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2020-Jan-28  Last update: 2022-Mar-1

之前笔者写过一篇文章《电子激发任务中轨道跃迁贡献的计算》（<http://sobereva.com/230>），介绍了如何对TDDFT及类似方法计算的激发态计算轨道跃迁的贡献。在很多电子激发的研究文章中都会给出各个激发态中各种主要MO跃迁情况。虽然计算贡献很简单，但当考察的态比较多的时候，一个一个去考察、记录贡献值还是比较费事的，初学者还容易弄错。

Multiwfn的电子激发分析（主功能18）里的子功能15专门用于快速输出所有激发态中的主要的轨道跃迁贡献，使得从MO角度考察各个激发态的特征非常简单容易。此功能支持Gaussian、ORCA、GAMESS-US、Firefly的CIS/TDHF/TDA-DFT/TDDFT/ZINDO的输出文件。也支持CP2K的TDDFT输出文件，此文有专门的例子：《使用CP2K结合Multiwfn对周期性体系模拟UV-Vis光谱和考察电子激发态》（<http://sobereva.com/634>）。Multiwfn可以在其主页<http://sobereva.com/multiwfn>免费下载。不熟悉Multiwfn者推荐阅读《Multiwfn FAQ》（<http://sobereva.com/452>）。

下面是个简单的例子。启动Multiwfn后输入以下内容  
examples\excit\D-pi-A.out  //Gaussian做标准TDDFT任务的输出文件（其中的IOp(9/40=4)关键词对于当前功能是多余的）  
18  //电子激发分析  
15  //输出各个激发态中主要的轨道跃迁贡献  
然后马上看到以下信息  
 HOMO index:    56  
 LUMO index:    57

 Only MO transitions with absolute contribution >=  5.0 % are shown below. It co  
rresponds to 10 times of "compthres" parameter in settings.ini

 #   1   3.9069 eV    317.35 nm   f=  0.01880   Spin multiplicity= 1:  
   H-4 -> L 81.9%, H-4 -> L+2 12.1%  
 #   2   4.0624 eV    305.20 nm   f=  0.63550   Spin multiplicity= 1:  
   H -> L 86.0%, H-3 -> L 5.3%  
 #   3   4.4166 eV    280.72 nm   f=  0.00010   Spin multiplicity= 1:  
   H-6 -> L 85.3%, H-6 -> L+2 11.9%  
 #   4   4.7912 eV    258.77 nm   f=  0.01350   Spin multiplicity= 1:  
   H-2 -> L 54.5%, H -> L+1 27.6%, H-3 -> L+1 6.4%  
 #   5   4.8872 eV    253.69 nm   f=  0.00790   Spin multiplicity= 1:  
   H -> L+3 57.3%, H-2 -> L 17.0%, H-1 -> L+2 8.8%, H-1 -> L 8.0%

由输出可见，比如对于第3激发态，主要特征是HOMO-6 -> LUMO贡献85.3%，其次是HOMO-6 -> LUMO+2贡献11.9%，输出的格式非常明确直观。Multi代表自旋多重度，激发态序号和激发能也都一起给出了。

之后如果你输入y，上面的信息将会被导出到当前目录下的一个文本文件里，便于后处理。

默认情况下，如提示所示，只有MO跃迁贡献大于5%的才会被输出。如果你想提升或者降低阈值，可以修改settings.ini里的compthres，当前功能输出阈值是compthres值的10倍。

此功能输出的信息可以放到你写的文章的补充材料去，目前有不少文章都这么做。

下面是基于Gaussian对一个开壳层体系做TDDFT的输出文件，用此功能输出的信息  
#   1   2.2737 eV    545.30 nm   f=  0.00120   Spin multiplicity= ?:  
  Hb-1 -> Lb 96.6%  
#   2   2.8507 eV    434.93 nm   f=  0.00530   Spin multiplicity= ?:  
  Hb -> Lb 90.7%, Ha -> La 8.4%  
#   3   3.4525 eV    359.11 nm   f=  0.02330   Spin multiplicity= ?:  
  Hb-2 -> Lb 69.7%, Ha -> La+1 27.6%  
#   4   4.1909 eV    295.84 nm   f=  0.03500   Spin multiplicity= ?:  
  Ha -> La 85.5%, Hb -> Lb 7.6%  
#   5   4.4035 eV    281.56 nm   f=  0.00820   Spin multiplicity= ?:  
  Ha-1 -> La 48.5%, Hb -> Lb+1 40.4%  
#   6   5.1640 eV    240.09 nm   f=  0.00020   Spin multiplicity= ?:  
  Hb-3 -> Lb 96.3%  
#   7   5.2669 eV    235.40 nm   f=  0.21880   Spin multiplicity= ?:  
  Ha -> La+1 65.4%, Hb-2 -> Lb 22.4%, Hb -> Lb+1 8.8%  
#   8   5.6860 eV    218.05 nm   f=  0.00020   Spin multiplicity= ?:  
  Hb-4 -> Lb 89.1%, Hb-1 -> Lb+1 6.8%  
由于参考态是开壳层时TDDFT算的激发态有自旋污染，因此Multi后面是问号。当前情况轨道自旋都明确标出了，a、b分别代表alpha和beta。比如基态到第5激发态中alpha的HOMO-1到alpha的LUMO跃迁贡献了48.5%。

如果你是ORCA用户，当前功能显得更有意义了。ORCA里有个令很多人讨厌的习俗是轨道序号是从0开始记，导致很多人搞错HOMO和LUMO的序号，指使在文章中描述激发态的MO跃迁情况时出现错误。而使用Multiwfn查看主要MO跃迁贡献就可以完全杜绝这个问题。此功能结合ORCA使用的方式在《Multiwfn结合ORCA的TDDFT计算做空穴-电子等分析的方法》（<http://sobereva.com/758>）里有专门演示。

如果你是GAMESS-US用户，别忘了要把电子激发任务输出文件设成.gms后缀，否则此功能无法正常使用。比如examples\excit\H2CO_TDDFT_GAMESS.gms就是GAMESS-US对甲醛做TDDFT的输出文件，可以直接给Multiwfn作为输入文件使用当前功能。

使用此文的做法计算轨道跃迁贡献发表文章时请记得引用Multiwfn程序的原文，在程序启动时明确提示了。
