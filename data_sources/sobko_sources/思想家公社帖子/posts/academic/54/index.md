---
post_id: 54
title: 计算不同z位置水能形成氢键数的VMD Tcl脚本
url: http://sobereva.com/54
date: '2015-06-07T23:43:00+08:00'
source_categories:
- VMD
primary_topic: VMD
secondary_topics:
- 分子动力学
- 弱相互作用
academic_relevant: true
classification_reason: 主要是 VMD Tcl 脚本，用于计算不同 z 位置水的氢键数。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**计算不同z位置水能形成氢键数的VMD Tcl脚本**VMD Tcl script to calculate the number of hydrogen bonds that water can form at different z positions  
  
文/Sobereva@[北京科音](http://www.keinsci.com)   2009-Nov-8

  
  
有人请我写一个计算垂直于溶液界面的即不同z值处的水能形成氢键数的脚本，下面是我的VMD Tcl脚本，或许有人也用得着。如果你不懂VMD tcl脚本的编写，想完全读懂此脚本，并能随心所欲写出类似的分析脚本，非常推荐参加笔者讲授的**北京科音分子动力学与GROMACS培训班**（<http://www.keinsci.com/KGMX>），里面专门有一节“VMD分析脚本的编写”极其详细讲授了分析脚本编写所需要的一切知识，并给出了巨量我写的面向不同目的的脚本作为例子并给出了详细解释。  
  
氢键判据用的是常用的35度3.5埃的几何判据，当然也可以直接在脚本里改。计算方法是，只要有水分子有一个原子在某一层里，则这个水分子就认为属于这一层的水。对于每一帧，计算属于每一层的水selin与其它物质selbig之间的氢键数，氢键包括了这一层中的水作为氢键受体和供体两种情况，其数目分别为代码中的变量a和b。并且加上这一层水内部之间的氢键数（变量c）的2倍。a+b+2c除以这一层的水数，作为这一帧这一层的每个水的平均氢键数。脚本中循环轨迹中的每一帧，最终得到这一层平均氢键数。nonum变量记录有多少帧在所设定的范围里没有水，这些帧不计算。#后面那行用于调试目的，要考察每帧结果就去掉开头的#。  
  
首先运行下面的脚本，来加载实现这个功能的子程序   
proc numhbavg {sel fps1 fps2} {   
 set selin [atomselect top $sel]   
 set selbig [atomselect top "same resid as exwithin 3.5 of $sel"]   
 set k 0.0   
 set nonum 0   
 for {set i $fps1} {$i<=$fps2} {incr i} {   
 $selin frame $i   
 $selin update   
 $selbig frame $i   
 $selbig update   
 if {[$selin num]!=0} {  
 set a [llength [lindex [measure hbonds 3.5 35 $selbig $selin] 0]]   
 set b [llength [lindex [measure hbonds 3.5 35 $selin $selbig] 0]]   
 set c [llength [lindex [measure hbonds 3.5 35 $selin] 0]]   
 set k [expr $k+($a+$b+2*$c)*3.0/[$selin num]]  
 #puts "fps:$i $a+$b+[expr 2*$c] num_water:[expr [$selin num]/3.0] avg:[expr $k+($a+$b+2*$c)*3.0/[$selin num]]"   
 } else {incr nonum}   
 }   
 if {[expr $fps2-$fps1+1]==$nonum} {return "no result"}   
 return [expr $k/[expr $fps2-$fps1+1-$nonum]]   
 }   
  
然后下面的循环会调用这个子程序来输出每一层的平均氢键数，这里假设要计算z=4.0~5.6埃的数据，间隔为0.1埃，且限定20<x<40，20<y<40，每计算完一层输出一次。计算结果是帧数范围为100~150内的平均值。注意x/y/z的上下限范围不要恰顶着体系的边界，最好至少留出5埃的距离。选择范围中resname SOL代表了水。  
  
for {set i 40} {$i<=55} {incr i} {   
 set k [expr $i*0.1]   
 set now [numhbavg "same resid as resname SOL and x<40 and x>20 and y<40 and y>20 and z<[expr $k+0.1] and z>=$k" 100 150]   
 puts [format "%4.2f %4.2f %5.3f" $k [expr $k+0.1] $now]   
 }   
  
我这里随便算一个主要由水构成的普通的体系，水形成的氢键数大概在3.1左右，标准放宽到4.0埃，40度，则可形成氢键数约为3.6。在冰中由于结构十分有序，可形成4个氢键，在液态情况下分子的动能必然造成氢键的破坏，所以结果是很合理的。   
帧数范围越大、xy平面越大计算越慢，这个脚本计算速度比较慢，不要一下将范围设得太大。  
  
输出结果如下，前两列代表统计的z值范围，第三列是水的平均氢键数  
  
4.00 4.10 3.015  
4.10 4.20 3.161  
4.20 4.30 3.201  
4.30 4.40 3.159  
4.40 4.50 3.237  
4.50 4.60 3.130  
4.60 4.70 3.201  
4.70 4.80 3.338  
4.80 4.90 3.201  
4.90 5.00 3.041  
5.00 5.10 3.122  
5.10 5.20 3.182  
5.20 5.30 3.160  
5.30 5.40 3.309  
5.40 5.50 3.189  
5.50 5.60 3.327
