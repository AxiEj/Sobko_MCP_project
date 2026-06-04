---
post_id: 564
title: XCrySDen在CentOS上的傻瓜式安装方法
url: http://sobereva.com/564
date: '2020-07-22T06:19:00+08:00'
source_categories:
- 第一性原理
primary_topic: 其它软件
secondary_topics:
- 第一性原理
- 可视化
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 XCrySDen 在 CentOS 上的安装方法，软件不在指定列表内。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**XCrySDen在CentOS上的傻瓜式安装方法**

Foolproof installation method of XCrySDen on CentOS

文/Sobereva@[北京科音](http://www.keinsci.com)  2020-Jul-22

## 1 前言

XCrySDen（<http://www.xcrysden.org>）是非常流行的第一性原理程序Quantum ESPRESSO用户经常用的重要工具，可以观看输入输出文件、观看轨迹、设置k点等，而且作图效果挺不错。XCrySDen在Ubuntu上比较容易运行，但对于做计算化学的人用得非常多的CentOS就不那么容易了。XCrySDen很老的版本提供了semishared版，在CentOS里解压后就能运行，但较新的XCrySDen官方只提供了shared版（至少是对于撰文时最新的1.6.2版而言），里面涉及的一些动态库在CentOS里没有相应的源。为了让CentOS用户用XCrySDen毫无障碍，笔者在CentOS下编译了XCrySDen，并且同时提供了傻瓜式编译的源代码包。

## 2 预编译版XCrySDen的安装

下载<http://sobereva.com/attach/564/xcrysden-1.6.2_sobereva.tar.gz>。解压后，进入此目录，运行./xcrysden就可以启动了。如果在~/.bashrc目录下加上export PATH=$PATH:[XCrySDen的目录名]，则重新进入终端后就可以在任意目录下直接启动XCrySDen了。

这个笔者编译的XCrySDen 1.6.2在CentOS 7系列各个版本上都可以运行。如果读者装系统的时候装的方式和《在VMware 15中安装CentOS 7.6的完整过程视频演示》（<http://sobereva.com/454>）里演示的相同，不需要装额外的库就可以直接运行。如果运行时提示缺库，Google一下报错提示，用yum安装相应的包即可。

对于CentOS 8.0，笔者发现没法直接运行，但只要把解压后目录下的tcl目录下的xcInit.tcl里的两处0m都改为0就可以运行，并且关闭程序的时候必须点击右上角强行关闭。

## 3 XCrySDen的编译

下面是基于笔者修改的XCrySDen 1.6.2的源代码包的编译过程。前面说的笔者的预编译版如果能正常用就没必要自己编译。在CentOS 7.x和8.0下按以下方法都能编译通过。

运行以下命令安装编译过程要用的库  
yum install libGL-devel libGLU-devel libXmu-devel

机子里应当已经装了gcc和gfortran，如果没装的话运行yum install gcc-gfortran来安装。

下载笔者修改的源代码包：<http://sobereva.com/attach/564/xcrysden-1.6.2_src_sobereva.tar.gz>。解压后进入其中，运行make all即可，大约5分钟就能编译完毕。之后直接运行./xcrysden即可启动。

对于某些CentOS版本，比如CentOS 7.4，编译中途可能失败，需要在解压目录下的Makefile中的X_LIB=后面加入-lXss选项，然后重新make all。经测试至少对于CentOS 7.7不用加这个。

关于笔者修改的XCrySDen源代码包的一些细节：Make.sys文件是在system/Make.sys-shared基础上修改的，原先的这个文件完全没法用，笔者改了许多地方才终于令编译能成功。具体改了哪些，自行对照Make.sys-shared就知道了。Makefile文件也做了修改，把all:后面的mesa去掉了，因为CentOS的源直接就有这个，通过前述的yum步骤已经安装了，因此就没必要再在make all的时候编译了。其实对于CentOS 8，由于源里的tcl/tk已经升为了XCrySDen 1.6.2要求的8.6版，因此不编译tcl/tk而直接通过源来装也不是不可以。另外，原本make all的时候会自动下载tcl、tk、Togl、fftw、bwidget包，但在大陆地区由于网速问题，很容易中途下载失败。因此笔者直接将这些压缩包放到了external/src目录下，这样编译过程中就会自动利用，而不自动下载这些包了。
