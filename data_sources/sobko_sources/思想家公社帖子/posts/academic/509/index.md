---
post_id: 509
title: 给def2以ma-方式加弥散函数的Gaussian格式的基组定义文件（含所有def2支持的元素）
url: http://sobereva.com/509
date: '2019-08-28T07:28:00+08:00'
source_categories:
- 量子化学
primary_topic: 结构与文件格式
secondary_topics:
- Gaussian
- 量子化学
academic_relevant: true
classification_reason: 文章提供的是 Gaussian 格式的基组定义文件，重点在文件与基组资源。
topic_family: 资源经验
exclude_reason: ''
confidence: 0.94
image_count: 0
local_assets_dir: assets
---

**给def2以ma-方式加弥散函数的Gaussian格式的基组定义文件（含所有def2支持的元素）**

Basis set definition file in Gaussian format that adds diffuse functions to def2 series in the way of "ma-" (including all elements supported by def2)

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2019-Aug-28   Last update: 2019-Oct-11

def2系列基组非常流行，在笔者的很多博文里都提到、用到，但遗憾的是没有官方标配的带弥散函数的版本。之前笔者写过一篇文章《给ahlrichs的def2系列基组加弥散的方法》（<http://sobereva.com/340>）介绍了几种给def2加弥散函数的方法，其中一个是以ma-方式加弥散函数，诸如def2-TZVP以ma-方式加弥散后叫ma-TZVP。在Truhlar课题组的基组网站<http://comp.chem.umn.edu/basissets/basis.cgi>上直接提供了这些ma-基组的定义，但关键缺点是元素不全。原本def2系列是对于除了锕系以及最后一个周期外所有元素都有定义，但那个网站上提供的ma-TZVP.gbs基组文件里甚至连常用的碘都没有，因此用的时候还得自己去基于def2的定义和ma-规则手写，比较麻烦，初学者还容易搞错。而且每当有人问怎么去手动改，如果对方没基组常识，解释起来可费劲了。

为了解决上述问题，笔者写了个程序，直接基于BSE上的def2系列基组支持的所有元素的定义文件，自动批量按照ma-方式添加弥散函数。这些文件可以在这里下载：<http://sobereva.com/attach/509/file.zip>。此文件包里比如ma-QZVPP.txt就是def2-QZVPP所有元素按ma-方式加上弥散函数的版本。里面还有个文件def2-ECP.txt，这是所有def2基组共用的赝势文件，因为def2系列对第五周期开始的元素是赝势基组。

基于这个文件包里的文件，用Gaussian使用ma-系列基组可省事了。只要把文件先放到某个目录，要用的时候用@来include即可。

下面是一个Windows下计算的例子，用B3LYP-D3(BJ)/ma-TZVP计算水-氟代甲烷的单点。计算前先把ma-TZVP.txt放到C:\下。@代表把后面的文件计算Gaussian之前会被自动展开。

#p B3LYP/gen em=gd3BJ int=fine  
[空行]  
test  
[空行]  
0 1  
 O                  2.21137200   -0.00419200   -0.00194900  
 H                  2.78894100   -0.77058600    0.00034800  
 H                  2.79813100    0.75514700   -0.00127500  
 C                 -0.65861500    0.01454700    0.00490000  
 H                 -0.29784800   -0.58761200    0.83720700  
 H                 -0.28960200   -0.38738100   -0.93713900  
 H                 -0.32683900    1.04530400    0.12361900  
 F                 -2.04578600   -0.01206800   -0.00406300  
[空行]  
@C:\ma-TZVP.txt

由于ma-TZVP.txt里所有元素前头都有个负号，因此只有当前体系里存在的元素才会自动取.txt里的基组定义，而.txt里定义的其它元素不影响当前计算。

再看另一个例子，BP86计算顺铂，对所有元素用ma-SVP，对Pt还加了赝势，因为def2系列对Pt是赝势基组。计算前先把ma-SVP.txt和def2-ECP.txt放到C:\下。  
#P BP86/genecp int=fine  
[空行]  
b3lyp/def2TZVP opted  
[空行]  
0 1  
 Pt                 0.00000000    0.00000000    0.18195700  
 Cl                 0.00000000    1.70827400   -1.36819100  
 Cl                 0.00000000   -1.70827400   -1.36819100  
 N                  0.00000000    1.59755500    1.56108400  
 H                 -0.82596600    1.64390200    2.14978600  
 H                  0.00000000    2.40772900    0.93575300  
 H                  0.82596600    1.64390200    2.14978600  
 N                  0.00000000   -1.59755500    1.56108400  
 H                 -0.82596600   -1.64390200    2.14978600  
 H                  0.00000000   -2.40772900    0.93575300  
 H                  0.82596600   -1.64390200    2.14978600  
[空行]  
@C:\ma-SVP.txt  
[空行]  
@C:\def2-ECP.txt

上例中C:\ma-SVP.txt对体系涉及的所有元素都定义了基组，对Pt而言相当于赝势基组。C:\def2-ECP.txt是def2系列支持的从第五周期开始的所有元素的赝势定义，其中自然也包括对Pt的定义。此文件里也是各个元素前头都有负号，因此定义的元素在当前体系中没出现也不会报错。

在Linux下也可以用引用的方式用，下面还是顺铂的例子。这里/N避免Linux下运行时自动把文件里的内容完整输出一遍。两个文件之间这回没有了空行，因为如果有的话，会导致Pt的赝势信息没法被载入。  
[同上...一直到坐标]  
[空行]  
@/sob/ma-SVP.txt/N  
@/sob/def2-ECP.txt/N  
[空行]  
[空行]

当然了，自己手动把.txt文件里的涉及到的元素的基组、赝势定义拷出来，按照常规的genecp的格式去定义基组和赝势也可以正常使用这些ma-基组，但显然不如靠@来引用基组/赝势文件省事。如果在看上文时感到有不解之处，参看《详解Gaussian中混合基组、自定义基组和赝势基组的输入》（<http://sobereva.com/60>）。

文件包里还有个ma-TZVP(-f).txt，是对def2-TZVP(-f)以ma-方式加弥散函数的版本。def2-TZVP(-f)比def2-TZVP便宜得多，差异在于前者把后者的f极化函数去掉了（对镧系元素笔者保留了f函数，因为f函数对于La系并非是极化函数，而g极化函数被去掉了）。ma-TZVP(-f)比6-311+G(2d,p)略大一丁点，由于def2系列基组很适合代替Pople系列基组，因此强烈鼓励将之代替6-311+G(2d,p)使用。顺带一提，由于def2-TZVP(-f)比def-TZVP更大（比如对于碳，前者有两层d极化而后者只有一层），因此ma-TZVP比起将def-TZVP用ma-方式加弥散函数的版本更贵一些。

最后，给出笔者构建上面那些ma-的基组定义的程序ma-diffuse：<http://sobereva.com/soft/ma-diffuse.rar>。里面是Windows版可执行文件，Def2-SVP.gbs是原始的def2-SVP的定义文件，可以作为ma-diffuse的输入文件。此程序运行时可以由用户设定最小的s和p指数要除的因子，如果设成3，对应的就是以标准的ma-方式加弥散函数的情况。新产生的基组会输出到当前目录下的new.txt。

PS：笔者之前还有另一个给原有基组加弥散函数的工具，见《给基组以even-tempered方式增加弥散函数的工具adddiffuse》（<http://sobereva.com/347>）。
