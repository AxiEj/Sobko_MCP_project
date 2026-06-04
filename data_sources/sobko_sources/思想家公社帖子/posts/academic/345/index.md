---
post_id: 345
title: 各种Sadlej基组的Gaussian格式的定义
url: http://sobereva.com/345
date: '2016-09-18T18:16:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- 量子化学
academic_relevant: true
classification_reason: 内容是把Sadlej基组整理成Gaussian可直接使用的格式，核心是Gaussian输入/基组文件。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**各种Sadlej基组的Gaussian格式的定义**Definition of various Sadlej basis sets in Gaussian format  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)   2016-Sep-18

  
  
Sadlej曾经提出过很多专用于算偶极矩、极化率、超极化率这些电场响应性质的基组，比用普适的Dunning系列基组算这类问题更划算。在EMSL上也有Sadlej基组但是很不全面。虽然他们也提供了含有基组定义的网页，但是格式是他们自己的，没法直接用在Gaussian上。笔者通过自编程序，把各种Sadlej基组转换成了Gaussian格式便于大家使用。  
  
下载地址：[/usr/uploads/file/20160918/20160918181551_95453.rar](http://sobereva.com/usr/uploads/file/20160918/20160918181551_95453.rar)  
  
压缩包里的.gbs文件就是把源基组文件转换后的文件，可以用文本编辑器打开。在Gaussian中用的时候可以把要用的元素的定义拷出来，也可以直接用@把整个文件进行引用，Gaussian就会自动从中提取当前计算所需的元素信息。比如  
#p B3LYP/gen  
  
Title Card Required  
  
0 1  
 C                  0.00000000    0.00000000   -0.52710800  
 H                  0.00000000    0.93885600   -1.11413900  
 H                  0.00000000   -0.93885600   -1.11413900  
 O                  0.00000000    0.00000000    0.67386600  
  
@C:\POL.gbs  
详见《详解Gaussian中混合基组、自定义基组和赝势基组的输入》（<http://sobereva.com/60>）。  
  
笔者不敢保证转换过程100%没错误，毕竟牵扯到的基组和元素很多无法一一人工检查，而且有的源基组文件的格式不是很清楚。另外注意，Sadlej搞基组的时候对原子不同组态有时候弄了不同的基组，所以.gbs文件里有个别元素被定义了两遍，大家去看基组源文件里的注释就知道是怎么回事了。  
  
源基组文件来自于这两个网页  
1 <http://www.qch.fns.uniba.sk/Baslib/>  
这个网页提供了完整的POL、HYPOL、POL_F的定义，以及Z2POL、Z3POL对从H到Cl的定义。  
2 <http://www.chem.uni.torun.pl/zchk/basis-sets.html>  
这个网页提供了ZPOL对于第一周期过渡金属的定义，以及完整的LPOL的定义。  
  
以上两个网页都有专用于相对论计算的版本，由于这个大家一般不涉及到，所以笔者没有对这些基组进行转换，即笔者提供的压缩包里都是给非相对论计算用的。  
  
这里简单提两句这些Sadlej基组的特征。  
  
Sadlej POL：也叫Sadlej pVTZ基组，从1988年陆续提出。参数是优化计算静态极化率得到的。这种基组大小和cc-pVTZ差不多，但对第二、三周期原子都没有f函数，却比cc-pVTZ多了弥散函数。用于计算TDDFT以及相应外场的性质，如偶极矩、极化率、红外强度、拉曼强度、振动频率都很好，比同等大小的其它基组都好不少，与昂贵得多的aug-cc-pVTZ相仿佛。  
（注：在EMSL上有Sadlej pVTZ基组，其实就是Sadlej POL基组，但和这里提供的Sadlej的POL基组不完全相同。EMSL上的那个是片段收缩的，这里提供的是广义收缩的，据说结果差不多，但用这里的话在Gaussian等基于片段收缩的程序中会慢不少。）  
  
Sadlej POL_F：在POL的基础上对一些元素增加了f极化，POL原先的参数没变。  
  
Sadlej HYPOL基组：1998年提出。专门适合于计算超极化率的基组，是在Sadlej POL基组基础上进行一些去收缩再增加轨道指数相同的更高一阶角量子数的基函数得到的。  
  
Sadlej ZPOL：2004年陆续提出。对POL基组进行简化。适合计算大体系偶极矩和极化率。ZPOL和Z3POL是一回事。另外还有Z2POL，是把Z3POL的收缩的极化函数里的primitive shell数减少一层。  
  
Sadlej LPOL：2009年提出。广义收缩程度很高，所以若在Gaussian中会很慢。L代表Large，比POL大，适合计算中、小体系极化率和第一、第二超极化率。只对C H O N F有定义。LPOL具体分为fl、fs、dl、ds。其中l是指large，s是指small，后者是对前者减少极化函数和调整收缩方式来降低耗时。而f、d是指重原子的最高角动量极化函数。大小关系：ds < dl < fs < fl。  
  
EMSL上还有个Sadlej+，这个不是Sadlej课题组搞的，而是Casida等人在JCP,108,4439中计算里德堡激发态的时候，在Sadlej POL基础上增加弥散函数后的结果，只定义了C、H、O、N，都是给s增加了两层弥散函数，p、d增加了一层弥散函数（H没有d也不给它加d）。算超极化率应该比POL有不小改进。
