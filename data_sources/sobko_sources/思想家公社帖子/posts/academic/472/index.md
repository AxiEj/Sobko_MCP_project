---
post_id: 472
title: 将多帧xyz文件转化成量子化学输入文件的工具：xyz2QC
url: http://sobereva.com/472
date: '2019-03-17T12:21:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 结构与文件格式
- 量子化学
- xTB
academic_relevant: true
classification_reason: 标题是 xyz2QC 工具，用于把多帧 xyz 转成量化软件输入文件，主角是未列出的工具。
topic_family: 软件
exclude_reason: ''
confidence: 0.94
image_count: 0
local_assets_dir: assets
---

**将多帧xyz文件转化成量子化学输入文件的工具：xyz2QC**

xyz2QC: A tool to convert multi-frame xyz files to input files of quantum chemistry program

文/Sobereva@[北京科音](http://www.keinsci.com)  
 First release: 2019-Mar-17  Last update: 2021-Aug-26

## 1 前言

笔者开发的免费的做构象搜索和团簇构型搜索的Molclus程序是如今最为流行的构型和构象搜索程序之一，介绍和下载见官网<http://www.keinsci.com/research/molclus.html>。Molclus做搜索过程一般流程是先用十分廉价但粗糙的级别（如调用Openbabel跑MMFF94、调用xtb跑GFN-xTB）做结构优化和初步筛选，将其中能量最低的、为数不多的一批体系保留，最后再调用量子化学程序用更准确的方法算能量或做进一步优化。在整个过程中，初筛的耗时很低，在个人计算机上跑也没有任何压力，而最后对为数不多的筛出来的体系进一步做DFT/后HF量子化学计算才是占整个搜索过程的大头，才是真正有必要弄到超算上跑的（对于那些没有自己的像样的服务器的人而言）。然而，在超算上，计算任务一般是以提交方式进行的，而molclus这样自动调用其它程序去运行的方式在超算上不方便使用。为了解决这个矛盾，本文介绍笔者开发的xyz2QC程序。xyz2QC作为Molclus程序（1.7版及之后）的一个子程序发布，在Molclus压缩包里就可以找到。

## 2 xyz2QC介绍

xyz2QC可以基于Gaussian和ORCA的模板文件，将含有多帧的.xyz文件中指定的一批帧转化成Gaussian和ORCA输入文件。

模板文件的格式要求和molclus的完全一样，Gaussian的必须叫template.gjf，ORCA的必须叫template.inp，运行xyz2QC前必须将之放在当前目录下。

读进xyz2QC的多帧的.xyz可以是genmer、gentor直接产生的，也可以是molclus跑完后产生的isomers.xyz，也可以是isostat筛选、排序、归簇后产生的cluster.xyz。

转化出的Gaussian/ORCA的输入文件，既可以是所有被选择的结构作为多步任务出现在同一个输入文件里的，也可以要求拆分成一个个独立的文件，比如000001.gjf、000002.gjf...文件名是.xyz里的帧号，文件名数字前头可以自行定义前缀。

## 3 例子

xyz2QC使用极其简单，下面是一个简单例子。

假设我们之前用molclus对某个有机分子在粗糙的半经验方法PM7下做了批量优化，并用isostat做了处理，得到了按照能量排序后的cluster.xyz文件（可以这里下载：<http://sobereva.com/attach/472/cluster.xyz>）。这里我们想把其中能量最低的三个转化成.gjf文件，之后弄到超算/服务器上算更准确的能量，于是我们准备一个Gaussian模板文件template.gjf，内容为比如

%nproc=4  
 # M062X/TZVP

Template file

0 1  
 [GEOMETRY]  
 <---此处有空行  
 <---此处有空行

我们将cluster.xyz、template.gjf都放到xyz2QC目录下，然后进入此目录，启动xyz2QC，按照屏幕操作，依次输入：  
1  //产生含多步的单一Gaussian输入文件  
cluster.xyz  //输入.xyz的实际路径，因为此文件就在当前目录，因此这里不用输绝对路径  
1-3  //我们只需要算能量最低的三个结构，由于cluster.xyz里已经按照能量排序，所以这里我们选择xyz文件里的第1~3帧

此时程序提示Gaussian.gjf已经产生在了当前目录，按回车退出即可。这个文件的内容是这样的：  
%nproc=4  
 # M062X/TZVP

Template file

0 1  
 O          -2.30907426      1.90383755      0.11387296  
 ...略  
 H          -3.80099226     -1.36391720      0.45491869

--link1--  
 %nproc=4  
 # M062X/TZVP

Template file

0 1  
 O          -2.47455224      1.86708010     -0.16509991  
 ...略  
 H          -3.70656780     -1.42641602      0.64335011

--link1--  
 %nproc=4  
 # M062X/TZVP

Template file

0 1  
 O          -2.34444893      1.89718026      0.06136974  
 ...略  
 H          -3.75360804     -1.39079507      0.53898348

有一定Gaussian基础的人都知道，在Gaussian的输入文件里可以用--link1--来将多步任务进行分隔，因此直接执行Gaussian.gjf，这三个结构的能量就都会挨个算出来了。之后我们可以用比如Ultraedit或者Linux下的grep命令直接把带有SCF Done字样的行都提取出来，就直接得到这三个结构的能量了，非常方便！

注意--link1--前头的空行数目必须对，否则多步任务将运行不成功，上面产生的Gaussian.gjf这样是没问题的。--link1--前面空行数目取决于template.gjf末尾的空行数。

xyz2QC还允许将.xyz里的指定帧拆分成产生单独的.gjf文件，这有何意义？一般来说，像上面这样把多个结构弄到一个.gjf里运行起来最方便，但有一个缺点是如果其中一个任务失败了（如SCF不收敛、几何优化不收敛），那么整个任务就会停了，后面的步骤也不算了。如果拆成单独的.gjf文件，那就没这个问题了。

Gaussian模板文件中可以使用[FILENAME]占位，xyz2QC产生输入文件时它将被替换为"前缀 帧号"，因此可以在模板文件里写比如%chk=/sob/[FILENAME].chk从而使得计算完毕后chk文件以恰当的名字留存在/sob目录下。这对于通过Multiwfn程序批量做波函数分析尤其有用。当有多帧的xyz文件，想对里面每个结构都用Multiwfn做波函数分析时，可以拆分完了后批量执行，得到对应的chk文件，然后再批量转换成fch，最后通过批处理脚本调用Multiwfn批量分析。怎么靠脚本实现批量转换和执行见《使用Gaussian时的几个实用脚本和命令》（<http://sobereva.com/258>）。

类似地，xyz2QC还可以产生ORCA的输入文件，也是可以作为多步任务构成单一文件，或拆分成不同的文件。对于多步任务，强烈建议在模板文件template.inp里加入noautostart关键词，要不然下一个任务的初猜会自动用前一个任务收敛的波函数，然而你选定的那些结构的几何差异可能不小，因此这样得到的初猜可能会很糟糕。noautostart代表不自动从与当前文件同名的.gbw文件中读取初猜波函数，就可以确保没这个问题。
