---
post_id: 286
title: 使用sobMECP程序结合Gaussian程序搜索极小能量交叉点
url: http://sobereva.com/286
date: '2015-06-08T00:18:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 其它软件
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 核心是结合Gaussian使用sobMECP程序搜索MECP。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**使用sobMECP程序结合Gaussian程序搜索极小能量交叉点**  
Using sobMECP program combined with Gaussian program to search for minimum energy crossing points

文/Sobereva @[北京科音](http://www.keinsci.com)

First release: 2015-Mar-18    Last update: 2025-Oct-5

本文主要介绍怎么用sob修改版的Harvey的MECP程序（称sobMECP）结合Gaussian搜索两种不同自旋多重度的态之间的极小能量交叉点(MECP)。第一节先简单介绍一下基本理论和算法方面的知识，第二节介绍一下sobMECP程序的特点和使用流程，第三节给出一些具体实例。

注：本文的内容很简略。如果大家对于MECP和极小能量圆锥交叉（MECI）的理论知识、应用、实际计算方法感兴趣，想真正完整、深入、系统学习，十分推荐学习笔者讲授的**北京科音高级量子化学培训班（**[**http://www.keinsci.com/KAQC**](http://www.keinsci.com/KAQC)**）**，里面专门有一节“势能面交叉与光化学”，用超过130页幻灯片极其全面讲了这些知识，并给出了巨量的搜索MECP和MECI的例子，能一次性快速从这方面研究的初学者成为内行！

## 1 原理

### 1.1 MECP的相关理论知识

我们先看看什么情况下两个态的势能面才会交叉。设两个态波函数分别为|1>和|2>，体系哈密顿算符为H，则这样的两态模型构成2*2哈密顿矩阵，其四个矩阵元包括两个对角元H11=<1|H|1>、H22=<2|H|2>，以及两个等价的耦合矩阵元H12=<1|H|2>=H21=<2|H|1>。让这两个态的能量E1、E2相同需要同时满足两个条件：(1) H11=H22 (2) H12=0。

这些哈密顿矩阵元的数值都是体系几何结构的函数。对于两个自旋多重度不同的态，在不考虑旋轨耦合情况下，由于波函数自旋部分不同，导致耦合矩阵元H12总为0，因此只需要满足H11=H22就够了。对于非线性分子，坐标是3N-6维的，我们可以对坐标进行某种变换，使得H11-H22只依赖于某一维坐标，只要这个坐标恰为某个值时就能满足H11=H22，而不管其它3N-7个坐标的数值是如何的。这也就是说，不考虑旋轨耦合下两个自旋多重度不同的态的交叉并不是一个特定的点（对应某个具体的结构），而是在3N-7维的超曲面中交叉的。换句话说，能让两个态能量相同的结构有无限个，自然不可能都考察，我们研究的只是其中最有意义的一个点，这一般就是极小能量交叉点(MECP, Minimum energy crossing point)，它是指两个态能量相同的3N-7维超曲面中能量最低的那个结构。但也不一定MECP就只有一个，正如同几何优化时往往可以得到多个能量极小点，两个态之间也可以有多个MECP，能找到哪个取决于MECP搜索时的初猜结构是否离它比较近。

一般搜索MECP的时候是不考虑旋轨耦合的。如果在此之后在计算能量时将旋轨耦合算符引入哈密顿，由于此时两个态之间耦合矩阵元H12=H21不再为0，两个态就会发生混合，产生A、B两个新的态，波函数表示为c1*|1>+c2*|2>形式，且能量相应地出现小幅分裂（即E_A≠E_B）。这种情形类似于自旋多重度相同的两个态之间的避免交叉极小点（Avoided crossing minimum），因为都是H12=H21≠0.

系间窜越(Intersystem crossing)是重要的光化学过程，是指电子激发后，由于不同自旋多重度的态的势能面之间存在交叉，导致体系经历这样的结构时以非辐射方式改变自旋多重度。因此，寻找MECP的结构对光化学研究十分重要。

### 1.2 MECP结构的搜索方法

搜索MECP结构涉及两个问题：（1）理论方法与基组（2）优化算法。

搜索MECP可以用的理论方法有两类，一类是做态平均CASSCF计算（或MS-CASPT2、MRCI等进一步考虑动态相关的），同时计算多个根，并搜索指定的两个自旋多重度不同的根之间的MECP。另一类是用普通的理论方法，如DFT、MP2、CCSD，分别对两个不同自旋多重度的态做单点计算，并由此搜索这两个态的MECP。一般来说基于DFT搜索MECP是首选，便宜、方便，结果也不错，可以用在颇大的体系。泛函、基组的选择和常规DFT计算并无区别。如果对结果要得很精确，可以再考虑CCSD或CASSCF。  
（PS：这里说的都是搜索自旋多重度不同的态之间的MECP。搜索自旋多重度相同的态之间的MECP或避免交叉极小点只能用CASSCF，但如果能量分裂较大用TDDFT等单参考态方法也凑合，这些与本文无关就不多说了。）

Robb提出的搜索MECP的算法其实很简单，和普通几何优化算法思路颇为类似，这也是最常用的MECP搜索方法。定义两个有效梯度，f和g。f是(E1-E2)^2对核坐标求导，具体写为E1-E2乘以两个态的梯度矢量之差。沿着f移动坐标会令两个态能量差减小。g是E1对核坐标求导，并且投影掉了它在f方向上的分量以使f和g正交。沿着g移动会令第一个态的能量降低。若将f和g考虑到一起，按照f+g作为体系有效受力进行优化，那么在优化过程中就会一边降低两个态的能量差一边降低体系总能量，显然最后得到的就是MECP结构。优化过程用的具体数值算法和一般几何优化一样是基于牛顿法或赝牛顿法，只不过Hessian矩阵也相应地和普通几何优化不同，详细公式见Theor. Chem. Acc., 99, 95(1998)。

MECP搜索一般同时使用位移、受力、两个态能量差作为收敛判断标准，三者都非常小的时候才算收敛。但如果把能量差必须接近0这条收敛标准去掉，那么上面介绍的MECP搜索算法也可以直接用于搜索避免交叉极小点。

搜索MECP用的初猜就取平衡结构或过渡态结构就行，离预期的MECP结构越近越好，但并不需要很精确。上述MECP搜索算法还是比较稳健的。如果搜索不成功可以再考虑调整初猜结构。

## 2 MECP程序的使用

Harvey的MECP程序基于Gaussian，只能用于Linux平台，搜索可以在HF、DFT、MP2等级别下进行，运行过程中会生成Gaussian输入文件、调用Gaussian进行计算，并且读取受力，对结构按照搜索算法进行位移。优化算法基于L-BFGS赝牛顿法。MECP原版可以在这里下载：<http://pan.baidu.com/s/1o682NB8>。使用时应引用Harvey对苯基阳离子搜索MECP的文章Theor. Chem. Acc., 99, 95(1998)。值得一提的是MECP搜索算法并非是Harvey提出来的，MECP程序里用的，也即上一节介绍的算法是Robb提出的标准的MECP搜索方法。之所以Harvey的MECP程序知名度较高，是因为它支持的是最常用的Gaussian，而与此同时Gaussian自身仅支持用CASSCF搜索MECP（众所周知Gaussian的CASSCF不给力，而且CASSCF本身又相对复杂、耗时），这才导致了MECP程序在文献中用得很多。

笔者发现这MECP程序用起来颇不方便，每处理一个新体系要改好多地方，用法上也有不少别扭的地方。笔者遂对此程序进行了很多修改，使之变得方便好用得多，修改版称为sobMECP，下载地址：<http://sobereva.com/soft/sobMECP.zip>。下文讨论全都是对于sobMECP而言的。如果你使用了sobMECP发表了文章，**请在文中以这种格式引用：Tian Lu, sobMECP program,** [**http://sobereva.com/286**](http://sobereva.com/286) **(accessed month day, year)**

### 2.1 sobMECP程序的基本使用流程

将sobMECP解压到任意一处，进入其中，然后按下列步骤使用之。

1 设定好Input_Header_A和Input_Header_B文件，内容分别是两个态的分子坐标之前的部分。%chk必须得写，chk文件具体怎么命名无所谓。force和guess(read)这两个关键词是必须写的，其它关键词，包括方法和基组、辅助SCF收敛的选项等，根据实际情况去写。必须用#n。

如果需要用gen或genECP从分子坐标末尾读取基组/赝势定义，则需要在Input_Tail文件中以常规方式写明基组/赝势定义，比如  
C H 0  
cc-pVTZ  
****  
Cu 0  
 SDD  
****  
[空行]  
Cu 0  
 SDD  
[空行]  
[空行]  
如果不需要自定义基组/赝势，则Input_Tail文件留空即可。

2 在geom里填好体系初始结构，注意末尾空一行，原子名必须用元素的序号代替。例如：  
   6   -0.17110831    0.45776462    0.00000000  
   8   -0.01984499   -0.74914326    0.00000000  
   1   -1.10138660    1.00356716    0.00000000  
   1    0.76276200    0.95429984    0.54191098  
   1    0.76276200    0.95429984   -0.54191098  
[空行]

3 运行./prepare.sh。这将会在当前目录下编译产生MECP.x可执行文件、运行进度文件ProgFile、主脚本runMECP.sh，并且清空当前目录下的零碎文件和JOBS目录。

4 运行./runfirst.sh，这将会在初始结构下对两个态进行计算，产生Job0_A.gjf、Job0_B.gjf、Job0_A.log、Job0_B.log以及相应的chk文件。

5 运行./runMECP.sh，即开始搜索MECP，直到全部标准收敛为止，收敛信息会不断输出到屏幕上以便监控。随着搜索的进行，geom文件会不断更新为当前结构，ab_initio文件内容会不断更新为当前两个态的能量和梯度，ProgFile里记录的进度信息也会不断更新。

运行过程中产生的各种细节信息都会输出到当前目录下ReportFile文件中。包括每一步的结构、两个态的能量、收敛情况、有效梯度（即前文提到的f+g，但这里f额外乘了个刻度因子）、差值梯度（两个态受力之差）、平行梯度（前文的g）。

运行过程中产生的每一步的Gaussian输入输出文件都在JOBS目录下。

MECP搜索过程中产生的每一步的结构都会记录到traj.xyz下作为轨迹文件，可以用VMD程序打开来方便地观看搜索过程中的结构变化，第一帧对应于初始结构。

如果运行中途中断，应重新依次执行prepare.sh、runfirst.sh、runMECP.sh，这会基于geom文件中储存的最后一步结构重新进行搜索。

### 2.2 sobMECP程序的相关细节

默认情况prepare.sh是调用gfortran编译器来编译MECP程序。如果机子里没有gfortran，可以改用ifort编译，做法是在prepare.sh里在gfortran前头写上#将之注释掉，而把ifort那行开头的#去掉。

如果要调整收敛判断阈值，应修改temp/MECP.f的第300行。总共有5个标准。TDE是能量变化，TDXMax和TDXRMS是位移最大值和方均根，TGMax和TGRMS是受力最大值和方均根。默认情况下，受力和位移判断标准比Gaussian几何优化默认判断标准松将近一倍。

如果要调整搜索步数上限，应修改temp/runMECP.sh第30行的数字。默认是100步。

有sobMECP用户反映把优化过程的置信半径减小五倍，往往令收敛更容易、降低震荡倾向。我未充分考证这一点，读者可以试试。做法是在MECP.f里搜索STPMX = 0.1d0，将数值改小。

进行如上修改后需再次运行./prepare.sh方可生效。

extract_energy是Linux下awk工具的脚本文件，用于从Gaussian输出文件中提取能量。提取不同理论方法输出的能量需要用不同的脚本。temp目录下自带了四种：  
extract_energy_SCF：提取HF/DFT/半经验的  
extract_energy_MP2：提取MP2的  
extract_energy_CIS：提取CIS的  
extract_energy_TD：提取TDHF/TDDFT的（对于G09用户，此文件里的TD-DFT必须手动改为TD-KS）  
当前计算在哪个级别下进行，就把上述哪个文件拷到上一级目录下改名为extract_energy。程序包里直接带的extract_energy对应的是extract_energy_SCF。  
如果第一个态和第二个态用的理论方法不同，比如第1个态用TDDFT计算S1，第二个态用UKS计算T1，那么应同时准备extract_energy和extract_energy2，前者会被用于提取第一个态的能量，后者会被 用于提取第二个态的能量。

如果用的Gaussian不是16版，需把sub_script和runfirst.sh中的g16替换为相应命令。笔者只测试了Gaussian 09和16，都可以完全正常运行。

## 3 MECP搜索实例

下面给出一些sobMECP程序使用例子，涉及到的文件都在sobMECP的test文件夹里。注意这些文件是我以前用sobMECP调用Gaussian 09算的，16和09的结果会多多少少有些差别。

### 3.1 CH2（卡宾）

这一节寻找CH2的单-三重态间的MECP。

在sobMECP文件夹中编辑Input_Header_A文件成为如下内容，对应单重态计算  
%mem=6GB  
%nproc=4  
%chk=singlet.chk  
#n B3LYP/6-311G** force guess(read)

First State

0 1

然后，类似地将Input_Header_B文件写为下面这样，对应三重态计算  
%mem=6GB  
%nproc=4  
%chk=triplet.chk  
#n B3LYP/6-311G** force guess(read)

Second State

0 3

注意上面两个文件末尾无空行，后同。

然后编辑geom文件，将下面的初始结构写进去  
 6                  0.00000000    0.00000000    0.13397933  
 1                  0.00000000   -0.92611695   -0.40193800  
 1                 -0.00000000    0.92611695   -0.40193800  
[空行]

然后用chmod +x *将sobMECP下的文件都加上可执行权限。确保Gaussian 16可以在命令行下用g16直接正常调用。之后依次运行  
./prepare.sh  
./runfirst.sh  
./runMECP.sh

收敛情况随着计算不断在屏幕上输出，仅用了5步就收敛了，屏幕上显示5个YES。此时geom文件中的结构就是MECP结构了。从ab_initio文件中可见，两个态的能量分别是-39.1443410840和-39.1443771072 a.u.，确实基本一致。搜索过程的详细信息在ReportFile里可看到。

将traj.xyz拖到VMD程序的主窗口里可以看到搜索过程结构的变化，可见一开始H-C-H角度是119.9度，而在最后一帧，即MECP结构下，角度减小为100.1度。

### 3.2 FeO+

这一节寻找FeO+阳离子的四-六重态间的MECP。对O用6-311G*，对Fe用SDD赝势。对应四重态的Input_Header_A文件应当为  
%chk=A.chk  
#n B3LYP/genecp force guess(read)

First State

1 4

对应六重态的Input_Header_B文件应为  
%chk=B.chk  
#n B3LYP/genecp force guess(read)

Second State

1 6

还要写一个Input_Tail文件，用来设定要从分子坐标后面读取的内容，这里就是自定义基组和赝势信息：  
O 0  
6-311G*  
****  
Fe 0  
 SDD  
****  
[空行]  
Fe 0  
 SDD  
[空行]

然后在geom里写入初始坐标  
26 0.000000 0.000000 0.000000  
8 0.000000 0.000000 0.670000  
[空行]

然后也是依次运行prepare.sh、runfirst.sh、runMECP.sh。

初始结构中Fe-O长度为0.67埃，从输出结果可见，最后Fe-O长度变为了1.322埃。对于这样只有一个几何变量的体系，显然也可以自行对两个态做势能面扫描，然后拟合成曲线来确定交叉点。

注：在2.0埃附近实际上还有个交叉点，但是在附近区域，当前理论方法下两个态的势能曲线几乎完全平行，此时MECP搜索算法完全失效，因此没法让初猜Fe-O长度在2.0附近来寻找这个点。这个交叉点只能通过自行考察势能曲线获得。

### 3.3 C6H5+

苯基阳离子C6H5+正是使用MECP需要引的Theor. Chem. Acc., 99, 95(1998)这篇文章中研究的体系，文中使用不同方法考察了它的单-三重态MECP结构。类似前面的例子，也是先写Input_Header_A、Input_Header_B、geom文件，然后依次运行prepare.sh、runfirst.sh、runMECP.sh。涉及的文件在sobMECP/test/C6H5+中可找到，这里就不累述了。

这里用的初始结构就是把苯去掉一个氢而已，在B3LYP/6-31G**下经过十几步就找到了想要的MECP。体系依然是C2v构型，但是环发生了一定变形。

sobMECP的test目录下还有两个单-三重态MECP搜索例子，其中H3CO+就是原版MECP程序中自带的一个例子，Pt_coord是个含铂配合物，算是个较大体系的例子。

### 3.4 激发态单重态与三重态的交叉

前面考察的单-三重态的MECP，单重态都是直接用DFT算的基态。但是激发态单重态与三重态的交叉也很重要。比如S1-T1的交叉对于TADF（热活化延时荧光）的研究是关键，和反系间窜越效率问题密切相关。  
  
test目录下有几个这样的例子，C6H5+_A2-3B1、C6H5+_B1-3A2、Pyrrole_A2-3B2，横杠前是单重态的电子态，横杠后是三重态电子态。这些任务计算第一单重态激发态用的是TDDFT，算三重态用的和之前一样是UKS。计算的时候要把相应目录下extract_energy和extract_energy2都拷到sobMECP目录下，前者提取第一个态的能量（TDDFT给出的），后者提取第二个态的能量（DFT算的）。注意像这些高对称结构，不同初始结构下T1电子态的不可约表示经常不同。找S1与三重态的MECP时由于不断读取上一步的初猜，所以跟踪的是初始结构下的T1态（这个态到了MECP结构下，未必是能量最低的三重态了）。而TDDFT计算时，S1的电子态的不可约表示则可能发生改变。  
  
虽然原理上也可以用TDDFT算三重态能量，但之所以这里用UKS来算，一方面是更省时间，另一方面是结果往往更合理。

## 4 关于MECP处的自由能

有人问怎么计算MECP的自由能。一般没必要算它的自由能，绝大部分涉及到MECP的文章中也只讨论电子能量。但如果非要说怎么算的话，应当是在MECP处计算两个自旋态的能量简并的3N-7维空间里的3N-7个振动模式的频率，这是有意义的，因为在这3N-7维空间中MECP相当于极小点。有了振动频率，就可以用常规方式计算热力学量了，比如可以把振动频率等信息提供给Shermo来计算，见《使用Shermo结合量子化学程序方便地计算分子的各种热力学数据》（<http://sobereva.com/552>）。然而，这3N-7个频率据我所知没有简单现成的工具可以计算。

网上有文章称在MECP处用Gaussian里的freq=projected关键词可以得到MECP的自由能（此关键词本来目的是对IRC上的点计算垂直于IRC方向的频率），这明显不具备普适性。例如用上面的C6H5+的例子，在MECP处对单重态和三重态分别做freq=projected时，自由能分别为-231.188990和-231.186629 Hartree，可见存在显著差异，即结果依赖于自旋多重度的选取，结果不唯一。因此对于非特殊情况，靠freq=projected关键词是没法得到MECP的自由能的。其问题在于，从MECP位置可以对两个自旋态用IRC关键词跑downhill路径，见《谈谈Gaussian产生downhill路径的功能》（<http://sobereva.com/571>），对于MECP来说freq=projected算的是垂直于downhill路径的3N-7维空间的振动频率。而MECP处两个自旋态的downhill路径不仅方向往往不同，而且也往往都不垂直于唯一决定H11-H22的方向，即垂直于downhill路径的子空间不等同于两个态能量简并的3N-7维空间，因此靠freq=projected一般是没法正确计算MECP的自由能的。
