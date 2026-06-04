---
post_id: 235
title: 从H到Lr所有元素的全电子波函数文件
url: http://sobereva.com/235
date: '2015-06-08T00:08:00+08:00'
source_categories:
- 量子化学
primary_topic: 结构与文件格式
secondary_topics:
- Multiwfn
- 波函数分析
academic_relevant: true
classification_reason: 标题是全电子波函数文件集合，重点是数据文件资源而不是单个软件。
topic_family: 资源经验
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**从H到Lr所有元素的全电子波函数文件**

All-electron wave function files for all elements from H to Lr

文/Sobereva @[北京科音](http://www.keinsci.com/)  2014-Jun-1

Multiwfn (<http://sobereva.com/multiwfn>)最新版本已经内置了从H到Lr的全部径向原子密度用于生成Hirshfeld权重（免得用户自己提供原子波函数文件了），在这个过程中笔者把H到Lr共103个元素通过Gaussian用全电子基组全都算了一遍。计算中得到的全部.fch文件，以及相应的输入输出文件都打包在这里提供，我想肯定会有人用得着，对初学者也是有用的参考。下载地址：<http://pan.baidu.com/s/1bnhDG0B>。

  

### 说明：

计算的都是原子基态。对于过渡金属和镧系锕系，默认初猜下往往得不到正确的基态组态，都在输入文件里通过guess=alter调换初猜轨道来解决。  
  
若未注明，对开壳层情况都是用非限制性开壳层计算。  
  
对于大于18号的元素，都用DKH2来考虑标量相对论效应。  
  
对于主族元素，序号<=18的都用B3LYP/cc-pVQZ计算。对于>18的，适合DKH2计算的cc-pVQZ-DK只有第四周期的而且没有K和Ca，因此都改用对周期表涵盖全面的ANO-RCC计算。例外是Ca，EMSL上ANO-RCC的基组定义有误，同一收缩基函数里存在指数相同的GTF，遂对Ca改用UGBS。  
  
对过渡金属使用HF/UGBS。用HF是为了对这些元素使收敛容易，密度并不比DFT的差。用UGBS是因为对于Gaussian这样的基于片段收缩的程序它比使用ANO-RCC（高度广义收缩基组）快一个数量级。UGBS在Gaussian中使用的一个需要注意的问题是需要很高质量的径向DFT积分格点，否则会报错。尽管HF计算本身不需要格点积分方法，但是产生初猜的Harris泛函还是需要的，因此在输入文件中可见使用了int=grid=400434来手动设定积分格点，径向400个，比默认的高得多，角度部分434个，也相当精确了。  
  
镧系和锕系都用B3LYP/SARC-DKH。SARC-DKH是效果很好而且大小适中的很适合HF/DFT+DKH计算的全电子基组。唯独U和Np用了ROHF，因为DFT没法真实重现它们的基态组态（分别是5f3,6d1,7s2和5f4,6d1,7s2），单个d电子会跑到f上。又由于UHF不收敛，所以用此时能够收敛的ROHF。  
  
  
Hint：假设非要让H~Lr所有元素都用同一种基组、同一种方法，可以都使用HF/UGBS。
