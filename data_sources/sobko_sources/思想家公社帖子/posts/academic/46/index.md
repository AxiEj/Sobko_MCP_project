---
post_id: 46
title: 谈谈BSSE校正与Gaussian对它的处理
url: http://sobereva.com/46
date: '2015-06-05T01:25:00+08:00'
source_categories:
- 量子化学
primary_topic: 量子化学
secondary_topics:
- Gaussian
- 弱相互作用
academic_relevant: true
classification_reason: 主要讨论 BSSE 校正这一量子化学问题，并结合 Gaussian 的处理方式。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**谈谈BSSE校正与Gaussian对它的处理**  
 On the BSSE correction and its processing in Gaussian

文/Sobereva @[北京科音](http://www.keinsci.com)  
First release 2009-Aug-27  Last update: 2024-Sep-26

  

计算两个分子A、B间的相互作用能时，除非基组很大如def2-QZVP这样的4-zeta档次，否则不宜简单地通过E_interaction = E_AB - E(A) - E(B)来计算，因为E_AB能量相对于E(A) + E(B)的降低来自两方面，一方面是真实的A、B分子间的相互作用能，这是我们要求的；另一方面来自于A、B分子的基函数在复合物体系中重叠，相当于增大了复合物的基组而使E(AB)能量降低（严格来说前提是所用的理论方法是基于变分原理的），这个部分贡献如果也掺入了E_interaction则会高估相互作用强度（即精确的相互作用能实际上没有算出来的那么负），这个问题称为基组重叠误差（Basis Set Superposition Error, BSSE）。为了解决这个问题需要考虑BSSE校正，即严格的双分子的相互作用能应该表述为E_interaction = E_AB - E(A) - E(B) + E_BSSE，这里E_BSSE称为BSSE校正能。当基组不很大而相互作用本身又较弱时，E_BSSE所占E_interaction的比例往往不小，不考虑BSSE校正的话甚至可能结果定性不合理。由于BSSE问题的大小、能否忽略是直接取决于你计算的问题和用的基组的，所以提及BSSE、问是否需要考虑BSSE的时候一定要把这两点交代清楚！没有前提的情况下说BSSE毫无意义！

BSSE问题会影响势能面，因此BSSE效应不仅影响弱相互作用能，也会影响几何优化、振动分析等依赖于势能面任务的结果，只不过BSSE对弱相互作用能的影响远大于对其它问题的影响，因此BSSE校正一般只是对计算弱相互作用能来说的。

用2-Zeta基组如6-31G*、def2-SVP算弱相互作用能时BSSE问题是极为显著的，必须通过适当方法计算出E_BSSE来解决，否则结果根本没法用。3-zeta基组如6-311G**、def-TZVP算弱相互作用能的BSSE问题比2-Zeta基组的轻，但依然必须解决，否则结果定量不准。注：def/def2系列基组比6-311G系列的BSSE问题更小，因为后者的弥散程度低于前者。E_BSSE会随着基组趋于完备而逐渐减小至0，即基组越大BSSE问题越轻。对于4-Zeta基组，BSSE问题通常就很不显著了，故一般可以不考虑BSSE校正。给3-zeta及以下档次的基组加上弥散函数能显著减小BSSE问题。对于氢键、卤键等静电主导的强度不很弱的作用，用了带弥散的3-Zeta级别的基组后，不做BSSE校正算出来的相互作用能也还行。而范德华吸引、pi-pi堆积作用能一般强度很弱，即便用了带弥散函数的3-Zeta基组计算它们，BSSE问题往往仍然不可充分忽略，故最好考虑BSSE校正，而若是仅仅用带弥散的2-Zeta基组的话则更必须考虑BSSE校正。如果你对弱相互作用类型没概念的话，看《谈谈“计算时是否需要加DFT-D3色散校正？”》（<http://sobereva.com/413>）里面的相关文字。

计算E_BSSE有多种方法，目前使用最广泛的是Boys和Bernardi发展的counterpoise方法，被Gaussian等很多程序直接支持。应注意这种方法计算出来的只是实际E_BSSE的近似，并非完全严格、精确，而本来也没有完全严格的方法来计算E_BSSE。设E_i为第i个分子在自身基组下的能量，E_i'为第i个分子在全部n个分子的基函数都出现下的能量，则n个分子间的相互作用能的E_BSSE=∑[i]( E_i - E_i' )。对于变分的方法，由于基组越大能量越低，因此E_i'比E_i更负，故E_BSSE必为正值。注意计算E_i与E_i'时的分子几何结构必须与i处在复合物时的一致，Gaussian做counterpoise任务时会自动这样处理。每个几何结构下都可以计算E_BSSE，数值不同。由于我们计算弱相互作用时用的复合物结构一般是经过优化的，因此一般做counterpoise计算的时候一般也是用的优化后的复合物结构。

