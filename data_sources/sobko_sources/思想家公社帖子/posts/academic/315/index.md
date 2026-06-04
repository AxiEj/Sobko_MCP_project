---
post_id: 315
title: Shermo：计算气相分子配分函数和热力学数据的简单程序
url: http://sobereva.com/315
date: '2015-12-26T08:03:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 量子化学
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 核心是Shermo程序用于计算热力学数据。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**2020-May-19注**：本文对应的是Shermo 1.0版，此程序已经完全没有意义了，因为后来笔者发布了Shermo 2.0版，介绍见《使用Shermo结合量子化学程序方便地计算分子的各种热力学数据》（<http://sobereva.com/552>）。2.0版比1.0版好用、强大、灵活得多得多得多，是日常量子化学研究者计算分子热力学数据离不开的工具。

**Shermo：计算气相分子配分函数和热力学数据的简单程序**  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)  2015-Dec-26

用过Gaussian的人都知道Freq任务会输出一堆热力学数据，但真正搞懂这些量到底怎么算出来的人不多。于是笔者开发了一个既有实用意义也有教学意义的Shermo程序（名字由来是Sob+Thermo）。  
  
基于给定的谐振频率、惯性矩、温度、压力、原子质量、转动对称数等信息，Shermo程序可以输出分子配分函数和理想气体近似下的每mol的内能、焓、熵、自由能、热容，并且平动、转动、振动和电子贡献会独立输出，每种振动模式的贡献也能独立输出（这一点很有意义，能很方便直观地考察各个振动模式对热力学数据的影响）。  
  
Shermo由Fortran编写，代码简洁易懂，也很适合学习热力学计算之用，以加深对概念的理解。程序附带了写得极为清楚的文档，里面有所有数据的计算公式，和源代码一对照就能透彻搞懂这些量是怎么算的了。  
   
下载链接：<http://sobereva.com/soft/Shermo.rar>  
压缩包里包含Windows版可执行程序、源代码、文档、示例输入文件以及与之对应的Gaussian freq任务的输出文件。

如果你的研究中使用了本程序，请这样引用：Tian Lu, Shermo program, <http://sobereva.com/315> (accessed month day, year)

