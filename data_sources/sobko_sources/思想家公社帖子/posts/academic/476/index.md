---
post_id: 476
title: 计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）
url: http://sobereva.com/476
date: '2019-04-17T20:48:00+08:00'
source_categories:
- Multiwfn
- 分子模拟
primary_topic: Multiwfn
secondary_topics:
- 分子模拟
- 静电势与电荷
academic_relevant: true
classification_reason: 标题是用 Multiwfn 一行命令计算 RESP 原子电荷，属于软件脚本教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**计算RESP原子电荷的超级懒人脚本（一行命令就算出结果）**

A super lazy script to calculate RESP atomic charges (one line of command calculates the result)

文/Sobereva@[北京科音](http://www.keinsci.com)  
First release: 2019-Apr-17  Last update: 2024-Sep-6

RESP电荷主要优点是特别适合对柔性分子做分子动力学计算。之前笔者写过《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）一文，极其详细地介绍了RESP电荷，并结合实际例子充分展现了Multiwfn在计算RESP电荷上的强大性，可谓极度便利而且极度灵活，明显比Antechamber等其它能计算RESP的程序好用、方便得多得多得多。但在网上的答疑过程中，笔者也看到很多要计算RESP电荷的人完全是量子化学外行，甚至GaussView都不会用，Gaussian的关键词一点也不会写，需要一个极度傻瓜化的“一键”工具来计算RESP电荷，为此笔者在这里介绍一个基于Gaussian和Multiwfn的仅仅需要写一条命令就可以算出RESP电荷的Linux环境下的脚本，可谓将RESP电荷的计算极尽简化，不可能做到更简单了。

另外，笔者在《RESP2原子电荷的思想以及在Multiwfn中的计算》（<http://sobereva.com/531>）中介绍了RESP2电荷，在文中也提供了和本文使用方式基本一样的脚本RESP2.sh来专门用于一键计算RESP2电荷。如果你计算RESP电荷的目的是用于分子动力学模拟，笔者更建议用RESP2来算，有较大可能结果更好。

如果你没买Gaussian，也可以用免费的ORCA量子化学程序结合Multiwfn算各种原子电荷，笔者也提供了相应的傻瓜式脚本，见《ORCA结合Multiwfn计算RESP、RESP2和1.2*CM5原子电荷的懒人脚本》（<http://sobereva.com/637>）。

如果你想了解本文提供脚本原理是怎么回事，强烈建议仔细阅读《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>），里面将一切细节都解释得特别清楚，并能充分体会到写脚本运行Multiwfn多么重要和便利。

## 1 准备工作

在机子里安装Gaussian。不会装的话仔细看《Gaussian的安装方法及运行时的相关问题》（<http://sobereva.com/439>）。去<http://sobereva.com/multiwfn>下载Multiwfn最新版本。然后严格按照《Multiwfn在Linux下安装的中文说明》（<http://sobereva.com/688>）说的方式安装到Linux下面，从而能通过输入Multiwfn命令启动程序（如果你装的是noGUI版，需要把下面说的脚本里的Multiwfn改为Multiwfn_noGUI）。

对Multiwfn目录下的examples\RESP\目录下的RESP.sh根据需要进行恰当的修改。此脚本默认调用的是g09，Gaussian16的用户应当将其中的g09替换为g16。此脚本默认为在B3LYP-D3(BJ)/def2-SVP级别下对结构进行优化，然后在B3LYP-D3(BJ)/def2-TZVP级别下计算单点能同时产生分子表面静电势数据，然后调用formchk把chk文件转化为fchk，最后调用Multiwfn产生RESP电荷。量化计算级别在这个脚本里都体现得很清楚，大家可以根据需要对关键词进行修改。

此脚本默认的计算级别算出的RESP电荷的质量已经很好。当前脚本自动做的B3LYP-D3(BJ)/def2-SVP级别的几何优化对50个原子体系的耗时就已经不太低了，因此几何优化部分如果算不动或者想显著降低耗时的话，可以把原有的关键词改为# PM6D3 opt，即使用PM6-D3半经验方法在真空中做优化，但这个级别主要只适合普通有机体系而且体系没有局部具有显著离子特征的情况。虽然这样得到的结构精度不如B3LYP-D3(BJ)/def2-SVP的理想，但对于算RESP电荷的目的问题不大。单点任务部分算不动的话，可以把def2-TZVP降到6-311G**，如果是阴离子建议改为6-311+G**。

注意Gaussian09 D.01版本之前不支持DFT-D3校正，因此用老版本者应当把脚本里em=GD3BJ关键词取消，相关信息看《DFT-D色散校正的使用》（<http://sobereva.com/210>）。

## 2 使用脚本

将Multiwfn目录下的examples\RESP\目录下的RESP.sh拷到当前目录，使用chmod +x ./RESP.sh给它增加可执行权限。把含有分子结构信息的文件也拷到当前目录，格式必须是Multiwfn认识的（可以是xyz/mol/mol2/pdb/fch/wfn/molden/gjf等等）。然后运行下面的命令：

./RESP.sh [文件名] [净电荷] [自旋多重度] [溶剂名]

比如./RESP.sh H2O.xyz 0 1 ethanol命令将在IEFPCM隐式溶剂模型表现的乙醇环境中计算中性单重态水分子的RESP电荷。如果净电荷和自旋多重度不写，则分别默认为0和1。如果溶剂名不写，默认为water，如果写gas，则在真空下计算。支持的溶剂名见<http://sobereva.com/g09/k_scrf.htm>的末尾。

计算完毕后，当前目录下就有了和输入文件同名的.chg文件。这是个文本文件，前四列是元素名和优化后的坐标，最后一列就是RESP电荷。以下是运算过程的输出例子：

[root@192 other2]# ./RESP.sh H2O.xyz  
Net charge was not defined. Default to 0  
Spin multiplicity was not defined. Default to 1  
Running optimization task via Gaussian...  
Done!  
Running single point task via Gaussian...  
Done!  
Running formchk...  
Running Multiwfn...  
Finished! The optimized atomic coordinates with RESP charges (the last column) have been exported to H2O.chg in current folder

如果调用Gaussian运行失败，脚本就会自动停止，届时大家请仔细检查当前目录下的gau.out文件判断出错原因。

计算的时候用的CPU核数取决于Default.Route文件里的-P-设置，这点在《Gaussian的安装方法及运行时的相关问题》（<http://sobereva.com/439>）里说了。

本文的做法只是以最一般的方式计算RESP电荷，如果需要更灵活的拟合方式，比如设置电荷等价性、设置某个片段总电荷为特定值等等，需要在Multiwfn的RESP模块的界面里进行设置，在《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）文中有充分、详细的介绍。

如果你的输入的结构文件里的结构就已经足够好，不想让脚本自动再做优化浪费时间，可以用examples\RESP\目录下的RESP_noopt.sh代替前述的RESP.sh，二者用法完全一样，只不过前者不做优化步骤。

如果你的体系里含有18号及以后的元素，由于Gaussian没有内置拟合静电势用的原子半径，因此无法通过以上脚本自动得到RESP电荷，而必须手动做Gaussian计算得到fch文件后自行利用Multiwfn按照<http://sobereva.com/441>说的操作来计算RESP电荷（届时也会提示缺半径，但按照屏幕上的提示，用Multiwfn自动推荐的半径即可）。

如果以本文的方式计算了RESP电荷，请别忘了引用Multiwfn原文。引用方式在《Multiwfn FAQ》（<http://sobereva.com/452>）里写明了。
