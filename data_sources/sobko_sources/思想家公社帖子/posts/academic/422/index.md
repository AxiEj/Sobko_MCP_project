---
post_id: 422
title: 将Gaussian与ORCA联用搜索过渡态、产生IRC、做振动分析
url: http://sobereva.com/422
date: '2018-05-31T21:26:00+08:00'
source_categories:
- 量子化学
- ORCA
primary_topic: Gaussian
secondary_topics:
- ORCA
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章讲Gaussian与ORCA联用做过渡态、IRC和振动分析，Gaussian是主线。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**将Gaussian与ORCA联用搜索过渡态、产生IRC、做振动分析**

Use Gaussian with ORCA to search for transition states, generate IRC, and perform vibration analysis

文/Sobereva @[北京科音](http://www.keinsci.com)

First release: 2018-May-31  Last update: 2022-Jul-13

## 1 前言

在《将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC、做振动分析》（<http://sobereva.com/421>）中笔者介绍了Gaussian的external功能的使用，以及如何利用这个功能，借用xtb程序产生的能量、受力、Hessian来进行过渡态搜索、IRC、振动分析任务。类似地，只要自己写一个接口，也可以令Gaussian借用知名的、用户数目仅次于Gaussian的ORCA程序产生的这些信息来做这些任务，本文就介绍具体怎么实现。看本文前一定先把上文看了。顺带一提，ORCA是十分强大的量子化学程序，**北京科音高级量子化学培训班**（<http://www.keinsci.com/KAQC>）对ORCA有极其全面深入系统的讲解，希望完整学习ORCA并达到游刃有余的水平的话这个培训是绝对不容错过的！  
  
这种Gaussian与ORCA联用的做法可以带来以下好处：  
(1)可以令Gaussian做上述任务的时候支持ORCA才支持的理论方法，比如PBEh-3c、B97-3c、PWPB95-D3、NEVPT2、MRCI、DLPNO-CCSD(T)等。虽然其中有的理论方法并没有解析梯度，但原理上，我们可以通过自写脚本以有限差分方式得到Gaussian所需的梯度信息  
(2)虽然Gaussian支持的DFT泛函很广，速度也快，但是由于ORCA的RI做得十分出色，借用ORCA来产生能量和导数可以使得上述任务耗时更低，尤其是对于大体系、大基组而言  
(3)虽然ORCA也能直接做几何优化和找过渡态，但Gaussian在这方面算法上明显更成熟、更稳健，选项也更丰富、更易用  
(4)ORCA目前没有IRC功能，和Gaussian联用使得ORCA中的理论方法也可以用来产生IRC  
(5)使得ORCA产生的Hessian所对应的振动模式能够通过gview来观看  
  
实际上，ORCA有个关键词ExtOpt，即在ORCA优化过程中通过外部文件读入能量、导数信息，这和Gaussian的external关键词颇为相似，但ORCA的optimizer的算法跟Gaussian比还是有差距，而且也只能用来优化，所以没太大意义。  
  
本文使用Gaussian 09 E.01版，ORCA是4.0.1.2版，系统是CentOS 7.2。本文涉及的所有文件都可以在此处下载： <http://sobereva.com/attach/422/gau_orca.zip>

如果大家的实际研究中使用了本文的接口，请这样引用：Tian Lu, gau_orca: A Gaussian interface for ORCA program, <http://sobereva.com/422> (accessed month day, year)

## 2 Gaussian与ORCA联用的external脚本的写法

文件包里的orca.sh就是笔者编写的接口脚本，Gaussian输入文件里写上external='./orca.sh'关键词就代表需要能量和导数信息的时候会调用当前目录下的orca.sh。下面解释一下此脚本的内容。  
  
脚本一开始的部分，需要由用户自己填写ORCA运行时候是几核并行、内存用多大，用什么计算级别，以及数值精度方面的设定，比如SCF收敛限、积分格点精度。为了导数计算准确，脚本默认带了tightscf。还要设ORCA可执行文件路径。这些信息都需要用户使用前根据实际情况修改  
#Set the number of parallel cores and maximum memory utilized by each core (MB)  
 nprocs=1  
 maxcore=1000  
 #Set calculation level  
 level="BLYP def2-svp def2/J"  
 #Set parameters for numerical aspects  
 numset="tightscf"  
 #ORCA executable path  
 orcapath="/sob/orca/orca"  
  
之后，用read命令从Gaussian自动产生的InputFile中读取原子数、需要的导数阶数、净电荷、自旋多重度到相应变量  
read atoms derivs charge spin < $2  
  
下面的语句判断当前任务要用的关键词。ORCA里面engrad（即energy+gradient）关键词和Gaussian里的force关键词等价，用来计算当前结构下能量和受力，并输出到当前目录下与输入文件同名的.engrad文件中。如果写上freq，则会计算Hessian并且输出到当前目录下与输入文件同名的.hess文件中。这俩文件都是文本文件。  
if [ $derivs == "2" ] ; then  
 task="engrad freq"  
 elif [ $derivs == "1" ] ; then  
 task="engrad"  
 fi  
  
之后产生ORCA输入文件mol.inp。由于从InputFile读过来的坐标单位是Bohr，所以用了BOHRS关键词。  
#Create ORCA input file  
 echo "Generating mol.inp"  
 cat >> mol.inp <<EOF  
 ! $level $numset $task BOHRS nopop  
 %pal nprocs $nprocs end  
 %maxcore $maxcore  
 * xyz $charge $spin  
 $(sed -n 2,$(($atoms+1))p < $2 | cut -c 1-72)  
 *  
 EOF  
值得一提的是，ORCA在计算上面语句产生的mol.inp的时候，会在当前目录下产生mol.gbw。ORCA默认是开启了autostart设定的，即如果计算时候发现当前目录下已经有了后缀为.gbw的与当前输入文件同名的文件，就会自动从中读取波函数作为初猜波函数。整个Gaussian任务在运行期间是把mol.gbw一直保留在当前目录的，因此如果Gaussian和ORCA联用做几何优化，ORCA在计算当前结构的时候会自动读取上一次运算时候产生的.gbw里的波函数当做初猜，这样一方面节约了计算时间（毕竟比重新产生的初猜好），另一方面有助于保持所处的电子态的连续性。（稍有Gaussian知识的人都知道，Gaussian做几何优化的时候，每一步的初猜用的就是上一步收敛的波函数，通过orca.sh将Gaussian与ORCA联用时也借助gbw文件同样发挥了这种效果）  
  
再往后是调用ORCA运行mol.inp  
#Run ORCA  
 echo "Running ORCA..."  
 $orcapath mol.inp > mol.out  
 echo "ORCA running finished!"  
  
下面通过笔者用Fortran自写的extorca程序从ORCA产生的.engrad和.hess文件中提取能量以及导数信息，写入到与$3参数对应的OutputFile文件中  
echo "Extracting data from ORCA outputs via extderi"  
 ./extorca $3 $atoms $derivs  
extorca的源程序是extorca.f90，内容并不复杂，就不多说了。  
   
最后，orca.sh用以下命令清空ORCA运行中途产生的各种mol和mol_开头的文件以保持当前目录的清洁。但为了保留下来mol.gbw，用rm之前临时改了个名字。  
mv mol.gbw tmp.gbw -f  
 rm mol.* mol_* -f  
 mv tmp.gbw mol.gbw -f  
  
通过Gaussian与ORCA联用可以留下chk文件，但里面显然是没有波函数信息的，因此之后没法用Multiwfn等程序来看轨道、做波函数分析。不过，由于mol.gbw文件被保留了下来，这里面记录了ORCA计算最后一个结构时产生的波函数信息，因此可以转换为.molden格式，然后载入到Multiwfn里看轨道和做波函数分析。怎么把.gbw转换成.molden看《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）。  
  
  

## 3 实例：HCN->CNH异构化的过渡态搜索、振动分析以及IRC生成

在本文的压缩包的example目录里有HCN->CNH异构化的所有输入输出文件，用的是RI-BLYP/def2-SVP级别。由于这个体系非常小，用的计算级别也较低，因此实际上完全发挥不出借用ORCA计算能量和梯度的优势，反倒比纯粹用Gaussian还慢。而对于较大体系，ORCA仗着开挂般的RI，就完全不是同样的光景了。  
  
首先运行找过渡态的任务，要把TS.gjf、orca.sh、extorca三个文件都放到当前目录下，并且根据实际情况恰当修改orca.sh开头的变量，特别是ORCA的可执行文件路径。TS.gjf中的坐标是初猜的过渡态结构，文件前三行为  
%chk=TS.chk  
%nproc=1  
#P opt(nomicro,calcfc,ts,noeigen) external='./orca.sh'  
用诸如g09 < TS.gjf |tee TS.out运行即可。注意Gaussian用external功能时应当确保以串行方式计算，因此刻意写了%nproc=1，否则在通过orca.sh调用ORCA期间，Link401会有很高无意义的CPU占用。  
  
过渡态任务完成后，可以做振动分析检验有无虚频。对应的输入文件freq.gjf总共就三行，其它信息通过geom=allcheck从找过渡态后产生的TS.chk里读  
%chk=TS.chk  
%nproc=1  
# freq geom=allcheck external='./orca.sh'  
  
用gview观看输出文件freq.out，可确认有且只有一个虚频，振动模式正是期望的，虚频数值为1089.0cm-1。同样在BLYP/def2-SVP下，完全由Gaussian计算所给出的虚频为1088.4 cm-1，可见相符极好。  
  
最后来跑一下IRC，对应的输入文件IRC.gjf内容也只有以下三行。此任务从TS.chk里读取过渡态结构，由于用了%oldchk又避免了此任务改写TS.chk。  
%oldchk=TS.chk  
%nproc=1  
# IRC=calcfc geom=allcheck external='./orca.sh'  
  
读者可用gview打开IRC.out绘制IRC曲线图，可以看到曲线很光滑，而且IRC轨迹正常，证明Gaussian和ORCA联用非常成功。
