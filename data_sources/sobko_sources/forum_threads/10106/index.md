---
thread_id: 10106
source_id: forum_thread:10106
title: "将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC、做振动分析"
url: http://bbs.keinsci.com/thread-10106-1-1.html
date: "2018-07-01T00:00:00+08:00"
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: wsl2_chrome_cdp_verified_session
source_crawled_at: "2026-06-05T12:09:09.078Z"
original_reply_count: 103
page_count: 10
views: 175513
software_tags:
- Gaussian
- xTB
topic_tags:
- 综述/教程/投稿经验
- 量子化学
authority_level: A
confidence: 0.97
classification_reason: sobereva教程，17.5万浏览，讲解Gaussian与xtb联用方法。
---

# 将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC、做振动分析

- 原帖 URL：<http://bbs.keinsci.com/thread-10106-1-1.html>
- 论坛板块：量子化学
- 作者：**sobereva**
- 浏览量：175513 | 回复数：103 | 共10页
- 完整性：**全部内容已完整抓取**。

## 楼层正文

### 1 楼（楼主）｜sobereva

注：本文仅简略说明xtb的用法，更多细节请结合xtb自带文档和官方手册。





将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC、做振动分析Use Gaussian with xtb program to search for transition states, generate IRC, and perform vibration analysis



文/Sobereva @北京科音First release: 2018-May-29  Last update: 2024-Oct-2

0 前言



在《盘点Grimme迄今对理论化学的贡献》（http://sobereva.com/388）一文中笔者曾简单提到GFN-xTB方法，说白了就是类似于DFTB那种半经验意味的DFT，精度不错普适性也好，对与之耗时相仿佛的半经验方法和DFTB带来了极大的冲击。Grimme开发了名为xtb的专门做GFN-xTB计算的程序。xtb程序用过的人都说好，速度很快，普适性挺好，推出不久已经开始有很多人使用了，在《2018年度计算化学公社杯最常用的量子化学程序和DFT泛函投票结果统计》（http://sobereva.com/420）里已经有一些得票率了，而且一些第三方程序已经支持xtb了，比如Multiwfn (http://sobereva.com/multiwfn)可以读取xtb的振动分析的输出来绘制红外光谱、基于xtb产生的波函数做波函数分析和绘制分子轨道，molclus程序可以结合xtb来做团簇构型和分子构象搜索（见http://www.keinsci.com/research/molclus.html）。另外计算化学公社上fhh2626还写了NAMD与xtb结合做QM/MM的界面（http://bbs.keinsci.com/thread-7583-1-1.html）。



xtb程序目前可以做单点、优化、振动分析等任务，但是对于一般计算化学研究者来说，还希望能够找过渡态、产生IRC，并且希望振动分析的结果（特别是虚频模式）可以可视化，但这些xtb程序目前还做不到。好在Gaussian从09开始加入了external关键词，在进行极小点/过渡态优化、IRC、振动分析等任务时，可以从外部文件直接读入能量、受力、Hessian，而外部文件的这些信息可以用任意程序来产生，当然也包括xtb，不过需要自己写个接口才能实现。因此Gaussian可以被当做一个“optimizer”来使用，这种用法似于ASE（atomic simulation environment）程序。



本文的目的就是介绍如何将Gaussian与Grimme的xtb程序联用搜索过渡态、产生IRC，并且使得xtb振动分析结果能够被gview来可视化，从而弥补xtb的不足、极大地扩展xtb的实用价值。本文Gaussian使用G09 E.01版。



本文介绍的这个接口笔者称为gau_xtb，可以从这里下载：http://sobereva.com/soft/gau_xtb。如果大家的实际研究中使用了此接口，请务必这样引用：Tian Lu, gau_xtb: A Gaussian interface for xtb code, http://sobereva.com/soft/gau_xtb (accessed month day, year)。此页面里的脚本始终兼容目前最新版本xtb。当笔者发现xtb的更新导致老的gau_xtb脚本不能用的时候，笔者会在此网页里对脚本进行更新。因此如果你发现gau_xtb无法正常调用xtb时，首先应当把xtb和gau_xtb都更新为最新版。



笔者还另写了一篇文章，《Gaussian与ORCA联用搜索过渡态、产生IRC、做振动分析》（http://sobereva.com/422），将Gaussian和ORCA联用也带来很多好处，有兴趣可以看看。



下面先介绍xtb的基本用法，然后介绍gau_xtb接口的原理，之后给出具体例子。如果大家已经会用xtb，对接口的原理和细节不感兴趣，只想马上用起来，直接看第4节就行了。



注：经常有人问怎么用本文提供的接口联用不成功，还怀疑是本文的接口不支持较新版本的xtb。在此明确说明，本文的接口没任何问题。通过实测，至少令G16 C.01结合xtb 6.5.1以及G16 C.02结合xtb 6.6.1、6.7.1运行都没问题。遇到跑自己的任务失败时，起码先把本文提供的例子重复一遍，死活不成功的话，在读懂接口脚本的内容基础上，让脚本输出一些中间信息（比如脚本里用ls命令显示当前目录下的文件都有哪些、用cp命令将临时产生的文件复制出来然后人工进行检查），总能搞明白原因。另外也不要用一些稀奇古怪的运行环境。





1 xtb简介



借本文的机会简单介绍一下xtb的相关知识和使用。在https://xtb-docs.readthedocs.io/en/latest/contents.html可以看到在线手册。



1.1 xtb的安装



xtb是开源的，可以在https://github.com/grimme-lab/xtb/下载到源代码，如果想自行编译的话参看《Grimme的xtb程序的编译方法》（http://sobereva.com/521）。作为普通用户，直接用https://github.com/grimme-lab/xtb/releases里提供的预编译好的版本即可，文件名为比如xtb-191025.tar.xz这样的形式，代表2019年10月25日发布的版本。这是Linux版，目前没有预编译的Windows版。



创建一个目录，比如/sob/xtb。将比如xtb-191213.tar.xz放进去，在此目录下执行tar -xJf xtb-191213.tar.xz目录解压之，之后应当会看到此目录下出现了bin、lib64等目录。



用gedit或vi等工具编辑~/.bashrc文件，加入以下语句

export PATH=$PATH:/sob/xtb/bin

export XTBPATH=/sob/xtb/share/xtb

export OMP_NUM_THREADS=N

export MKL_NUM_THREADS=N

export OMP_STACKSIZE=1000M

ulimit -s unlimited

其中N是并行计算时使用的CPU核心数，不要超过CPU的物理核心数。



然后保存.bashrc文件，重新进入终端，xtb就可以用了。



注：根据我的诸多测试，发现xtb（至少对于GFN2-xTB真空下计算而言）做优化、动力学的速度在大约12核的时候就封顶了，用更多的核来并行对速度的提升微乎其微，某些情况下反倒速度还稍微变得更慢。因此，如果你的机子的物理核心数很多，比如三、四十核，那么建议把N设为12，同时跑多个任务来充分利用计算资源。如果你的CPU比如只有6核，那么N就设6核就好了。但是，如果你要做振动分析，那么用几十核还是值得的，比如36核速度可以达到12核的两倍出头（这是由于振动分析是基于有限差分做的，原理上并行效率可以做得较高）。



1.2 xtb的基本使用



xtb的输入文件就是一个xyz文件，这是最常用的记录分子结构的格式之一，很多程序都可以产生。用Multiwfn产生也可以，可以把fch、pdb、mol、wfn、wfx、molden等Multiwfn能认的格式载入Multiwfn，然后进入主功能100的子功能2，选择输出xyz文件。由于这个文件格式非常简单，比如自己把Gaussian的.gjf文件编辑一下产生也可以。



