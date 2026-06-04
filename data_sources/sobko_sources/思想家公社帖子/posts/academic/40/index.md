---
post_id: 40
title: Gromacs的pull code介绍(3.3.x+4.0.x)
url: http://sobereva.com/40
date: '2015-06-05T01:02:00+08:00'
source_categories:
- 分子模拟
primary_topic: GROMACS
secondary_topics:
- 分子动力学
academic_relevant: true
classification_reason: 主要介绍 GROMACS 的 pull code，属于分子动力学软件使用。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**Gromacs的pull code介绍(3.3.x+4.0.x)**Introduction to pull code of GROMACS (3.3.x+4.0.x)  
  
文/sobereva @[北京科音](http://www.keinsci.com)    2009-May-4

  
  

## Gromacs 3.3.x:

Pull Code有三种类型：AFM pulling,Umbrella sampling,constraint  
AFM是给原子一个外力，实际上是一个弹簧点在恒速远离，弹簧点拉动一组原子，其力取决于弹簧点与这组原子质心的距离和自己定义的力常数。类似amber的jar=1。  
比如A-------B=C   A是参考组，B是pull组，C是弹簧点。模拟开始后AC距离根据constraint_rate1的设定恒速增加，C的移动拉动B，B受C的力等于BC的距离乘以afm_k1。  
Constraint是保持两组原子质心间距离不变(用SHAKE算法实现)，监视它们之间的限制力  
Umbrella是给一组原子的质心加一个谐振势  
输入文件有-pi pull.ppa里面包含pull的控制代码。-pn index.ndx指定哪写原子组成哪些组。  
输出文件有-po pullout.ppa是形式化的输入文件的拷贝，也就是各种参数都写齐了的输入的.ppa，类似mdout.mdp。-pdo pull.pdo记录了pull的过程中的力、位置等的变化信息  
  
定义组的方法：  
com 每一步计算一次设定的组内原子的质心  
com_t0 每一步计算一次设定的组内原子的质心，但是对原子穿越盒子跑到另一侧导致质心位置突然变动这种现象进行校正  
dynamic 只有组内的在某个柱形空间范围内的才被当回事  
dynamic_t0 同com_t0与com的关系，做校正而已  
  
一般参数：  
verbose = 默认为no，如果设yes，会往.pdo里面多写一些东西，并通过stderr多输出一些东西。  
Skip steps = pdo里面每多少步输出一次结果，默认为1  
runtype = 可设afm,contraint,umbrella  
ngroups = 总共有多少组（不含参考组），最大可设20个  
group_1 = LT 设定第一个组  
group_2 =  
....  
reference_group = LTWD 设定参考组。定义的那些group_x与这个组的距离会被计算。比如得到两个粒子之间的constraint force，则一个定义为group_1一个定义为这个组。如果用AFM或umbrella并且不定义这个组，则外力是从绝对坐标而来。  
如果用了参考组，则pull组都是相对于参考组的坐标的，而体系质心不会因为pull了某个东西而平移，字面上看是参考组不动，实际上与pull组相反方向走。如果不定义参考组，pull组在绝对坐标中pull，如果此时设了comm_mode = none，就会导致体系质心也发生移动，若开了消平动，质心基本还是原处。  
weights_1 = pull组1的权重  
weights_2 = pull组2的权重  
reference_weights = 参考组的权重，权重对决定质心位置和相关原子受力有影响，见手册  
reftype = 参考组的类型，可以是com,com_t0,dynamic,dynamic_t0  
reflag = 1 参考组的位置由许多步取平均得到  
pulldim = N N Y 往哪个方向pull，这里是Z方向。默认都是Y。设了几个Y，在.pdo里面就会有几个维度，相对于一个Y时除了时间以外就有几倍列数的数据。不管afm_dir1怎么设的，这里是N的方向就被忽略。  
  
Dynamic参考组选项：  
r = 0 用的是dynamic/dynamic_t0类型参考组时，这个设柱形的半径  
rc = 0 在r至rc的范围内的粒子，权重为1至0。建议r=1，rc=1.5  
update = 1 多少步更新一次dynamic参考组  
  
当runtype=constraint时的参数：  
constraint_direction = 限制的方向，默认为0.0 0.0 0.0也就是没有方向，因此两个组之间的距离被限制住。  
constraint_distance1/constraint_distance2 = 最初的限制距离，默认是0，也就是根据初始坐标决定距离  
constraint_rate1 constraint_rate2 = 距离限制的变化速率，为nm/ps，默认为0  
constraint_tolerance = 距离限制的容忍限，也就是SHAKE的tolerance，默认1e-6  
  
当runtype=afm时的参数：  
例：不设参考组，afm_k1 = 1 -1.0 0，pulldim = N Y N，afm_rate1 = 0.5，不设afm_init1，则pull组会一直朝自己的y的负方向走，不主动向x方向走即便afm_dir1设了这个方向，虽然弹簧点的绝对坐标应该是0 -0.1 0，0 -0.2 0，0 -0.3 0这样变化从而也应该带动pull组的x和z接近0，但因为这两个方向都是N所以不会。但如果pulldim都设Y，则pull不仅y随弹簧点的y增大而增大，由于弹簧点的x和z一直都是0，x和z也逐渐趋近于0，pull组会追着从绝对坐标0点开始走的弹簧点。  
afm_rate1 afm_rate2 = 对于每个组的弹簧移动的速率(nm/ps)  
afm_k1 afm_k2 = 对于每个组的弹簧力常数(KJmol^-1*nm^-2)  
afm_dir1 afm_dir2 = 弹簧点移动的向量（相对于弹簧点当前位置），如果设了参考组，则参考组动时，弹簧点也随之动，保持相对位置不变。  
afm_init1 afm_init2 = 描述弹簧最初位置相对于参考组的向量。如果想让开始时的力为0，则弹簧初始位置必须设为pull组相对于参考组的值。  
  
当runtype=umbrella时的参数：  
umbrella给pull组施加谐振势来维持pull组相对于参考组的位置。如果参考组移动了，pull组也会随之移动。如果没有定义参考组，pull组就处于绝对坐标中，参考组被设为[0 0 0]。  
例如：不设参考组，pos1设0.0 5.0 0.0，当.pdo中的距离很小后，检查pull组的y值，应当很接近于5.0。相当于把pull组往某个坐标点拉。但是不能设得过大、离谱，否则预计与结果不符甚至被无视了。  
例如：设参考组，pos1设0.0 5.0 0.0，当.pdo中的距离很小后，检查pull组的y值和参考组的y值，其差应当很接近于5.0。动的时候参考组和pull组一起在对称地动，并非只动pull组。  
k1 k2 = 指定每个pull组的力常数(kJ*mol^-1*nm^-2)  
pos1 pos2 = 指定pull组被限制到的位置，此值是相对于参考组的。  
  
  
注：总的来说，umbrella和afm实际上是一样的，区别只是umbrella的弹簧点是不相对移动的（相当于afm_rate1=0，没有afm_dir1选项），afm的弹簧点是相对移动的。  
pull组始终是向着弹簧点坐标受力。pulldim控制这个力的哪些分量被表达出来。弹簧点的t=0位置(原始位置)都是这两项的矢量和：参考组(reference_group)+相对参考组的初始位置(afm_init1或pos1)。弹簧点是从原始位置开始根据afm_dir移动。如果参考组不是固定的坐标而是一个组，则这个组的位置变化会加到弹簧点上。  
==========  
输出结果  
时间都是ps，位置都是nm  
对于Constraint，如10.5 -81.2，分别代表时间和限制力，负数说明pull组与参考组相互吸引。  
对于AFM，如10.5 3.5 3.63 3.6，分别代表时间，参考组的位置，pull组的位置，弹簧的位置。只有pulldim设为Y的维度的结果才会被输出。pull组与参考组距离之差的变化与afm_rate相等  
对于Umbrella，如10.5 0.002，分别代表时间和pull组相对于其限定的位置。  
  
  
其它：如果跑起来没多久就出现一堆东西，提示write pdb之类，说明体系崩了，就把力常数设小点。并且检查是否拉伸过程合理，比如拉伸过程中是否出现过度碰撞、挤压。  
  
  

## Gromacs 4:

gromacs4中，pull代码进行了重写，参数定义从pull文件改为了.mdp中定义。拉伸的三种方式也有所变化，把afm和umbrella合并为umbrella（因为本质一样），新增加了常力拉伸(constant_force)，即外加力大小一直不变。  
pull_vec1和pull_init1的格式是例如：1.0 2.0 3.0。  
主要参数对应关系：3.3 vs 4.0  
runtype=pull  
pulldim=pull_dim  
reference_group=pull_group0 (下文中参考组指的就是pull_group0)  
group_1=pull_group1  group_2=pull_group2......  
pos1/afm_init1=pull_init1 (与pull_geometry有关)  
afm_dir1=pull_vec1 (与pull_geometry有关)  
afm_rate1=pull_rate1  
ngroups=pull_ngroups (二者数目皆不包含group0)  
k1/afm_k1=pull_k1  
  
4.0多了个pull_geometry选项。包含position、distance、direction、cylinder四种模式，这里只讨论前三种。  
======================  
使用pull=umbrella结合这三种模式的情况：  
  
position模式(重点)：等价于3.3.3的afm，即弹簧点位置是参考组位置+pull_init+time*pull_rate*pull_vec，朝着弹簧点拉。如果将pull_rate1设为0，则相当于弹簧点位置不变，就等价于3.3.3版本中的umbrella。  
  
distance模式：始终顺着连接参考组与pull组向量的方向拉。用这种模式时弹簧点只会在参考组与pull组连线方向上移动。pull_init1只能设一个数而不是坐标，这个数就是弹簧点t=0时在这个连线方向上与参考组的距离。pull_rate1是弹簧点在连线方向上的移动速度，逐渐离近还是逐渐远离可以通过此值的正负号来控制。pull_vec1对弹簧点运动方向无任何影响。  
  
direction模式：定义一个过pull组在t=0时坐标的向量，pull_vec1方向。pull_init只能设一个数而不是坐标。设参考组在这个向量上投影点是P，则弹簧点的位置是P+pull_init*uni(pull_vec)+time*pull_rate1*pull_vec1。uni()代表求单位向量。  
  
上述都是假设参考组是绝对坐标或者固定住参考组，如果参考组在拉伸过程中位置变化，弹簧点位置也相应变化。  
======================  
使用pull=constraint结合这三种模式的情况和umbrella一样，区别只是将pull组位置用约束算法固定在弹簧点位置上，而不是被弹簧点拉着走。比较常用的是distance模式，这个模式可使参考组与pull组之间的距离固定保持不变(即pull_init1)或者刻意让其逐渐改变(即pull_init1+time*pull_rate1)，而它们之间的相对角度方位可随意变化。  
======================  
使用pull=constant_force结合这三种模式的情况：  
注意，拉力大小始终不变，为pull_k1。无论哪种模式皆没有弹簧点的概念，故pull_rate1、pull_init1对结果皆无影响。  
  
position模式：pull组由t=0时的位置向-1,-1,-1方向拉（不是指朝着(-1,-1,-1)坐标）。pull_group0、pull_vec1的设定不对结果产生影响。这种模式不适合constant_force。  
  
distance模式：如果参考组设的是一个组，则无论何时，pull组始终朝着参考组方向拉，若拉伸过程中经过了参考组，则拉力方向反过来。如果参考组是绝对坐标(0,0,0)，则拉力方向始终是t=0时pull组朝着参考组的方向，即便pull组可能已经经过了参考组。pull_vec1的设定不对结果产生影响。  
  
direction模式(重点)：将pull组（将其假想为坐标原点）向pull_vec1的反方向拉。pull_group0的设定不对结果产生影响。  
  
======================  
上述六种组合中，假定参考组位置固定，若不进行位置固定，则group0与group1是对称运动的，质心位置不变（包括constant_force+direction这样不直接涉及到group0的模式也是如此），两个组相当于等价。  
  
pull_dim控制哪个方向上的力真正生效，上述假定此项设为了Y Y Y。无论是哪种模式、怎么设定拉伸拉伸，最终在pull组上真正生效的力是pull_dim允许方向上的分量。但如果是constant_force，则在pull_dim方向上的总受力仍是pull_k1。  
  
总结：前面说的三种pull_geometry模式，总的来说position本意是相对于参考组位置设定一个点，以其为依据进行拉伸操作。用distance时，拉伸的方向是根据pull组与参考组连线的瞬时方向。direction是直接定义pull组的拉伸方向。  
常用的组合模式是umbrella+position可固定势阱位置；constraint+distance可约束pull组与参考组的距离；constant_force+direction方便地直接将pull组往某个方向拉。  
  
另外，pull_start如果设为yes，则最终的pull_init相当于你设的pull_init加上被pull组与参考组之间质心的距离矢量。  
  
  
  
mdrun时利用-pf可以指定输出的包含pull组的时间和对应时刻受力的xvg文件名（输出的是外加的pull力，而非这个组的净受力。另外，若为position模式会输出受力xyz分量，distance和direction只输出总受力）。-px可以指定输出的包含pull组的坐标和对应时刻受力的xvg文件名，第一列是时间，第2、3、4列是pull_group0的xyz绝对坐标，5、6、7列是pull_group1相对于pull_group0的xyz坐标。它们的输出频率使用pull_nstfout和pull_nstxout选项控制。  
  
同时pull N个组：  
设定方法同pull一个组，写pull_ngroups=N，增加定义pull_group2、pull_init2、pull_k2、pull_rate2；pull_group3、pull_init3...... 受力-时间 和 坐标-时间的.xvg文件内也会输出这些组。
