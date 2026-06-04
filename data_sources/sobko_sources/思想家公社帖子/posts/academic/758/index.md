---
post_id: 758
title: Multiwfn结合ORCA的TDDFT计算做空穴-电子等分析的方法
url: http://sobereva.com/758
date: '2025-12-07T14:21:00+08:00'
source_categories:
- Multiwfn
- 量子化学
- ORCA
primary_topic: Multiwfn
secondary_topics:
- ORCA
- 激发态与光谱
academic_relevant: true
classification_reason: 标题聚焦 Multiwfn 结合 ORCA 的 TDDFT 空穴-电子分析流程。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

**Multiwfn结合ORCA的TDDFT计算做空穴-电子等分析的方法**  
Method of performing hole-electron and relevant analyses via Multiwfn in combination with TDDFT calculation of ORCA

文/Sobereva@[北京科音](http://www.keinsci.com)  2025-Dec-7

### 0 前言

Multiwfn是电子激发分析的十分强大的武器库，在《Multiwfn支持的电子激发分析方法一览》（<http://sobereva.com/437>）里有全面盘点。其主功能18中有很多分析方法依赖于参考态轨道波函数和激发态组态系数，典型的如《使用Multiwfn做空穴-电子分析全面考察电子激发特征》（<http://sobereva.com/434>）介绍的空穴-电子分析和δr指数、《在Multiwfn中通过IFCT方法计算电子激发过程中任意片段间的电子转移量》（<http://sobereva.com/433>）介绍的IFCT分析、《使用Multiwfn做自然跃迁轨道(NTO)分析》（<http://sobereva.com/377>）介绍的NTO分析，等等一大堆。它们通常结合目前研究电子激发最常用的TDDFT方法使用。在这些文章里我都明确示例了怎么结合Gaussian的TDDFT计算实现这些分析，而如今免费又强大的量子化学程序ORCA的用户也很多，因此在本文专门示例一下怎么结合ORCA来实现。本文只使用如今特别流行的空穴-电子分析作为例子，其它的需要轨道+组态系数的分析方法所用的文件与空穴-电子分析完全一样，就不一一举例了。

这里我假定读者已经看过上述博文了解了空穴-电子分析的原理和用法。如果读者不了解Multiwfn的话，看《Multiwfn FAQ》（<http://sobereva.com/452>）和《Multiwfn入门tips》（<http://sobereva.com/167>）。读者请务必使用**2025-Dec-7**及以后更新的Multiwfn版本，否则情况与本文说的不符。Multiwfn可以在官网<http://sobereva.com/multiwfn>免费下载。读者务必使用ORCA **6.1.1**及以后的版本，本文用的是ORCA 6.1.1。我假定读者已了解ORCA的各种常识和做TDDFT的方法，在《北京科音高级量子化学培训班（<http://www.keinsci.com/KAQC>）中对ORCA的各方面使用有极为全面系统的讲解，ORCA的安装方法见《量子化学程序ORCA的安装方法》（<http://sobereva.com/451>）。

本文的例子使用与《使用Multiwfn做空穴-电子分析全面考察电子激发特征》中相同的D-pi-A体系，只不过基组从6-31G*改为了ORCA用户更常用的def2-SVP。所有例子的输入输出文件都在<http://sobereva.com/attach/758/file.rar>里。

### 1 TDA-DFT情况下的空穴-电子分析

在演示使用严格的TDDFT做电子激发分析之前，这一节先说ORCA默认用的TDA近似下的TDDFT的情况，即TDA-DFT的情况，这种情况最为简单。

使用ORCA运行以下输入文件，对应本文文件包里的ORCA_TDA_D-pi-A\TDA.inp，算完后得到输出文件TDA.out。还同时在当前目录下产生了一堆其它文件，除了TDA.gbw外都删掉。

! CAM-B3LYP def2-SVP pal16 tightSCF miniprint  
%tddft  
  nroots 5  
  tprint 1E-8  
end  
%maxcore 3000  
* xyz 0 1  
 C                  3.55863800   -1.13874700    0.39983600  
 C                  2.17031600   -1.13391800    0.39359500  
...略  
*

注意%tddft中的tprint 1E-8很重要，代表对电子激发贡献大于1E-8的组态都输出系数，相当于Gaussian的IOp(9/40=4)。想让结果更精确也可以设得更小，但改进甚微，而输出文件尺寸会增大、Multiwfn的分析耗时会增加。

运行orca_2mkl TDA -molden命令，会基于TDA.gbw转换出TDA.molden.input，其中记录了参考态轨道波函数，类似于Gaussian的fch文件。

启动Multiwfn，载入TDA.molden.input，然后输入  
18  //电子激发分析  
1  //空穴-电子分析  
[回车]  //这一步让用户输入ORCA的输出文件路径，直接按回车代表载入与输入文件同路径的同名但后缀为out的文件（TDA.out）  
2  //以分析第2激发态为例

现在Multiwfn就从TDA.out中载入了组态系数。之后可照常做后面的分析，比如输入  
1  //可视化空穴、电子、跃迁密度等函数  
2  //中等质量格点  
3  //同时显示空穴和电子的等值面

### 2 TDDFT情况下的空穴-电子分析

至少截止到笔者撰文时（2025-Dec-7）的最新版ORCA 6.1.1来说，ORCA尚无法在TDDFT计算时将激发组态系数和去激发组态系数分别输出。为了使得Multiwfn基于ORCA的TDDFT计算做空穴-电子分析可行，需要导出记录所有组态系数的json文件并令Multiwfn从其中读取。

！！注意！！由于笔者撰文时最新版ORCA对于参考态为开壳层的情况无法在json文件中以正确格式输出组态系数，因此本节的做法目前只适用于参考态为闭壳层的情况！等以后ORCA修正了这个bug，Multiwfn也会使本节的做法支持开壳层参考态。

运行以下输入文件，对应本文文件包里的ORCA_TDDFT_D-pi-A\TDDFT.inp，算完后得到输出文件TDDFT.out。还同时在当前目录下产生了一堆其它文件，除了TDDFT.gbw外都删掉。

! CAM-B3LYP def2-SVP pal16 tightSCF miniprint  
%tddft  
  nroots 5  
  tda false  
end  
%maxcore 3000  
* xyz 0 1  
 C                  3.55863800   -1.13874700    0.39983600  
 C                  2.17031600   -1.13391800    0.39359500  
...略  
*

运行orca_2mkl TDDFT -molden命令，会基于TDDFT.gbw转换出TDDFT.molden.input。

创建一个文本文件叫TDDFT.json.conf，在里面写入如下内容  
{  
"CIS": true,  
"CISNRoots": true  
}  
然后运行orca_2json TDDFT.gbw，就会在当前目录下产生TDDFT.json。

说明：TDDFT.json.conf是orca_2json的控制文件，控制orca_2json在处理TDDFT.gbw时用的设置，当前内容要求把所有激发的组态系数都写入json文件，而默认不会写入。若控制文件的名字为orca.json.conf，则对于当前目录下任意名字的gbw在用orca_2json处理时都会用其中的设置。

启动Multiwfn，载入TDDFT.molden.input，然后输入  
18  //电子激发分析  
1  //空穴-电子分析  
[回车]  //载入与输入文件在同目录下同名的out文件（TDDFT.out）  
2  //以分析第2激发态为例  
此时如屏幕上的提示所示，由于Multiwfn发现在TDDFT.out的同目录下有名字相同但后缀为json的文件（TDDFT.json），Multiwfn就自动从json文件中载入了组态系数。json文件里记录的是全部组态系数，Multiwfn默认只载入绝对值大于1E-4的组态系数以节约之后的分析时间，这个阈值可以通过settings.ini中的ORCAloadcoeff修改。

现在就进入了空穴-电子分析界面，照常做分析即可，结果和同级别下Multiwfn+Gaussian的分析结果差异可忽略不计。

技巧：如果你把Multiwfn的settings.ini里的orca_2mklpath设为了orca_2mkl的实际路径，则以上例子中不需要手动用orca_2mkl转换gbw文件成molden.input文件，而是可以直接用Multiwfn载入gbw文件，此时Multiwfn会自动将之转换为.molden.input文件并载入，然后再删掉molden.input。

顺带再举个例子，对ORCA的TDDFT计算使用《使用Multiwfn便利地查看所有激发态中的主要轨道跃迁贡献》（<http://sobereva.com/529>）介绍的功能。启动Multiwfn后载入TDDFT.out，然后进入主功能18的子功能15，就得到了如下结果，所有5个态的组态系数也都是从json文件中读取的。

 #   1   3.8520 eV    321.87 nm   f=  0.01007   Spin multiplicity= 1:  
   H-4 -> L 82.3%, H-4 -> L+2 13.0%  
 #   2   4.0470 eV    306.36 nm   f=  0.64110   Spin multiplicity= 1:  
   H -> L 87.4%, H-3 -> L 5.2%  
 #   3   4.3730 eV    283.52 nm   f=  0.00009   Spin multiplicity= 1:  
   H-6 -> L 84.4%, H-6 -> L+2 12.7%  
 #   4   4.7440 eV    261.35 nm   f=  0.01900   Spin multiplicity= 1:  
   H -> L+1 38.7%, H-2 -> L 25.3%, H -> L+3 18.0%, H-1 -> L 5.8%  
 #   5   4.8350 eV    256.43 nm   f=  0.00409   Spin multiplicity= 1:  
   H -> L+3 43.3%, H-2 -> L 41.1%, H-3 -> L+1 5.1%
