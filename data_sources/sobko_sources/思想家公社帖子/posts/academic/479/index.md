---
post_id: 479
title: 使用Multiwfn一键批量产生各类光谱图（含演示视频）
url: http://sobereva.com/479
date: '2019-04-29T12:12:00+08:00'
source_categories:
- Multiwfn
- 量子化学
primary_topic: Multiwfn
secondary_topics:
- 激发态与光谱
- 可视化
- 结构与文件格式
academic_relevant: true
classification_reason: 标题是用 Multiwfn 一键批量产生各类光谱图，核心是软件自动化流程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**本文配有操作演示视频，强烈建议一看**：<https://www.bilibili.com/video/av50818216>

**使用Multiwfn一键批量产生各类光谱图**

Using Multiwfn to batch generate various spectra with one click

文/Sobereva@[北京科音](http://www.keinsci.com)  2019-Apr-29

## 0 前言

如果读者还没看过《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（<http://sobereva.com/224>）请先看此文。波函数分析程序Multiwfn具有非常强大的光谱绘制功能，本文目的是介绍一个小技巧，使用批处理文件，仅通过一条命令就令Multiwfn把当前目录下所有输入文件转化为光谱图。这里说的输入文件是指Multiwfn绘制光谱图的功能支持的输入文件，比如Gaussian、ORCA等程序的电子激发计算、振动分析任务的输出文件等，详见上面提到的文章。

Multiwfn可在主页<http://sobereva.com/multiwfn>免费下载，读者务必使用2019-Apr-28及之后更新的程序包，否则没有本文中提到的文件。

在程序包的examples\spectra\indigo目录下有四个.out文件，都是Gaussian使用不同级别做电子激发计算的输出文件，我们以这四个文件为例，说明怎么一下子就把它们都转化成UV-Vis光谱图像文件。

## 1 在Windows下运行

这里首先假设读者用的是Windows版。将四个.out文件都拷到Multiwfn目录下，然后把examples\spectra目录下的UV-Vis.txt和batchspec.bat也拷到Multiwfn目录下。然后把Multiwfn目录下的settings.ini里的isilent设为1并保存文件。直接双击batchspec.bat，马上当前目录下就出现了四个与输入文件同名的png文件，是UV-Vis谱的图像文件，可见极其方便！

原理是什么？首先看batchspec.bat，这是一个Windows下的批处理文件，点击右键选编辑，就可以看到以下内容  
for /f %%i in ('dir *.out /b') do (  
 Multiwfn %%i < UV-Vis.txt > NUL  
 rename DISLIN.png %%~ni.png  
 )

其中dir *.out显示当前目录下所有.out文件，利用for循环将每个文件名依次赋值给%%i，并对每个文件调用当前目录下的Multiwfn程序按照UV-Vis.txt文件里记录的指令进行处理。由于输出在屏幕上的信息不是我们需要的，所以将这些信息重定向到NUL，它相当于是个垃圾桶，定向到里面的信息都会消失不见。Multiwfn每次处理完一个文件后，会在当前目录下产生DISLIN.png文件，为了让文件名与输入文件相同，因此用rename重命名一下，%%~ni的写法代表把%%i变量记录的文件名的后缀去除。

再来看记录了在Multiwfn里输入的指令的UV-Vis.txt文件，内容如下，每一行对应在Multiwfn里敲入的一次指令，//后面是注释。如果还有不理解的，启动Multiwfn载入任意一个out文件，照着里面的命令敲一遍就肯定懂了  
11  //光谱绘制功能  
3  //绘制UV-Vis  
0  //显示一次光谱，否则之后无法修改纵坐标  
3  //修改横坐标设定  
150,850,100  //初值，终值，步长  
4  //修改左侧坐标轴（对应摩尔吸收系数）  
0,45000,5000  //初值，终值，步长  
y  //对右侧纵坐标做相应的缩放/平移  
5  //修改右侧坐标轴（对应振子强度）  
0,1.0,0.1  //初值，终值，步长  
n  //不对左侧坐标轴做相应的缩放/平移  
1  //产生图像文件

由于在选择选项0的时候光谱会在屏幕上弹出来，因此要把settings.ini里的isilent设为1使程序处于安静模式，这样就不会蹦出图像，免得到时候还得手动关闭了。

可见批量调用Multiwfn绘制光谱的机理非常简单易懂，想改什么，只要改相应内容就行了。一般需要改的就是坐标轴范围，可以先跑一下，发现范围不合理的话，改一下UV-Vis.txt里的坐标轴设置然后重新跑即可。

在examples\spectra目录下还有个IR.txt。如果你把此文件拷到Multiwfn目录，把batchspec.bat里的UV-Vis.txt改为IR.txt，那么双击batchspec.bat时就会把当前目录下所有.out文件转化为红外光谱的图像文件。IR.txt的内容就不再解释了，因为只要照着IR.txt里的指令在Multiwfn里敲一遍，对照屏幕上的提示，马上就能理解其中的内容。

想用Multiwfn批量绘制其它类型的光谱，如ROA、Raman、VCD、ECD、光电子谱，只要自己创建个记录了绘制命令的.txt文件，按照上述过程使用它来批处理即可。

## 2 在Linux下运行

如果你用的是Linux版Multiwfn，也想这样通过批处理绘图的话，先按照Multiwfn手册2.1.2节的步骤以正规方式安装Multiwfn，把examples\spectra中的batchspec.sh、UV-Vis.txt以及要绘图的文件都拷到当前目录下，然后在终端里输入./batchspec.sh运行之即可。如果提示没有可执行权限，先运行一下chmod +x ./batchspec.sh。

batchspec.sh是个Bash shell的脚本，内容为：

#!/bin/bash  
 for inf in *.out  
 do  
 Multiwfn ${inf} < UV-Vis.txt > /dev/null  
 mv -f dislin.png ${inf//out/png}  
 done

可见和batchspec.bat的内容大同小异，只不过命令改为了Linux下的情况。${inf//out/png}代表把$inf变量记录的文件名的out后缀替换为png。

为了用起来更方便，读者还可以把batchspec.sh和UV-Vis.txt放到比如/sob目录下，把./batchspec.sh里的UV-Vis.txt改为/sob/UV-Vis.txt，然后在~/.bashrc文件里增加一行  
alias UV='/sob/batchspec.sh'  
 alias gUV='gedit /sob/UV-Vis.txt'  
重新进入终端后，只要某个目录里有比如Gaussian的电子激发任务的输出文件，就在这个目录下运行UV命令即可将它们全都瞬间转化为UV-Vis光谱文件。如果发现坐标范围不合适，输入gUV命令就可以启动gedit编辑UV-Vis.txt的内容。

## 3 总结

希望读者举一反三，效仿本文的运行方式，使得Multiwfn实现其它任务的批量处理。笔者的很多与Multiwfn有关的博文都充分利用了批处理文件，比如《使用Multiwfn做空穴-电子分析全面考察电子激发特征》（<http://sobereva.com/434>）、《使用Multiwfn做自然跃迁轨道(NTO)分析》（<http://sobereva.com/377>）、《使用Multiwfn绘制跃迁密度矩阵和电荷转移矩阵考察电子激发特征》（<http://sobereva.com/436>）、《通过键级曲线和ELF/LOL/RDG等值面动画研究化学反应过程》（<http://sobereva.com/200>）等等，读者可参考之，写出功能更强的批处理脚本。
