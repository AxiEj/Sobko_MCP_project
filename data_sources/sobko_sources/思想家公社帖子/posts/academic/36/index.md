---
post_id: 36
title: 使VMD实时显示gromacs轨迹中原子的受力
url: http://sobereva.com/36
date: '2015-06-05T00:49:00+08:00'
source_categories:
- VMD
primary_topic: VMD
secondary_topics:
- GROMACS
- 分子动力学
- 可视化
- 结构与文件格式
academic_relevant: true
classification_reason: 核心是用VMD脚本读取GROMACS轨迹力信息并实时显示，主题非常明确。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**使VMD实时显示gromacs轨迹中原子的受力**Making VMD show the atomic forces in GROMACS trajectory in real time

文/Sobereva@[北京科音](http://www.keinsci.com)   2009-Jan-31

显示原子受力有时很重要，但实现起来又是个麻烦事。由于这两天要用这个功能，所以写了一个VMD的tcl脚本，可以用箭头显示指定原子的受力，并且随进度条拖动实时更新，在这里做一下介绍。  
  
VMD当前版本并不读取轨迹中的力，不能在内部直接调用，所以需要手动把轨迹中的力提取出来并读入VMD。在此例中，我们要分析序号为977的原子的受力，序号由0开始算。  
  
  
这里用到一个技巧，结合gmxdump和grep可以容易地从.trr文件中提取977号原子受力，虽然比较慢，但是很方便：  
gmxdump -f all.trr |grep "f.  977" > force.txt   
包含f[  977]的行就被提取出来了。force.txt内容如下：  
      f[  977]={ 1.02676e+03, -1.37174e+03,  1.29441e+03}  
      f[  977]={ 5.54416e+01,  9.32820e+02, -7.47177e+02}  
      f[  977]={ 7.87461e+02,  7.43057e+02, -9.03874e+02}  
      f[  977]={ 1.52381e+02, -5.37775e+02,  1.38345e+02}  
      f[  977]={-6.90852e+02, -1.33539e+02, -9.30110e+02}  
......  
应当注意，为了使每一行都对应一帧结构，.mdp的nstxout和nstfout应当相同。（最后一帧未必，因为最后一步的结构不管怎么设nstxout都会被输出，而这一帧未必会正好是输出力的那步，但这个问题无关紧要）  
  
把force.txt放到tcl启动后的默认文件夹（比如d:\study\vmd186，在控制台输入pwd可显示），启动vmd，载入轨迹，在控制台运行：  
set i 0;set fx 0;set fy 0;set fz 0  
set force [open force.txt r]  
while {[gets $force line] >= 0} {           //检测何时停止循环读取  
scan [string range $line 16 55] "%f,%f,%f" fx fy fz       //把force.txt的每行读入并只保留a,b,c的形式，赋值到fx fy fz  
set f(x$i) $fx;set f(y$i) $fy;set f(z$i) $fz    //赋值到数组  
incr i  
}  
close $force  
我们已将全部受力读入一个数组f，例如f(x43)代表第43帧时977号原子受力的x分量。  
  
然后运行下面的内容，定义一个名为showforce的过程，用于绘制箭头  
proc showforce {args} {  
global vmd_frame  
global f  
global atom         //引用全局变量  
graphics 0 delete all      //清空已绘制的物体  
set sel [atomselect top "index $atom" frame $vmd_frame(0)]  
set x [$sel get x]  
set y [$sel get y]  
set z [$sel get z]        //得到$atom原子当前帧的坐标  
set init "$x $y $z"       //箭头尾巴坐标  
set middle "[expr $x+$f(x$vmd_frame(0))/400] [expr $y+$f(y$vmd_frame(0))/400] [expr $z+$f(z$vmd_frame(0))/400]"    //箭头锥形和柱形衔接处坐标  
set after "[expr $x+$f(x$vmd_frame(0))/300] [expr $y+$f(y$vmd_frame(0))/300] [expr $z+$f(z$vmd_frame(0))/300]"    //箭头头部坐标  
graphics 0 color red  
graphics 0 cylinder $init $middle radius 0.3 filled yes resolution 20 //绘制圆柱  
graphics 0 cone $middle $after radius 1.3 resolution 20  //绘制锥形  
$sel delete       //释放atomselect所占用的内存  
}  
  
运行：  
trace variable vmd_frame(0) w showforce  
说明跟踪vmd_frame(0)变量，这个变量每当ID为0的分子的进度条移动后都会更新，内容是当前帧号。此时便触发showforce过程根据此帧的受力来重绘箭头。  
  
最后定义要显示哪个原子受力，在此例中运行set atom 977  
拖动进度条，就可以看到效果了，如图所示的红箭头，箭头的长度与受力大小成正比。  
  
  
如果不想显示了，只需输入  
trace vdelete vmd_frame(0) w showforce  
graphics 0 delete all  
如果又想显示，仍然是运行trace variable vmd_frame(0) w showforce  
  
  
为了方便，我将上述内容写进了showforce.tcl脚本。简要来说使用方法如下：  
1. 将force.txt和showforce.tcl放入VMD默认文件夹  
2. 启动VMD，载入轨迹  
3. 在控制台运行source showforce.tcl  
4. set atom 977  
即可。  
  
  
  
showforce.tcl文件内容如下  
  
set i 0;set fx 0;set fy 0;set fz 0  
set force [open force.txt r]  
while {[gets $force line] >= 0} {  
scan [string range $line 16 55] "%f,%f,%f" fx fy fz  
set f(x$i) $fx;set f(y$i) $fy;set f(z$i) $fz  
incr i  
}  
close $force  
  
  
proc showforce {args} {  
global vmd_frame  
global f  
global atom  
graphics 0 delete all  
set sel [atomselect top "index $atom" frame $vmd_frame(0)]  
set x [$sel get x]  
set y [$sel get y]  
set z [$sel get z]  
set init "$x $y $z"  
set middle "[expr $x+$f(x$vmd_frame(0))/400] [expr $y+$f(y$vmd_frame(0))/400] [expr $z+$f(z$vmd_frame(0))/400]"  
set after "[expr $x+$f(x$vmd_frame(0))/300] [expr $y+$f(y$vmd_frame(0))/300] [expr $z+$f(z$vmd_frame(0))/300]"  
graphics 0 color red  
graphics 0 cylinder $init $middle radius 0.3 filled yes resolution 20  
graphics 0 cone $middle $after radius 1.0 resolution 20  
$sel delete  
}  
  
trace variable vmd_frame(0) w showforce  
  
  
PS：还可将此脚本改写，显示每一帧某原子的速度。
