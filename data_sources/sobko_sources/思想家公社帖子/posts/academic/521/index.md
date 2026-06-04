---
post_id: 521
title: Grimme的xtb程序的编译方法
url: http://sobereva.com/521
date: '2019-11-21T05:29:00+08:00'
source_categories:
- 量子化学
primary_topic: xTB
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 Grimme 的 xtb 程序编译方法，明确是软件安装/编译教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**Grimme的xtb程序的编译方法**

Compilation method of Grimme's xtb program

文/Sobereva@[北京科音](http://www.keinsci.com)  2019-Nov-21

之前笔者在《将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC、做振动分析》（<http://sobereva.com/421>）中已经对xtb程序的基本情况进行了介绍，也说明了安装方法。通常直接用预编译版的xtb就够了，但有时候为实现特殊目的需要改代码，这就需要自己编译了。本文介绍一下在CentOS 7.4下的编译。机子里已经装了ifort+icc 19.0.1.144编译器。xtb用的是<https://github.com/grimme-lab/xtb/releases>下载的6.2.1版。对于其它操作系统、其它版本xtb的情况请根据实际提示随机应变。

先安装Python 3：  
yum install python3  
这会把pip3也装上。

之后运行以下命令把meson和ninja都装上，这俩是干什么的参考《DFT-D4色散校正的简介与使用》（<http://sobereva.com/464>）里的说明。  
pip3 install meson  
yum install ninja-build  
（注：虽然yum install meson也可以装meson，但源里面的版本太老，而xtb 6.2.1要求必须版本>=0.49，因此用pip3来装）

将xtb的源代码包解压，打开此目录下的meson.build，在  
## ========================================== ##  
## LIBRARIES  
部分的前头一行加上  
add_project_link_arguments('-L/usr/lib/x86_64-redhat-linux6E/lib64/', language: 'c')  
否则在链接可执行文件时可能会提示找不到库文件。

之后在xtb目录下运行  
export FC=ifort CC=icc CXX=icpc  
meson setup build_intel --optimization=2  
ninja -C build_intel

编译过程不到10分钟，中途如果卡着不动，屏幕上提示dep hack，不要着急，慢慢等着即可。

编译完了之后在build_intel目录下就会看到xtb可执行文件。将之挪到xtb可执行文件包里覆盖原有的可执行文件即可。
