---
post_id: 126
title: GauMD2xyz：将Gaussian的从头算动力学轨迹转换为xyz轨迹的程序
url: http://sobereva.com/126
date: '2015-06-07T23:53:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- 分子动力学
- 可视化
academic_relevant: true
classification_reason: 标题是Gaussian动力学轨迹转xyz程序，软件焦点非常明确。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**GauMD2xyz：将Gaussian的从头算动力学轨迹转换为xyz轨迹的程序**  
GauMD2xyz: A program that converts Gaussian ab-initio dynamics trajectories to xyz trajectories

文/Sobereva@[北京科音](http://www.keinsci.com)   2020-Apr-5

最新版本：1.2  
下载地址：<http://sobereva.com/soft/GauMD2xyz_1.2.zip>  
其中带.exe的是Windows版可执行文件，无后缀的是Linux版可执行文件。

简介：  
此程序用来将Gaussian的BOMD或ADMP任务产生的轨迹转化为多帧.xyz格式（格式介绍见<http://sobereva.com/477>），以便被动力学可视化程序如VMD所进一步分析。

首先在Gaussian中执行BOMD或ADMP任务。之后启动本程序，输入fch/fchk文件名或者Gaussian输出文件名（必须以.out或.log为后缀），然后输入要产生的.xyz文件路径即可。文件包里有个test目录，里面包含了一些例子。

如果BOMD任务的ntraj设为了大于1，即计算多条轨迹，本程序还会提示用户选择要读入哪条轨迹。
