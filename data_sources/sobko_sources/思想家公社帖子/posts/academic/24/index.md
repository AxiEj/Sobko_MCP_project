---
post_id: 24
title: Gromacs 4杂谈
url: http://sobereva.com/24
date: '2015-06-04T23:09:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 分子动力学
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章围绕GROMACS 4的新特性杂谈，核心仍是软件与分子动力学工作流。
topic_family: 软件
exclude_reason: ''
confidence: 0.94
image_count: 0
local_assets_dir: assets
---

**Gromacs 4杂谈**

Miscellaneous talk on Gromacs 4

文/Sobereva @[北京科音](http://www.keinsci.com/)   写于约2008年

  
  
随便谈谈gromacs4。  
  
新支持仅xy方向的PBC，以前版本实现二维周期边界条件只能靠那个方向增加很厚的真空层来实现。可以与WALL组合使用（WALL也只能用于二维周期边界条件）。nwall设2就是在box的z值位置上加两个wall，此时可以用控压和ewald相关静电加和方法。设1就是z=0上一个wall。  
  
新支持周期性分子。  
  
pull代码作了完全改写，以前的ppa文件不能用了，而是在mdp里面设。  
  
grompp去除了-np设置，也就是不用事先指定tpr在各个节点上的负载怎么分配，在mdrun时候默认是使用域分解方法均衡负载，这样并行或是串行都可以用一个tpr了，很方便。用法还是mpirun -np 4 mdrun....同时grompp也去掉了shuffle和sort选项，对于默认的域分解方法已经没用了。在某些情况下不能用域分解，比如pbc=xy，界时还得用-pd (particle decomposition)  
  
新加了个checkpoint设计，默认每隔15分钟更新一个.cpt。有一些好处。mdrun的时候用-cpt调整多长时间写一次，-1就是不写cpt。每个新的.cpt生成之后会把老的.cpt改名为_prev.cpt的后缀，再之前的.cpt就删了。这个cpt里面包含了速度、坐标、能量，文件并不大，只需要有这个.cpt，断的工作就可以完整继续，比如mdrun用-cpo参数设的checkpoint文件名是sdf.cpt，mdrun -v -deffnm a-sol-md4 -cpi sdf就可以继续了，会接着checkpoint位置算直到预定时间，生成新的末尾是part0002的trr/log/edr。以前要继续算必须用trjconv，trr轨迹得读一遍生成新的.tpr，而且继续开始时间受制于.trr里面的一些东西的保存频率。  
  
令我不太舒服的是mdrun的-v选项开了之后默认是每100步输出一次剩余时间和当前步数，以往是10步输出一次。  
  
mdrun有了-pforce，可以设定受力大于多少的原子被打印出来。  
  
目前的版本开了-enable-fortran选项会编译不过去，解决方法是  
把src/gmxlib/libxdrf.c的第1156行#define XDR_INT_SIZE 4挪到第68行，即在#ifdef GMX_FORTRAN之前。  
  
  
gmx4最主要的改进是并行效率问题，这是gmx最大诟病。我对此进行了详细的测试，体系是gmxbench里面d.dppc，包含12万个原子，5000步，是个磷脂膜体系。把库仑作用改成了PME，其它没变。测试平台Q6600 oc 3.2，ifort，gcc，mpich2，编译方法完全一致，优化参数全开。  
下面pc的p代表parallel，没p就是串行版本。pc的c代表没开-enable-fortran，f代表开了。  
  
  
不知道是什么原因，可能是有个体特异性，不开-enable-fortran，gmx4并行效能反到不如gmx3.3.3开了shuffle，当然比不开shuffle还是强很多。很多人感觉gmx4并行效率大增，实际上是有些人不知道以前gmx应该开-shuffle -sort！gmx4对均衡负载很注重，在跑的时候加了-v还会输出imbalance的情况(imb)。  
  
注意一点，mdrun的时候开-dlb yes可以使imb也就是不均衡负载降低，在我的Q6600上，可以看到输出的imb由4%降到了1%以下，性能能提高约3%。默认是auto，似乎是没开，和-dlb no差不多。dlb只能用于-dd，也就是默认的域分解。对不均匀体系应该更好。  
  
但是gmx4并行版本如果用了-enable-fortran，性能激变，竟达到gmx3.3.3默认方式并行的3/2。  
  
对于串行版本，奇怪的是gmx4比gmx3.3.3还慢（在A64 3000+上gmx4却比gmx3.3.3略快），但开了-enable-fortran后，gmx3.3.3长进不大，无论是并行还是串行。gmx4却获益非浅，超过gmx3.3.3+fortran，尤其是并行速度，达到了新高。  
  

总之对于具体体系和具体配置得到的数据还不能说明问题，而且因为条件所限没法试gmx4集群性能，但是我至少做出倡议：用gmx4要用-enable-fortran。用gmx3.3.x最好用-enable-fortran，并行计算一定要在grompp时设-shuffle -sort，开-dlb yes

PME gmx4 pc -np 4  
                NODE (s)   Real (s)      (%)  
        Time:    802.000    802.000    100.0  
                        13:22  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     44.139      8.466      1.077     22.278  
  
 PME gmx4 pf -np 4  
                NODE (s)   Real (s)      (%)  
        Time:    611.000    611.000    100.0  
                        10:11  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     57.991     11.109      1.414     16.972  
  
 PME gmx3.3.3 pc -np 4  
               NODE (s)   Real (s)      (%)  
        Time:    902.000    902.000    100.0  
                        15:02  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     38.744      8.223      0.958     25.056  
  
 PME gmx3.3.3 pf -np 4  
                NODE (s)   Real (s)      (%)  
        Time:    880.000    880.000    100.0  
                        14:40  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     39.710      8.428      0.982     24.444  
  
 PME gmx3.3.3 pc -np 4 -shuffle  
                NODE (s)   Real (s)      (%)  
        Time:    750.000    750.000    100.0  
                        12:30  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     46.687      9.891      1.152     20.833  
  
 PME gmx3.3.3 pf -np 4 -shuffle  
                NODE (s)   Real (s)      (%)  
        Time:    737.000    737.000    100.0  
                        12:17  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     47.498     10.063      1.172     20.472  
  
 PME gmx3.3.3 pc -np 4 -sort  
                NODE (s)   Real (s)      (%)  
        Time:    901.000    901.000    100.0  
                        15:01  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     38.787      8.232      0.959     25.028  
  
 PME gmx3.3.3 pc -np 4 -sort -shuffle  
                NODE (s)   Real (s)      (%)  
        Time:    724.000    724.000    100.0  
                        12:04  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     54.572     10.250      1.193     20.111  
  
 =================serial version comparion  
  
 PME gmx4 c  
                NODE (s)   Real (s)      (%)  
        Time:   2824.000   2824.000    100.0  
                        47:04  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     12.380      2.449      0.306     78.444  
  
 PME gmx4 f  
                NODE (s)   Real (s)      (%)  
        Time:   1975.000   1975.000    100.0  
                        32:55  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     17.695      3.440      0.437     54.861  
  
 PME gmx3.3.3 c  
                NODE (s)   Real (s)      (%)  
        Time:   2143.480   2144.000    100.0  
                        35:43  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     16.305      3.119      0.403     59.541  
  
 PME gmx3.3.3 f  
                NODE (s)   Real (s)      (%)  
        Time:   2109.680   2109.000    100.0  
                        35:09  
                (Mnbf/s)   (GFlops)   (ns/day)  (hour/ns)  
 Performance:     16.574      3.170      0.410     58.602
