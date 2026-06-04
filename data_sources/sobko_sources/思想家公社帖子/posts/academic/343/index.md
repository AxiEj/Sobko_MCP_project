---
post_id: 343
title: 从Gaussian和GAMESS-US中提取电子积分
url: http://sobereva.com/343
date: '2016-07-30T23:55:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 其它软件
- 结构与文件格式
academic_relevant: true
classification_reason: 标题焦点在Gaussian中提取积分，并与GAMESS-US对照，属于软件与文件接口。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**从Gaussian和GAMESS-US中提取电子积分**Extract electronic integrals from Gaussian and GAMESS-US  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)  2016-Jul-31

  
  
获得电子积分是自己写量化程序的关键。在网上能找到一些零散的从常用的Gaussian或GAMESS-US程序中提取单、双电子积分的帖子，但是往往语焉不详，说得不确切、不全面，有的做法不雅，有的还会令人白绕弯路。这里把从Gaussian和GAMESS-US中提取电子积分的方式清楚、详细、准确地说一下。  
  
无论输出的是单电子积分还是双电子积分，都是基函数已归一化后的值。  
  
双电子积分形式是(IJ|KL)，I,J基函数是r1坐标，K,L基函数是r2坐标。由于积分有对称性，即IJKL=IJLK=JIKL=JILK=KLIJ=LKIJ=KLJI=LKJI，所以程序输出双电子积分的时候都只输出对称唯一的部分。  
  
  

## 1 从Gaussian中提取积分

以下内容对Gaussian09 D.01亲测有效。  
  
由于Gaussian会自动调整朝向，会影响积分值，建议加上nosymm，这样也避免因对称性等价的积分不被输出。  

#### 1.1 单电子积分

计算时加上IOp(3/33=1)即可，输出的包括  
*** Overlap ***：重叠积分  
*** Kinetic Energy ***：动能积分  
***** Potential Energy *****：核吸引势积分（没考虑电子带负电荷，所以数值皆为正）  
****** Core Hamiltonian ******：核哈密顿矩阵。其数值就是动能积分矩阵元减去核吸引势积分矩阵元  
Multipole matrices：输出三次，IX= 1、IX= 2、IX= 3分别对应X,Y,Z方向的偶极矩积分矩阵。  
  

#### 1.2 双电子积分

Gaussian可以通过L316模块双电子积分。用这些关键词即可：IOp(3/33=3) extralinks(L316) scf=conventional noraff。同时上一节的单电子积分也会输出。  
  
输出信息诸如：  
 IntCnt=   4238596 ITotal=   4238596 NWIIB=    262144 ISym2E=0  
 I= 44 J= 29 K= 43 L= 10 Int=  0.147872132379D-07  
 I= 44 J= 43 K= 29 L= 10 Int= -0.396977105787D-08  
 I= 45 J= 29 K= 43 L= 10 Int= -0.403826333553D-07  
...  
这里IntCnt是实际输出的积分总数。注意并行计算时每次输出的积分顺序可能不同。  
  
Gaussian计算并输出双电子积分的值阈值可以用IOp(3/27=N)调节，小于10^-N的积分不会被计算和输出。默认N=10，精度已经很高了，若要计算并输出数值更小的可以比如设N=12。  
  
用32bit版本时这种方式输出积分时基函数最多127个。虽然64bit版没这个限制，但基函数多于这个时输出文件会巨大。  
  
  
  

## 2 从GAMESS-US中提取积分

  
以下方法对2014-Dec版亲测有效。相同基组下（Dunning基组不算，因Gaussian会自动会去掉其中冗余的GTF）输出的结果和Gaussian中的一致。  
  
输出单电子积分和双电子积分都有改代码和不改代码两种做法，结果一样，前者省事，但后者可以自由控制输出格式，而且还能同时用NPRINT=-5来避免计算时输出一堆翔一样的大量无用的信息。  
  
输出积分时绝对不要用并行运算，否则输出内容会癫狂。  
  

### 2.1 单电子积分

#### 2.1.1 方法1（不用改源码）

$CONTRL里写上NPRINT=3即可在计算时输出基函数间的各种积分矩阵，会看到这样的段落  
          ********************  
          1 ELECTRON INTEGRALS  
          ********************  
下面输出的包括：  
OVERLAP MATRIX：重叠矩阵  
BARE NUCLEUS HAMILTONIAN INTEGRALS (H=T+V)：核哈密顿矩阵  
KINETIC ENERGY INTEGRALS：动能积分矩阵  
程序没直接给出核吸引势积分，这只需自行把核哈密顿矩阵减去动能积分矩阵即可。  
  