xtb的详细使用说明也可以通过xtb -h查看。几个比较常用的选项如下

-c或--chrg：设定体系净电荷

-u或--uhf：设定alpha电子数减beta电子数（相当于自旋多重度减1）

--gbsa：使用GBSA隐式溶剂模型。目前支持的溶剂有acetone、acetonitrile、benzene、CH2Cl2、CHCl3、CS2、DMF、DMSO、ether、H2O、methanol、n-hexane、THF、toluene

--alpb：使用ALPB隐式溶剂模型。目前支持的溶剂有acetone、acetonitrile、aniline、benzaldehyde、benzene、ch2cl2、chcl3、cs2、dioxane、dmf、dmso、ether、ethylacetate、furane、hexandecane、hexane、methanol、nitromethane、octanol、woctanol、phenol、toluene、thf、water

--molden：计算结束后产生molden.input，这是Molden输入文件

--gfn：选择GFN-xTB理论的版本，可以为0、1、2。如--gfn 0就代表GFN0-xTB。GFN2-xTB物理上最严格，多数情况精度最佳，但有时候SCF收敛困难；GFN1-xTB不如GFN2-xTB严格，平均精度稍逊一点，但SCF收敛容易（因此明显更适合SCF难收敛的金属团簇等情况），耗时也比GFN2-xTB低一些。GFN0-xTB精度最烂但速度也最快，非常适合快速简单粗暴地搞巨大体系，但对于找过渡态的目的就太糙了而不建议用



常用任务类型：

--sp：计算单点（此为默认，可不写）

--grad：计算梯度

--opt [级别]：几何优化。级别默认为normal，更佳的是tight、verytight、extreme

--hess：计算数值Hessian并做振动分析

--ohess [级别]：优化后自动计算Hessian并做振动分析

--md：基于当前结构做分子动力学（目前xtb还支持metadynamics，详见手册）

--omd：优化后做分子动力学



例如：

对yoshiko.xyz做真空中的单点计算，电荷为1，自旋多重度为2（alpha比beta电子多1个）：xtb yoshiko.xyz --chrg 1 --uhf 1 -sp

对yohane.xyz做甲苯溶剂下优化和振动分析，体系是默认的中性单重态：xtb yohane.xyz --ohess --gbsa toluene



xtb运行时一方面会在屏幕上输出信息，同时也会在当前目录下产生一大堆文件。这些文件的含义在自带的文档里有说明。



xtb目前有解析梯度，但只支持数值Hessian。--hess或-ohess任务做完会输出g98.out，是模仿高斯freq输出格式来输出频率、红外强度、正则坐标。后者没用。



--opt任务产生的xtbopt.xyz是最后结构的xyz坐标文件，其中第二行是对应的能量。xtbopt.log是含有优化过程每一帧的多帧xyz文件，后缀改为.xyz后就可以拖入VMD查看优化轨迹。



Multiwfn可以载入xtb用--molden产生的molden.input文件做十分丰富的波函数分析，相关知识看《Multiwfn入门tips》（http://sobereva.com/167）、《Multiwfn FAQ》（http://sobereva.com/452）。



Multiwfn载入--hess或--ohess的输出文件后，进主功能11，选择IR或Raman，进入界面后选0就可以绘制出相应的光谱，超级容易。更多信息见《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（http://sobereva.com/224）。



1.3 xtb的控制文件



xtb运行时还可以载入控制文件（xcontrol），见在线手册。通过控制文件，可以对xtb的运行细节做更多的控制、实现更多的功能。有些设置（比如设置体系净电荷）既可以通过上述选项来指定，也可以在控制文件里指定，前者的优先级更高。



控制文件的文件名随意，通过-I指定。比如控制文件名字叫inp，那就可以比如这样执行：

xtb rei_ayanami.xyz -I inp --molden --chrg 1



控制文件里可以设置很多字段，每个字段通过$开头，到下一个$结束。例如计算当前体系时alpha电子比beta电子多两个，并且让3,19,20,21,22原子的位置在优化过程中被冻住，则控制文件的内容应当为：

$spin=2

$fix

atoms:3,19-22

更多xtb细节请看自带文档和官方手册。





2 Gaussian的external功能简介



关于Gaussian的external功能的使用，详见http://sobereva.com/g09/k_external.htm。简单来说，Gaussian的输入文件里写上比如external='./xtb.sh'，在计算时候就会以这样的方式调用当前目录下的xtb.sh脚本：

xtb.sh layer InputFile OutputFile MsgFile FChkFile MatElFile

各个参数的含义可以看手册，后五个是文件名，这里我们主要关心的是其中第二个参数InputFile和第三个参数OutputFile。如果查看Gaussian输出文件，会发现这样的提示

Running external command "./xtb.sh R"

         input file       "/sob/g09/scratch/Gau-28355.EIn"

         output file      "/sob/g09/scratch/Gau-28355.EOu"

         message file     "/sob/g09/scratch/Gau-28355.EMs"

         fchk file        "/sob/g09/scratch/Gau-28355.EFC"

         mat. el file     "/sob/g09/scratch/Gau-28355.EUF"

其中"/sob/g09/scratch/Gau-28355.EIn"和"/sob/g09/scratch/Gau-28355.EOu"正是分别传递给xtb.sh的InputFile和OutputFile的文件名。



InputFile文件是Gaussian产生的，记录了当前步的信息，格式为：

原子数  需要的导数  电荷  自旋多重度

原子1元素序号  X  Y  Z  MM电荷 MM原子类型

原子2元素序号  X  Y  Z  MM电荷 MM原子类型

...

原子N元素序号  X  Y  Z  MM电荷 MM原子类型

如果当前任务只需要能量信息，“需要的导数”为0；如果需要受力，则为1（比如几何优化任务）；如果还需要Hessian，则为2（比如freq任务，以及优化或IRC时用了calcfc等情况）。



OutputFile是要在执行xtb.sh时候由这个脚本来生成的，里面记录能量、受力、Hessian等，按照手册的要求格式为：










1.png (24.76 KB, 下载次数 Times of downloads: 543)

下载附件 Download



2018-5-29 06:42 上传 Uploaded






其中诸如4D20.12是数据格式，稍微懂点Fortran就能明白。按照这个格式产生好OutputFile文件，则Gaussian就会从中读取当前任务需要的信息开展计算。比如如果当前任务只需要能量，则填上能量和偶极矩那一行即可，而如果比如需要Hessian，则整个文件所有信息都得填上。此文件中的偶极矩、极化率对于本文涉及的优化、走IRC、振动频率计算都是不需要的，可以直接填0（但相应地，涉及到这些信息的Gaussian输出，比如偶极矩、freq任务的红外强度等也将都为0）。



要想将Gaussian和xtb联用，关键就是要恰当编写xtb.sh，使得这个脚本可以基于InputFile里的信息去调用xtb计算出当前结构下的能量、受力、Hessian，并按照Gaussian要求的格式转化出OutputFile文件。下一节就介绍怎么实现。





3 Gaussian与xtb的接口xtb.sh的编写



笔者写好的xtb.sh文件在本文一开始提到的压缩包里有。这是bash shell脚本，本节解释一下脚本内容，需要懂得一些Linux命令和shell编程知识才能完全理解（值得一提的是，写这种脚本并非必须用bash shell，也并非必须是Linux环境才能用external功能。比如在Windows下也完全可以写成.bat脚本，例如Windows版Gaussian调用NBO6就是通过external来调用NBO6的.bat文件实现的）。



