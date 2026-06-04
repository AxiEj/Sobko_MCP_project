---
post_id: 347
title: 给基组以even-tempered方式增加弥散函数的工具adddiffuse
url: http://sobereva.com/347
date: '2016-09-23T20:27:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 量子化学
- 结构与文件格式
academic_relevant: true
classification_reason: 文章介绍给基组增加弥散函数的adddiffuse工具，属于具体软件/工具使用。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**给基组以even-tempered方式增加弥散函数的工具adddiffuse**Adddiffuse: A tool for adding diffuse functions to a basis set in even-tempered manner

文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2016-Sep-23   Last-update: 2023-Jul-3

  
  
有的基组本身没弥散函数，或者虽然有弥散函数但只有一层，比如aug-cc-pVTZ，而对于精确计算超极化率、里德堡激发态的目的一层弥散函数不够。  
  
有一种构建基组的方式称为even-tempered，即相邻GTF的指数是成比例的。若当前基组中某个角动量函数中指数最小的是ζ(n)，第二小的是ζ(n-1)，则这个角动量的弥散函数的指数应当为ζ(n)*[ζ(n)/ζ(n-1)]。  
  
例如aug-cc-pVTZ对碳的三层D极化函数的指数：  
1.0970000  
0.3180000  
0.1000000  
指数最小的两个的比例是0.1/0.318=0.314，因此，再增加一层弥散函数（构成d-aug-cc-pVTZ），指数应当为0.1*0.314=0.0314，如果再增加一层（构成t-aug-cc-pVTZ），就是0.1*0.314^2=0.00986。  
   
笔者写的adddiffuse是用来按照上述方式增加弥散函数的。下载地址：<http://sobereva.com/soft/adddiffuse.zip>。其中带.exe后缀的是Windows版可执行文件，无后缀的是Linux版可执行文件。需要源程序可以直接联系我。  
   
启动后需要输入含有Gaussian格式的基组定义的文件。可以从EMSL上拷出来放到文本文件里。文件中可以包含多个元素，每个元素末尾都要有****。压缩包里的aug-cc-pVTZ.txt就是个例子。启动程序后，输入这个文件名，然后选择要增加几层弥散函数，以及对什么角动量增加弥散函数（比如只增加S、P、D弥散就输入SPD，如果输入A就对所有角动量都增加弥散）。然后程序就会在当前目录下产生new.txt，这是添加弥散函数后的Gaussian格式的基组定义。  
  
new.txt里面每个元素前头多了个负号，这样做的好处是，用gen使用自定义基组的时候，若把一堆元素的基组定义放在坐标后头，即使其中有的元素没有在当前计算中出现Gaussian也不会报错。adddiffuse不支持SP壳层。如果某个角动量只含一层基函数，则adddiffuse也不会对之增加弥散函数。  
  
或许有人觉得这程序没多大用，因为用计算器点几下就得到弥散函数的指数了。但是，当你同时需要对多个基组、多个元素都增加一层乃至更多层弥散的时候，手工去弄就很痛苦了，还容易出错。  
  
此程序一个重要用处是基于EMSL上的aug-的Dunning相关一致性基组产生d-aug-和t-aug-版本。虽然EMSL上也有d-aug-的定义，但是撰文时只对前两周期有定义，而t-aug-则在EMSL上根本没有。另外，虽然Gaussian里面内置了d-aug-的定义，比如写CCSD/daug-cc-pVTZ，但是其最外层弥散函数的指数和EMSL上的不符。EMSL上的d-aug-的最外层指数是通过上述even-tempered方式构建的，而Gaussian里的不知道怎么来的，大抵没even-tempered方式构建的合理。
