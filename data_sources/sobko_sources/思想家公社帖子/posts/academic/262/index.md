---
post_id: 262
title: MOPAC的安装方法
url: http://sobereva.com/262
date: '2015-06-08T00:14:00+08:00'
source_categories:
- 量子化学
primary_topic: MOPAC
secondary_topics:
- 综述/教程/投稿经验
- 结构与文件格式
academic_relevant: true
classification_reason: 标题是MOPAC安装方法，属于典型软件安装说明。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**MOPAC的安装方法**  
Installation method of MOPAC

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2014-Nov-21  Last update: 2022-Jul-20

### 0 前言

MOPAC的安装极为简单，自带的说明已经写得很清楚，但还是经常见到有初学者问，这里就再说说。不熟悉MOPAC的话先看看《大体系弱相互作用计算的解决之道》（<http://sobereva.com/214>）里面的介绍。

先去<http://openmopac.net/Download_MOPAC_Executable_Step2.html>下载程序。Windows版就下载页面上最新的即可。Linux版建议下载“Download 64-bit MOPAC2016 for LINUX”（不要下载Latest open-source release下面的Linux版，否则安装时需要图形库，麻烦得很）。此页面里还有GPU版，加速效果很有限，可以无视。

.mop后缀的文件是MOPAC的输入文件，这里提供一个用PM6计算水分子的mop文件用于大家测试：<http://sobereva.com/attach/262/H2O.mop>。

顺带一提，用Multiwfn（<http://sobereva.com/multiwfn>）程序可以非常方便地创建MOPAC的输入文件。启动Multiwfn，载入xyz/pdb/gjf/fch/mol/mol2/mwfn等等含有结构信息的文件（详情看《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》<http://sobereva.com/379>），然后进入主功能100的子功能2，再选14，然后输入要产生的MOPAC输入文件路径，再选一个理论方法如PM7，就得到输入文件了，非常简单。在选择理论方法之前还可以用屏幕上的其它选项设置是否用溶剂模型、是否冻结原子、要做的任务之类。

### 1 Windows版MOPAC的安装方法

运行Windows版.exe安装文件，一直点下一步即可。所有设置，包括安装目录，都用默认的。

MOPAC在Windows下的使用方法：双击mop文件，操作系统如果问你选择用什么程序执行，就选MOPAC。MOPAC算完后会自动关闭窗口（如果一瞬间就关闭了，说明一瞬间就算完了，不是出错）。之后在当前目录下会出现与mop文件同名的其它文件，其中带.out后缀的就是输出文件，用文本编辑器打开即可查看结果。.arc是archive文件，

在Windows下也可以用命令行方式运行。进入命令行模式，输入MOPAC H2O.mop即可运行。

### 2 Linux版MOPAC2016安装方法

比如想装到/sob/MOPAC2016下面，就把压缩包解压到这里，然后在自己的用户主目录下的.bashrc文件末尾添加  
export MOPAC_LICENSE=/sob/MOPAC2016  
export PATH=$PATH:/sob/MOPAC2016  
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sob/MOPAC2016  
之后重新进入终端使上述环境变量设置生效。然后运行chmod +x /sob/MOPAC2016/*给此目录下面的文件都加上可执行权限。

MOPAC在Linux下的使用方法：比如要就是yohane.mop，就输入MOPAC2016.exe yohane.mop。会在同目录下得到.out、.arc等文件。
