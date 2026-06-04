---
post_id: 625
title: 令Gaussian 16中SCF未收敛到默认收敛限也能继续做后续计算的方法
url: http://sobereva.com/625
date: '2021-11-17T01:32:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 量子化学
- 激发态与光谱
academic_relevant: true
classification_reason: 标题直接讨论 Gaussian 16 的 SCF 收敛问题。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

**令Gaussian 16中SCF未收敛到默认收敛限也能继续做后续计算的方法**

A method to enable subsequent calculations to continue even if SCF in Gaussian 16 does not converge to the default convergence limit

文/Sobereva@[北京科音](http://www.keinsci.com)  2021-Nov-17

注：本文内容对目前我用过的Gaussian 16 A.03、B.01、C.01都适用，对未来的版本不一定。

Gaussian程序从09版开始默认的收敛限成为了tight，相当于SCF=conver=8关键词设的收敛限，这在所有量子化学程序里几乎是最严的。Gaussian程序从16版开始加入了一个规则，就是如果SCF过程中如果SCF收敛精度没达到默认的收敛限，而且你的任务涉及到计算能量的导数，如几何优化、振动分析，或者用的是后HF、TDDFT等涉及到多行列式/多组态的方法，在SCF模块运行完之后就会有下面的提示，导致程序以报错方式终止

 SCF Error SCF Error SCF Error SCF Error SCF Error SCF Error SCF Error SCF Error

                                    ERROR!!!!

    SCF has not converged.  Gradients and post-SCF results would be GARBAGE!!

Gaussian 16做这么一个检查本身没什么问题，因为如果SCF收敛精度如果不够高，则上述那些任务、方法的计算精度可能会比较糟糕，而且这也避免了一些菜鸟被其它菜鸟误导而乱用IOp(5/13=1)还不知道自己检查收敛情况。Gaussian 16的这个收敛精度检查设计的最变态的地方是没法关闭，程序手册里和IOp文档里对关闭方法都只字未提，这给许多用户的实际研究带来极大的不便。比如很多SCF特别难收敛的体系，如过渡金属团簇、用小核赝势的镧系锕系配合物（《使用Gaussian做镧系金属配合物的量子化学计算》<http://sobereva.com/581>里提到了）、加较大外电场时，本来SCF收敛到默认的很严的收敛限就普遍较难，而对于几何优化任务，由于初始搭的结构往往不够理想（偏离极小点较远）导致电子结构更复杂，SCF收敛到默认收敛限的难度就更大，很多情况下即便使用《解决SCF不收敛问题的方法》（<http://sobereva.com/61>）里的诸多做法尝试很久也没法解决。这种情况，一个常见解决策略是先用相对较松的SCF收敛限比如SCF=conver=6做粗略的几何优化。当体系结构离极小点结构比较近的时候，SCF就相对容易收敛到默认收敛限了，因此之后可以再用默认的收敛限进一步优化（如果你是老司机而且永不会忘记检查SCF收敛情况的话，IOp(5/13=1)也不是一定不能用）。然而由于Gaussian 16上述变态设定，导致这重要的技巧都无法实现了，令我感到Gaussian开发者严重脱离广大群众的应用场景。有的时候我为了用上述技巧我都不得不刻意改用Gaussian 09。还有时候，要对体系做TDDFT、双杂化、CCSD(T)等计算，但个别情况SCF收敛到SCF=conver=8就是特别困难，而用#P监控SCF过程发现收敛到SCF=conver=7的程度是可以达到的，此时做这些计算的精度并没什么明显问题，可Gaussian 16来了个一刀切，这种情况下就是死活不让你做SCF之后的计算，真是特别荒诞！

今天在CCL上有人分享了一个解决上述问题的奇技淫巧，令SCF没收敛到默认收敛限也能做后续计算，这对Gaussian用户极为重要，我觉得很有必要在这里具体说一下。不了解下述的Gaussian的Link、IOp的话看《Gaussian的Link、IOp与非标准计算路径》（<http://sobereva.com/57>）。

从Gaussian 16开始，在调用Link 701、Link 801模块开始时都会调用SCFChk做一下SCF收敛性的检查，没收敛到默认收敛限就会出现前述报错提示并终止任务。Link 701是计算单电子积分的一阶或二阶导数的模块，所有算能量的导数的任务都会经历它。Link 801是初始化双电子积分变换，TDDFT、双杂化、后HF等涉及到多行列式/组态函数的任务都会经历它。这个Gaussian 16引入的新设计导致了前述问题。

实际上，可以通过官方IOp手册（<http://gaussian.com/iops/>）里都只字未提的选项来关闭SCF收敛性检查（估计CCL上那个人是看到了一般用户都拿不到的Gaussian 16源代码分析出来的）。对于需要经历Link 701的任务，可以用IOp(7/127=-99)来关闭，对于需要经历Link 801的任务，可以通过IOp(8/117=-99)来关闭。实际上不是必须=-99，只要是比-100更正的值都可以。

因此，在Gaussian 16中用比如# B3LYP/6-31G* SCF=conver=6 opt，由于负责SCF的Link 502模块收敛到较松的收敛限就结束了，因此在计算几何优化要用的受力时由于发现SCF没收敛到默认的SCF=conver=8的程度，会报错并出现前述提示。而如果你写# B3LYP/6-31G* SCF=conver=6 opt IOp(7/127=-99)，就可以让几何优化进行下去，和Gaussian 09的情况一样。

如果你嫌上述IOp不好记，每次写的时候也麻烦，有一个技巧可用：如《Gaussian的安装方法及运行时的相关问题》（<http://sobereva.com/439>）所述，可以在Default.Rou（Windows版）或Default.Route（Linux版）里面写上默认的计算资源设置，实际上默认的关键词也可以写进去。如果你在里面加上一行-#- IOp(8/117=-99) IOp(7/127=-99)，则这两个IOp设置会对之后所有计算都会默认启用，以后就再也不会遇到前述的烦人的问题了！

还有一点要注意，根据体系的不同，大多数时候Gaussian默认在SCF计算前期用精度较低的方式算电子积分（SCF一开始会看到Integral accuracy reduced to 1.0D-05 until final iterations.的提示。若强行要求总是这么做可以写varacc关键词），此时SCF=conver=x的设置其实是不起实际作用的，虽然在SCF开始之前显示的收敛限和自己设的一致，但实际还是会迭代到满足tight收敛标准才结束。如果想让SCF=conver=x总是如实生效，应当在SCF里同时写上novaracc。即前例建议改为# B3LYP/6-31G* SCF(conver=6,novaracc) opt IOp(7/127=-99)，可确保每一轮如实迭代到conver=6的程度就视为收敛。如果你想让novaracc默认启用的话，可以在Default.Rou/Route里的-#-后面加上scf=novaracc。

最后对初学者们强调一点，看本文绝对别断章取义！绝对不要把SCF=conver=6时几何优化的结果当做最终用的结构！SCF=conver=6情况下的优化只能算得上预优化，实际发表用的结构要在默认的SCF收敛限下优化得到！