xtb.sh文件里$2、$3分别对应于xtb.sh接收到的第2、第3个参数，也即InputFile和OutputFile文件名。脚本首先用

read atoms derivs charge spin < $2

从InputFile中把原子数、需要的导数、电荷、自旋多重度分别读到atoms、derivs、charge、spin四个变量里，然后用以下命令构建一个mol.tmp文件

cat >> mol.tmp <<EOF

$atoms



$(sed -n 2,$(($atoms+1))p < $2 | cut -c 1-72)

EOF

这个mol.tmp文件是xyz文件的雏形，还需要做两个处理才能变成xyz格式文件，一方面是把从InputFile读过来的元素序号转化成元素名，另一方面是把读过来的以Bohr为单位的坐标转化成埃。为此，笔者写了个Fortran小程序genxyz.f90，编译好的可执行文件是压缩包里的genxyz。这个小程序稍微懂点编程的人都能看懂，就不解释了。xtb.sh以下两行就是调用genxyz把当前目录下的mol.tmp转化为mol.xyz

./genxyz

rm -f mol.tmp



之后，脚本设置xtb并行运行时的线程数，并根据读入的自旋多重度，将之减1，算出来-uhf后面的参数。然后根据当前任务需要的导数信息，来判断在调用xtb时是用-grad还是用-hess

export OMP_NUM_THREADS=4

export MKL_NUM_THREADS=4

uhf=`echo "$spin-1" | bc` #nalpha-nbeta

if [ $derivs == "2" ] ; then

 echo "Running: xtb mol.xyz --chrg $charge --uhf $uhf --hess --grad > xtbout"

 xtb mol.xyz --chrg $charge --uhf $uhf --hess --grad > xtbout

elif [ $derivs == "1" ] ; then

 echo "Running: xtb mol.xyz --chrg $charge --uhf $uhf --grad > xtbout"

 xtb mol.xyz --chrg $charge --uhf $uhf --grad > xtbout

fi



xtb程序默认用的是GFN1-xTB理论，如果想用原理上更好的GFN2-xTB，可以将上述调用时的参数里加上--gfn 2来改用之。



最后，xtb.sh如下调用笔者自编的extderi程序产生OutputFile文件。对应的源代码extderi.f90也很简单，就不解释了

./extderi $3 $atoms $derivs

extderi会读取xtb运行后在当前目录下产生的gradient、hessian文件，分别提取受力、Hessian信息，并且从xtbout文件中读取能量，然后输出到OutputFile中。传递给extderi的三个参数$3、$atoms、$derivs分别告诉这个程序要产生的OutputFile文件的文件名是什么、总共多少原子、要读取/写入哪些导数信息。



xtb.sh中还用了一些rm -f命令，用来删除xtb产生的各种文件，确保Gaussian运算后当前目录不残留多余的文件。





4 Gaussian与xtb联用搜索过渡态、做振动分析、产生IRC应用示例



注：以下数据用的是本文刚发布的时候的xtb程序算出来的，结果和最新版本xtb可能不同。



我们这里将Gaussian与xtb联用，搜索一下下图所示的环丙基卡宾异构化过程的过渡态








2.png (12.79 KB, 下载次数 Times of downloads: 668)

下载附件 Download



2018-5-29 06:42 上传 Uploaded








对应的Gaussian输入文件是本文压缩包里的TS.gjf，开头两行如下

%chk=mol.chk

#P opt(ts,calcfc,noeigen,nomicro) external='./xtb.sh'



可见这里用的是常用的opt=TS方式搜索过渡态，因此输入文件里的结构应当是这个与实际过渡态比较像的过渡态初猜结构。opt里必须写nomicro，否则Gaussian在优化的时候会试图调用分子力学的optimizer去搞，达不到我们的目的。这里我们刻意保留了chk文件，因为这样的话之后做IRC、freq任务就可以直接用geom=allcheck从chk文件中读取已经优化好的过渡态结构来计算了。注意对于当前情况，不能在这里直接写opt freq，必须把opt和freq拆成两步做才行，否则freq任务会出错。另外，由于当前任务的能量、导数都调用xtb来算了，因此理论方法和基组就不需要写了。



我们确保机子里已经装好Gaussian了，xtb也已经配置好了从而可以直接通过xtb命令调用了，然后把TS.gjf、xtb.sh、genxyz和extderi都放到当前目录下，把xtb.sh里的OMP_NUM_THREADS和MKL_NUM_THREADS都设为CPU的物理核心数。再运行诸如g09 < TS.gjf |tee TS.out，就开始计算了。



这里特别强调一点，如果你的Gaussian的Default.route里已通过-M-设置为默认并行做Gaussian计算，一定要改为串行计算（如果不想动这个文件就在.gjf文件里设%nproc=1），否则在Gaussian通过external方式调用外部脚本期间会造成很高无意义的CPU资源消耗，导致总耗时增加。



此任务收敛很顺利，13步就收敛了。找到的过渡态精度如何？下图上半部分是将Gaussian+xtb找到的过渡态（白线）与B3LYP/TZVP下找到的过渡态（红线）放在一起进行对比，已经按照《在VMD中计算RMSD衡量两个结构间的几何偏差》（http://sobereva.com/290）文中的做法将两个结构进行了Align使之最大程度匹配。下图下半部分是过渡态结构的球棍图，便于读者看清楚结构。










3.png (42.76 KB, 下载次数 Times of downloads: 669)

下载附件 Download



2018-5-29 06:42 上传 Uploaded








从上面的对比来看，GFN-xTB方法当初虽然没有特意考虑过渡态问题，但是优化过渡态的结果和较好精度的B3LYP/TZVP比，误差基本可以接受，至少定性正确。大家可以用Gaussian+xtb尝试用不同初猜搜索过渡态，等搜出来一个看着基本合理的过渡态，再用DFT去进一步优化（当然，Gaussian+xtb不是干这个的唯一选择，笔者也尝试了用PM7半经验方法优化这个过渡态，结果也一样定性正确，至于和Gaussian+xtb给出的结构孰优孰劣，从相对于B3LYP/TZVP结构的RMSD偏差上看半斤八两）



接下来再做一下振动分析，看看虚频情况。虽然xtb直接就能做振动分析给出振动频率，但是不便于观看振动模式，而通过Gaussian+xtb联用，结果就可以直接用gview看了。输入文件是本文文件包里的freq.gjf，内容只有两行，为

%chk=mol.chk

#P freq geom=allcheck external='./xtb.sh'

运行之，结果是压缩包里的freq.out。虚频模式的正则矢量如下








4.png (42.52 KB, 下载次数 Times of downloads: 591)

下载附件 Download



2018-5-29 06:42 上传 Uploaded








从振动动画上看，过渡态确实找对了。虚频大小是732cm-1，而B3LYP/TZVP下是686.7cm-1，PM7下是843.1cm-1，可见Gaussian+xtb的结果合理，而且误差比PM7明显更小。



最后，我们再走一下IRC。输入文件是本文文件包里的IRC.gjf，内容为

%oldchk=mol.chk

#P IRC(maxpoints=20,calcfc) geom=allcheck external='./xtb.sh'

这里用%oldchk是避免IRC任务改写之前的chk。用Gaussian执行之。gview看到的IRC如下










5.png (58.11 KB, 下载次数 Times of downloads: 630)

下载附件 Download



2018-5-29 06:42 上传 Uploaded