若要计算A、B两个分子的E_BSSE，并且顺带计算校正后的相互作用能，在Gaussian中使用counterpoise=2关键字（可简写为counter=2）。会自动依次计算5个体系，依次输出以下能量：  
 E_AB：A、B基函数下AB复合物的能量  
 E_A,bAB：A、B基函数下A的能量  
 E_B,bAB：A、B基函数下B的能量  
 E_A：A基函数下A的能量  
 E_B：B基函数下B的能量

计算过程中会输出类似这样的语句Counterpoise: doing DCBS calculation for fragment   1。这里就是说明接下来计算的是E_A,bAB（假设A分子为fragment 1），其中DCBS代表dimer centered basis set，说明以A、B分子为中心的基函数都出现，但是计算中并不纳入B的电子和原子核，这称为计算A的能量时添加了B的基函数；如果是doing MCBS calculation for fragment   1，就是要计算E_A，MCBS代表monomer centered basis set，计算中只出现属于A分子的基函数。

如果你用的是G09早期版本或者更早的Gaussian，任务最后会输出"Counterpoise: BSSE energy"，这即是E_BSSE，即(E_A - E_A,bAB) + (E_B - E_B,bAB)。还会看到"Counterpoise: corrected energy"，记为E_corrected，这是消除了因单体基函数重叠造成的虚假能量降低后的AB复合物能量，E_corrected = E_AB + E_BSSE。

如果你用的是Gaussian09靠后期的版本，或者G16，counterpoise任务末尾会有类似下例的输出，看着更方便  
Counterpoise corrected energy =    -200.665575667261  //校正后的整体能量  
BSSE energy =       0.001681932370  //BSSE校正能  
sum of monomers =    -200.659550058648  //两个单体在自己基组下的能量和  
complexation energy =      -4.84 kcal/mole (raw)  //校正前的相互作用能  
complexation energy =      -3.78 kcal/mole (corrected)  //校正后的相互作用能

若计算n个分子间的E_BSSE，则关键词为counterpoise=n，能量按如下顺序输出：E_complex, E_1', E_2'...E_n', E_1, E_2...E_n。E_BSSE = (E_1 - E_1') + (E_2 - E_2') + ... + (E_n - E_n')。计算过程中也用DCBS和MCBS来说明接下来将要计算的是哪项，但此时DCBS中的D的含义就不是具体指Dimer了，而是多分子复合物。

如果有特殊原因，需要手动进行上述counterpoise的每步计算，则可以通过设定Ghost原子来实现（比如很老的Gaussian版本不支持counterpoise关键词，要获得E_BSSE不得不手动计算）。只要把某个原子名后面加上-Bq就说明它是Ghost原子（如Na-Bq），即这个原子照常有它原本的基函数，但是没有原子核和电子。因此，比如要计算E_A,bAB，只需要在复合物的输入文件中把B片段的所有原子后面都加上-Bq使之成为Ghost原子即可。注意Bq原子若破坏了原有对称性，最好加上nosymm，否则可能中途报错停止。分别计算得到E_AB、E_A,bAB、E_B,bAB、E_A和E_B之后，就能按照前面的式子立刻算得E_BSSE。在能用counterpoise关键词的情况下这样手动做counterpoise显然没直接用counterpoise关键词省事，不过也有好处，就是手动做counterpoise的每个步骤比直接用counterpoise关键词可能更省时，尤其是高度对称的体系甚至能省几倍，因为用counterpoise关键词时所有任务都关掉了对称性，而手动做时，对单体、复合物仍然可以利用对称性来节省时间。

