---
post_id: 308
title: Gaussian单点能自动相互运算工具enecalc
url: http://sobereva.com/308
date: '2015-11-03T18:47:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- Gaussian
- 结构与文件格式
academic_relevant: true
classification_reason: 核心是enecalc工具对Gaussian单点能进行自动运算。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**Gaussian单点能自动相互运算工具enecalc**  
enecalc: A tool for performing mathematical operations on single point energies calculated by Gaussian

文/Sobereva @[北京科音](http://www.keinsci.com/)

 First release: 2015-Nov-3   Last update: 2020-Aug-21

1.0版下载地址：<http://sobereva.com/soft/enecalc_1.0.rar>

### 1 用途

enecalc程序用来对指定的结构在不同级别下调用Gaussian来计算单点能，然后根据预设的系数进行相互运算，得到最终能量，很适合用来做基组外推计算。

### 2 压缩包内容

enecalc.exe：编译好的Windows版可执行文件  
enecalc：编译好的Linux 64bit版可执行文件  
settings.ini：用来设定运行参数  
template.gjf：模板文件，里面包含体系结构和内存、内核数等设定，关键词部分留空。

### 3 实例1：一般情况

例如对某个结构，按照以下外推公式计算能量：  
E[QCISD(T)/CBS]=1.4629*E[QCISD(T)/TZ]-0.4629*E[QCISD(T)/DZ]+1.6938*E[MP2/QZ]-2.1567*E[MP2/TZ]+0.4629*E[MP2/DZ]  
  
可以将settings.ini写为  
"D:\study\g09w\g09"   // Gaussian的路径，注意用双引号扩住  
 1   // 设定当前的系统，1为Windows，2为Linux或MacOS  
 0   // enecalc支持ONIOM计算，如果是ONIOM任务写1，否则为0  
 5   // 要考虑的计算级别数，可以为无穷多  
 1.4629 -0.4629 1.6938 -2.1567 0.4629     // 每个级别的能量要乘的系数  
 QCISD(T)/cc-pVTZ  // 第1个级别计算时用的关键词，后同  
 QCISD(T)=   // enecalc从输出文件末尾读取能量，这里设定用于定位第1个级别能量的字符串，后同  
 QCISD(T)/cc-pVDZ  
 QCISD(T)=  
 MP2/cc-pVQZ  
 MP2=  
 MP2/cc-pVTZ  
 MP2=  
 MP2/cc-pVDZ  
 MP2=  
  
以下是模板文件template.gjf示例  
%mem=1500MB  
 %nproc=4  
 #  
  
 B3LYP/6-31G* opted  
  
 0 1  
  O                  0.33287540   -1.10635328    1.50332174  
  H                  0.33287540   -0.34740028    0.90678174  
  H                  0.33287540   -1.86530628    0.90678174  
  
  
启动enecalc之后，程序先读取当前目录下的settings.ini，然后将第一个计算级别的关键词套入当前目录下的模板文件template.gjf里，生成001.gjf，然后调用Gaussian产生001.out，从中读取能量并显示出来。然后再如此处理第二个级别，直至全部级别都处理完，最后输出根据定义的规则运算出最终总能量。

注：做CBS外推最好的做法是看此帖里我的回复：<http://bbs.keinsci.com/forum.php?mod=redirect&goto=findpost&ptid=19058&pid=128867&fromuid=1>

### 4 实例2：ONIOM的情况

此例和上例一样进行能量外推计算，但是是基于ONIOM计算。下面是settings.ini文件，注意不需要写用于定位的字符串，因为enecalc直接读取输出文件中的ONIOM: extrapolated energy =后面的值。  
"g09"  
 2  
 1  
 5  
 1.4629 -0.4629 1.6938 -2.1567 0.4629  
 oniom(CCSD(t)/cc-pVTZ:M062X/TZVP)  
 oniom(CCSD(t)/cc-pVDZ:M062X/TZVP)  
 oniom(MP2/cc-pVQZ:M062X/TZVP)  
 oniom(MP2/cc-pVTZ:M062X/TZVP)  
 oniom(MP2/cc-pVDZ:M062X/TZVP)  
  
模板文件template.gjf示例：  
%mem=7GB  
 %nproc=4  
 #  
  
 Title Card Required  
  
 0 1  
  C                0    0.87378638   -1.26213590    0.00000000 L  
  H                0    1.23044081   -2.27094591    0.00000000 L  
  H                0    1.23045922   -0.75773771   -0.87365150 L  
  H                0   -0.19621362   -1.26212272    0.00000000 L  
  C                0    1.38712860   -0.53617963    1.25740497 L H 8  
  H                0    1.03207226    0.47319346    1.25642745 L  
  H                0    1.02885949   -1.03944806    2.13105486 L  
  C                0    2.92712600   -0.53863598    1.25881364 H  
  H                0    3.28539448   -0.03569410    0.38497547 H  
  H                0    3.28218223   -1.54800868    1.26016738 H  
  O                0    3.40380116    0.13590181    2.42615231 H  
  H                0    4.36379924    0.13453019    2.42749555 H
