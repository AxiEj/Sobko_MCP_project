---
post_id: 409
title: root用户在用openmpi并行计算时避免加--allow-run-as-root的方法
url: http://sobereva.com/409
date: '2018-03-04T11:56:00+08:00'
source_categories:
- 其它
primary_topic: 其它软件
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章讨论OpenMPI在root用户下运行的技巧，属于科研软件运行经验。
topic_family: 软件
exclude_reason: ''
confidence: 0.86
image_count: 0
local_assets_dir: assets
---

**root用户在用openmpi并行计算时避免加--allow-run-as-root的方法**

Avoid adding --allow-run-as-root when root user employs OpenMPI for parallel computing

文/Sobereva @[北京科音](http://www.keinsci.com)   2018-Mar-4

OpenMPI从2.0开始有个变态要求，即如果用户是root，则通过mpirun来并行运行程序时，会提示  
mpirun has detected an attempt to run as root.  
Running at root is *strongly* discouraged as any mistake (e.g., in  
defining TMPDIR) or bug can result in catastrophic damage to the OS  
file system, leaving your system in an unusable state.  
然后不给算。如果非要算的话，必须mpirun命令带上--allow-run-as-root参数。这个设计在我来看极其讨厌、多管闲事！我在自己机子上从来都是用root账户，因为没权限限制，畅通无阻。只要我还没有变得脑痴，根本不会因为用了root而把系统搞坏。  
  
对于某些程序，要想避免每次运行时都手动加上--allow-run-as-root倒也不难，比如跑DIRAC程序，环境变量里设定export DIRAC_MPI_COMMAND="mpirun -np 36 --allow-run-as-root"就完了。但是有些程序解决起来没这么简单，比如ORCA就是，在.bashrc里添加alias mpirun='mpirun --allow-run-as-root'或alias orca='orca --allow-run-as-root'也都不行。  
  
为了彻底去掉OpenMPI变态的要求，干脆直接改源码。洒家发现这很简单：在编译openmpi之前，分别修改openmpi目录下的  
orte/tools/orte-dvm/orte-dvm.c  
orte/tools/orte-submit/orte-submit.c（对于OpenMPI 3.x是orte/orted/orted_submit.c）  
orte/tools/orterun/orterun.c  
在里面都搜索if (0 == geteuid，将对应段落（一直到这个if对应的}符号为止）删掉，然后编译，OpenMPI就不会因为发现是root还没用--allow-run-as-root而报错退出了。

**2020-May-6后记**：从OpenMPI 4.0开始，可以通过如下方式定义两个环境变量来允许root下也可以用mpirun，因此就不必像上文那样改源代码了。  
export OMPI_ALLOW_RUN_AS_ROOT=1  
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