特别要注意，计算强相互作用能，即牵扯到化学键作用时，绝对不要用counterpoise考虑BSSE问题，否则自取其辱！见《计算化学键键能时若基组合理则考虑BSSE是完全多余的》（<http://sobereva.com/381>）。两个片段间如果既有显著的弱相互作用也有化学键作用，也属于这种情况。计算强相互作用能的时候直接用一个足够大的基组就完了（不需要弥散函数，除非作用区域带显著负电荷），通常至少def-TZVP，用def2-TZVP更好，如果是后HF方法或双杂化泛函并想得到尽可能好的结果则建议cc-pVQZ或def2-QZVP。更多信息看《谈谈量子化学中基组的选择》（<http://sobereva.com/336>）。

另一种如今也挺常用的解决BSSE的方法是Grimme提出的gCP，见此文的介绍：《大体系弱相互作用计算的解决之道》（<http://sobereva.com/214>）。counterpoise任务的耗时是复合物单点耗时的三倍多（对于DFT而言），而gCP校正则是“免费”的，而且涉及到强相互作用时也能用（只不过一般起不到额外益处）。此外，gCP校正有解析导数，因此带着gCP做几何优化、振动分析也不会带来额外的成本。gCP可以结合不带弥散的一些极小基、2-zeta和3-zeta基组使用。gCP在ORCA里支持，截止到Gaussian 16为止Gaussian还不支持。在2024年我研究碳环与富勒烯相互作用的Chem. Eur. J. DOI: 10.1002/chem.202402227文中，对于很大的体系就用了def2-TZVP结合gCP的方式，结果理想，是个很好的应用例子。可见BSSE校正的方法不止一种，所以提问的时候必须说清楚你用的是哪种BSSE校正方法，不要光说BSSE校正。

涉及分子内弱相互作用时一般也要考虑BSSE。比如一条长链分子，计算一字形和字母C形的能量差就不能忽略这个问题。但由于两个片段属于同一个分子，不能直接用counterpoise方法处理。非要用counterpoise的话，可以将分子人为地切成两段，悬键用比如H来封闭，然后适当调整两个片段，即让切断的部位离得远一些（否则这部分也会对E_BSSE产生影响），原本可能造成BSSE问题的部位相对位置保持不变，然后将两个片段当成两个分子来通过counterpoise方法获得E_BSSE。而更优雅的做法是直接在计算时令基组带充分的弥散函数，或者不带弥散函数但是用gCP，这就省得切割片段了。

counterpoise方法有几个问题值得注意：  
1 很多文章专门探讨counterpoise怎么用可以达到最佳效果，各有不同的说法。比如JCTC,10,49(2013)中作者认为对于aug-cc-pVDZ/TZ，在计算弱相互作用时counterpoise校正能只用一半效果最佳，比起不用counterpoise或用完整的counterpoise更好。而对于aug-cc-pVQZ及以上级别的基组，或者进行基组外推，则应当用完整的counterpoise，比不用counterpoise或只用一部分counterpoise更好。  
2 使用counterpoise时没有能量的解析导数，只能通过有限差分以数值方式获得导数，因此优化，尤其是频率计算都慢到吐血，因此强烈不建议在counterpoise下进行优化和计算频率！！！实际上BSSE问题对于优化出的几何结构的影响一般很小。因此通常的弱相互作用计算，都应当在不使用counterpoise的情况下先做优化，然后再带着counterpoise计算相互作用能（对于基组不够大的情况下）。优化时候只要基组用3-zeta如def-TZVP就够了（比6-311G**更合适一些，因为def-TZVP的弥散程度相对更高一点），不加弥散函数误差也不大。如果在弱相互作用体系的优化和振动分析过程中就想明确考虑BSSE校正（优化时只用得起不带弥散函数的2-zeta基组时必须如此），那么应该用gCP方法，ORCA程序里的gCP有解析一阶和二阶导数。  
3 溶剂模型下考虑BSSE问题没有严格的办法，一般做法是在气相下做counterpoise计算得到E_BSSE，然后加到溶剂模型下以常规方式E(AB)-E(A)-E(B)计算的相互作用能上。  
4 counterpoise有时有过校正问题，例如计算E_A,bAB时，A感受到的是完全“空闲”的B的基函数，能被A充分利用；而在复合物中A感受到的B的基函数已经有一定占据了，不能被A充分利用。由于两种状况B的基函数的状态不同，用E_A - E_A,bAB作为复合物中A的校正显得校正过头了，故所得相互作用能会被低估，个别时候结果还不如不用counterpoise。

