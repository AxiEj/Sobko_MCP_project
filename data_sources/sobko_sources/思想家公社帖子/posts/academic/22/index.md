---
post_id: 22
title: gromacs和amber处理环肽的办法
url: http://sobereva.com/22
date: '2015-06-02T21:43:00+08:00'
source_categories:
- 分子模拟
primary_topic: AMBER
secondary_topics:
- GROMACS
- 结构与文件格式
academic_relevant: true
classification_reason: 文章讲GROMACS和AMBER处理环肽的办法，AMBER部分更具体。
topic_family: 软件
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**gromacs和amber处理环肽的办法**The way of dealing with cyclic peptides in GROMACS and AMBER   
  
文/Sobereva @[北京科音](http://www.keinsci.com/)   写于约2008年

  
  
环肽的模拟其实和直链肽没有区别，只是环肽首尾相接，在读入gmx和amber时需要做一些处理，否则会被当作N端和C端残基自动进行特殊处理，而我们的目的就是让pdb两端的氨基酸被程序当成普通的处于中端的氨基酸残基来处理，这样使环中的每个氨基酸都没有特殊性。  
  
在amber的leap中，读如氨基酸库之后，用list可以看到N打头和C打头的一批氨基酸unit，分别是N端和C端的氨基酸。这种带前缀的氨基酸和普通氨基酸残基有一些不同，N打头的比普通残基多了氨基的两个氢，C打头的多了一个羧基氧。如果直接读入环肽，自动将pdb开头的氨基酸当作带N开头的氨基酸，加上两个氢，结尾的当作C开头的氨基酸，加上氧，而加入的这些并非我们所需。而且库文件中这种端基氨基酸的原子类型和电荷与处于中间的氨基酸残基不同，一个个手动改成普通中段氨基酸太麻烦。  
  
对这个问题，可以使用loadpdbusingseq，使读取pdb的时候每个残基都按照所设残基为参照来读取。  
  
例如  
  
temp={ARG ARG TYR TYR ALA PHR}        //此为此环肽pdb中的序列  
b=loadpdbusingseq /sob/t/cycli/cycli.pdb temp  
bond b.1.N b.6.C         //将pdb开头的氨基酸和pdb末尾的氨基酸连成肽键  
  
之后按照常规方法添加电荷、溶剂，并进行模拟。  
  

---

  
Gromacs中，对端基氨基酸处理方式是在力场中定义处理氨基和羧基的方式，但没有把端基氨基酸专门设定为特殊的残基从而赋予与中段氨基酸不同的原子类型和电荷。  
  
比如ffG43a1，在top目录下存在ffG43a1p-n.tdb和ffG43a1p-c.tdb，从中可见几种处理方法，比如[NH3+]下面描述了对于N端的残基，删掉哪些原子，添加哪些原子，替换哪些原子。默认情况下，用的是[NH3+]和[COO-]  
  
如果在pdb2gmx的时候加上-ter，可以手动指定端基氨基酸的处理方式，比如N端氨基可设为[NH2] [NH3+] [none]。设none的话，就什么都不动。  
  
为了不让pdb2gmx给环肽pdb开头和结尾的氨基酸添上多余的东西，所以N端和C端氨基酸都选none。  
  
若pdb中本来没有氢，或者有氢但为了用联合原子力场而开了-ignh选项，又选了none，头尾氨基酸相连的肽键就没有氢了。这种情况下需要简单修改ffG43a1p-n.tdb，加上：  
  
[cycliN]  
  
[add]  
  
1 4 H N CA C  
  
  H 1.008 0.28  
  
注意gmx与amber不同，不同氨基酸的肽键上的氢的电荷都是0.28，故这个设置对所有氨基酸都是通用的，不会造成总电荷不为整数。  
  
保存之后，上述情况下pdb2gmx时选择N端氨基酸时，选cycliN那项，就有氢了。  
  
然后在.top文件中，补上这个肽键的bond、angle、dihedral的信息即可。