以下是输出例子：  
  
 Shermo: A utility to calculate various thermodynamic properties  
 Programmed by Sobereva (sobereva@sina.com)  
 First release: 2015-Dec-26  
  
 Temperature(K):     298.150  
 Pressure(Atm):       1.000  
 Rotational symmetry number: 6  
 Note: This is a non-linear molecule  
 Moments of inertia:    22.457510   90.665730   90.665730 amu*Bohr^2  
 Rotational constant:   80.362480   19.905440   19.905440 GHz  
 Rotational temperature:    3.856786    0.955309    0.955309 K  
 Spin multiplicity: 1  
 The number of atoms:    8  
  
 The number of frequencies:   18  
 Atom:    1   Mass:  12.000 amu  
 Atom:    2   Mass:   1.008 amu  
 Atom:    3   Mass:   1.008 amu  
 Atom:    4   Mass:   1.008 amu  
 Atom:    5   Mass:  12.000 amu  
 Atom:    6   Mass:   1.008 amu  
 Atom:    7   Mass:   1.008 amu  
 Atom:    8   Mass:   1.008 amu  
 Total mass:   30.046980 amu  
  
 Note: Only for translation motion, contribution to CV and U are different to CP  
 and H, respectively  
  
                          ======= Translation =======  
  
 Translational q(T):        0.389858E+31  
 Translational q(T)/N:      0.647375E+07  
 Translational U(T):    0.888728 kcal/mol  
 Translational H(T):    1.481213 kcal/mol  
 Translational CV:      2.980807 cal/mol/K  
 Translational CP:      4.968012 cal/mol/K  
 Translational S(T):   36.133874 cal/mol/K  
  
                          ========= Rotation ========  
  
 Rotational q(T):      0.810623E+03  
 Rotational U(T):    0.888728 kcal/mol  
 Rotational CV:      2.980807 cal/mol/K  
 Rotational S(T):   16.290714 cal/mol/K  
  
                          ======== Vibration ========  
  
  Mode  Wavenumber   Freq     Vib. Temp.   q(V=0)      q(BOT)  
          cm^-1      GHz          K  
    1    312.37   0.9365E+04    449.43    1.284493    0.604507  
    2    827.24   0.2480E+05   1190.22    1.018810    0.138433  
    3    827.24   0.2480E+05   1190.22    1.018810    0.138432  
    4   1005.19   0.3013E+05   1446.24    1.007885    0.089144  
    5   1225.75   0.3675E+05   1763.58    1.002706    0.052087  
    6   1225.76   0.3675E+05   1763.59    1.002706    0.052087  
    7   1417.66   0.4250E+05   2039.69    1.001070    0.032728  
    8   1439.90   0.4317E+05   2071.69    1.000961    0.031015  
    9   1516.70   0.4547E+05   2182.19    1.000663    0.025761  
   10   1516.70   0.4547E+05   2182.20    1.000663    0.025761  
   11   1521.35   0.4561E+05   2188.88    1.000648    0.025473  
   12   1521.35   0.4561E+05   2188.89    1.000648    0.025473  
   13   3043.61   0.9125E+05   4379.08    1.000000    0.000647  
   14   3044.76   0.9128E+05   4380.72    1.000000    0.000645  
   15   3099.30   0.9291E+05   4459.20    1.000000    0.000565  
   16   3099.30   0.9291E+05   4459.20    1.000000    0.000565  
   17   3123.19   0.9363E+05   4493.57    1.000000    0.000534  
   18   3123.19   0.9363E+05   4493.57    1.000000    0.000534  
  
  Mode  Wavenumber     ZPE      U(T)-U(0)    U(T)      CV(T)       S(T)  
          cm^-1      kcal/mol   kcal/mol   kcal/mol  cal/mol/K  cal/mol/K  
    1    312.373      0.447      0.254      0.701      1.650      1.350  
    2    827.245      1.183      0.044      1.227      0.607      0.186  
    3    827.245      1.183      0.044      1.227      0.607      0.186  
    4   1005.188      1.437      0.023      1.460      0.372      0.092  
    5   1225.753      1.752      0.009      1.762      0.189      0.037  
    6   1225.756      1.752      0.009      1.762      0.189      0.037  
    7   1417.658      2.027      0.004      2.031      0.100      0.017  
    8   1439.897      2.058      0.004      2.062      0.092      0.015  
    9   1516.703      2.168      0.003      2.171      0.071      0.011  
   10   1516.703      2.168      0.003      2.171      0.071      0.011  
   11   1521.351      2.175      0.003      2.178      0.070      0.011  
   12   1521.353      2.175      0.003      2.178      0.069      0.011  
   13   3043.615      4.351      0.000      4.351      0.000      0.000  
   14   3044.757      4.353      0.000      4.353      0.000      0.000  
   15   3099.303      4.431      0.000      4.431      0.000      0.000  
   16   3099.303      4.431      0.000      4.431      0.000      0.000  
   17   3123.188      4.465      0.000      4.465      0.000      0.000  
   18   3123.190      4.465      0.000      4.465      0.000      0.000  
  
 Vibrational q(V=0):         0.135737E+01  
 Vibrational q(BOT):         0.464776E-34  
 Vibrational ZPE:    0.074930 a.u.      47.019 kcal/mol     196.729 kJ/mol  
 Vibrational U(T)-U(0):    0.404393 kcal/mol  
 Vibrational U(T):        47.423838 kcal/mol  
 Vibrational CV(T):        4.085798 cal/mol/K  
 Vibrational S(T):         1.963524 cal/mol/K  
  
                         ======== Electron spin ========  
  
 Note: Thermal excitation of electronic states is not taken into account, so ele  
ctronic contribution to CV and U are zero  
 Electronic q:     1.000000  
 Electronic S:     0.000000 cal/mol/K  
  
                           ===========================  
                           ========== Total ==========  
                           ===========================  
  
 Total q(V=0):           0.428966E+34  
 Total q(BOT):           0.146882E+00  
 Total q(V=0)/N:         0.712315E+10  
 Total q(BOT)/N:         0.243904E-24  
 Total CV(T):     10.047412 cal/mol/K  
 Total CP(T):     12.034617 cal/mol/K  
 Total S(T):      54.388112 cal/mol/K  
 Thermal correction to U(T):      49.201 kcal/mol    0.078407 a.u.  
 Thermal correction to H(T):      49.794 kcal/mol    0.079351 a.u.  
 Thermal correction to G(T):      33.578 kcal/mol    0.053510 a.u.