#### 2.1.2 方法2（需改源码）

在gamess/source/int1.src中----- OPTIONAL DEBUG PRINTOUT -----有两处，在第一处的下面加上  
      write(*,"(/,' Overlap integrals, num:',i8)") LL2  
      write(*,"(4D18.10)") S  
      write(*,"(/,' Kinetic energy integrals, num:',i8)") LL2  
      write(*,"(4D18.10)") T  
      write(*,"(/,' Core Hamiltonian matrix, num:',i8)") LL2  
      write(*,"(4D18.10)") H  
      write(*,"(/,' Potential energy integrals, num:',i8)") LL2  
      write(*,"(4D18.10)") H-T  
      write(*,*)  
可见，改过之后可以直接把核吸引势积分输出出来，已经考虑电子是带负电荷。  
  
重新编译此文件并链接成新的可执行文件使之生效，即在GAMESS-US目录下执行./comp int1;./lked gamess 00。瞬间就完事，用不着把整个GAMESS-US都重头编译一遍。  
  
之后一般计算时屏幕上就会输出各种单电子积分，上述几种积分矩阵都是对称矩阵，这里依次输出的是下三角部分的元素。如重叠积分：  
 Overlap integrals, num:      28  
  0.1000000000D+01  0.2367039205D+00  0.1000000000D+01  0.0000000000D+00  
  0.0000000000D+00  0.1000000000D+01  0.0000000000D+00  0.0000000000D+00  
  0.0000000000D+00  0.1000000000D+01  0.2005800301D-16  0.2537204019D-17  
  0.0000000000D+00  0.0000000000D+00  0.1000000000D+01  0.5362008406D-01  
  0.4729709355D+00  0.0000000000D+00 -0.3205127531D+00  0.2265160217D+00  
  0.1000000000D+01  0.5362008406D-01  0.4729709355D+00  0.0000000000D+00  
  0.3205127531D+00  0.2265160217D+00  0.2327636225D+00  0.1000000000D+01  
这里num后面是输出的元素数目。  
  
  

### 2.2 双电子积分

一定要用$SCF DIRSCF=.F. $END使用conventional的SCF方式，否则不会输出这些积分。  

#### 2.2.1 方法1（不用改源码）

$CONTRL里写上NPRINT=4即可在计算时输出双电子积分，会看到如  
 II,JST,KST,LST =  1  1  1  1 NREC =         1 INTLOC =    1  
 II,JST,KST,LST =  2  1  1  1 NREC =         1 INTLOC =    2  
   1   1   1   1  1.0      4.785065752    2   1   1   1  1.0      0.741380321  
   2   2   1   1  1.0      1.118946840    3   3   1   1  1.0      1.115813819  
   4   4   1   1  1.0      1.115813819    5   5   1   1  1.0      1.115813819  
   2   1   2   1  1.0      0.136873367    3   1   3   1  1.0      0.024477411  
...  
 TOTAL NUMBER OF NONZERO TWO-ELECTRON INTEGRALS =                 228  
最后一行就是实际输出的双电子积分数，当前是228个。默认是小于10^-9的积分不被输出，可以在$CONTRL里用ICUT=N来把输出阈值调为10^-N，显然N越大输出得越多。  
  
对(IJ|KL)积分，有8种等价形式，程序自动把指标调换成I>=J、K>=L、I>=K的形式。  
  

#### 2.2.2 方法2（需改源码）

在gamess/source/int2a.src的I4 = LOCL+L下面加上  
write(*,"(4i6,D25.16)") I1,I2,I3,I4,VAL  
重新编译此文件并链接成新的可执行文件使之生效，即在GAMESS-US目录下执行./comp int2a;./lked gamess 00。  
  
之后一般计算时屏幕上就会输出双电子积分，诸如  
     1     1     1     1   0.4785065752035100D+01  
     2     1     1     1   0.7413803207944081D+00  
     2     2     1     1   0.1118946840438162D+01  
     3     3     1     1   0.1115813818563188D+01  
     4     4     1     1   0.1115813818563188D+01  
     5     5     1     1   0.1115813818563188D+01  
...  
  
如上一节所述，非常小的积分不会输出，阈值可以用ICUT来设。如果想输出所有积分，直接把int2a.src中IF(ABS(VAL).LT.CUTOFF) GO TO 200这一行注释掉即可。  
  
如果想输出NPRINT=4那样的将序号调换为I>=J、K>=L、I>=K后的积分，把前述输出语句加到IF (OUT) CALL INTOUT(I1,I2,I3,I4,QQ4,IJKL_INDEX,VAL)的上面一行。
