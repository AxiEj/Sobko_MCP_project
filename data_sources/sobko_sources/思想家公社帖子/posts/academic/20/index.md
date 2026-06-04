---
post_id: 20
title: 将prodrg得到的itp转化为rtp的程序itp2rtp V1.0
url: http://sobereva.com/20
date: '2015-06-02T21:39:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 结构与文件格式
- 其它软件
academic_relevant: true
classification_reason: 文章是把prodrg生成的itp转换为rtp的工具，围绕GROMACS拓扑文件处理。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**将prodrg得到的itp转化为rtp的程序itp2rtp V1.0**

Itp2rtp V1.0: Converting the itp file produced by prodrg to rtp file

文/Sobereva @[北京科音](http://www.keinsci.com/)   写于2008年

通过prodrg获得的小分子.itp文件中，原子的顺序总是发生变化，无法直接include使用。如果分子数目较少可以手动修改，但对于磷脂层这样分子数众多的情况就十分麻烦。

笔者开发了itp2rtp程序以解决此问题。此程序对.itp的格式进行简单的转换，输入.itp文件，得到result.rtp，其中的内容可以拷进力场的.rtp中，在pdb2gmx中相应力场就
认识了此分子。pdb2gmx读进去的结构如果原子顺序和itp中不符，输出的结构就会按照rtp中的顺序进行排列，与itp相符，使用这样的结构就可以
直接在拓扑文件中include小分子.itp文件了。

使用方法：输入文件名即可，如c:\pop.itp  
此处pop.itp为prodrg得到的.itp文件，不要修改格式。

下载地址[/usr/uploads/file/20150602/20150602213936_34328.rar](http://sobereva.com/usr/uploads/file/20150602/20150602213936_34328.rar)
