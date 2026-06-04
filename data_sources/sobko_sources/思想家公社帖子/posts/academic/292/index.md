---
post_id: 292
title: GaussView保存输入文件时内坐标变量不用字母表示的解决方法
url: http://sobereva.com/292
date: '2015-06-08T00:21:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
academic_relevant: true
classification_reason: 文章讨论GaussView保存Gaussian输入文件时内坐标变量的处理。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**GaussView保存输入文件时内坐标变量不用字母表示的解决方法**  
Solution to the problem that internal coordinate variables are not represented by letters when GaussView saves input files

文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2015-Feb-2   Last update: 2021-Jul-9

今天在思想家公社QQ群里有人问GaussView保存Gaussian输入文件时，在保存界面中取消了write cartesian选项以保存成内坐标形式，但是保存出来的内坐标的变量直接用数字表示，如下面这样，应该怎么做才能保存成变量形式？  
O                
 H                  1    0.94740744  
 H                  1    0.94740744    2  105.47857762

解决办法很简单，先把体系保存成.mol等其它格式，然后载入之，再保存成Gaussian输入文件，就会看到内坐标都用字母表示了：  
O                
 H                  1            B1  
 H                  1            B2    2            A1

   B1             0.94740000  
    B2             0.94735254  
    A1           105.47684474

没有相应选项直接选择是否把变量用字母表示是GaussView一个不人性化的地方。

更好的做法是使用笔者的Multiwfn程序保存Gaussian输入文件，你可以直接设置保存成哪种内坐标形式。Multiwfn可以在<http://sobereva.com/multiwfn>免费下载。Multiwfn支持从大量格式中载入结构信息，如xyz/pdb/pqr/mol/mol2/cif/gjf/wfn/cub/fch/molden/mwfn等等，完整介绍见<http://sobereva.com/379>。如果把自带的settings.ini文件里的iloadGaugeom设为1，还可以直接从Gaussian输出文件里载入结构信息。

启动Multiwfn并从输入文件里载入结构信息后，输入gi就可以进入Gaussian输入文件保存界面。默认保存成笛卡尔坐标形式，如果先输入zmat，再输入要保存的文件路径，则产生的Gaussian输入文件就是内坐标形式，而且所有几何参数都是通过变量表示。如果进入Gaussian输入文件保存界面后先输入zmat2，再输入要保存的文件路径，则产生的Gaussian输入文件里就是内坐标直接带变量值的形式表示。

注：Multiwfn的以上特性在2021-Jul-9及以后更新的版本中才支持。
