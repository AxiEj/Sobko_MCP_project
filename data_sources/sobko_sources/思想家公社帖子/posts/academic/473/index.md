---
post_id: 473
title: 分子动力学初始结构构建程序Packmol的使用
url: http://sobereva.com/473
date: '2019-03-23T04:39:00+08:00'
source_categories:
- 分子模拟
primary_topic: 其它软件
secondary_topics:
- 分子动力学
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题是 Packmol 的使用教程，Packmol 不在给定软件列表中。
topic_family: 软件
exclude_reason: ''
confidence: 0.95
image_count: 6
local_assets_dir: assets
---

**分子动力学初始结构构建程序Packmol的使用**

Use of Packmol to construct initial structure of molecular dynamics

文/Sobereva@[北京科音](http://www.keinsci.com) 

First release: 2019-Mar-23   Last update: 2026-Feb-9

由于经常有人问Packmol怎么安装、怎么用，这里就写一篇文章，做一个完整的介绍，初学者应该都能读懂，之前用过的人看了可能还能了解一些之前没注意到的细节和技巧。笔者在北京科音的分子动力学与GROMACS培训班（<http://www.keinsci.com/workshop/KGMX_content.html>）里会对Packmol讲得更具体、给更多例子。

## 1 Packmol简介

Packmol是一个免费的、很有价值的构建分子动力学模拟初始结构的工具，非常流行。简单来说就是由用户提供一种或多种分子的结构文件，并且设定一些约束条件，Packmol就会把各种分子按照设定将指定数目的分子堆积到满足要求的区域中。程序会通过优化算法不断尝试各种堆积方式，直到构建出原子间没有不合理接触而且能满足所有约束条件的结构。在堆积过程中分子结构会保持刚性，即构象不会变化。Packmol在堆积过程只考虑空间因素，完全不考虑能量、电荷分布等额外问题。

Packmol的选项设定非常灵活，可以容易地构建出复杂的模型。Packmol产生的结构可以被用于各种主流的分子动力学程序的模拟中，比如GROMACS、AMBER等。M$程序里的Amorphous Cell的用处和Packmol颇有类似之处，但远远不及Packmol灵活、强大。

Packmol的网址是<https://m3g.github.io/packmol/>，在上面有关键词介绍，可以下载到源代码和预编译的Windows版，还提供了一些例子。

## 2 Packmol的安装与运行

### 2.1 在Linux下编译和使用Packmol

在Linux下使用Packmol之前需要先对源代码进行编译，如下所示。如果你不方便自己编译，也可以直接下载我已经编译好的：<http://sobereva.com/soft/packmol_18.169_Linux.zip>

Packmol是Fortran写的，如果你的机子里还没有Fortran编译器，需要先安装Fortran编译器。比如在CentOS下使用yum install gfortran命令即可安装gfortran编译器。

将官网上下载到的packmol.tar.gz解压，进入解压后的目录，在命令行模式下输入make即可编译，十秒钟左右就能编译完。编译完成后当前目录就出现了名为packmol的可执行文件。

修改用户目录下的.bashrc文件（比如输入gedit ~/.bashrc命令），在末尾加上一行export PATH=$PATH:/sob/packmol-18.169，这里假定/sob/packmol-18.169是packmol可执行文件的所在目录。保存文件后重新进入终端，输入packmol命令检查是否能正常启动，如果能冒出一堆和packmol有关的信息来，就说明已经装好了。

之后用比如packmol < test.inp命令，就代表以test.inp作为输入文件运行packmol程序。输出文件都会产生在当前目录下。

### 2.2 在Windows下使用Packmol

Packmol源代码也可以在Windows下编译，但我们没必要这么做，因为在Packmol主页上已经提供了编译好的可执行文件，仅适用于64bit Windows系统。你也可以直接在这里下载：<http://sobereva.com/soft/packmol_18.169_win64.rar>。

解压此文件包，然后进入Windows的命令行模式下（cmd环境。不会进入的话自行google，属于Windows使用常识。绝对不要用恶心的powershell环境），输入packmol < test.inp命令即可运行。如果packmol不在当前目录下，则需要输入其绝对路径，或者加入到Windows的Path环境变量里（不会的话参考《GROMACS 2018.4原生Windows版的安装演示》<https://www.bilibili.com/video/av39914815/>视频中的对应部分）。

PS：别问为什么双击packmol.exe图标运行不了，因为packmol根本就不是这么用的！

### 3 Packmol输入文件的设置

Packmol的使用需要提供两类文件  
• 输入文件。文件名随意，用来定义各种类型分子如何分布、有多少个。  
• 各种要加入的分子的结构文件。一般使用pdb格式，用什么程序产生都可以。

输入文件里的关键词在<http://m3g.iqm.unicamp.br/packmol/userguide.shtml#basic>有汇总。下面只提及常用的关键词，方括号里的是参数。

### 3.1 全局设定

tolerance [数值]：要求原子间距离不能小于多少，一般设为2.0。Packmol里所有长度的单位都是埃

output [文件名]：输出文件的路径

filetype [类型]：输出文件的格式。默认为pdb，也可以设比如xyz

seed -1：写这个的话每次运行产生的结构都会不同

add_box_sides：给输出的pdb中增加CRYST1字段定义盒子，盒子尺寸对应体系中原子最大、最小坐标。如果写诸如add_box_sides 1.2，则会给盒子各方向再增加1.2埃，避免做模拟时有某些边界的原子和镜像盒子里的原子间存在不合理接触

### 3.2 分子设定

每个下面这种字段设置一种分子如何出现在当前体系中。可以写无数个这种字段。

structure [分子结构文件]  
number [分子数]  
[分子规则]  
end structure

分子规则用来定义分子里的所有原子必须满足的条件，其常用关键词如下。

inside cube [xmin ymin zmin d]：要求分子出现在长度为d的立方盒子内，盒子x,y,z最小值为xmin ymin zmin

inside box [xmin ymin zmin xmax ymax zmax]：要求分子出现在矩形盒子内，盒子两个顶角坐标分别为xmin ymin zmin和xmax ymax zmax

inside sphere [x y z r]：要求分子出现在中心为(x,y,z)半径为r的圆球中。另外，用inside ellipsoid关键词的话还可以要求出现在特定的椭球中

inside cylinder [a1 b1 c1 a2 b2 c2 r l]：要求分子出现在圆柱内。圆柱的定义是从(a1,b1,c1)往(a2,b2,c2)方向伸展l长度，半径为r

以上inside都可以改为outside，要求不能出现在指定范围内。上面的空间范围要求可以同时使用多个，条件会同时满足。还有一些设置：

over plane [a b c d]：要求分子出现位置满足平面方程ax+by+cz-d>=0。比如over plane 1 0 0 10.5就相当于要求出现在x>=10.5埃的区域。over可以改成below来反转条件。

constrain_rotation [x/y/z 平均值 最大偏差]：默认情况下分子可以绕x,y,z轴随意旋转任意角度。用这个选项可以设置分子绕x或y或z旋转的情况，可以同时设多个。如constrain_rotation x 20 5代表允许绕着y和z轴随意旋转，而绕着x轴旋转的范围必须在15~25度之间，平均值为20度。

fixed [x y z a b c]：用来直接定义分子出现在哪里。此设置代表将分子结构文件里的坐标平移(x,y,z)，并绕x,y,z轴分布旋转a,b,c弧度。如果还同时写了center关键词，相当于把分子的中心摆到(x,y,z)位置再旋转

### 3.3 原子设定

Packmol里还可以要求某种分子的某些特定序号的原子出现的范围必须满足的要求，格式为

structure [分子结构文件]  
[分子规则]  
atoms [第一批原子序号]  
[原子规则]  
end atoms  
atoms [第二批原子序号]  
[原子规则]  
end atoms  
...  
end structure

原子规则的设置语法、关键词和分子规则完全一样。

## 4 几个实例

下面举几个Packmol使用例子。所有输入输出文件都可以在此下载：<http://sobereva.com/attach/473/file.rar>

### 4.1 构建5*5*5 nm^3甲醇盒子

首先在GaussView或其它可以对分子建模的程序里画一个甲醇，然后保存为methanol.pdb。对于这种刚性小分子，用Packmol之前结构不需要非得优化，毕竟GaussView直接画的甲醇的基本几何参数是合理的，而且不管对其做不做优化，等动力学跑起来之后就都一样了。

创建一个名为methanol_box.inp的文本文件，内容如下

tolerance 2.0  
add_box_sides 1.2  
output methanol_box.pdb  
structure methanol.pdb  
  number 1000  
  inside cube 0. 0. 0. 50.  
end structure

将methanol.pdb和methanol_box.inp都放到当前目录，运行packmol < methanol_box.inp，经过几秒钟，当前目录下就出现了methanol_box.pdb。将之拖到VMD（<http://www.ks.uiuc.edu/Research/vmd/>）程序里观看，并且在VMD的命令行窗口里输入pbc box显示出盒子，看到的图像如下

![1](assets/001.png)

可见构建得很成功。但是1000个甲醇肯定不是Packmol能填充进这个5*5*5 nm^3盒子的上限，因为Packmol很容易就产生成功了，而且从图上看还有一些空隙。如果大家希望得到更致密的盒子，可以尝试一点点增加甲醇的number数，看看设到多少的时候Packmol半天也没法成功产生结构或者提示产生失败，Packmol最多能插入多少甲醇你心里就有数了。

### 4.2 构建水+甲醇混合溶液的气液界面体系

此例我们想构建一个水+甲醇摩尔比1:1溶液的气液界面体系，界面平行于XY方向，盒子的X、Y长度都为4nm，溶液层厚度是5nm，溶液上下两侧都是真空区，每一侧真空区厚度都是3nm。

首先，我们靠Packmol创建一个水+甲醇的4*4*5 nm^3的溶液盒子。甲醇的pdb文件已经有了，我们再用GaussView画个水，保存为water.pdb。然后编辑一个文件mix.inp，内容如下（经测试，水和甲醇各插入1000个时盒子已经比较致密了，而且已经需要好多轮循环才能成功产生结构，所以笔者就不再尝试插入更多了）

tolerance 2.0  
add_box_sides 1.2  
output mix.pdb  
structure water.pdb   
  number 1000   
  inside box 0. 0. 0. 40. 40. 50.  
end structure  
structure methanol.pdb  
  number 1000  
  inside box 0. 0. 0. 40. 40. 50.  
end structure

将得到的mix.pdb弄到VMD里显示：

![2](assets/002.png)

但是目前还没有真空区。由于溶液层厚度为5nm，每一侧真空区厚度为3nm，因此盒子Z方向总长度应为5+3+3=11nm。因此我们在VMD里输入pbc set {40 40 110}来设置盒子尺寸为4*4*11 nm^3，这里单位是埃。

目前溶剂区域在盒子最底部，我们要将之挪到盒子中间去，也即把所有原子往Z的正方向挪3nm。这可以用VMD的几何变换命令轻易实现。在VMD里输入[atomselect top all] moveby {0 0 30}，然后将VMD改成正交视角便于观看（Display - Orthographic），看到下图。

![3](assets/003.png)

然后在VMD里将当前体系保存成新的pdb文件即可。值得一提的是，动力学模拟开始后，肯定最后达到稳定状态时溶液层厚度不可能正好是我们最初期望的5nm，但由于目前已经堆积得比较致密了，应该偏离不太大。如果发现偏离的程度超过自己能接受的程度，可以在建模时再适当增加点分子数、在packmol建模时让盒子在Z方向稍微大一点。

### 4.3 氯仿+甲醇+富勒烯体系

这是一个稍微复杂的例子，没有什么实际意义，主要是体现Packmol的灵活性。此例我们要构建一个半径1.5nm的溶剂球，甲醇和氯仿各一个半球区域，并且富勒烯正好出现在球中央。

此例的输入文件如下。chloroform.pdb和C60.pdb都是GaussView直接构建的，后者在GaussView的片段库里直接就有。

tolerance 2.0  
output mix.pdb  
structure chloroform.pdb   
  number 200   
  inside box 0. 0. 0. 40. 40. 20.  
  inside sphere 20. 20. 20. 15.  
end structure  
structure methanol.pdb  
  number 200  
  inside box 0. 0. 20. 40. 40. 40.  
  inside sphere 20. 20. 20. 15.  
end structure  
structure C60.pdb  
number 1  
center  
fixed 20. 20. 20. 0. 0. 0.  
end structure

此例我们假定球的中心在(2,2,2) nm的位置，因此直接用center和fixed关键词将C60的中心定位在这个地方。对于氯仿和甲醇，inside sphere要求它们只能出现于距离(2,2,2)半径1.5 nm的区域内，由于二者的inside box设定范围正好相接，因此这两种分子会分布出现在Z=2nm平面的上、下两侧。由于当前模拟的是孤立体系，所以没有用add_box_sides关键词来产生盒子信息。

用VMD观看得到的pdb文件，如下所示

![4](assets/004.png)

### 4.4 构建水球+十二烷基磺酸钠

这个例子主要用来体现怎么使用原子设定。十二烷基磺酸钠(SDS')的头部基团是亲水的，烷烃尾巴是疏水的。此例我们要构建一个半径为20埃的水球，让100个SDS'绕着它分布，SDS'的头部基团都埋在水球里，而且让烷烃尾巴的方向基本上垂直于水球的界面，最终构建出的结构应该类似于海胆，SDS'就是海胆的刺。

我们先用GaussView画一个SDS'。由于钠离子的位置放在哪可能凭直觉不好确定，因此画完之后可以做一下几何优化，比如用Gaussian在PM7半经验方法下粗略优化后得到如下结构，看起来很合理

![5](assets/005.png)

创建packmol输入文件，内容如下

tolerance 2.0  
output mix.pdb  
structure water.pdb   
  number 1200   
  inside sphere 0. 0. 0. 20.  
end structure

structure SDS.pdb  
number 100  
atoms 42  
  inside sphere 0. 0. 0. 15.  
end atoms  
atoms 1  
  outside sphere 0. 0. 0. 30.  
end atoms  
end structure

创建水球那部分没什么好说的，经测试差不多最多就能放1200个水，再多就很难产生成功了。安置SDS'的这一段值得提一下。我们让42号原子，即钠离子必须出现在距离水球中心15埃范围以内，而让1号原子，即烃链最末端的碳原子必须距离水球中心30埃以上。由于在SDS'中这俩原子距离为18埃，仅略大于30-15=15埃，因此这么定义可以起到让SDS'链垂直于水球界面的效果。

在VMD里绘制产生后的pdb，如下所示，结构完全达到了我们的期望。

![6](assets/006.png)

官网上<http://m3g.iqm.unicamp.br/packmol/examples.shtml>里也有一些例子，有兴趣可以看看。

## 5 相关问题&注意事项

这里说一些使用Packmol建模应当注意的问题，并且结合最主流的分子动力学程序GROMACS说一些相关事项。

Packmol的执行过程实际上是个循环过程，如果你当前的空间范围设定比较简单，Packmol很快就会顺利产生最终结构。空间约束设定得越多、越复杂，往往成功产生结构需要的循环次数越多，总耗时越高。如果你把空间范围约束得过度复杂甚至相互矛盾，或者要加入的分子数较多但允许分子出现的空间范围相对而言过度狭小，那么Packmol会反复循环，一直也收敛不了，或者最终宣告产生失败。碰到这种情况，应当将约束条件适当放宽、简化，或者设的分子数少一点再试。

一般情况下，用Packmol构建的体系肯定是比较松散的，或者说其密度肯定显著低于真实密度，因为此时还没有考虑分子间相互作用、构象的变化从而使得分子间能够接触得更紧密。但这没关系，在NPT下跑一下MD就好了，盒子尺寸会自发进行调节。而直接用Packmol产生的结构做NVT模拟一般是无意义的，因为跑起来之后分子会自发紧密聚集，其它地方就成了真空区了，和实际不符。

虽然也可以用Packmol构建蛋白质、核酸浸在溶剂环境中的体系，但是这样做明显不如用动力学程序自带的专用做这种事情的程序好，因为Packmol产生的水的密度偏低，水的分布特征和实际体相水相差较大，可能NPT模拟起来之后盒子变形、收缩得厉害，出现溶质与其镜像最近距离太近之类问题。而如果用比如GROMACS里的gmx solvate命令给蛋白质/核酸加溶剂，由于是直接用事先已经做NPT平衡好的溶剂盒子（比如加水一般用自带的spc216.gro）通过平移复制来填充真空区，加的溶剂的分布状态明显理想得多得多。

GROMACS有一个命令叫gmx insert-molecules，可以由用户提供分子结构文件、指定插入盒子的分子数，然后试图将这些分子都插入盒子（但如果设的数目太多，会能插入多少就插入多少）。此命令远没有Packmol那么灵活，它能做的事用Packmol都可以实现，而且Packmol会通过优化算法试图让分子尽可能好地堆叠，因此对于同样的盒子范围，靠Packmol最多能插入的分子数比用gmx insert-molecules明显要多，故能得到更紧凑的结构。

Packmol原理上也可以产生磷脂双分子膜，乃至膜蛋白这样的体系的，但是这需要设置很多约束条件才能产生靠谱的结果，而且耗时很高，结果也不理想。比如磷脂之间或者磷脂与蛋白之间会有好多空隙，这会导致模拟刚开始就有水大量跑进疏水区，后续模拟将毫无意义。构建磷脂膜我最推荐用我写的genmixmem程序，速度很快，用着很方便，结合GROMACS模拟磷脂体系特别容易，详见《生成混合组分的磷脂双层膜结构文件的工具genmixmem》（<http://sobereva.com/245>）。至于产生膜蛋白，我最推荐使用GROMACS可以实现的membed方法，在北京科音动力学与GROMACS培训班里会演示操作。

如果你要建模的是分子团簇，用于构型搜索之类目的，用笔者开发的genmer比使用Packmol好得多，一次可以产生一大批，输入文件写起来省事得多，参见《genmer：生成团簇初始构型结合molclus做团簇结构搜索的超便捷工具》（<http://bbs.keinsci.com/thread-2369-1-1.html>）。

如果你用Packmol建模的目的是之后用GROMACS做模拟，别忘了GROMACS的拓扑文件里[molecules]字段里的分子按顺序完全展开后，原子的顺序必须和结构文件完全相同。为保证这一点，用于Packmol建模的分子结构文件里的原子顺序首先就得和这个分子的拓扑信息（具体来说是[atoms]字段）相对应。
