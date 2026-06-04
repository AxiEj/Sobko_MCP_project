---
post_id: 112
title: 提取Gaussian的rwf文件信息的工具rwfdump简介
url: http://sobereva.com/112
date: '2015-06-07T23:51:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章介绍Gaussian的rwf文件信息提取工具，软件和文件格式都是重点。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**提取Gaussian的rwf文件信息的工具rwfdump简介**Introduction to rwfdump, a tool for extracting information from Gaussian rwf file

文/Sobereva @[北京科音](http://www.keinsci.com/)   2011-Dec-15

Gaussian程序是由一个个独立的Link子程序组成的，完成一个计算任务需要各种Link按照指定顺序和特定选项依次被调用，如同一条作业流水线。在每个Link之间传递临时数据最主要依靠的是rwf文件，即读写文件，这个文件在计算任务一开始被初始化，随着计算的进行，不断地被填进更多的信息，如果没有通过%rwf=xxx来指定rwf文件保存的位置，在任务正常结束时会被自动删除。rwf文件里面储存的信息过于丰富，尤其是后HF计算中要需要储存积分变换数据，会十分庞大，不便于在硬盘上长期保存和拷贝。为了解决这个问题，rwf文件中一部分最重要的信息会在checkpoint文件（chk文件）中留有一个副本。由于chk文件只保留了rwf中的精华数据，因此体积比较小，而且通过formchk工具可以转换为文本格式，能够方便地从中提取有用信息进行进一步分析。另外，重新启动中断的任务也需要chk文件中的一部分信息。  
  
rwf文件包含很多“子文件”，分别存放不同类别的信息，我更愿意将之称为一个个槽位，毕竟rwf文件在硬盘上是作为一个而不是多个文件来保存的。每个槽位有一个对应编号，保存的内容可以参考<http://sobereva.com/g09/e_progdev.htm>当中的RWF Numbers部分。以下是从其中截取的一部分  
P 501 Gen array.   
P 502 /LABEL/—Title and atomic orbital labels.   
  503 Connectivity information (MxBond,0),NBond(NAtoms),IBond(MxBond,NAtoms),RBond(MxBond,NAtoms), where arrays are rounded to a multiple of IntPWP.   
  504 Dipole derivative matrices (NTT,3,NAt3).   
P 505 Array of copies of /Gen/ from potential surface scan.   
P 506 Saved basis set information before massage, uncontraction, etc.   
P 507 ZMAT/ and /ZSUBST/.   
P 508 /IBF/ Integral Bugger Format.   
  509 Incomplete integral buffer.   
T 510 /FPINFO/ Fletcher-Powell optimization program data.   
P 511 /GRDNT/ energy, First and second derivatives over variables, NVAR.   
P 512 Pseudo-potential information.   
P 513 /DIBF/ integral derivative buffer format.   
  514 Overlap matrix, optionally followed by absolute overlap and absolute overlap over primitives.   
  
开头有P的，代表这类信息也同时储存在了chk文件里；有T的，说明这类信息在任务执行过程中被储存在chk文件里，以备重新启动任务之需，但是由于普遍价值不大，在任务正常结束后就会从chk文件中删掉；而开头是空的信息，说明只存在于rwf文件中而在chk文件中没有副本。  
  
也就是说，那些没写P的信息没办法在任务结束后从chk文件里找到。然而这些信息有时候却很有用，在后续分析时可能要用到，比如基函数间的重叠积分矩阵。好在基函数间重叠矩阵通过guess=only iop(3/33=1)可以直接迅速输出出来，然而其它的一些信息，有的就没有对应IOp可以输出，或者有对应的命令能输出之，但是还得把耗时的过程重新算一次才能输出出来，很不方便。  
  
Gaussian中自带了一个颇有用的小程序rwfdump，它就在Gaussian安装目录下，专门用来将rwf文件中指定槽位中的信息提取出来并转化为可读的文件。可惜这个小程序并未在Gaussian用户手册，乃至程序员手册中提及，导致被很多人忽视。本质上，rwf文件指定槽位的信息是通过Gaussian代码中FileIO子程序进行读写的，rwfdump这个工具就是给FileIO子程序加个壳，使之成为能够独立运行的程序罢了。  
  
rwfdump通过命令行调用，语法是：rwfdump a.rwf a.txt iiix  
其中a.rwf是被提取信息的rwf文件。a.txt是提取出的信息储存的地方，如果输出文件名只写为一个横杠-，那么就直接输出到屏幕上。iii是rwf是信息的槽位编号。x控制输出数据的数据类型，I代表十进制整数，H代表十六进制数，R代表浮点数，A代表ASCII文本。  
  
例如，从官方的表格中查到540号槽位储存的是Molecular alpha-beta overlap (U), real，也就是非限制性计算中alpha轨道和beta轨道间的重叠积分，想提取它就可以输入比如  
rwfdump c:\idol-master\a.rwf d:\sob\BLOOD-C.txt 540R  
这里用的例子是uhf/sto-3g下计算的三重态乙酸。打开d:\ltwd\BLOOD-C.txt，在一开始会看到一堆类似这样的信息  
 Number         534        536        538        540        551        552        559        562  
 Base        121856     122368     129024     128000     104960     103936     107520      98304  
 End         122156     122668     129324     128576     104985     103950     107521     103801  
 End1        122368     122880     129536     129024     105472     104448     108032     103936  
 Wr Pntr     121856     122368     129024     128000     104960     103936     107520      98304  
 Rd Pntr     121856     122368     129024     128000     104960     103936     107520      98304  
 Length         300        300        300        576         25         14          1       5497  
这些信息是rwf文件里各个槽位的汇总，包括起始偏移量（Base）、终止偏移量（End）、长度（length，即End与Base之差）、写/读的指针位置（Wr/Rd Pntr），单位都是word（8字节，即一个双精度浮点数的大小）。可以看到，540号槽位的长度是576。由于提取的数据类型是浮点数，因此下面将出现576个数据，对应于这个体系中总共24个alpha轨道与24个beta轨道间的重叠积分。  
以下内容是那576个数据开头的一部分  
Dump of file   540 length           576 (read left to right):  
       0.99999749D+00      0.29425608D-03      0.26009204D-04      0.58930395D-06     -0.17093304D-02  
       0.75910206D-03      0.36841903D-03      0.63739342D-03      0.15016508D-03     -0.60968183D-08  
      -0.53159908D-03      0.21762391D-09     -0.82064171D-04      0.77445410D-04     -0.49774090D-09  
      -0.19852883D-04     -0.58360576D-08      0.67017502D-04      0.40140158D-03     -0.10351407D-03  
       0.13467769D-08     -0.14894984D-03      0.86191700D-04      0.61374239D-03     -0.29426013D-03  
       0.99999992D+00      0.15971966D-04      0.65829259D-06     -0.47920802D-04     -0.20630445D-03  
       0.50406617D-04      0.75184201D-04     -0.53428238D-04     -0.15868756D-08     -0.33577428D-04  
...  
-0.53159908D-03这种表示代表-0.00053159908，D是Fortran双精度浮点数中代表10的多少次方的意思。在自旋极化体系的非限制性计算中，alpha轨道与alpha轨道间正交归一，beta与beta轨道间正交归一，但alpha与beta轨道间没有正交归一的限制，因此这些数据中并不是1或0。接近0的表明相应alpha和beta轨道重叠积分很小，接近正交。而接近1的，可以认为是几乎配对、相互重合的alpha和beta轨道。rwfdump只是把数据简单提取出来，并没有自动排成舒服、容易由人类读取的格式，哪个数值对应哪两个alpha和beta轨道间重叠积分很难看出。实际上，在笔者的Multiwfn程序（<http://sobereva.com/multiwfn>）中有计算alpha和beta轨道间重叠积分矩阵的功能，载入wfn或fch文件后进入主功能100选5就行了，经过计算后会输出诸如这样的信息  
             1             2             3             4             5  
     1  0.999997D+00 -0.294260D-03  0.204458D-05 -0.251504D-04  0.101833D-02  
     2  0.294256D-03  0.100000D+01  0.987506D-06 -0.157908D-04  0.150142D-03  
     3  0.260092D-04  0.159720D-04 -0.103676D+00  0.994608D+00  0.892031D-03  
     4  0.589304D-06  0.658293D-06  0.994611D+00  0.103676D+00 -0.148590D-04  
     5 -0.170933D-02 -0.479208D-04  0.995302D-04 -0.832881D-03  0.847507D+00  
     6  0.759102D-03 -0.206304D-03  0.390161D-04 -0.322454D-03  0.529753D+00  
...  
其中i行j列代表第i个alpha轨道与第j个beta轨道的重叠积分。Multiwfn给出的数据可以与rwfdump输出的相互对应，rwfdump的横着的一行一行的数据对应于Multiwfn输出的一列一列的数据。  
  
  
另外，rwfdump也能用来从chk文件中直接提取指定槽位的数据。例如，从rwf槽位对照表中得知501储存的是Gen数组（这个数组包含的是各种各样的标量数据），由于前面写着P，表明它不仅保存在rwf文件里也保存在chk文件里，因此就可以从chk文件里提取它，即运行比如rwfdump c:\ltwd\a.chk h:\K-ON\touhou.txt 501R  
提取出的Gen数组的前几行是  
       0.20068411D+01      0.00000000D+00      0.00000000D+00      0.00000000D+00      0.20297583D+03  
       0.00000000D+00      0.00000000D+00      0.00000000D+00      0.00000000D+00      0.00000000D+00  
       0.00000000D+00      0.00000000D+00      0.00000000D+00      0.00000000D+00      0.00000000D+00  
       0.00000000D+00      0.00000000D+00      0.00000000D+00      0.00000000D+00      0.00000000D+00  
       0.00000000D+00      0.00000000D+00      0.81962558D-08      0.20000118D+01      0.00000000D+00  
       0.00000000D+00      0.00000000D+00      0.00000000D+00      0.40442442D+01      0.00000000D+00  
       0.00000000D+00     -0.22469385D+03      0.00000000D+00      0.00000000D+00      0.00000000D+00  
通过查阅Gaussian程序员手册得知Gen数组第32个数是SCF能量，这里即-0.22469385D+03，它与Gaussian输出文件中显示的E(UHF) =  -224.693847643是完全对应的。