可见IRC曲线很光滑，而且所有点的结构都正常，证明Gaussian和xtb联用很成功。



对于上面这个普通有机反应，xtb和PM7都可以给出定性正确的结果。但对于比较复杂、比较难算的牵扯过渡金属的反应情况又会如何？笔者用Sc金属引发C-H活化的反应做了个测试，结果如下。具体来说，笔者是先用肯定稳妥的PBE0-D3(BJ)优化出过渡态（下图左上角。涉及反应的原子被高亮了），然后用这个结构作为初始结构，再用Gaussian+xtb和PM7分别在相应级别下优化过渡态。为了便于对比，三个级别得到的结构都摆成了相同视角。C1和C2分别指的是苯基和甲基上与Sc成键的碳。








6.png (446.19 KB, 下载次数 Times of downloads: 653)

下载附件 Download



2019-3-5 18:59 上传 Uploaded








可见，Gaussian+xtb很好地维持住了PBE0-D3(BJ)的过渡态结构，而且虚频、键长都很合理，笔者也跑了IRC，也很顺利且结果正常。然而在PM7下过渡态严重变形，跑了一百多步还在严重震荡，最后一帧结构也完全看不出能收敛到合理过渡态的迹象。从最后的结构看，Sc没有和两个茂环配位，反倒是与其中一个碳配位了；另外，Sc和甲基、苯基的碳的键长居然变得相同了。这说明，用PM7哪怕试图做这种反应的预优化也根本没法用。



虽然本文只考察了两个体系，但至少证明Gaussian+xtb用来粗略研究化学反应是充分可行的，值得在实际研究中广泛使用。对于普通有机体系，这种做法比起直接用Gaussian自带的PM6/PM7优势不显著。但碰到略诡异，尤其是涉及过渡金属的体系，预感半经验方法连定性正确结果也给不出的时候，则十分建议改用Gaussian+xtb。



最后提醒一下，虽然GFN-xTB往往很不错，但也别以为它的普适性和精度能和一般的DFT计算抗衡。例如优化Li2，M06-2X/def2-TZVP下结果是2.7064埃，实验值是2.6729埃，但xtb优化出来是2.2991埃，误差还是不小的，尽管比PM7优化出来的1.8106埃已经强得多了。



如果你要用本文的做法计算很重的元素，比如Pt，有一点主要注意，即虽然Gaussian与xtb联用时Gaussian自己并不会去做任何量化计算，但是由于你没写基组，Gaussian程序内部默认当前设的基组是STO-3G，程序会进而判断你当前体系里的所有元素是否对于STO-3G有定义，如果没有就报错。对很重的元素STO-3G都是没有定义的。为了避免这个报错，解决办法就是关键词里写上UGBS，这是一个几乎涵盖整个周期表的基组，因此就不会因为当前的基组对元素没有定义而报错了。

### 2 楼

本帖最后由 yjmaxpayne 于 2018-5-29 08:53 编辑 



社长大作，牛！ 越发的期待高级班了。

### 3 楼

社长真是天才，全才！

### 4 楼

社长写啥是根据自己兴趣来的，请愿啥的不好使，这几天非常想要一个这样的帖子。然后，这就来了……激动啊

### 5 楼

卢老师太强大了

### 6 楼

请问opt＝calcall或者irc=calcall也可以兼容这种方法吗？

### 7 楼

smutao 发表于 2018-5-30 22:05

请问opt＝calcall或者irc=calcall也可以兼容这种方法吗？

可以

### 8 楼

谢谢

### 9 楼

有个专门做几何优化和过渡态搜索的library叫DL-Find，以前做方法开发的时候还折腾过，结果发现效果相当一般，早知道Gaussian这个external功能就好了，毕竟Gaussian的几何优化模块还是很好用的...

### 10 楼

由于Grimme在2018-Jul-13更新了一次xtb，输出的文件名和格式发生了变化，因此笔者对本文的代码和脚本进行了更新以兼容之，同时不再兼容2018-Jul-13以前的xtb版本

### 11 楼

请问xtb支持外加电荷吗？



下面这个帖子问过 没搞懂 谢谢

http://bbs.keinsci.com/forum.php ... 76&fromuid=7918

### 12 楼

pyscf 发表于 2018-9-5 00:50

请问xtb支持外加电荷吗？



下面这个帖子问过 没搞懂 谢谢

你可以试试红字的做法。我没试过



Appenix B: (incomplete) file description list



xtbopt.coord          : optimized coordinates

xtbopt.log            : optimization history (xyz in A)

scoord.<nnn>          : ensemble coordinates in TM format in siman or screen searches

xtbsiman.log          : same but one molden type xyz file

xtbscreen.log         : same but from -screen option      

xtbhess.coord         : optimized coordinates but distorted along imag modes

xtbpath.xyz           : reaction path (xyz in A)

xtb_mode*xyz          : output coords (xyz in A) from modefollowing

xtbrestart            : restart file (remove for clean restart)

wfn.xtb               : WFN file for stda spectra calculation

xtblmoinfo            : file for xTB-IFF intermolecular force-field

g98.out               : normal modes for visualization

hessian               : Hessian for input into TURBOMOLE or read by qmdff

                        if it exists, its read in opt. for ANC generation

                        (remove if unwanted)

xtb_normalmodes       : as the name says ...

xtb_localmodes        : ocalized normal modes

.xtb*ok*              : signal files for parallel runs

pcharge               : file with point charges (first line: # of PC followed by 

                        one charge and xyz coordinates in Bohr per line)

### 13 楼

对本文做了巨大更新，重写了对xtb使用介绍部分，以使内容和目前最新的2019-Feb-14版相符。

对本文的脚本做了更新，兼容了2019-Feb-14发布的xtb。但愿xtb以后别老改来改去了，上次更新就害得我重新更新了一次脚本，没想到刚过一个多月我又被迫重新更新一次本文的脚本。

### 14 楼

给本文增添了Sc活化C-H键的例子，充分体现出对于难算的体系GFN2-xTB理论比PM7靠谱得多得多。

### 15 楼

同时安装了Multiwfn和XTB，添加了环境变量export OMP_STACKSIZE=1000m后，在运行时出现了如下提示：

OMP_STACKSIZE: ignored because KMP_STACKSIZE has been defined。

请问该如何避免？

### 16 楼

Novice 发表于 2019-3-13 20:45

同时安装了Multiwfn和XTB，添加了环境变量export OMP_STACKSIZE=1000m后，在运行时出现了如下提示：

OMP_S ...

不是报错，不用管，没事

### 17 楼

用GFNx-XTB来做反应 因为参数并没有对反应数据做拟合优化 误差会比较大 可能用来算反应不是很合适

### 18 楼

pyscf 发表于 2019-3-23 03:43

用GFNx-XTB来做反应 因为参数并没有对反应数据做拟合优化 误差会比较大 可能用来算反应不是很合适

虽然没有专门对计算势垒做考虑，但是根据GFN2-xTB原文的测试，计算结果比其它半经验方法以及DFTB都好。根据我的测试，优化过渡态结构也比较不错。所以据已知信息来看，算反应没什么大问题

### 19 楼

sob老师，您好。我参考本文的做法，尝试用g16进行联用，但是输出报错显示Failed to open output file from external program。请问这是怎么回事呢？附件是Gaussian的输出文件。

### 20 楼

GoldenBaby 发表于 2019-3-25 17:36

sob老师，您好。我参考本文的做法，尝试用g16进行联用，但是输出报错显示Failed to open output file from  ...

