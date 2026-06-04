---
post_id: 21
title: VMD的APBS插件提示...unreadable的解决方法
url: http://sobereva.com/21
date: '2015-06-02T21:42:00+08:00'
source_categories:
- VMD
primary_topic: VMD
secondary_topics:
- 结构与文件格式
academic_relevant: true
classification_reason: 核心是VMD的APBS插件报错及修复方法，属于VMD相关软件问题。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**VMD的APBS插件提示...unreadable的解决方法**

The solution to APBS plug-in of VMD prompts ...unreadable

文/Sobereva   写于约2008年

这个插件是有bug的，mailing list也有报告，但是没给出解决方法。

实际上这个问题是由于APBS插件写入apbs.in里面的pqr文件路径有误导致的。

虽然偶尔莫名其妙地通过改临时文件路径解决了，但大多数情况并不奏效

解决方法是：

照常操作，点击Run之后出现...unreadable

然后进入生成的临时文件夹，比如c:\apbs.27460，修改apbs.in里面mol pqr后面的pqr路径成为正确路径

然后进入dos提示符，进入此目录，手动运行apbs apbs.in             //之前把apbs.exe路径加入系统-高级-环境变量-PATH环境变量中

在此目录下得到.dx文件，根据任务不同，文件名会不同

进入VMD载入pqr文件，再把这个.dx文件加载进此分子ID中，就行了，然后该干什么干什么。

PS:实际上也可以改apbsrun.tcl，就是麻烦点，有兴趣者不妨尝试。
