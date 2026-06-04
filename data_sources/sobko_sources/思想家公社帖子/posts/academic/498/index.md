---
post_id: 498
title: OfakeG：使GaussView能够可视化ORCA输出文件的工具
url: http://sobereva.com/498
date: '2019-07-17T19:42:00+08:00'
source_categories:
- 量子化学
- ORCA
primary_topic: 其它软件
secondary_topics:
- ORCA
- Gaussian
- 可视化
- 结构与文件格式
academic_relevant: true
classification_reason: 标题是 OfakeG 工具，主要目的是让 GaussView 可视化 ORCA 输出文件。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**OfakeG：使GaussView能够可视化ORCA输出文件的工具**

OfakeG: A tool that enables GaussView to visualize ORCA output files

文/Sobereva@[北京科音](http://www.keinsci.com)

First release: 2019-Jul-17  Last update: 2024-Oct-30

## 1 前言

量子化学程序ORCA用的人越来越多，功能很强大而且免费，用户数在所有量化程序中已经是第二高（虽然跟Gaussian比还遥不可及）。但至少在笔者撰写此文时，相对于用户数占绝对主导地位的Gaussian程序而言，仍有一个不足之处是没有像GaussView那样的很理想的图形界面。虽然也有Avogadro、Chemcraft、Gabedit等程序能支持ORCA，但都没GaussView用着舒服。

在产生输入文件方面，Multiwfn已经提供了产生ORCA常见任务的输入文件的功能，见《详谈Multiwfn产生ORCA量子化学程序的输入文件的功能》（<http://sobereva.com/490>），用户只需要用GaussView画好结构，保存为gjf/mol/mol2/pdb格式，就可以用Multiwfn很方便地得到ORCA输入文件，所以在建模、产生输入文件方面，对ORCA用户没什么困难的。在观看ORCA产生的轨道、做波函数分析方面，Multiwfn也都提供了极其丰富的功能，相关信息见《使用Multiwfn观看分子轨道》（<http://sobereva.com/269>）、《Multiwfn FAQ》（<http://sobereva.com/452>）等文章，因此ORCA用户在后处理分析方面也没任何压力。另外，Multiwfn可以基于ORCA的输出文件绘制各类光谱图，所以ORCA用户在光谱研究方面也已经很方便了，相关信息见《Simulating UV-Vis and ECD spectra using ORCA and Multiwfn》（<http://sobereva.com/485>）、《Simulating UV-Vis and ECD spectra using ORCA and Multiwfn》（<http://sobereva.com/485>）。笔者在**北京科音高级量子化学培训班**（<http://www.keinsci.com/KAQC>）里还对ORCA的使用做了超级全面系统又深入的讲解，可以很快上手并用得游刃有余。

虽然Multiwfn已经解决了ORCA用户在使用方面的大量障碍，但几何优化轨迹/收敛情况的考察以及振动模式的观看不属于Multiwfn的范畴，而目前却没有理想的解决办法。虽然Chemcraft也能观看ORCA的优化轨迹，但终究没有常用的GaussView用着舒服，而且还是收费程序；Avogadro虽然也观看ORCA的振动分析对应的振动动画，但显示效果不理想，在Windows下容易崩溃、出现异常（至少在笔者的Win7-64bit机子上是如此）。尽管也可以让Gaussian与ORCA挂接，这样可以使ORCA做计算但是输出的是Gaussian格式的信息，从而等效实现让GaussView观看ORCA计算的结果的目的，见《将Gaussian与ORCA联用搜索过渡态、产生IRC、做振动分析》（<http://sobereva.com/422>），但这样做稍显麻烦、在Windows下也没法用。

显然，如果能开发个程序把ORCA的优化、振动分析、优化+振动分析的输出文件“伪造”成Gaussian的，这样就可以令GaussView直接支持读取ORCA的输出文件了，使得ORCA对于常见问题的研究用起来方便得多，也明显便于Gaussian用户同时掌握ORCA程序。笔者开发的OfakeG程序就是实现这个目的，下面介绍一下。如果你想一睹为快这个程序的实际效果，可以看这个视频：《基于ORCA量子化学程序对分子做优化、振动分析、观看红外光谱、观看轨道的简单演示》（<https://www.bilibili.com/video/av59599938>），其中用到了此程序。

**OfakeG的学术合理性声明**：本程序的开发灵感来自于Grimme的xtb程序。xtb程序做振动分析的时候会自动输出一个伪造Gaussian的振动分析输出文件，目的是为了让用户看振动模式方便；xtb程序为了兼容GSM也官方支持伪造ORCA的输出文件。大牛Grimme直接用的就是fake这个词。显然令A程序输出B程序的格式在学术界是非常正常的事情。Gaussian的输出格式是公开的而非加密的，GaussView能读入的格式也相当于是公开的，本文的OfakeG程序亦没有对GaussView本身做任何篡改，明显从各个角度上本程序的开发是完全学术正当的。本程序所做的事仅仅是将ORCA的输出信息转化成Gaussian的格式而已，文中所谓“伪造”只不过是常规的文件格式转换而已，和数据层面的“造假”有天壤之别，转换出的文件里也根本没有任何文字体现这文件是靠Gaussian程序算出来的。此程序的开发目的是给广大科研工作者提供个便利，开发/使用此程序不涉及任何侵权和学术不端（除非你利用OfakeG之后，把ORCA算的结果说成是Gaussian算的）。此程序愿意用就用，不爱用的、缺乏对计算化学领域程序状况基本认识的、怀有恶意的、有特殊利益驱动的人以及杠精，不要强词夺理在学术合理性上乱喷此程序。

## 2 OfakeG程序

### 2.1 介绍+使用方法

OfakeG程序可以在官方页面下载：[**http://sobereva.com/soft/OfakeG**](http://sobereva.com/soft/OfakeG)  
其中带.exe后缀的是Windows版，不带后缀的是Linux版。

此程序目前支持处理ORCA的opt、freq和opt freq任务的输出文件（不支持单点任务文件，因为根本没有任何转换的意义！）。此程序对ORCA 4.x、5.x、6.x版经测试可用，对于其它版本可能兼容也可能不兼容，请读者自行尝试。等ORCA以后出新版本，并且笔者发现和OfakeG不兼容时，预计笔者会更新此程序并更新本文。

OfakeG使用非常简单。启动此程序后，把上述任务的ORCA输出文件路径输入进去（对于Windows也可以直接把文件拖进去，路径会直接显示出来），一按回车，就会在当前目录下产生伪造的Gaussian输出文件。如果输入文件名字是yuri.out，则输出文件将是yuri_fake.out。这个输出文件可以直接载入GaussView，对opt或opt freq任务可以播放优化过程的动画、用results - Optimization观看优化过程的收敛情况，对freq或opt freq任务可以用results - Vibrations观看振动模式。

在Windows下还有更省事的运行方式，即可以直接将ORCA输出文件拖到OfakeG.exe图标上，此时在ORCA输出文件的目录下会出现文件名带_fake的伪造的Gaussian输出文件。

OfakeG也可以通过命令行方式使用，比如在Linux下可以在OfakeG所在目录下运行./OfakeG Aika.out，将在当前目录下得到Aika_fake.out。显然，你也可以自写shell脚本用这个程序大批量转换ORCA输出文件。

OfakeG文件包里的.out文件是一些ORCA的示例输出文件。如果你的输出文件转换不成功，请尝试通过对照这些示例文件搞清楚是怎么回事。目前OfakeG名义上只支持HF/DFT的输出文件，其它理论方法不一定能支持。对于加了乱七八糟复杂关键词的情况，OfakeG也不一定能处理。

如果OfakeG处理你的文件时崩溃，且得到的_fake后缀的文件里只有几行信息，很有可能是因为你的ORCA输出文件的编码是UTF16造成的，OfakeG是处理不了前者的情况的，是什么编码和你用的终端有关系。比如Windows的cmd终端重定向输出的文件是ASCII编码的，而PowerShell是UTF16编码的。对于UTF16编码的输出文件，你可以用比如Ultraedit打开，选另存为，把编码改成Unicode或UTF8，之后再用OFakeG处理。如果你平时习惯用PowerShell且希望重定向出的文件直接就ASCII编码，可以用诸如这样的命令运行test.inp得到test.out：D:\study\orca\orca test.inp | out-file test.out -encoding ascii  
如果是Win10，还可以直接指定默认的重定向的编码，详见<https://stackoverflow.com/questions/40098771/changing-powershells-default-output-encoding-to-utf-8>。

如果你怎么也搞不清楚为什么你的ORCA输出文件无法转化成功，或者可判定OfakeG程序有bug，请在<http://bbs.keinsci.com/thread-13952-1-1.html>贴子里发回帖，把文件压缩后上传。

### 2.2 OfakeG的几个细节

以下内容建议留意一下，以更好地理解OfakeG的细节，但初学者不看也可以。

OfakeG给出的是简化到不能再简化的能令GaussView正常读取的伪造的Gaussian输出文件，因此如果你写类似工具把其它程序的输出文件也伪造成类似格式，就也可以令GaussView读取。

GaussView要求输出文件里必须有basis functions、alpha electrons、beta electrons信息，但ORCA输出文件里不直接体现，而且这仨对于观看优化和振动分析没有意义，因此在伪造的输出文件开头有这仨信息，但数值都为0。

OfakeG从ORCA输出文件里读能量的时候读的是FINAL SINGLE POINT ENERGY，即当前计算级别下的最终能量。而产生伪造的Gaussian输出文件时，为了省事和统一，是以SCF Done标签来输出的。

Gaussian做优化任务的时候，对每一步，输出次序是[结构i]-[结构i的能量]-[结构i的受力]-[结构i的收敛情况]，所以结构、能量、收敛信息都是一一对应的。而对于ORCA，输出也是这样的顺序，但最后在第i步时发现已经满足收敛限了，之后还会根据第i步的信息再预测出第i+1步的结构，并且计算这个结构下的能量（也顺带得到波函数），而这个i+1结构就不再计算受力了，也因此对这个结构也不再输出收敛判断信息。所以OfakeG产生的伪造的Gaussian输出文件中，第1步到第i+1步的结构、能量、收敛情况都会给出，但最后一次输出的收敛情况信息里当前值全都被设成0来占位。

优化过程中除了像Gaussian一样用受力/位移的最大/RMS值作为判断标准外，ORCA还用能量变化作为判断标准。为了体现这点，在伪造的Gaussian输出文件中也在收敛判断部分添加了这项，但这项不会被GaussView所读取，大家可以自行考察。

对于振动分析，由于ORCA不会给出约化质量和振动模式的力常数，所以伪造的Gaussian输出文件里也没这项，这不影响一般的分析。由于ORCA不给出振动模式的不可约表示，所以OfakeG把不可约表示都一律输出为A。

OfakeG把ORCA振动分析输出的热力学数据也都转化为了Gaussian的输出形式，对于用惯了Gaussian的人来说读起来方便不少，并且还顺带多显示了一项Electronic energy=，后面是振动分析对应的结构的电子能量。

OfakeG以后版本也有可能支持处理ORCA的IRC任务的输出文件，但目前没有打算支持。因为笔者撰文时最新的ORCA 4.1.2版的IRC功能非常弱、速度慢，甚至就连反应坐标都不给出来，原理上没法转换成Gaussian的格式。另外OfakeG也不会去支持转换ORCA的TDDFT等电子激发任务的输出文件，因为做这个转换没有任何实际意义。Multiwfn直接就能基于ORCA的TDDFT输出信息绘制各种电子光谱和做电子激发分析（后者我都有现成的例子，见<http://sobereva.com/485>。Multiwfn绘制光谱的更详细介绍见<http://sobereva.com/224>），而且ORCA目前版本给出的是TDDFT组态函数的贡献而不是系数，原理上也不可能转换为Gaussian形式的输出。

OfakeG是100%纯Fortran写的，没有利用任何库和其它任何编程语言（或许有的人能猜到我为什么刻意彰显这点）。