确认你用的xtb是目前最新版，而且接口文件也是刚在本文下载的

### 21 楼

sobereva 发表于 2019-3-25 17:41

确认你用的xtb是目前最新版，而且接口文件也是刚在本文下载的

接口文件是刚刚下载的，xtb是3月4号收到的。

### 22 楼

GoldenBaby 发表于 2019-3-25 17:48

接口文件是刚刚下载的，xtb是3月4号收到的。

测试了，没问题，输出文件见附件。xtb是2019年3月18日的







TS.out

(206.11 KB, 下载次数 Times of downloads: 21)



2019-3-26 06:59 上传 Uploaded
点击下载
Click to download










应该是你没用对，再照着帖子仔细检查下

### 23 楼

sobereva 发表于 2019-3-26 06:59

测试了，没问题，输出文件见附件。xtb是2019年3月18日的

感谢sob老师，我又检查了一下，xtb和Gaussian单独使用都是正常的，但是联用好像就是一直不行，请问这种情况应该检查哪些文件或者步骤呢？

### 24 楼

GoldenBaby 发表于 2019-3-26 16:33

感谢sob老师，我又检查了一下，xtb和Gaussian单独使用都是正常的，但是联用好像就是一直不行，请问这种情 ...

我能交代的在文中都尽可能交代清楚了，其它情况我也想不出来实在不行你就调试一下脚本，自行检查一下调用期间临时产生的那些文件，看看怎么回事

### 25 楼

sobereva 发表于 2019-3-27 04:34

我能交代的在文中都尽可能交代清楚了，其它情况我也想不出来实在不行你就调试一下脚本，自行检查一下调用 ...

好的，谢谢sob老师了

### 26 楼

从grimme最近的更新来看 xtb程序的定位好像要偏重构象扫描、NMR计算这种保留完整化学结构的计算

反应建模方面没有着重在弄

### 27 楼

xtb今天这回更新居然又把输出格式给改了！

害得我又更新了一次脚本。现在本文的脚本已更新为对应2019-Apr-18的xtb了，不兼容老版本

这么折腾下去我要吐血了，这已经是为了兼容xtb第四次改脚本了！

### 28 楼

求助：按照sob老师的教程编辑了用户目录下的.bashrc文件，出现了以下问题，该如何解决：

bash: /yyh/Downloads/xtb-190318/Config_xtb_env.bash: 没有那个文件或目录

### 29 楼

447951397 发表于 2019-4-23 11:43

求助：按照sob老师的教程编辑了用户目录下的.bashrc文件，出现了以下问题，该如何解决：

bash: /yyh/Downl ...

仔细检查路径

有那个文件存在自然就没有这个报错

### 30 楼

sobereva 发表于 2019-4-24 02:56

仔细检查路径

有那个文件存在自然就没有这个报错

感谢sob老师，确实是路径出了问题，问题已经解决

### 31 楼

本帖最后由 fallleave 于 2019-5-23 21:14 编辑 



发现只要gaussian输入文件中含Pt原子，一运行gaussian就会报错。

### 32 楼

fallleave 发表于 2019-5-23 16:32

发现只要gaussian输入文件中含Pt原子，一运行gaussian就会报错。

写上UGBS关键词即可。这点我刚刚添加到本文文末了

### 33 楼

是在external后面写上UGBS吗？比如这样写：#P opt(ts,calcfc,noeigen,nomicro) external='./xtb.sh'/UGBS

### 34 楼

fallleave 发表于 2019-5-24 08:20

是在external后面写上UGBS吗？比如这样写：#P opt(ts,calcfc,noeigen,nomicro) external='./xtb.sh'/UGBS

诸如#P opt(ts,calcfc,noeigen,nomicro) UGBS external='./xtb.sh'

### 35 楼

非常感谢sob老师。

### 36 楼

@Sobereva 卢老师，请教您一个问题，在单独使用xtb计算结合能的时候需不需要考虑bsse？xtb有没有基组的概念呀。谢谢老师！

### 37 楼

lichengqiao 发表于 2019-5-29 11:30

@Sobereva 卢老师，请教您一个问题，在单独使用xtb计算结合能的时候需不需要考虑bsse？xtb有没有基组的概念 ...

基组是方法自定义的

不用考虑BSSE

### 38 楼

请教sob老师，我在安装xtb时遇到问题，搜索论坛帖子后未发现相关内容，因而打扰您了。我下载xtb后，按照http://sobereva.com/421的描述，解压到/home/programe/bin/xtb目录，然后到用户目录下vi ./basrc，在末尾加入了“source /home/program/bin/xtb/Config_xtb_env.bash”这句，退出编辑后source ./basrc。然后输入xtb命令，提示“segmentation fault”。我google了一下，得知这是“段错误”，但不知如何解决。尝试用root登录修改/home/programe/bin/xtb目录及其中所有文件的权限，设为777，仍然提示该错误信息。求教问题出在哪里，谢谢！

### 39 楼

vigaryang 发表于 2019-7-19 13:47

请教sob老师，我在安装xtb时遇到问题，搜索论坛帖子后未发现相关内容，因而打扰您了。我下载xtb后，按照htt ...

文中说了，还有其它要做的事，诸如ulimit

### 40 楼

sobereva 发表于 2019-7-19 23:55

文中说了，还有其它要做的事，诸如ulimit

感谢回复。我将文中提到的其它命令添加之后，运行xtb仍然提示segmentation fault。下面是我.bashrc文件中的相关部分：



###for xtb env

source /home/program/bin/xtb/Config_xtb_env.bash

export OMP_NUM_THREADS=8

export MKL_NUM_THREADS=8

export OMP_STACKSIZE=1G

ulimit -s unlimited

#

### 41 楼

vigaryang 发表于 2019-7-20 14:36

感谢回复。我将文中提到的其它命令添加之后，运行xtb仍然提示segmentation fault。下面是我.bashrc文件中 ...

可能和操作系统兼容有问题，没有更多信息说不清楚。换个机子/系统再试

### 42 楼

sobereva 发表于 2019-7-21 01:29

可能和操作系统兼容有问题，没有更多信息说不清楚。换个机子/系统再试

非常感谢sob老师。应该是您所说的原因。我在提问时所用的操作系统是SUSE，一直不能运行。后来改用虚拟机上的CentOS，就可以成功运行了。

### 43 楼

请问老师，运行中出现了Generating mol.tmp和Generating mol.xyz via genxyz，但之后出现错误“./xtb.sh: line 22: bc: command not found”。用的是xtb-190806版本。

### 44 楼

dingniu2 发表于 2019-8-12 17:25

请问老师，运行中出现了Generating mol.tmp和Generating mol.xyz via genxyz，但之后出现错误“./xtb.sh: l ...

这是你的操作系统的问题，没有bc命令

### 45 楼

给本文提供的接口做了一个英文页面：http://sobereva.com/soft/gau_xtb

引用的方式也有所改变，请注意本文第0节的说明

### 46 楼

星斗如盘 发表于 2021-6-7 12:12

在linux虚拟机中使用xtb的接口，报错的原因是什么呢？输入文件为里面的示例文件

xtb没装好，没法通过xtb命令调用xtb程序

### 47 楼

老师，想请问过渡态是只要有且只有一个虚频就可以吗，对大小有要求吗？

### 48 楼

xxzj 发表于 2021-10-27 13:13

老师，想请问过渡态是只要有且只有一个虚频就可以吗，对大小有要求吗？