5 算相互作用能是否有必要用counterpoise严重取决于基组。用def2-QZVP、cc-pVQZ、aug-cc-pVTZ及其月份基组变体（<http://sobereva.com/119>）时可以不考虑BSSE校正，因为此时E_BSSE非常小，尤其是对于基组要求不是很高的非双杂化泛函来说。对于3-zeta档次基组，def2-TZVP和6-311+G(2d,p)算弱相互作用能能及格，但考虑counterpoise后才能足够理想，参见《使用sobEDA和sobEDAw方法做非常准确、快速、方便、普适的能量分解分析》（<http://sobereva.com/685>）的2.3节提到的sobEDA原文里的不同基组算相互作用能误差的测试的表格。对于明显更小的基组，如6-311G**、6-31+G**、def2-SVP等，算相互作用能如今不考虑BSSE校正能绝对不能接受，若嫌counterpoise明显增加耗时至少也应当用免费的gCP。

最后顺带一提，如果你对弱相互作用的计算非常关注，推荐参加《北京科音中级量子化学培训班》（<http://www.keinsci.com/workshop/KBQC_content.html>），里面专门有一节“弱相互作用的计算与相关问题”，全面深入系统讲解相互作用计算的各种知识并给出大量例子，在BSSE、基组选择这方面讲得远比本文深入得多。

**附：Gaussian中counterpoise输入文件的写法**

每个原子最后需要有一个整数说明这个原子属于第几个片段。例如：  
# B2PLYPD3/jul-cc-pVTZ counterpoise=2

Counterpoise with Cartesian

0 1   //此例整体、片段1、片段2的电荷和自旋多重度都一样，只需写一次即可  
H 0.00 0.00 0.92 1  
F 0.17 0.00 2.73 2  
H 0.77 0.00 3.43 2  
F 0.00 0.00 0.00 1

若整体与片段的电荷和自旋多重度不一样，应该写：整体电荷，整体自旋多重度，片段1电荷，片段1自旋多重度，片段2电荷，片段2自旋多重度。

坐标部分也可以如下这么写来设置片段，效果和上面一样。  
H(fragment=1) 0.00 0.00 0.92  
F(fragment=2) 0.17 0.00 2.73  
H(fragment=2) 0.77 0.00 3.43  
F(fragment=1) 0.00 0.00 0.00

如果你是ORCA程序的用户，做counterpoise任务最方便的做法是通过Multiwfn产生输入文件，这里给了明确的例子：《在ORCA中做counterpoise校正并计算分子间结合能的例子》（<http://sobereva.com/542>）。

**补充**：由于有网友看过此文后对BSSE的认识仍然有误，因此我将对他的回复也贴到了这里（修改了符号以与本文一致），希望读者看了之后能对BSSE问题根源了解得更明白一些。为简化讨论，这里假设不考虑单体在复合物状态下结构的改变。

对于计算相互作用能，E_interaction = E_AB - E_A - E_B这个式子没错，这是由结合能的定义直接得到的。而必须指出的是，在实际计算中，E_interaction = E_AB,bAB - E_A,bA - E_B,bB这个式子中（b代表基组）， E_AB,bAB作为复合物能量是对的，E_A,bA和E_B,bB作为单体能量也是对的，但是，这么计算相互作用能，在基组完备性差的时候，是绝对错误的！因为计算复合物和计算单体时不在相同的基组级别下。例如，A单体中靠近B单体的原子的基组完备性在复合物状态下高（因为B的基函数侵入此原子空间），而在A单体单独计算时低，这就导致能量在求差值时基组误差无法被抵消，这就是BSSE的根源。只有在基组完备的情况下，或者计算复合物和计算单体时都在相同基组级别下才能直接通过计算出的复合物能量减去单体能量来计算结合能。即正确的写法是E_interaction = E_AB,bQ - E_A,bQ - E_B,bQ，Q可以代表平面波基函数，也可以代表一套原子中心的基函数，比如可以指AB的基函数，这正是为什么本文中给出了这样的式子：E_interaction = E_AB - E_A,bAB - E_B,bAB，即计算复合物和单体的能量时都在AB基组下（文中E_AB和E_AB,bAB在符号上是等价的）。
