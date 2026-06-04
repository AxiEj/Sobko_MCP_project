---
post_id: 32
title: 原子-残基B因子/rmsf转换小工具ba2r
url: http://sobereva.com/32
date: '2015-06-05T00:26:00+08:00'
source_categories:
- 分子模拟
primary_topic: 其它软件
secondary_topics:
- GROMACS
- 结构与文件格式
academic_relevant: true
classification_reason: 这是自制的ba2r转换工具，围绕PDB/B因子/RMSF和GROMACS输出格式处理。
topic_family: 软件
exclude_reason: ''
confidence: 0.92
image_count: 0
local_assets_dir: assets
---

**原子-残基B因子/RMSF转换小工具ba2r**  
ba2r: Atom-residue B factor/RMSF conversion tool

文/Sobereva@[北京科音](http://www.keinsci.com)

文献一般都是比较残基的B因子或者RMSF，而一般算出来的都是原子的B因子或者RMSF，寡人写的这个ba2r工具就是用来将它们转换的，ba2r会输出残基号和残基B因子/RMSF两列内容，方便作图。输入的pdb不需要做任何修改，带着各种注释性的文字无妨，会自动跳过去。

ba2r下载地址<http://sobereva.com/soft/ba2r.rar>

B因子转换为RMSF的公式为RMSF^2=B*3/8/pi^2，参见*Biochemistry*, **48**, 7986–7995 (2009) DOI: 10.1021/bi900811p（文中搜RMSF可找到），**大家用这个程序的时候可以引用此文章**。

软件的Readme：

此软件有三个功能  
1.将pdb中的原子B因子转换为残基B因子（原子B因子取平均）  
2.将gmx rmsf输出的或者此软件第3个功能输出的原子RMSF的.xvg转换为残基的RMSF（原子RMSF取平均）  
3.将蛋白质原子B因子转换为原子的RMSF

运行后首先输入选择哪个功能，然后输入文件名，例如D:\study\sob.pdb，处理完的结果存于程序当前目录下。输出的文件名见提示。

pdb中的B因子单位都是埃^2，RMSF的单位都是nm

第一个和第三个功能需要输入pdb文件。第二个功能需要输入pdb文件和原子的RMSF文件，两个文件内容需要对应，pdb用来判断出哪些原子属于哪些残基。

例如，将1.pdb的B因子转化为残基的RMSF。首先用第3个功能得到其原子的RMSF文件rmsf-atomic.txt，再选择第2个功能，分别输入1.pdb和rmsf-atomic.txt即可得到rmsf-residue.txt。

输入的pdb不必事先手动处理，不必删掉开头或者TER，会自动选择读取其中有用内容。  
输入的.xvg如果来自GROMACS的gmx rmsf，开头的内容也无需手动删掉，会自动略过。

有问题请联系寡人sobereva[at]sina.com。
