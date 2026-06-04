---
post_id: 307
title: molpro2010的编译方法
url: http://sobereva.com/307
date: '2015-10-23T05:31:00+08:00'
source_categories:
- 量子化学
primary_topic: Molpro
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 内容是Molpro的编译安装方法，属于软件使用教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**molpro2010的编译方法**  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)  2015-Oct-23

  
  
  
Intel i7-2630QM CPU，RHEL6U1 64bit系统，root用户。安装到/sob/molpro2010.1下。MKL库是以前安装Intel fortran & C compiler 12.1.0时的包里面带的（但这个不是必须的）。本想用ifort+icc编译，结果运行不正常（可能intel编译器版本太新），于是本文用系统自带的gcc+gfortran编译。  
  
本文提供的是最简单的编译方法，步骤最大程度精简。  
  
  

**============= 并行版本的编译 =============**

  
解压molpro2010.1包，产生/sob/molpro2010.1目录，进入此目录，运行  
./configure -mpp -auto-openmpi -gcc -gfortran  
会看到提示已经识别了编译器以及MKL库。所有的提示都按回车用默认（安装目标的路径依实际情况输入）。程序会自动下载openmpi-1.4.3到/root/.molpro/cache/openmpi-1.4.3.tar.gz，并自动解压、进行编译，产生到src/openmpi-install目录。（如果机子没联网，可以自行获取openmpi压缩包并放到那个目录，程序会直接自动使用）  
  
开始编译：  
make -j  
大约8分钟编译完毕。如果编译完毕后提示输入username，直接Ctrl+C中断掉。（如果需要在其它选项下重新编译，可以先用make veryclean清掉编译生成的文件，然后再重做以上步骤）  
  
把license文件token改为.token放到/sob/molpro2010.1/lib目录下  
  
然后然后进行测试：  
make MOLPRO_OPTIONS=-n4 quicktest  
代表用4核进行快速测试。几分钟，所有测试悉数通过。全面测试需要用把quicktest改为test。  
  
在自己目录下的.bashrc中加入  
export PATH=$PATH:/sob/molpro2010.1/bin  
再把默认运行参数设定为环境变量，比如以下设定让运行时自动用四核、不自动备份同名老文件、运行后不生成.xml文件、分配6400MB内存：  
export MOLPRO_OPTIONS="-n 4 -s --no-xml-output -m 800m"  
  
输入bash或重新打开shell使以上环境变量生效，然后我们可以用个小例子测试是否运行正常。把以下内容写为h2co.inp：  
geometry={  
4  
test  
 C                  0.00000000    0.00000000   -0.56221066  
 H                  0.00000000   -0.92444767   -1.10110537  
 H                 -0.00000000    0.92444767   -1.10110537  
 O                  0.00000000    0.00000000    0.69618930  
}  
  
basis=cc-pvtz  
hf  
ccsd(T)  
  
然后在其所在目录下运行molpro h2co.inp，看看输出的h2co.out内容是否正常。  
  
  
  

**============= 串行版本的编译 =============**

  
把并行编译的相应步骤替换为以下即可  
./configure -gcc -gfortran  
make -j  
make quicktest  
  
  
  
PS 1：molpro程序结果观看程序molproView的安装和使用见<http://sobereva.com/70>。  
PS 2：基于Molpro产生的.molden文件，可以通过Multiwfn极为方便地看结构、看轨道图形，以及做各种波函数分析，见《使用Multiwfn观看分子轨道》（<http://sobereva.com/269>）。  
PS 3：程序手册、quickstart等文档的pdf文件在压缩包的doc目录下。