如果特别小（比如绝对值小于50 cm^-1），可以考虑加大格点之类的确认一下，看看是不是数值误差导致的假虚频。

如果特别大（比如绝对值大于3000 cm^-1），建议检查一下是不是计算有问题，比如没收敛之类的。

除此之外对大小没有要求

### 49 楼

xxzj 发表于 2021-10-27 20:13

老师，想请问过渡态是只要有且只有一个虚频就可以吗，对大小有要求吗？

大小不是判断过渡态合理性的依据

以唯一虚频的振动方向来判断是否是你想要的

### 50 楼

sobereva 发表于 2021-10-28 10:47

大小不是判断过渡态合理性的依据

以唯一虚频的振动方向来判断是否是你想要的

收到，谢谢老师

### 51 楼

wzkchem5 发表于 2021-10-27 20:30

如果特别小（比如绝对值小于50 cm^-1），可以考虑加大格点之类的确认一下，看看是不是数值误差导致的假虚 ...

好滴，感谢老师

### 52 楼

本帖最后由 鱿鱼起司 于 2021-11-9 16:37 编辑 



老师，我在联用时出现了l402报错，具体细节如下。

高斯版本为G16 B.01，gau_xtb为在centos系统上直接下载的最新版，xtb分别尝试了6.4.1(最新版）、6.3.1、6.2.3，测试三个版本均可正常跑xtb的opt任务。

在使用例子中TS.gjf进行连用测试时，TS.out文件末尾如图片（与xtb的三个版本联用报错一样，图片为与xtb6.4.1版本联用out文件的截图）：



请问老师，该怎么处理，还是G16版本无法联用？

### 53 楼

本帖最后由 鱿鱼起司 于 2021-11-10 08:47 编辑 

鱿鱼起司 发表于 2021-11-9 16:36

老师，我在联用时出现了l402报错，具体细节如下。

高斯版本为G16 B.01，gau_xtb为在centos系统上直接下载 ...

老师，解决了，之前报错是因为没给几个文件加权限。

### 54 楼

鱿鱼起司 发表于 2021-11-9 16:47

老师，解决了，之前报错是因为没给几个文献加权限。

6.4.1不行吧，6.3.3是可以的

### 55 楼

喵星大佬 发表于 2021-11-9 17:33

6.4.1不行吧，6.3.3是可以的

我这用着没报错

### 56 楼

I would like to read the mentioned articles in this post, what's their DOI ?

### 57 楼

本帖最后由 vitalys 于 2022-1-25 03:00 编辑 



thank you very much for the wonderful tutorial, but the process doesn't work in Windows OS, despite I'm using Cygwin, and I get the following error:






XTB.JPG (196.47 KB, 下载次数 Times of downloads: 143)

下载附件 Download



2022-1-25 02:58 上传 Uploaded










How can I solve this issue ?

### 58 楼

vitalys 发表于 2022-1-25 02:59

thank you very much for the wonderful tutorial, but the process doesn't work in Windows OS, despite  ...

Please use Linux, or install Linux guest system under VMware

### 59 楼

请问卢老师，这个接口可以做大分子体系使其中一部分使用xtb去算，另外重要的部分使用b3lyp/def2tzvp这样的组合去算吗

### 60 楼

nianbin 发表于 2022-4-7 15:49

请问卢老师，这个接口可以做大分子体系使其中一部分使用xtb去算，另外重要的部分使用b3lyp/def2tzvp这样的 ...

不能

记得论坛里有个Gaussian的ONIOM结合xtb的脚本也许适合你

### 61 楼

Novice 发表于 2019-3-13 20:45

同时安装了Multiwfn和XTB，添加了环境变量export OMP_STACKSIZE=1000m后，在运行时出现了如下提示：

OMP_S ...

不用管

### 62 楼

这个接口可以只进行几何优化吗？我应该对xtb.sh进行修改吗？

### 63 楼

hanlan8702 发表于 2022-10-23 17:34

这个接口可以只进行几何优化吗？我应该对xtb.sh进行修改吗？

本来这接口直接就能用于调用xtb算受力做几何优化

### 64 楼

请问sob老师，是否可以通过Gaussian的External功能进行MECP搜索？

我的想法是，从其他程序获得梯度，换算成f+g，然后作为受力传递给Gaussian用于更新结构。

能量差作为能量传给Gaussian，不过此时收敛标准没法设为能量差接近于0，不过应该可以在External里进行处理，一般比较难收敛的应该也不是能量差。

（主要是懒得自己写一个优化器了233）

### 65 楼

Kalinite 发表于 2022-10-25 18:16

请问sob老师，是否可以通过Gaussian的External功能进行MECP搜索？

我的想法是，从其他程序获得梯度，换算 ...

我觉得希望不大，或者就算成功了，优化效率可能也很低。

### 66 楼

sobereva 发表于 2022-10-26 14:24

我觉得希望不大，或者就算成功了，优化效率可能也很低。

我试了下，感觉效果确实不行，特别是能量差一直徘徊在0.01-0.02au左右，没有明显降低的趋势（~50 steps）。但是Harvey的文章里提到使用最陡下降法优化MECP是比较高效的：

With a simple to implement steepest descent method, the geometry can be rapidly (10-15 steps) converged, at least within chemical accuracy.

如果只给Gaussian External提供能量和梯度，优化时使用的似乎也正是最陡下降法。这里效率很低的原因是什么呢？老师有兴趣分享一下sobMECP的细节吗。

### 67 楼

Kalinite 发表于 2022-10-30 19:06

我试了下，感觉效果确实不行，特别是能量差一直徘徊在0.01-0.02au左右，没有明显降低的趋势（~50 steps） ...

sobMECP代码都提供了，看一下就知道，就是很简单的优化算法，没多少行

### 68 楼

不知道有沒有人提過, 似乎這個聯用也可以做 opt freq 的任務, 但需要適應設置 path variable, 讓 external = ./xtb.sh 變成 external = xtb.sh , 這樣就可以 opt freq 一起做。我懷疑是因為 Gaussian 沒法識別 ./ 的部分, 才會令後面的 freq 任務失敗

### 69 楼

星斗如盘 发表于 2021-6-7 12:12

在linux虚拟机中使用xtb的接口，报错的原因是什么呢？输入文件为里面的示例文件

我用xtb6-5-1也出现了这个问题，应该是不兼容的原因。

### 70 楼

本帖最后由 啊不错的飞过海 于 2022-12-2 19:56 编辑 



2022年7月发布的xtb 6.5.1似乎是有了预编译Windows版了？主楼1.1提了一嘴xtb之前没有预编译Windows版的事，可以考虑下一版本更新一下情况。

==========

似乎仍然需要编译，只是压缩包命名和linux预编译版一致。

### 71 楼

啊不错的飞过海 发表于 2022-12-2 19:20

2022年7月发布的xtb 6.5.1似乎是有了预编译Windows版了？主楼1.1提了一嘴xtb之前没有预编译Windows版的事， ...

官方windows的预编译版早就有了，有一些bug，比如莫名其妙中断，我很不推荐使用

### 72 楼

请问linux 系统里直接执行xtb的时候，怎么让他后台运行, 而不是在屏幕上输出？  类似于gaussian 里面 &的命令，谢谢

### 73 楼

avatar_man 发表于 2023-1-6 09:19

请问linux 系统里直接执行xtb的时候，怎么让他后台运行, 而不是在屏幕上输出？  类似于gaussian 里面 &的命 ...

命令行后头用>把输出信息重定向到一个文件里，同时末尾加上&在后台运行

### 74 楼

请问老师，在高斯调用xtb计算时虽然能正常计算，但是一直在屏幕上循环输出下面的语句，这个如何解决呢？

OMP: Warning #182: OMP_STACKSIZE: ignored because KMP_STACKSIZE has been defined

normal termination of xtb

### 75 楼

PESPES 发表于 2023-7-21 10:58

请问老师，在高斯调用xtb计算时虽然能正常计算，但是一直在屏幕上循环输出下面的语句，这个如何解决呢？

O ...

不用管

用unset命令去掉KMP_STACKSIZE环境变量的定义也可以

### 76 楼

sobereva 发表于 2023-7-21 22:03

不用管

用unset命令去掉KMP_STACKSIZE环境变量的定义也可以

在xtb.sh 中添加了unset KMP_STACKSIZE语句，OMP: Warning #182: OMP_STACKSIZE: ignored because KMP_STACKSIZE has been defined这行不显示了，但是normal termination of xtb依旧在屏幕上循环输出，这个该怎么解决呢。

### 77 楼

PESPES 发表于 2023-7-23 16:06

在xtb.sh 中添加了unset KMP_STACKSIZE语句，OMP: Warning #182: OMP_STACKSIZE: ignored because KMP_ST ...

自己改脚本，把xtb显示的这种信息重定向到/dev/null里避免显示

### 78 楼

sobereva 发表于 2023-7-23 23:48

自己改脚本，把xtb显示的这种信息重定向到/dev/null里避免显示

xtb mol.xyz --chrg $charge --uhf $uhf --hess --grad > xtbout 2>&1 进行了如下修改，程序运行后在屏幕上不显示了。谢谢sob老师

### 79 楼

请问我用genmer产生了200个团簇构象，再用xtb优化，但是只优化一个结构就结束了怎么回事呀？

命令：xtb 200_Fe3O4.xyz --gfn 1 --opt tight -c 0 -u 5

### 80 楼

WOOOOWOOOO 发表于 2023-11-26 11:26

请问我用genmer产生了200个团簇构象，再用xtb优化，但是只优化一个结构就结束了怎么回事呀？

命令：xtb 20 ...

xtb又不会自动给你优化里面每一帧的结构，当然得用molclus调用xtb

### 81 楼

WOOOOWOOOO 发表于 2023-11-26 11:26

请问我用genmer产生了200个团簇构象，再用xtb优化，但是只优化一个结构就结束了怎么回事呀？

命令：xtb 20 ...

看卢老师博文《使用Molclus结合xtb做的动力学模拟对瑞德西韦(Remdesivir)做构象搜索》

技巧：利用crest程序节约xtb批量优化大量结构阶段的耗时



在前面文章中我们看到，Molclus结合xtb可以快速对xyz文件里记录的大批量结构进行快速优化。实际上这个阶段还可以明显节约时间，也就是利用crest程序。crest可执行程序在xtb的github页面上就能下载到。Molclus调用xtb时是对traj.xyz文件里的结构一个接一个来优化的，xtb在执行时是用OMP_NUM_THREADS环境变量指定的线程数做并行计算。而crest调用xtb来优化时，会同时启动OMP_NUM_THREADS个xtb程序同时对输入的xyz里的结构进行批量优化，每个xtb都只用单线程。crest这种方式调用xtb做批量优化的总耗时明显更低。



具体来说，运行以下命令就可以在GFN0-xTB级别下用normal几何优化收敛限（这是xtb默认的收敛限）对traj.xyz里所有结构进行优化：

/sob/crest -mdopt traj.xyz -gfn0 -opt normal -niceprint

其中/sob/crest是crest可执行文件路径，-niceprint代表计算过程中显示进度条。还可以用-chrg指定体系净电荷数，-uhf指定自旋，-g [溶剂名]指定溶剂模型。



计算完毕后在当前目录下得到了crest_ensemble.xyz文件，记录了优化后每一帧的结构和能量。从Molclus 1.9.3版开始，自带的isostat工具也能处理这个文件，当发现文件名里面有crest字样的时候就会自动以crest_ensemble.xyz文件的格式来读取内容，然后进行去重、排序并得到cluster.xyz。



用此做法对本文例子里高温MD跑完后的2000个结构用此方法优化，在笔者的Intel 36核机子上只花了11分钟，比起用Molclus调用xtb优化的时间节约了一个数量级。类似地，之后用GFN2-xTB在水模型下批量优化的那个阶段也可以借用crest来显著降低耗时。

### 82 楼

sobereva 发表于 2023-11-26 20:12

xtb又不会自动给你优化里面每一帧的结构，当然得用molclus调用xtb

好的，老师，谢谢您。还有个问题我想请教一下您，我是在做单个四氧化三铁团簇的构象搜索，用的是Fe.xyz和O.xyz，分别为3和4个。但是genmer产生的结构质量很差，用molclus调用xtb去优化由于结构过于离谱优化100来个程序就崩溃了。请问在用genmer产生初始的结构时有什么建议吗？要做一些什么约束呢？

### 83 楼

WOOOOWOOOO 发表于 2023-11-26 22:34

好的，老师，谢谢您。还有个问题我想请教一下您，我是在做单个四氧化三铁团簇的构象搜索，用的是Fe.xyz和 ...

说清楚什么程序崩溃

molclus调用xtb优化，在优化过程中不收敛，不可能导致molclus崩溃

### 84 楼

本帖最后由 WOOOOWOOOO 于 2023-11-27 10:50 编辑 

sobereva 发表于 2023-11-27 02:14

说清楚什么程序崩溃

molclus调用xtb优化，在优化过程中不收敛，不可能导致molclus崩溃

xtb。您翻到s开头的附件后面有很多的 Error: Cannot find .xtboptok file! The task is failed! 文本末尾显示srun: error: g0503: tasks 0-11,13-23: Killed

我在论坛里搜了一下这个问题，看了环境配置都是对的，xtb.out也没看出来啥问题。我跑了您在一个文章中的6个Li的团簇搜索，完全没问题。麻烦您看看我这个是啥问题。

### 85 楼

WOOOOWOOOO 发表于 2023-11-27 10:38

xtb。您翻到s开头的附件后面有很多的 Error: Cannot find .xtboptok file! The task is failed! 文本末尾 ...

                         *** Configuration     4  ***

 Current date: 2023-11-27   Time: 10:13:57

 Loading geometry         4 from the inputted trajectory file

 Wall clock time elapsed for calculating this configuration:       6 s

 Wall clock time elapsed for calculating this configuration:       5 s





                         *** Configuration     3  ***

 Generating xtb.xyz file...

                         *** Configuration     4  ***



诸如以上信息都是错乱的，明显并行方式不当，肯定是同时运行了多个molclus进程，输出信息搅合在一起，结果能正常就怪了，运行效率不巨低就怪了

### 86 楼

Is it possible to use the generated checkpoint file from optimisation (mol.chk) to run a DFT calculation (at B3LYP for ex) ? (I mean read geometry and wave function),

because i tried and didn't work.

### 87 楼

maximos 发表于 2024-9-4 18:51

Is it possible to use the generated checkpoint file from optimisation (mol.chk) to run a DFT calcula ...

The chk file produced by this Gaussian+xtb running may be used to provide geometry for subsequent DFT calculation, but this running cannot provide wavefunction as initial guess for subsequent DFT calculation.

### 88 楼

Dear Professor,

If we want to consider the solvent, what should we do ? add the solvent using Gaussview "ex scrf=(solvent=thf)", or add solvent to xtb code using --gbsa ? what's best

### 89 楼

zako 发表于 2024-9-5 20:04

Dear Professor,

If we want to consider the solvent, what should we do ? add the solvent using Gauss ...

It should be the latter. During the calculation process, Gaussian only acts as an optimizer, and all energy-related calculations are performed by the external program pointed to by the external keyword, so the energy-related settings are also external.

### 90 楼

zako 发表于 2024-9-5 20:04

Dear Professor,

If we want to consider the solvent, what should we do ? add the solvent using Gauss ...

You should add option for xtb code like that you mentioned.

### 91 楼

社长，威武，

### 92 楼

sob老师好，我想问一下，用您这个方法是不是可以对找过渡态的过程实现类似”构象搜索”的作用？

最近有一个体系，我发现不同初始结构执行opt=(calcall,ts,noeigen)竟然可以得到两个结构相似的过渡态。两个过渡态都符合唯一虚频，IRC也都能向产物和反应物两个方向跑通，但是自由能上存在差异。

不知道是不是因为反应涉及质子转移，这种的感觉有点像“构象”不同的情况。请问用您这的这个方法可以把所有能跑通的鞍点尽可能都搜寻出来吗？还是只能依靠经验去不断手动调整初始模型来尝试搜索出能量最低的鞍点？

### 93 楼

本帖最后由 陈AG 于 2026-1-21 14:20 编辑 



老师，我用xtb找到过渡态之后（只有一个虚频且方向正确)，

