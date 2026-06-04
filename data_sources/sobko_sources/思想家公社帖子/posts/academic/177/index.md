---
post_id: 177
title: 让指定化学键平行于笛卡尔坐标轴的方法
url: http://sobereva.com/177
date: '2015-06-08T00:00:00+08:00'
source_categories:
- VMD
primary_topic: VMD
secondary_topics:
- 结构与文件格式
- 可视化
academic_relevant: true
classification_reason: 标题明确是用 VMD 让指定化学键平行于坐标轴，软件操作是主线。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**后记**：此文用VMD的做法已经没有意义了，用Multiwfn来实现方便得多！仔细看《Multiwfn中非常实用的几何操作和坐标变换功能介绍》（<http://sobereva.com/610>）中的介绍，特别是2.3节的例子。

**让指定化学键平行于笛卡尔坐标轴的方法**  
Method to make specific chemical bond parallel to a Cartesian coordinate axis

文/Sobereva@[北京科音](http://www.keinsci.com)  2013-Jan-27

见到好几次有人问怎么让指定的化学键平行于某个笛卡尔坐标轴。这里提供一个笔者写的VMD的Tcl脚本用于实现此目的。虽然也可以在一些分子可视化程序里拖动鼠标旋转分子来达成此目的，但是那样做所得坐标并不精确。

首先启动VMD，将分子结构文件载入，然后在控制台里将以下内容拷进去执行

proc alignbond {ind1 ind2} {  
set atm1 [atomselect top "serial $ind1"]  
set atm2 [atomselect top "serial $ind2"]  
set vecx [expr [$atm2 get x] - [$atm1 get x]]  
set vecy [expr [$atm2 get y] - [$atm1 get y]]  
set vecz [expr [$atm2 get z] - [$atm1 get z]]  
set sel [atomselect top all]  
$sel move [transvecinv "$vecx $vecy $vecz"]  
}

之后，比如想让4,9号原子对应的键平行于X轴，就在控制台输入alignbond 4 9，效果在图形窗口上可以立刻见到。之后，file-save coordinate保存为坐标文件即可。（这两个原子也可以没有实际成键，它们只用于定义连线的矢量而已）

若想让这个键平行于其它笛卡尔坐标轴，先用上述方法令这个键平行于X轴，然后执行  
set sel [atomselect top all]  
之后，比如输入$sel move [transaxis z 90]就可以让体系坐标绕着Z轴转动90度。z可以改成x和y来分别绕着x和y轴旋转。根据实际要求，令体系适当旋转即可达到目的。

PS：如果你是想让体系的某一个矢量平行于笛卡尔轴，看《让体系(跃迁)偶极矩平行于某个笛卡尔轴的方法》（<http://sobereva.com/507>）。
