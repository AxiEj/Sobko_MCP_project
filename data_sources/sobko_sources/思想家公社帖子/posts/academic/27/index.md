---
post_id: 27
title: 写高斯输入文件的不错的参考
url: http://sobereva.com/27
date: '2015-06-05T00:07:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 综述/教程/投稿经验
- 结构与文件格式
academic_relevant: true
classification_reason: 内容是写Gaussian输入文件的参考方法，属于Gaussian使用教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**写高斯输入文件的不错的参考**  
文/Sobereva @[北京科音](http://www.keinsci.com/)   写于约2008年

  

一些新手使用高斯经常因为输入格式错误，导致高斯报错，又找不到好的例子作为参考，比如使用混合基组、QST2/3、oniom等，而且一些老手长时间不用相应功能也会忘。

  
实际上高斯自带了许多test文件，不光是作为功能测试用，里面也涵盖了高斯各功能的用法，可以作为参考。  
  
在windows版中，在高斯的tests目录下，有个tests.idx文件，里面简要列举了所有test文件的内容，比如想查QST2的使用格式，一搜就找到了test302。  
  
另外也可以直接用windows的文件内容搜索功能来搜关键字，首先在dos命令行下进入高斯目录下tests下的gjf目录，输入ren *.gjf *.txt，将所有文件转成txt格式。对于XP系统，在gjf文件夹上点右键-搜索，在左侧会看到“文件中的一个字或词组”，输入比如oniom，就可以找到一些使用了oniom的test文件作为写输入文件的参考。由于这个功能没法搜gjf文件的内容，所以需要先转换成txt格式。  
  
linux下也是一样的，可以用grep命令搜索。
