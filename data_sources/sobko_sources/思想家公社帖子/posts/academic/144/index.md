---
post_id: 144
title: 编译NBO5.0独立运行版和嵌入Gaussian03 C02版的方法
url: http://sobereva.com/144
date: '2015-06-07T23:56:00+08:00'
source_categories:
- 量子化学
primary_topic: NBO
secondary_topics:
- Gaussian
academic_relevant: true
classification_reason: 标题直接是NBO5.0编译和嵌入Gaussian的方法，主角就是NBO软件。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**编译NBO5.0独立运行版和嵌入Gaussian03 C02版的方法**  
Method to compile NBO5.0 standalone version and the version embedded in Gaussian03 C02

文/Sobereva @[北京科音](http://www.keinsci.com/)   2012-May-30

NBO程序有两种运行模式，一种是独立运行版，称GENNBO，也叫standalone版。一种是作为模块嵌入进其它大型量子化学程序的版本，称ESS(electronic structure system)版NBO，例如Gaussian的l607模块就是其免费的3.1版。ESS版可以实现更多功能，如自然化学屏蔽(NCS)、NBO Deletion、NEDA能量分解。然而，有很多重要功能都是在免费的NBO 3.x之后才加入NBO程序的。这里介绍收费的，功能已经比较全面的NBO5.0的Linux独立版本和嵌入Gaussian03 C02的版本（也叫NBO5.G）的编译方法，这两种版本的编译过程互不相干。

NBO5的源文件只有nbo_5g.src和enable.f两个，后者用来设定编译模式。

## ======编译独立运行版本的方法=======

编译平台：RHEL6 64bit，Q6600，Root，ifort 12.0.0

将nbo_5g.src的1~25125行保存为NBO_5GA.SRC  
将nbo_5g.src的25126行~末尾保存为NBO_5GB.SRC  
ifort -o enable enable.f  
./enable  
依次选  
(1) 32-bit Unix   UNIX/LINUX  //无论是否系统是64bit，都要选32bit，否则运行不正常  
(1) GEN      GENNBO  (standalone)  
第三步直接敲回车，得到gennbo.f

在gennbo.f里搜索IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR.NE.'gh')， 改为IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR).NE.'gh'))  
再搜索IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR).NE.'gh')，改为IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR).NE.'gh'))

最后ifort -o gennbo gennbo.f -diag-disable 8290即得到可执行程序gennbo。  
运行时输入比如./gennbo < AC.47即可，这里AC.47是GENNBO的输入文件。

## ======编译G03 C.02的l607版本方法=======

严格按照《Fedora7-64bit下编译Gaussian03-C02》（<http://sobereva.com/2>）的方法先编译一遍32bit g03 C.02版并设定好运行环境，确保编译到了/sob/g03下面。如果你的软件平台、目录和文中不一样，笔者不保证能按文中的方法编译成功。

将nbo_5g.src的1~25125行保存为NBO_5GA.SRC  
将nbo_5g.src的25126行~末尾保存为NBO_5GB.SRC  
将这两个文件连同enable.f都拷进/sob/NBO5，并进入此目录，运行  
ifort -o enable enable.f          //这步也可以用别的fortran编译器  
./enable  
选择32-bit Unix，然后选G03，然后直接回车

在新生成的g03nbo.f里面搜索IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR.NE.'gh')， 改为IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR).NE.'gh'))  
再搜索IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR).NE.'gh')，改为IF(MORB.EQ.0.AND.NAMEAT(IATNO(NCTR).NE.'gh'))

将g03目录下l607.a删掉，将l607.exe改名为l607old.exe，l607.F改名为l607old.F作为备份。  
将g03nbo.f复制到g03目录下作为l607.F文件。

进入csh环境，source /sob/g03/bsd/g03.login，并进入/sob/g03下  
make -f bsd/i386.make l607.exe  
一会儿，l607.exe就在g03目录下生成了。

对应NBO5.0的l607.F和编译好的l607.exe可以从这里下载：[/usr/uploads/file/20150610/20150610212517_49774.zip](http://sobereva.com/usr/uploads/file/20150610/20150610212517_49774.zip)  
对于其它版本g03这个编译好的版本应该是不兼容的。