#p opt=(calcfc,ts,noeigen,nomicro,maxstep=5) external='./xtb.sh' NOSYMM ugbs

#p freq geom=allcheck external='./xtb.sh' NOSYMM ugbs，

然后想在想在DFT级别下计算一遍

#p opt=(rcfc,ts,noeigen,maxstep=5) PBE1PBE GENECP freq em=gd3bj geom=check NOSYMM

计算正常结束但是虚频方向不对了，这是为啥呢

### 94 楼

陈AG 发表于 2026-1-21 14:17

老师，我用xtb找到过渡态之后（只有一个虚频且方向正确)，

#p opt=(calcfc,ts,noeigen,nomicro,maxstep=5) ...

有的时候化学直觉设想的过渡态，实际上未必存在，这是正常的；不该存在的过渡态在低级别下碰巧存在，这也是正常的。此外，也有可能DFT级别下也存在正确的过渡态，但和xtb的过渡态差别很远，导致以xtb过渡态为初猜无法收敛到DFT过渡态。第三种可能是你的过渡态因为协同异步等原因，虚频方向不符合化学直觉，此时只要IRC结果正确，仍可以说这个过渡态是正确的

### 95 楼

ginlpein 发表于 2026-1-21 01:59

sob老师好，我想问一下，用您这个方法是不是可以对找过渡态的过程实现类似”构象搜索”的作用？

