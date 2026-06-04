---
post_id: 657
title: sobeig：计算矩阵本征值和本征矢的便捷小程序
url: http://sobereva.com/657
date: '2023-01-28T21:02:00+08:00'
source_categories:
- 其它
primary_topic: 其它软件
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题直接指向名为sobeig的小工具，属于计算矩阵本征值的实用程序。
topic_family: 软件
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**sobeig：计算矩阵本征值和本征矢的便捷小程序**

sobeig: a convenient utility for calculating matrix eigenvalues and eigenvector

文/Sobereva@[北京科音](http://www.keinsci.com)   2023-Jan-28

自己写程序求解矩阵的本征值和本征矢极其简单。但有时候需要对给定的矩阵随手求一下本征值和本征矢，一般的计算器程序又没有这个功能，往往又懒得写或来不及现写个程序去做，还有些人则完全不会写。正好笔者在培训班讲课时需要现场求CP2K输出的超精细耦合各向异性张量的本征值，就顺手写了个小程序叫sobeig，这里也分享出来。

sobeig可以在<http://sobereva.com/soft/sobeig_1.0.zip>下载，带exe后缀的是Windows版，没后缀的是Linux版（PS：别问我怎么在Linux下启动此程序这种没必要问的问题）。

启动后，sobeig会让你输入记录矩阵的文本文件的路径，程序包自带的mat.txt就是例子，是个3*3的矩阵，是自由格式，如下所示：  
 0.0918507019        -4.9297513675        -5.2344223141  
-4.9297513675         0.8863948625         2.3565979846  
-5.2344223141         2.3565979846        -0.9782455645

然后程序会问你矩阵的维度是几，对于处理自带的mat.txt显然输入3。然后本征值就显示在屏幕上了：

 ******************************* Loaded matrix *******************************  
             1             2             3  
     1  9.18507E-002 -4.92975E+000 -5.23442E+000  
     2 -4.92975E+000  8.86395E-001  2.35660E+000  
     3 -5.23442E+000  2.35660E+000 -9.78246E-001

 Calculating, please wait...  
 Successful!

 Eigenvalues:  
         1     8.50318156E+000  
         2    -6.22710477E+000  
         3    -2.27607679E+000

同时本征值和本征矢都以极其清晰的格式输出到了当前目录下的eig.txt中，内容为：

 Eigenvalues:  
         1     8.50318156E+000  
         2    -6.22710477E+000  
         3    -2.27607679E+000  
   
 Eigenvector         1  
   0.64795841E+000  -0.57420585E+000  -0.50043735E+000  
   
 Eigenvector         2  
  -0.73900099E+000  -0.31481607E+000  -0.59562435E+000  
   
 Eigenvector         3  
  -0.18446527E+000  -0.75576351E+000   0.62832642E+000

可见使用便利到没法更便利！利用echo或重定向通过命令行方式运行也可以，参看《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>）。

sobeig可以处理任意大的矩阵。只能是方阵，可以是对称的也可以不是对称的。程序内部是基于Intel MKL数学库做矩阵对角化，速度极快。支持并行，把OMP_NUM_THREADS环境变量设为并行核数即可。
