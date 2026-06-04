---
post_id: 530
title: 一键把所有gjf文件转成xyz文件、把所有Gaussian输出文件转成gjf文件的脚本
url: http://sobereva.com/530
date: '2020-01-28T05:27:00+08:00'
source_categories:
- Multiwfn
- 量子化学
primary_topic: Multiwfn
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是批量转换 Gaussian 文件格式的脚本，核心是 Multiwfn 的格式转换功能。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**一键把所有gjf文件转成xyz文件、把所有Gaussian输出文件转成gjf文件的脚本**

Script to convert all gjf files to xyz files and convert all Gaussian output files to gjf files in one click

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2020-Jan-28  Last update: 2023-Jun-12

本文提供笔者写的两个Linux下的Bash shell脚本，对实际研究有一定价值，都利用了Multiwfn程序进行格式转换，因此Multiwfn必须已恰当安装从而能通过Multiwfn命令直接启动。Multiwfn可以在<http://sobereva.com/multiwfn>免费下载（Linux下的安装方法见手册2.1.2节），一定要用最新版本。这俩脚本在Multiwfn的examples\scripts目录下也可以找到。

把本文的脚本稍微改写几行，就也可以利用Multiwfn在其它格式间进行转换，非常方便。Multiwfn支持的格式详见《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）。笔者十分建议仔细看看《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>），里面对通过命令行和脚本批量运行Multiwfn做了特别透彻的说明，看过之后就可以游刃有余地改写本文的脚本。

## 1 一键把所有gjf文件转成xyz文件

脚本下载：<http://sobereva.com/attach/530/gjf2xyz.sh>

这是把当前目录下所有Gaussian输入文件（gjf）转成xyz文件的脚本，直接运行即可。gjf文件应当是以笛卡尔坐标记录。

输出信息例子  
Converting AlCl3.gjf to AlCl3.xyz ... (2 of 151)  
 Converting Aniline.gjf to Aniline.xyz ... (3 of 151)  
 Converting Azetidine.gjf to Azetidine.xyz ... (4 of 151)  
 Converting B2H6.gjf to B2H6.xyz ... (5 of 151)  
 Converting Benzaldehyde.gjf to Benzaldehyde.xyz ... (6 of 151)  
 Converting Benzene.gjf to Benzene.xyz ... (7 of 151)  
 Converting Benzonitrile.gjf to Benzonitrile.xyz ... (8 of 151)  
 ...

## 2 一键把所有Gaussian输出文件转成gjf文件

脚本下载：<http://sobereva.com/attach/530/out2gjf.sh>

这是把当前目录下所有Gaussian输出文件（out）转成gjf文件的脚本，直接运行即可。运行之前必须将Multiwfn的settings.ini文件里的iloadGaugeom设为1（否则Multiwfn在载入out文件时不会从中读取数据）。得到的gjf文件里是默认关键词，应当根据实际情况进行修改。电荷和自旋多重度和out文件里一致（用了赝势的情况除外，需要自行手动修改gjf）。坐标是输出文件里最后一次输出的（如果有输入朝向的坐标则新生成的gjf里也是输入朝向的，没有的话就是标准朝向的。不了解朝向问题的话参看《谈谈Gaussian中的对称性与nosymm关键词的使用》<http://sobereva.com/297>。如果把iloadGaugeom设为2，则总是载入标准朝向下的坐标）。

上面的脚本产生的Gaussian输入文件是笛卡尔坐标的，如果要输出为内坐标的输入文件，改用此脚本：<http://sobereva.com/attach/530/out2gjf_zmat.sh>。注意对某些体系，比如乙炔，原理上其结构就没法用内坐标描述（除非引入虚原子），对这样的体系无法成功产生Gaussian输入文件。

如果你的Gaussian输出文件是log后缀，把脚本里的out替换为log即可。也可以批量把诸如xyz、mol、mol2、pdb、gro、wfn、wfx、cub等各种Multiwfn支持的输入文件转成gjf，也是同样地把这个.sh脚本里的out替换成相应后缀即可（对于把fch、molden、mwfn等含有基函数信息的波函数文件转成gjf文件，应当在脚本的${inf//out/gjf}下面插入内容一行，内容是n，代表不把当前波函数作为初猜信息写入gjf）。

Multiwfn产生的gjf里关键词默认为B3LYP/6-31G*。可以按照《使用Gaussian时的几个实用脚本和命令》（<http://sobereva.com/258>）里第5节所述的方法批量把所有gjf文件里的关键词替换成实际要用的关键词。如果当前目录下有个template.gjf文件，并且其中坐标部分用[geometry]或[GEOMETRY]代替，则这个文件会自动被当做模板文件产生新的gjf，而含有[geometry]或[GEOMETRY]的这一行会被替换为当前体系的坐标。如果输入文件里某一行或几行里有[name]字样，则这六个字符会被替换为新产生的输入文件名（不含后缀）。如果你载入的是Gaussian输入或输出文件、ORCA输入文件或者含有波函数信息的文件，新产生的gjf文件里的净电荷和自旋多重度会用读入的，否则会沿用template.gjf里的。允许使用template.gjf的设计给产生特殊的输入文件的情况来了极大的灵活性。下面是个用template.gjf的例子，方法用B3LYP-D3(BJ)，给Ag用SDD赝势基组，给C H O用6-311G*，任务是优化和振动分析，并产生wfn和chk文件，其文件名和你创建的gjf的文件名相同。

%chk=D:\[name].chk  
 #p b3lyp/genecp em=GD3BJ opt freq out=wfn  
  
 niconiconi  
  
 0 1  
 [geometry]  
  
 Ag  
 SDD  
 ****  
 C H O  
 6-311G*  
 ****  
  
 Ag  
 SDD  
  
 D:\[name].wfn  
 <---此处有空行  
 <---此处有空行