最近有一 ...

这一点有成熟的解决方案，就是在限定特定键长的情况下做构象搜索。参见https://www.koushare.com/video/details/192997

### 96 楼

wzkchem5 发表于 2026-1-21 14:53

有的时候化学直觉设想的过渡态，实际上未必存在，这是正常的；不该存在的过渡态在低级别下碰巧存在，这也 ...

感谢老师回答，因为文章有类似的结构做过，这个虚频应该是没问题的，我在想是不是做DFT级别的时候用rcfc是读取了xtb的hessian结果，所以出现了这个情况

### 97 楼

本帖最后由 ginlpein 于 2026-1-21 17:50 编辑 

wzkchem5 发表于 2026-1-21 14:54

这一点有成熟的解决方案，就是在限定特定键长的情况下做构象搜索。参见https://www.koushare.com/video/d ...

感谢王老师的回复，

按您视频中的讲法，我的理解是把认为反应相关的局部冻住，然后其余部分搜索，最后挑出能量低的构象再做一次TS。

但是，如果把反应局部冻住的话，相当于默认进攻方式不变。但有时候反应中心涉及氢键变化与质子传递，氢键受体原子也是亲核反应进攻的中心原子(比如O，N，在过渡态中会出现氢键构成的“六元环”或“五元环”）。这种情况下可能会出现N种不同的进攻方式(大致就是氢键构成的多元环表现出不同构象)，也就是存在很多一阶鞍点。请问针对这类的情况，有没什么方法可以比较全面的一次性把所有鞍点找齐？

手动摆不同初始的办法，感觉很容易错过最低的那个鞍点，又容易摆了一堆初始最后都收敛到同一个位置导致无用功。



还是说类似亲核进攻的情况，只冻结进攻的电子给体原子与被进攻的电子受体原子这两个原子，其余部分全部放开进行MD搜索？

### 98 楼

陈AG 发表于 2026-1-21 15:04

感谢老师回答，因为文章有类似的结构做过，这个虚频应该是没问题的，我在想是不是做DFT级别的时候用rcfc ...

那就用DFT的Hessian再试一次就知道了

### 99 楼

ginlpein 发表于 2026-1-21 17:40

感谢王老师的回复，

按您视频中的讲法，我的理解是把认为反应相关的局部冻住，然后其余部分搜索，最后挑 ...

这个冻住局部，可以只冻结一两根键。如果冻结的方式不唯一，就分别跑多个不同的构象搜索任务，再写脚本汇总结果。例如亲核进攻一般只冻结正在形成的键和正在断裂的键（共两根键）即可

### 100 楼

ginlpein 发表于 2026-1-21 01:59

sob老师好，我想问一下，用您这个方法是不是可以对找过渡态的过程实现类似”构象搜索”的作用？

最近有一 ...

对过渡态的构象搜索在下文里说了

Molclus FAQ

http://sobereva.com/730（http://bbs.keinsci.com/thread-50349-1-1.html）

### 101 楼

sob老师好，我按博文方法运行程序后，中途查看任务没有收敛到过渡态，想kill掉正在运行的程序，但是xtb的PID号一直在变，没办法通过PID号kill程序，怎么办呢

### 102 楼

lkq1291127863 发表于 2026-2-13 12:07

sob老师好，我按博文方法运行程序后，中途查看任务没有收敛到过渡态，想kill掉正在运行的程序，但是xtb的PI ...

任务正在运行过程中也可以随时用gview打开输出文件看当前的状态

### 103 楼

本帖最后由 Stardust0831 于 2026-5-28 02:14 编辑 

啊不错的飞过海 发表于 2022-12-2 19:20

2022年7月发布的xtb 6.5.1似乎是有了预编译Windows版了？主楼1.1提了一嘴xtb之前没有预编译Windows版的事， ...

我用python重写了gau_xtb接口，不再依赖bash环境，可以用上xtb官方的windows预编译版在windows上联用gaussian来跑计算了。

详见：《跨平台实现gaussian与xTB程序联用搜索过渡态、产生IRC、做振动分析》

### 104 楼

elvisng 发表于 2022-12-2 11:21

不知道有沒有人提過, 似乎這個聯用也可以做 opt freq 的任務, 但需要適應設置 path variable, 讓 external  ...

我留意了这一问题。对于g16而言这样没问题；对于g09在跑完opt、开始freq的时候似乎会尝试去读chk里的波函数信息，而联用xTB的时候chk里并不会记录波函数，程序遂直接报错退出了。但—link1—的写法是能正常生效的，连跑还是有机会实现的。

./的“/”目前发现gview也不认识，可以换成bash xtb.sh这种写法，或者索性换python版的gau_xtb接口。

## 入库完整性评估

- 主帖全文收录
- 全部回复完整收录
