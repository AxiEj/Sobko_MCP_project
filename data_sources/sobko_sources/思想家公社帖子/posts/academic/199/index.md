---
post_id: 199
title: 产生Gaussian的IRC和SCAN任务每个点的波函数文件的工具：IRCsplit和SCANsplit
url: http://sobereva.com/199
date: '2015-06-08T00:03:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- Multiwfn
- 波函数分析
- 结构与文件格式
academic_relevant: true
classification_reason: 标题明确是 Gaussian 的 IRC/SCAN 波函数文件生成工具，软件中心很清楚。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**产生Gaussian的IRC和SCAN任务每个点的波函数文件的工具：IRCsplit和SCANsplit**  
IRCsplit and SCANsplit: Tools to generate wavefunction file for each point of IRC and SCAN tasks of Gaussian

文/Sobereva @[北京科音](http://www.keinsci.com/)  
First release: 2013-Sep-9   Last update: 2019-Mar-21

将Gaussian产生的IRC路径或SCAN任务（特指刚性扫描，后同）当中每个点的波函数文件导出，从而通过Multiwfn等程序进行分析，对于研究反应过程中电子结构的变化是十分有益的。以前写过一个帖子介绍怎么实现这一点，见《自写Link生成Gaussian的IRC任务中每个点的波函数文件》（<http://sobereva.com/85>），并介绍了应用实例，见《制作动画分析电子结构特征》（<http://sobereva.com/86>）。之前介绍的通过非标准路径+自写link的方法生成每个点的wfn文件虽然可以避免在每个点的结构下重新做一遍单点计算，但是实现过程对于初学者来说过于复杂，得自行编译Gaussian。为了简化这个过程，这里提供笔者开发的IRCsplit和SCANsplit程序，可以分别将Gaussian的IRC和SCAN任务的每个点的坐标提取出来生成一批新的单点任务文件，全都执行后就有了IRC上所有点的.wfn文件或.chk文件。

本文的一个应用例子见《通过键级曲线和ELF/LOL/RDG等值面动画研究化学反应过程》（<http://sobereva.com/200>）。

## 1 处理IRC任务

先介绍怎么处理IRC任务。IRCsplit程序的下载地址为<http://sobereva.com/soft/IRCsplit_1.0.3.rar>。

压缩包内IRCsplit.exe是Windows版可执行文件，IRCsplit是Linux版可执行文件。examples目录下是例子。script里是Windows下和Linux下用于Gaussian任务批量执行和chk->fch批量转换的小脚本。

下面就用examples下的SiH2+H2反应的IRC任务文件为例来说明用法。

examples\SiH2+H2.out是个普通的IRC任务的输出文件。Route section部分为  
# irc=(maxpoints=20,calcfc,maxcyc=50,stepsize=10) rhf/3-21g  
此任务中前后两个方向实际各走了20个点。（注意，如果maxpoints设得太大，由于可能走到了极小点，实际前后走的IRC点数都可能小于maxpoints。另外注意不要用geom=check关键词，否则输出信息和平时不符而无法被IRCsplit处理）

用户必须自己创建一个与这个IRC任务对应的普通单点文件，此文件将被作为模板来由IRCsplit生成新的输入文件。此文件中%chk不要写，route section里面只定义理论方法和基组而不写别的，但可以加上帮助收敛的关键词如vshift。里面的坐标就是过渡态结构的坐标，应当以笛卡尔坐标方式书写。末尾要空两行。examples\SiH2+H2_SP.gjf就是与SiH2+H2.out对应的单点文件例子，内容如下。  
# rhf/3-21g

IRC test:   SIH2+H2 OPTM. AT 3-21G LEVEL (STEP=0.1,POINT NUMBER 1-30)

0 1  
 Si                 0.00000000    0.00000000    0.00000000  
 H                  0.78338953    1.23552312   -0.25085843  
 H                  0.78338953   -1.23552312   -0.25085843  
 H                 -0.54807474    0.00000000    1.44193846  
 H                  0.54807474    0.00000000    1.59366154  
[空行]  
[空行]

启动IRCsplit，然后依次输入  
examples\SiH2+H2.out  
examples\SiH2+H2_SP.gjf  
3    //如果输入1，则生成的Gaussian输入文件只能用来产生.wfn，输入2则只能产生.chk，这里输入3可以让.wfn和.chk都产生  
C:\IRC\Watamote    //定义输出的.wfn和.chk文件的路径和名称  
（此时屏幕上显示出当前IRC任务文件里面向前和向后的点分别有多少。）  
20,20    //IRC前后方向的点都提取20个，加上TS结构，总共将提取41个结构。假设写的是8,13，则TS以及离它最近的正向8个点和最近的逆向13个点将被提取。当然，提取的点不能超过实际数目  
最后按回车退出。

程序已经在examples目录下生成了41个Gaussian单点任务的输入文件，即SiH2+H2_SP0001.gjf、SiH2+H2_SP0002.gjf、SiH2+H2_SP0003.gjf...建议自行随便打开一个看看内容对不对。编号从0001到0041对应于从IRC的始端经过TS到达末端的过程。

最后，将这些.gjf文件随便拷贝到某文件夹里，然后用Gaussian批量执行它们即可。可以通过如下方法实现：  
(1)如果是Windows系统，把script目录下的runall.bat拷到那个目录下，然后双击之，就会调用g09来执行此目录下所有.gjf文件。然后在就生成了C:\IRC\Watamote0001.wfn、C:\IRC\Watamote0002.wfn...以及C:\IRC\Watamote0001.chk、C:\IRC\Watamote0002.chk...如果想把所有这些.chk文件转换为.fch，就把script目录下的chk2fch.bat也拷到这个目录下并双击运行。  
注意：如果你还没有对Gaussian运行环境进行配置，应当进入 系统-高级系统设置-环境变量，把Gaussian的目录添加进用户的PATH环境变量，并新建GAUSS_EXEDIR环境变量，内容也定义为Gaussian的目录（如D:\study\g09w）。否则将无法通过命令行调用Gaussian和formchk。  
(2)如果是Linux系统，把script下的runall.sh和chk2fch.sh拷到相应目录下，然后进入此目录下运行./runall.sh和./chk2fch.sh就可以调用Gaussian运行当前目录下所有.gjf文件并且调用formchk将.chk都转换为.fch了。

注意如果用了rcfc关键词，由于过渡态结构的信息不出现在IRC任务的输出中，因此IRCsplit产生的对应于过渡态结构的.gjf文件将会是空的。请自行处理。

## 2 处理SCAN任务

SCANsplit的下载地址为<http://sobereva.com/soft/SCANsplit_1.0.rar>。

SCANsplit的使用方法和IRCsplit几乎如出一辙，区别仅在于处理的是G09的SCAN任务（注意只支持刚性扫描，不支持柔性扫描）而非IRC任务，因此不再详述。

操作例子如下，启动后输入  
examples\H2O2.out   //SCAN任务输出文件  
examples\H2O2_SP.gjf   //与此体系对应的普通单点文件，将被作为模板  
2   //假设只生成chk文件  
C:\SCAN\ltwd    //chk或wfn文件的输出路径  
按回车退出。  
此时Gaussian输入文件H2O2_SP0001.gjf，H2O2_SP0002.gjf...就在examples目录下生成了。按照前述方法批量执行即可。
