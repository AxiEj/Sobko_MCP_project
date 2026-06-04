---
post_id: 439
title: Gaussian的安装方法及运行时的相关问题
url: http://sobereva.com/439
date: '2018-09-05T07:18:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 标题直接是Gaussian安装与运行问题，属于典型软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

注：笔者在写这篇文章的时候，已经尽本人最大努力考虑到最初级的计算化学工作者理解能力的最底线，请睁大眼睛万分仔细一个字一个字过脑子地阅读本文5遍以上，只要理解能力正常的人100%能装上！如果还装不上，那么友情建议你及早改行成和计算模拟完全无关的领域，肯定能获得比搞计算化学更大的成果（也不要指望看网上其它文章就能装上，因为本文已经是网上关于装Gaussian的文章当中最详细的了）。

**Gaussian的安装方法及运行时的相关问题**

Installation method of Gaussian and issues related to running

文/Sobereva@[北京科音](http://www.keinsci.com)

 First release: 2018-Sep-5  Last update: 2026-Mar-27

Gaussian是目前最流行、用户最多的量化程序，从《2018年度计算化学公社杯最常用的量子化学程序和DFT泛函投票结果统计》（<http://sobereva.com/420>）的统计就可见一斑。很多初学者在安装Gaussian时总是遇到各种问题。网上有大量乌七八糟的关于安装Gaussian的中文资料，极少有完全正确的，严重毒害Gaussian初学者，导致他们绕了大量弯路。鉴于笔者答疑过程中关于安装Gaussian的问题出现频率很高，这里就说一下**最正确**的安装Gaussian的方法，以正视听，同时也说一些常见的相关问题。**如果你在网上看到的安装步骤与本文不同，那么要么有多余的步骤，要么是错误的**，导致配置完了之后Gaussian都没法完全正常运行。下文当中每一个空格都要看清楚，如果你视力太差看不清楚空格，可以从本文当中直接复制命令。

PS：如果你是几乎零基础想开始上手做量子化学计算的人，想最好、最快速、最系统、最正确地学怎么用Gaussian做量子化学计算，十分建议参加北京科音初级量子化学培训班，见<http://www.keinsci.com/KEQC>中的介绍和《谈谈学量子化学如何正确地入门》（<http://sobereva.com/355>）。

## 1 在Linux下安装和运行Gaussian

### 1.1 几个Linux常识

考虑到一些Gaussian使用者是Linux初学者，为便于他们顺利安装Gaussian，这里先普及几个常识。

关于shell：Linux下有很多种shell，诸如bash、csh、ksh等，相当于不同的文本终端的界面。不同的shell下一些命令不同，比如设置环境变量，在bash里用export命令，而在csh里用set命令。其中Bash是最常见的shell，也是大多数Linux系统默认的shell。如果你不确定你当前用的是什么shell的话，可以在Linux终端里输入echo $SHELL看显示的是什么。本文假定大家用的是bash，如果用的不是bash，也可以在终端里输入bash切换成bash shell。

关于用户主目录：Linux下每个用户都有自己的主目录。默认情况下，你以命令行方式登录系统后，你当前所在的目录就是用户主目录，可以敲pwd命令显示当前的目录。如果你是普通用户的话，那么主目录将为/home/[用户名]/。如果你是root的话，那么主目录就是/root/。

关于文件权限：Linux下每个文件都有称为权限的属性，可以用chmod命令来修改。权限包括是否可执行、是否可读取、是否可修改。比如chmod +x ./niconiconi就会把当前目录下的niconiconi加上可执行权限，再比如chmod 750 /sob/yoshiko.exe命令就会把/sob/yoshiko.exe文件设为750权限。这里750的百位数、十位数、个位数分别对应这个文件对于当前用户的权限、对于与当前用户同组用户的权限、对于其它组用户的权限。7对应完整的权限，即可执行、可读取、可写入，5代表可读取、可执行，而0代表所有权限都没有。更多关于chmod的知识请自行google。

关于.bashrc文件：每个用户主目录下都会有.bashrc文件，这是个文本文件，里面记录了当你每次登录bash shell的终端的时候都会自动执行的命令。因此如果有些命令你希望每次登录终端时都能生效，那么把命令写入.bashrc文件即可。.bashrc文件里有一些自带的内容，那些都不用管，自己加新的命令往此文件末尾添加即可。Linux下所有开头为.的文件都是隐藏文件，直接用ls命令看不到，而得用诸如ls -a才能看到。如果你是在系统自带的图形界面的文件浏览器下，得按一次Ctrl+H才能看到隐藏文件。显然，.bashrc文件也是个隐藏文件。

### 1.2 Gaussian的安装

假设当前用户名是sob，要把Gaussian安装到自己的主目录下，且用的是bash，那么安装过程为：

把Gaussian压缩包解压到/home/sob/目录下

建立一个文件夹用于储存Gaussian运行过程中产生的临时文件，位置随意。比如此例我们建立/home/sob/g09/scratch。

用vi或者gedit等文本编辑器打开/home/sob/.bashrc，在里面加入以下语句然后保存文件。  
export g09root=/home/sob  
export GAUSS_SCRDIR=/home/sob/g09/scratch  
source /home/sob/g09/bsd/g09.profile  
其中，g09root环境变量用来说明Gaussian目录被放在了哪个目录下。GAUSS_SCRDIR环境变量用来说明哪个文件夹作为临时文件夹。source命令用来执行Gaussian自带的脚本文件，其中包含了各种配置Gaussian运行环境的命令。

重新进入终端使以上内容生效（如果你是用Linux图形环境，就关闭终端窗口，然后重新打开。如果你是通过ssh方式登录服务器，就断开连接，然后重新连接服务器）

Gaussian目录下的Default.Route用来设定默认用的计算资源（如果没有此文件就新建一个），-M-设置默认用的最大内存量（一般用MB或GB为单位，也可以用MW和GW，1MW=8MB、1GW=8GB），-P-设置默认用多少CPU核数来并行计算。比如我们想默认用36个核心、最大60GB内存做计算，就在/home/sob/g09/Default.Route里面写入以下内容  
-M- 60GB  
-P- 36  
此文件中的设置优先级低于输入文件里的%mem和%nproc设置。因此，输入文件里没写%mem的时候才会用这里的-M-设置，输入文件里没写%nproc的时候才会使用这里的-P-设置。如果你既没在这里设-P-也没写%nproc，那么程序只用单核计算。如果你既没在这里设-M-也没写%mem，那么G09最多用256MB内存，G16最多用800MB内存（注：值得一提的是G16 C.01有bug，Default.Route里的-M-不生效，必须自己靠%mem方式定义内存。其它版本Gaussian没这个问题）。

最后，切换到/home/sob/g09/目录，运行chmod 750 -R *命令，之后Gaussian就可以使用了。这里-R *代表对当前目录下所有文件和所有子目录下的文件都设置权限。

如果你用的是Gaussian 16，只需把上面过程中所有g09改成g16即可，其它没有任何差别。

友情提示：默认情况下，当Gaussian任务运行中途中断，在GAUSS_SCRDIR环境变量设的临时文件夹里就会残留当前运行时生成的临时文件，文件名是任务的pid号。日积月累，可能此目录下的残留的临时文件体积会巨大，把硬盘占满，导致之后的各种Gaussian任务运行一开始就失败。因此，建议定期把临时文件夹里的内容清空，但不要在有任务运行的时候清理（或者，至少清理的时候别清掉当前任务对应的临时文件。用top或ps命令可以查看pid号）。

PS 1：网上一些乌七八糟的介绍安装Gaussian的文章中还说要设定PATH、LD_LIBRARY_PATH、GAUSS_EXEDIR之类的环境变量，这是完全多余的。打开g09.profile看一眼就知道，这些环境变量在profile文件里都会自动设好，因此按照前文source一遍.profile文件就完事了，根本没有丝毫必要手动去设那些环境变量。本文介绍的绝对是步骤最少而且最正确的安装步骤。

PS 2：如果要在集群中给所有用户安装公用的Gaussian，可参考<http://bbs.keinsci.com/thread-14301-1-1.html>。

### 1.3 Gaussian在Linux下运行的命令

这里顺便提一下Gaussian在Linux下的运行方法。常见有以下几种，test.gjf是输入文件  
g09 < test.gjf > test.out    （信息都输出到test.out里。末尾可以再加上&令任务在后台运行）  
g09 < test.gjf |tee test.out （信息输出到test.out的同时也同时输出到屏幕上）  
g09 test.gjf  （输出文件将默认为当前目录下的test.log）

以上面第1种或第3种方式运行时，如果你又想把输出信息在屏幕上不断同步显示了，那么可以运行tail -f test.out。

使用SSH远程登录服务器时，如果提交了Gaussian任务，则与服务器连接中断后任务也相应地中断。为了能让任务在断开连接后也能一直在服务器上继续跑完，提交任务时应当写  
nohup g09 < test.gjf > test.out &  
并且退出时要用exit命令先优雅地断开连接，而不要直接关终端。这样任务就会在服务器上继续跑直到完成。

从G16开始，如果在gjf里没定义%nprocs、%cpu、%mem，也可以在运行命令里方便地直接指定，比如  
g16 -p=16 -m="40GB" < love.gjf > love.out  
相对于定义了%nprocs=16和%mem=40GB。再比如  
g16 -c="0-47" < live.gjf > live.out  
相对于定义了%cpu=0-47只在第0~47号CPU核心上计算。命令行里直接指定参数的优先级高于Default.Route。

### 1.4 Gaussian运行的几个常见问题

**(1)运行时提示files in the gaussian directory are world accessible. this must be fixed**  
这说明你没做chmod 750 -R *这一步。Gaussian如果发现其可执行文件对于所有用户都可以访问时就不干，这是Gaussian的一个莫名其妙、很固执的地方。

**(2)运行时提示Error: illegal instruction , illegal opcode**  
这说明Gaussian和你的CPU不兼容，确切来说，是你的CPU太老，不支持Gaussian在开发者编译程序的时候使用的指令集。比如Gaussian 16有利用较新的AVX2指令集的版本，也有不利用AVX2指令集的版本，前者运行速度更快。如果你用的是前者，而你的CPU较老，比如是XEON v3及之前系列的服务器CPU，或者你用的是Intel的消费级的CPU而型号是3xxx及之前的，由于不支持AVX2指令集，运行就会报上面的错误。解决方法就是购买非AVX2版的Gaussian 16或者换机子。PS：什么CPU支持什么指令集，可以去看我的硬件资料库（<http://sobereva.com/datasheet.rar>），对于Intel的CPU也可以去查Intel ARK（<https://ark.intel.com/>）。

还有一种情况是你用的是较新的AMD的CPU，比如ZEN2架构的，虽然支持相应的指令集，但由于编译器与CPU架构之间的兼容问题导致以上报错。可尝试在运行Gaussian前通过这行命令定义环境变量：export PGI_FASTMATH_CPU=sandybridge。

**(3)运行时该用多少CPU核心？**  
 如果你的机子打算只跑一个Gaussian任务，那么一般建议CPU有多少物理核心就用多少核数来并行，这样通常最快。若有额外CPU核心闲着也是白白浪费。注意，对于采用了超线程(HT)技术的CPU而且管理机子的人没有把超线程关闭的话，逻辑核心数会是物理核心数的两倍。如果你搞不懂这一点，务必看《正确看待超线程(HT)技术对计算化学运算的影响》（<http://sobereva.com/392>）。比如，如果你的机子是双路2696v3 CPU，一共有36个物理核心，对应72个逻辑核心，而且你平时只跑一个Gaussian任务，那么Default.Route里的-P-或者输入文件里的%nprocs后面应该写36。

有一个特例是当你跑的任务特别小，比如就是10个原子左右的很小分子在很廉价的B3LYP/6-31G*下做柔性扫描，亦有可能分配诸如96核时反倒比分配16核时更慢。情况实测便知。

计算速度和使用的核数绝对不是理想的线性的正比关系。并行的核数越多，继续增加核数使速度提升的幅度就越低，对越是便宜的计算任务这点越明显。对于Gaussian 16，并行核数用到50核左右就接近速度的极限了，继续提升的余量看具体计算任务。即曰，虽然并行核数越多总耗时越低（不排除极个别例外），但并行效率越低。所以，如果CPU的核数很多，比如你用的是一个2*48=96个物理核心的双路服务器，同时用跑两个48核并行的任务远比跑一个96核的任务更能充分发挥CPU的性能。注意同时跑两个任务时建议把两个任务用%cpu分别绑定在两个不同CPU上以减少资源争抢拖慢速度，详见《淘宝上购买的双路EPYC 7R32 96核服务器的使用感受和杂谈》（<http://sobereva.com/653>）第6节关于跑Gaussian部分的文字。如果机子核数特别多，比如是128核服务器，有大量任务要跑，那么还可以同时跑4个乃至8个任务，CPU利用程度会更充分。注意所有Gaussian任务调用的核数的总和不要超过机子的物理核心数，且分配给各个任务的可用内存量的总和不能超过空余物理内存量。还要注意有些任务，比如后高阶的HF，不仅特别耗内存，而且读写硬盘量往往非常大，这样的任务别一次跑好几个，要不然可能内存不够直接崩溃，或者在硬盘读写上严重争抢，导致哪个任务都巨慢。

当设定的并行核数超过64时，对于Gaussian 16 B.01及之前的版本来说，Gaussian可能一上来就会报错。解决办法是在~/.bashrc里添加比如export OMP_THREAD_LIMIT=256，这样就把并行核数上限提升到256了，因此就可以使用超过64核并行了。

**(4)运行时该分配多少内存？**  
Gaussian里同一个任务可能有不同算法，有的速度快但是耗内存高，有的算法速度慢但是耗内存少，如果你的内存给得足够大，Gaussian往往会自动选择速度最快的算法。而且对于有的算法，当可用内存较大时，计算量就会较小。因此，一般建议是有多少空余物理内存，就分配多少内存给Gaussian。何况，有些任务本身就特别耗内存，内存分配小了则Gaussian根本没法完整执行完此任务，或者程序会自动降低并行线程数来降低内存消耗，使得任务在有限的内存量下得以算完，但显然会因此导致耗时增加。如果你的机子里打算只跑一个Gaussian任务，那么把实际物理内存量中扣除一部分分配给操作系统和后台任务的，其余部分都给Gaussian即可。为稳妥起见，我建议把90%左右的物理内存分配给Gaussian。如果内存分配量超过了空余物理内存，将导致程序运行一开始就会报错，或者程序可能会试图使用虚拟内存（即把相对来说速度很慢的硬盘虚拟成内存来用）而导致计算速度被严重拖慢。如果你要跑多个Gaussian任务，那么所有任务分配的内存量的总和不应当超过空余物理内存量。

给Gaussian分配的内存量是Gaussian对内存使用量的上限，不是说分配多少就都会被占满。诸如普通泛函的DFT单点任务（假设以默认的direct SCF方式运行时），由于其算法原因，注定就占不了什么内存，所以你分配200GB可能实际也只会占用300MB。

PS：有兴趣的读者不妨看看《硬盘速度与内存容量对量子化学计算速度影响的测试》（<http://sobereva.com/397>），里面有一些关于内存分配量对计算速度影响的测试。

我老看到有初学者，不知道是什么逻辑，做Gaussian计算时分配的内存量超级吝啬！常看到有人比如用36核做计算，内存只分配少得可怜的10GB甚至6GB，非常莫名其妙！有36核的机子的物理内存总量怎么可能连64GB都没有？**机子里那么多的空余内存不利用起来留着干嘛？**明明把更多的内存给Gaussian不仅没害处，还往往能加快计算，干嘛偏偏就只给一点点内存？到底在想什么？最最最最起码，用N核并行，也理应给不少于N GB内存，否则且不说速度，对很多耗内存略多的任务就连正常算完都做不到。而对于跑耗内存很多的任务，比如大体系的DFT的振动分析、CCSD(T)结合不小基组计算不小体系，应当在内存较大的机子上做计算（建议物理内存总量大于CPU物理核心数乘以4 GB），并且按上文说的把内存都尽可能多地分配给Gaussian。

**(5)如何在机子里令Gaussian 09和16并存？**  
比如你把g09和g16都放在了/home/sob下，为了能够令g09和g16都有可能被使用，你可以在.bashrc文件中加入比如以下内容  
export g09root=/home/sob  
source /home/sob/g09/bsd/g09.profile  
#export g16root=/home/sob  
#source /home/sob/g16/bsd/g16.profile  
export GAUSS_SCRDIR=/home/sob/g09/scratch  
其中#用来注释，因此凡是前头带#的行，说明此行在当前情况下不生效。因此，当前情况只能用g09而不能用g16。如果你接下来想改用g16，那么就修改.bashrc文件，把g16对应的两行前头的#挪到g09对应的两行的开头，然后保存文件，重新进入终端，此时g09就没法用了，而g16则可以使用了。

由于g09和g16在一些运行环境的配置上是共通的，没有办法同时令g09和g16命令都可以正常使用。

PS：实际上，每次运行bash命令，也会把.bashrc文件里的信息执行一遍，但在前面的叙述中，都是通过重新进入终端来使.bashrc内的信息生效，因为这样做是最保险的。这是考虑到g09或g16.profile的某些命令可能是对环境变量里的内容进行追加，而不是重设。只有重新进入终端，那么当前的环境变量和只执行过一次profile里的配置命令才是相同的，才可以严格确保g09和g16不会在运行时候出现混乱。

**(6)我运行formchk命令，怎么提示找不到命令？**  
这说明你没有严格按照前文的方法配置Gaussian（可能你被网上的一些文章坑了）。

**(7)运行一开始提示此类报错怎么回事？**  
 Entering Gaussian System, Link 0=g09  
PGFIO/stdio: No such file or directory  
PGFIO-F-/OPEN/unit=11/error code returned by host stdio - 2.  
 File name = /sob/g09/scratch/Gau-75009.inp  
这说明GAUSS_SCRDIR环境变量所指向的路径（比如当前为/sob/g09/scratch）目前不存在，应当仔细检查路径。另外，如果GAUSS_SCRDIR环境变量指向的是一个虽然存在，但是你没有可读写权限的路径，Gaussian运行时由于没法创建临时文件，显然也会运行失败。

**(8)运行一开始报错galloc:  could not allocate memory**  
说明你设Gaussian内存使用量上限过大了，超过了实际可分配的内存量。虽然如前所述，不是你给Gaussian分配多少内存Gaussian就会实际用多少（计算过程中内存实际使用量可以在top命令里看），但是Gaussian会在计算一开始就向系统请求你设的内存量，如果发现没法分配那么多就直接报错。

**(9)Gaussian任务没有报错，但是却莫名其妙停了怎么办？**  
有以下可能原因  
1 巧合。尝试重算，或者尝试其它也能达到类似目的的关键词再试。也可以尝试重启计算机  
2 当前版本Gaussian的bug。尝试其它版本或其它操作系统的Gaussian  
3 当前Gaussian版本和计算机的软件环境有兼容性问题。可尝试其它版本或其它操作系统的Gaussian。对于Linux尝试装其它版本或其它发行版的Linux再试，对于Windows把各种安全防护程序都关掉乃至完全卸载再试（最坏的情况也可能需要重装操作系统）  
4 任务被bad people杀了。重算，如果发现的确是有人恶意杀了你的任务，找管理员告状  
5 任务被作业调度系统杀了（如超过了任务执行时间上限、内存最大使用量等原因），咨询计算机的管理员  
6 给Gaussian用的内存分配得不够。增大%mem或配置文件里的默认的内存设置（-M-）。也可能虽然内存分配得够，但当前计算机的空余物理内存不够导致没法成功分配那么多内存。还可能一开始空余物理内存够，但运行中途有其它程序占了过多内存导致Gaussian没法再利用足够的内存  
7 计算机硬件不稳定，检修或换成其它机子

## 2 在Windows下安装和运行Gaussian

Windows版Gaussian的安装很简单，启动安装程序，输入序列号，然后下一步下一步即可。注意绝对别把Gaussian装到带有中文的路径下，否则以后使用过程中可能会碰到一些莫名其妙的错误。比如把程序装到了D:\study\G09W下，那么安装后应当手动建立一个文本文件D:\study\G09W\scratch\Default.Rou，这个文件就是Windows下的默认的计算资源的配置文件，里面要填的内容和Linux下的Default.Route是完全相同的。

绝大多数人用的Windows版Gaussian都是32bit版的，主要是因为Win32版售价比Win64版便宜得多（这里不是指操作系统是多少位，而是Gaussian程序自身是多少位）。32bit版Gaussian在运行时对资源限制极大，并行核数最多只能设为4（实际上还有只支持串行运行的Windows版Gaussian，售价更便宜，但很少见），而且内存最多只能分配1500MB左右。我个人建议设成1400MB，因为设成1500MB的时候仍有可能在个别情况下因为内存分配问题而运行失败。如果想不受制于核数和内存的限制，那就得改用64bit版Gaussian了。除非是计算量较小的任务，否则运行的时候都应当用64bit版。  
注：目前的Linux版Gaussian一律都是64bit的，32bit版也根本不卖了，很老版本的Gaussian才有32bit Linux版。

Windows用户一般还会安装GaussView，这是Gaussian官方开发的Gaussian图形界面程序。记得一定要先安装Gaussian再安装GaussView，而且GaussView应当安装到与Gaussian相同的目录下，否则可能导致GaussView识别不到Gaussian可执行文件。此时不仅启动GaussView的时候会有警告，而且由于GaussView将没法调用Gaussian目录下的可执行程序，此时GaussView很多特性和功能将无法使用，比如无法载入chk文件、无法绘制分子轨道等值面、无法向Gaussian提交任务等。

应当注意Gaussian和GaussView的版本兼容性。根据笔者经验，Gaussian 09建议搭配GaussView 5.0.9使用，Gaussian 16建议搭配GaussView 6使用，这样兼容性是最好的，否则会有很多问题。比如GaussView 6.0.16打开Gaussian 09的IRC任务的帧号顺序是错乱的，而GaussView 5.0.9无法正确载入Gaussian 16的振动分析输出文件等。

启动Gaussian的Windows版的图形界面后，在File - Preference里会看到一些配置选项，一般不用去改。Windows版默认的Gaussian临时文件夹是其目录下的scratch目录，如果你想把临时文件目录改为其它路径，可以修改里面的Scratch Path设置。ASCII Editor设的是在Gaussian图形界面里打开输出文件时调用的文本编辑器，默认是记事本，如果你机子里有Ultraedit、notepad++等更强大的文本编辑器，建议改成这些文本编辑器的路径。

有些人在运行Windows版Gaussian时明明输入文件正确，计算任务计算量也很小，却在中途莫名其妙地卡住、出现莫名其妙的报错，这往往是因为机子里的360等垃圾山寨安全程序捣的鬼。把这些垃圾程序删掉往往就能解决。另外，笔者发现XEON v3（对于v4等其它型号可能也有）系列的一些CPU运行win32版Gaussian09/16时会失败，这应当是CPU和程序兼容性的原因，目前没有发现好办法解决（不过这不是什么大问题，一般也不会有人用几十核的服务器去跑win32版Gaussian）。

**使得Gaussian在Windows下能通过命令行使用的方法：**

Windows下Gaussian通常是通过图形界面使用的，但有时候需要在Windows下也能通过命令行调用，比如让Gaussian能够被Multiwfn调用自动做一些计算、使用《从高斯windows下的批量执行谈dos批处理文件》（<http://sobereva.com/6>）里提供的Windows下的批处理脚本批量执行Gaussian等情况。为此，在依照上面说的方式安装后，还需要做以下步骤（细节和Windows版本有关，应随机应变）：进入“高级系统设置”，点击“环境变量”按钮，在用户变量列表中选择Path环境变量，对其编辑，在里面加入Gaussian的目录如D:\study\G16W。之后再创建一个新的环境变量，名为GAUSS_EXEDIR，将之也设为Gaussian的目录如D:\study\G16W。之后点确定并退出环境变量设定界面即可。在此之后就可以用命令行方式执行Gaussian了，运行比如g16 test.gjf或者D:\study\G16W\g16.exe test.gjf（注意不要写成g16w.exe，带w后缀的只是Windows版Gaussian的图形界面），就会开始计算test.gjf，输出文件为当前目录下的test.out，并且临时文件也会产生在当前目录。注意以这种方式执行Gaussian时，如果不把Default.Rou拷到当前目录下，其中的设置不会生效，因此如果你不想拷这个文件，就要在gjf里直接写明%nproc和%mem设置。
