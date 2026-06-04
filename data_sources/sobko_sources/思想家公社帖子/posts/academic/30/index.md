---
post_id: 30
title: 察看Gaussian全部IOp的方法
url: http://sobereva.com/30
date: '2015-06-05T00:15:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 综述/教程/投稿经验
- 结构与文件格式
academic_relevant: true
classification_reason: 标题直接是Gaussian的IOp查看方法，属于典型软件使用教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**察看Gaussian全部IOp的方法**The way to view all IOps in Gaussian

文/Sobereva @[北京科音](http://www.keinsci.com/)  Last update: 2010-Jul-22

虽然高斯网站上提供了IOp列表，网上也有相应的pdf版IOp查询手册，但是很多IOp在那里面都没有，甚至是常用的，比如6/7就没有，只能网上搜索。实际上这些IOp所代表的意思在link程序的.F源代码头部都有完整说明。  
  
这里说一下在windows下查阅源代码里IOp的方便的方法  
  
由于不知道IOp(6/7)会传递给哪个link子程序，所以不能确定iop(6/7)的注释会在哪个link源程序里面，所以先通过windows的文件内容搜索功能进行简单的筛选。  
  
首先进入dos，进入包含.F源代码的目录，ren *.F *.txt，把源码都转换为.txt格式。  
  
然后在包含源代码的文件夹上点右键-搜索，在左侧会看到“文件中的一个字或词组”，输入要找的IOp。  
  
比如要找IOp(6/7)，就输入IOp(7)，然后搜索。搜索出一大堆源代码里都有对应内容，但由于6/代表的是这个设定必然传递给l6??.exe的子程序，所以只要看百位是6的子程序的源代码就行了，这里就找到一个l601，于是打开l601.txt。再搜索IOp(7)，就找到了解释：  
  
C          These options are print/no-print options.  The  
C     possible values are:  
C  
C     0 ... DEFAULT.  
C     1 ... PRINT THE NORMAL AMOUNT.  
C     2 ... DO NOT PRINT.  
C     3 ... PRINT VERBOSELY.  
C  
C     IOp(6) ... DISTANCE MATRIX.  DEFAULT:  NO-PRINT.  
C  
C     IOp(7) ... MOLECULAR ORBITAL COEFFICIENTS.  DEFAULT:  PRINT.      <<----------即IOp(6/7)  
C  
C     IOp(8) ... DENSITY MATRIX.  DEFAULT:  NO-PRINT.  
C  
C     IOp(9) ... FULL POPULATION ANALYSIS.  DEFAULT:  PRINT.  
C  
C     IOp(10) ... Gross orbital charges.  Default:  Print.  
C  
C     IOp(11) ... GROSS ORBITAL TYPE CHARGES.  DEFAULT:  NO-PRINT.  
C  
C     IOp(12) ... CONDENSED TO ATOMS.  DEFAULT:  PRINT.  
  
要重视高斯源代码里的注释，很多高斯输出的内容很抽象，但是注释里面往往有解释。  
  
  
在一些linux的高斯版本中，会看到很多.hlp文件，实际上这些文件的内容就是对应的.F文件开头注释部分当中的IOp说明部分。我们可以将之拷到windows中，用上述同样方法改扩展名并搜索。若在Linux下，我们要找IOp(6/7)就直接用命令grep IOp(7) *.hlp就行了，会看到l601.hlp里面有它的说明。  
  
Linux版本高斯还带有一个ghelp辅助程序，可以分级查看高斯程序各种模块、选项的含义，用法是ghelp [条目] [子条目] [子条目中的子条目] ...。直接运行ghelp会显示有哪些主条目，例如在其中看到有ov6（即Overlap 6）一类，继续运行ghelp ov6，就会显示ov6的相关信息和它的子条目，并会看到子条目里有比如IOp(7)。再运行ghelp ov6 "IOp(7)"（注意要有双引号，否则括号将被系统解析），显示的就正是IOp(6/7)代表的意义，和上面从.hlp文件中看到的一样，实际上ghelp显示的正是.hlp文件中相应的内容。  
  

由于hlp文件不涉及版权问题，这里就直接给大家，是G09 D.01的。  
[/usr/uploads/file/20150605/20150605002014_39780.rar](http://sobereva.com/usr/uploads/file/20150605/20150605002014_39780.rar)
