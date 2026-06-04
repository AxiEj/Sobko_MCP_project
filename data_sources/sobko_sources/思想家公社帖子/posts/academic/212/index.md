---
post_id: 212
title: mopac2xyz：将MOPAC的几何优化过程转换为xyz轨迹文件的工具
url: http://sobereva.com/212
date: '2015-06-08T00:05:00+08:00'
source_categories:
- 量子化学
primary_topic: MOPAC
secondary_topics:
- 结构与文件格式
- VMD
- 可视化
academic_relevant: true
classification_reason: 标题明确是 MOPAC 相关工具，核心是软件工作流和轨迹文件转换。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**mopac2xyz：将MOPAC的几何优化过程转换为xyz轨迹文件的工具**mopac2xyz: A tool to convert geometry optimization process of MOPAC program into xyz trajectory file

文/Sobereva @[北京科音](http://www.keinsci.com/)  
First release: 2013-Nov-12    Last update: 2021-Sep-20

最近用MOPAC优化一些大体系，虽然有现成的程序诸如gabedit可以观看优化后的结构，但是没法像在GaussView里那样观看优化过程中的结构
变化。而看不到优化过程的话，特别是对于较大体系，就心里没谱。另外这些支持MOPAC的可视化程序的界面也着实不好。遂写了个小程序，把MOPAC的优化任务的输出文件转化为xyz格式的轨迹文件（介绍见谈谈记录化学体系结构的xyz文件<http://sobereva.com/477>），然后将xyz文件直接拖到VMD里就可以很方便地观看优化过程中结构怎么变化了。

mopac2xyz 1.0.3版下载地址：<http://sobereva.com/soft/mopac2xyz_1.0.3.zip>

### 使用说明：

mopac2xyz用来把MOPAC的EF方式的几何优化的结构变化过程提取出来构成多帧xyz文件。然后直接将生成的xyz文件拖进VMD就可以观看优化过程的结构变化了。  
  
当前mopac2xyz版本已测试能够兼容MOPAC 2012/2016。不保证能兼容其它版本的MOPAC的输出文件。  
  
压缩包内的test.mop是示例输入文件，test.out是相应的输出文件。mopac2xyz.exe是编译好的Windows版程序，无后缀的mopac2xyz文件是编译好的Linux版程序。  
  
启动mopac2xyz后先输入MOPAC的优化任务的输出文件名。由于优化过程可能步数很多，为了减少输出文件的帧数，程序会让你指定每多少步输出一次到.xyz文件里，如果输入1，那么每一步的结构都输出。程序处理完之后，结构变化过程就都存到当前目录下的.xyz文件中了。  
  
注意MOPAC的输入文件必须用笛卡尔坐标，并且必须写PRNT=2关键词。并且输入文件第三行的内容必须是All coordinates are Cartesian（是为了让mopac2xyz能够定位）。如果任务不是EF方法优化，而是比如L-BFGS方法优化（对较大体系默认如此），那么此程序提取出来的只有初始结构和优化后的结构，也有可能提取不成功。此时用户必须加上EF关键词才能提取优化过程的所有帧。建议用户总带着PRNT=2 EF关键词。  
   
有问题请电子邮件联系我（程序启动时显示了）。
