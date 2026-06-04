---
post_id: 285
title: 将Gaussian的IRC任务输出转换为.xyz轨迹文件的工具：GauIRC2xyz
url: http://sobereva.com/285
date: '2015-06-08T00:18:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- VMD
academic_relevant: true
classification_reason: 重点是把Gaussian IRC输出转换为xyz轨迹文件。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**将Gaussian的IRC任务输出转换为.xyz轨迹文件的工具：GauIRC2xyz**  
GauIRC2xyz: A tool to convert output file of IRC task of Gaussian into .xyz trajectory files

文/Sobereva @[北京科音](http://www.keinsci.com)

 First release: 2015-Mar  Last update: 2023-Aug-17

以前有人问诸如怎么得到Gaussian产生的IRC每个点的结构、怎么得到IRC中某个几何变量的变化。于是抽空写了这个程序解决此问题。

GauIRC2xyz最新版下载地址：<http://sobereva.com/soft/GauIRC2xyz_1.2.8.zip>。其中带.exe后缀的是Windows版可执行文件，无后缀的是Linux下的可执行文件。

此程序用于将Gaussian的IRC任务的输出文件转换为同目录下同名的.xyz轨迹文件。启动后输入文件名即可。trimerization.out是示例输入文件，trimerization.xyz是转换出来的轨迹。

.xyz轨迹格式很简单，见《谈谈记录化学体系结构的xyz文件》（<http://sobereva.com/477>）。很多程序都可以支持.xyz轨迹文件，比如VMD，它使得分析IRC过程中各个变量的变化很方便。比如想看IRC中某个键长度的变化，将.xyz轨迹文件载入VMD，然后按键盘上的2，点击相应两个原子，然后进Graphics - Labels，下拉框选Bonds，选中相应的项，选 Graph标签页，点Save即可将轨迹中这两个原子间距离保存到指定的文本文件中。
