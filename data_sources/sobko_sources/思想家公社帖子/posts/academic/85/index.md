---
post_id: 85
title: 自写Link生成Gaussian的IRC任务中每个点的波函数文件
url: http://sobereva.com/85
date: '2015-06-07T23:48:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- 波函数分析
- 可视化
academic_relevant: true
classification_reason: 核心是通过 Gaussian 的 Link 机制生成 IRC 每一步的波函数文件。
topic_family: 软件
exclude_reason: ''
confidence: 0.99
image_count: 0
local_assets_dir: assets
---

**自写Link生成Gaussian的IRC任务中每个点的波函数文件**Write an own Link to generate wavefunction file for each point of IRC task of Gaussian  
  
文/Sobereva    2011-Apr-24

  
  

## 1 前言

在Gaussian的IRC任务，以及scan、优化等任务中，只有最后一步波函数才允许在任务结束时被l9999输出为PROAIM波函数文件。如果想要用外部工具，比如Multiwfn绘制这个过程中实空间函数（电子密度、ELF等）的动态变化过程，就必须获得每一步的波函数文件。为实现这个目的，最笨的方法是写个脚本，提取每一帧结构再做单点计算，显然这要多费很多时间。另一个办法是自行编写、修改link，然后篡改link的执行顺序，使波函数文件在每一步中都输出，这就避免了重算波函数。本文将首先介绍Gaussian的link的基本代码结构、编译方法，然后再谈怎么自写link来实现使IRC任务的每一步都能直接输出波函数文件。  
  
建议阅读本文前先阅读《Gaussian的Link、IOp与非标准计算路径》一文，见http://sobereva.com/57。并且下载《Gaussian 09 Programmer's Reference》以备用，最好把前58页读一遍。本文会直接提供编译好的link，如果读者想自行编译，必须拥有Gaussian09源代码，最好是A02版本，并且自己已经成功编译过一遍，编译方法可参考《Gaussian09 A02、C01 64bit编译方法》，见http://sobereva.com/81，本文假设$g09root环境变量被设为/sob，用户是root。如果对波函数文件不熟悉，可以阅读《高斯fch文件与wfn波函数文件的介绍及转换方法》http://sobereva.com/55。  
  
本文涉及的源代码文件、例子输入文件都可以在这里下载：[/usr/uploads/file/20150609/20150609201400_25520.rar](http://sobereva.com/usr/uploads/file/20150609/20150609201400_25520.rar)  
  
  

## 2 Gaussian的link的基本结构

Link，也就是Gaussian目录下一个个lxxxx.exe，基本的模板是这样：  
      Program mytest  
      Implicit Real*8(A-H,O-Z)  
      Dimension Work(1)  
      Call InitSCM(1,O,O,Work,IOff,MDV)  
      Call ltwd(Work(IOff+1),MDV)  
      End  
  
      Subroutine ltwd(V,MDV)  
      Implicit Real*8(A-H,O-Z)  
      Integer Gen  
      Dimension V(MDV),Gen(1000)  
      Common /IO/ In, IOut, IPunch  
      Common /IOp/ IOp(200)  
      COMMON /PHYCON/ PHYCON(30)  
#include "commonmol.inc"  
      Call Drum(V,MDV)  
      Call FileIO(2,-501,1000,Gen,0)  
      Write(*,*) "Yoooo",nbasis,phycon(5)  !示例  
      Write(*,*) Gen(1),Gen(32)  !示例  
      Call ChainX(O)  
      End  
这里mytest程序是一个壳，也称dummy程序，而它所调用的ltwd子程序才是本体。Gaussian的link基本都是这种组织模式，各个link的本体都在g09/lxxx.F里，而相应的dummy程序是g09/bsd/main.F里的mlxxx。比如NBO模块l607的本体是GauNBO子程序，当Gaussian运行到l607的时候会先经过ml607程序才调用它。  
  
外壳中InitSCM函数用来分配一块空内存给这个link里本体使用，这块内存起始地址是Work数组的IOff+1元素所在地址，MDV是这块内存的大小，这样本体就会接收到长度为MDV的名为V的数组，本体中各种工作都利用这个数组做为临时空间。实际上带着#P执行任务时，输出中的MaxMem=后面的数字就是这个MDV的值（单位为word），%mem的值与MDV相对应。  
  
/IO/是输入输出位置与实际文件编号的映射（Drum子程序会将之填充为In=5, IOut=6, IPunch=7）。在Gaussian中对屏幕输出用IOut，从输入文件中读取信息用In，而punch关键词所对应的输出文件就对应于IPunch，比如punch=MO关键词会将分子轨道信息输出到fort.7里。  
对每一组link所赋予的IOp信息都是通过读取IOp数组被识别的。比如计算路径中有一行为6/4=2,7=80/65;，那么在l665的代码里，IOp(4)就等于2，IOp(7)就等于8。  
/PHYCON/里是一些常用的物理常数。  
commonmol.inc是一个头文件，它就在g09目录下，里面定义了common /mol/，在其中记录了很多重要信息，比如基函数数(nbasis)、alpha/beta电子数(NAE/NBE)、原子坐标(C数组)、原子序号(IAn数组)等等。  
  
除了Link 0和1以外的所有link在正式工作开始前都要调用Drum子程序，Drum起到初始化的作用，包括打开文件，将上述common中目前空着的数组里填充应有的数值等等。  
  
Call FileIO(2,-501,1000,Gen,0)代表从rwf文件（读写文件）中编号501的子文件读取长度为1000的信息到Gen数组里。rwf文件包含众多子文件，在手册里有介绍，其中501子文件对应于/Gen/的信息。Gen数组记录了计算过程中重要的标量信息，比如维里值Gen(1)、SCF能量Gen(32)等  
  
ChainX必须用在link的末尾，它用来做一些扫尾工作，比如更新rwf文件，关闭已打开的文件，确定接下来运行哪个link等等。参数0代表对执行顺序不进行修改，这样运行完当前link就会按照执行路径转到下一个link。  
  
这个模板程序中实际有用的内容就是输出一些信息。将它编译成比如叫l666.exe，然后将它插入到单点任务中的某一处，比如在l601之后执行，那么届时就会看到程序输出比如：  
 Yoooo                      23  6.0221417899999999E+023  
    1.998327281295026       -40.19463972178421   
说明基函数数(nbasis)为23，阿伏伽德罗常数，即phycon(5)为6.0221417899999999E+023，后两个分别是维里值和能量，和Gaussian在SCF完毕后输出的值是一致的。  
  
  

## 3 编译自己写的link和修改的link

再强调一下，编译link前必须先完整编译过一遍Gaussian程序，一些中间剩下的文件要用到。  
  
这里以编译上面的模板程序为例，假设此文件名叫666lite.F。首先确认$g09root已经设好，确认已经进入了csh，然后输入source /sob/g09/bsd/g09.login。将/sob/g09/bsd/link.make、666lite.F都拷到当前目录下，将link.make改名为Makefile，并将其中的MAIN502=后面的内容删掉，将OBJ502=后面写上666lite.o。然后输入mk，这是Gaussian自带的编译脚本，就得到了l502.exe。如果想让这个link叫l666.exe，就直接将它改名为l666.exe即可。  
  
还有一种情况，我们只想对现成的某个Link中某个子程序做一点点修改，而不想重写，比如这里想让l601中输出的偶极矩小数点位数更多些。首先确认$g09root已经设好，确认已经进入了csh，然后输入source /sob/g09/bsd/g09.login。运行gau-get DQ l601，这里DQ是与输出多极矩相关的子程序，此时DQ子程序就会被gau-get从l601.F中提取出来成为dq.F，将其中2002号format的格式从F20.4改为F20.8。然后将/sob/g09/bsd/link.make、dq.F都拷到一起，将link.make改名为Makefile，将其中502都替换为601，将MAIN601=后面填上ml601.o，这表明使用Main.F中ml601作为壳。将OBJ601=后面填上dq.o。然后运行mk，编译脚本会把修改过的DQ、ml601以及l601中其它子程序（在g09目录下l601.a里，是编译Gaussian过程剩下的）连接到一起成为l601.exe。用这个l601.exe代替原先的执行一遍，会发现已经生效了，偶极矩小数位数从原先4为变成了8位。  
  
若自己写一个新link，但又要调用某个link里的子程序，编译方法见下文的例子。如果Gaussian任务调用自己编译的模块出现...World accessible. This must be fixed.字样，用chmod修改文件权限即可，root的话就改为700。  
  
  

## 4 输出每一步的波函数文件

为了简单起见，本文只考虑生成SCF波函数的波函数文件。在IRC、优化、scan等任务的每一次循环中，l502做完之后SCF波函数信息就有了，所以只需要写一个link，假设叫l555（源代码文件名随意，这里假设叫555.F），将它插在l502之后，就能让每一步都输出波函数文件。原先，波函数文件由l9999产生，AllDun子程序是l9999的本体。打开l9999.F查看其代码可知，AllDun是通过调用DoWfn，然后DoWfn再调用WrtWfn来输出波函数文件的，所以要写的link中只要调用DoWfn即可。然而，DoWfn需要接收大量参数，在调用DoWfn之前必须做很多铺垫，才能给予DoWfn足够的信息来输出波函数文件。这些铺垫代码自己写比较麻烦也容易出错，所以这里用的策略是将l9999的AllDun全部内容拷过来，然后将与DoWfn无关的代码删掉，比如读取IOp、初始化无关变量、更新Z矩阵、对导数进行旋转、保存check文件等等内容。有用的信息则必须保留，尤其是计算IEnd变量（记录的是临时数组V中已被占用的长度）的过程不要动，避免引起麻烦。由于改动的地方比较繁多细碎，无法一一说明，完整的555.F已经提供在压缩包里了，和AllDun、WrtWfn原始代码对照一下就能知道哪些被改动过，其中插入了一些向屏幕输出内部变量的语句便于调试。判断哪些变量对DoWfn有用，主要方法是将其接收的各个参数往上搜，直接或间接相关的语句最好进行保留。  
  
在l9999.F中只有IOp(6)的百位数不为0的时候才会调用DoWfn，这里则把条件判断语句去掉，因为l555存在的目的就是输出波函数文件。原先l9999.F中在初始化一些变量时用到MOp函数，它是一个在AllDun内部直接定义的函数，但是在我这里编译不过，可以将之单独写成一个function，但由于与MOp相关的变量对输出波函数文件都没用，就把MOp声明和那些变量都删了。读取IOp数组、初始化变量部分虽然多数也没用，但是留着也不碍事，为避免潜在问题，就没去掉。  
  
还有个问题必须要考虑，也就是每一步输出的波函数文件名字必须不同才行，但是从输入文件中读取的文件名只有一个。分析WrtWfn会发现输出的文件名最终是在这里控制，所以也要把WrtWfn改了才行，于是首先将WrtWfn的代码也拷进555.F准备进行修改。  
  
WrtWfn开头的Read(In,'(A)') FilNam代表从输入文件读入字符串到FilNam，FilNam储存的就是要输出的波函数文件名。Gaussian假设这个模块只被调用一遍，但是我们需要将它调用许多遍。每次都读入一行的话，第二次调用时读入的文件名就可能为空或者因为读到文件末尾而报错，为了避免这种情况，在这行下面插一行backspace(In)。  
  
假设从输入文件中读入的文件名叫/sob/H2.wfn，我们想让每一步的编号顺延，即调用l555的时候依次生成/sob/H2_0000.wfn、/sob/H2_0001.wfn...这就需要将这样内容加到进去  
      inamelen=LenFil-4  
      inamefullen=LenFil+5  
      do itestname=0,9999  
           write(namedigit,"i4.4") itestname  ! namedigit是character*4型新增的变量  
           FilNam(inamelen+1:inamelen+1)='_'  
           FilNam(inamelen+2:inamelen+5)=namedigit  
           FilNam(inamefullen-3:inamefullen)=".wfn"  
           Inquire(file=FilNam(1:inamefullen),exist=wfnalive)  
           if (.not.wfnalive) then    ! wfnalive是新增的逻辑变量  
             goto 111  ! 111加在随后的Write(IOut,1000) FilNam(1:inamefullen)语句开头  
           endif  
      end do  
LenFil是读入的文件名的长度，inamelen是不含扩展名的文件名长度，inamefullen是加上编号的文件名长度。这段代码也就是说，程序会先检查/sob/H2_0000.wfn是否存在，若不存在这次就用这个名字作为波函数文件名，如果已经存在，就再检查/sob/H2_0001.wfn是否存在，反复如此，这样文件名编号就会依次累加了。然后将后面几行中ISt:LenFil都替换成1:inamefullen。ISt是指读入的文件名的起始位置（之前是空格），这里不想搞得这么麻烦，也假设用户不会在开头加空格，所以令ISt成了1。输出波函数文件title的部分也进行了修改，title内容会和步数编号一致，便于以后核查。  
  
现在开始编译。编译方法和第三节介绍的大体相似，但有些不同，这里link完全是新写的，但是又要里利用l9999的其它子程序（其实也可以只修改AllDun和WrtWfn而仍用ml9999的壳）。首先进入csh，source一下g09.login，将link.make拷贝为Makefile并与555.F放到一起。将Makefile里502都改为9999，然后把MAIN9999=后面的内容去掉，OBJ9999=后面写为555.o。运行mk，编译器编译l9999.exe时相当于把原本l9999里的外壳、AllDun、WrtWfn都用555.F里所定义的替换，l9999内其余子程序依然沿用。编译好后将l9999.exe改名为l555.exe。  
  
现在开始测试，这里用三重态H2拉伸scan为例，输入文件在压缩包里，共20步。输入文件中原始的route section仍被保留，但已经用叹号注释掉了。注意由于要从很近的距离0.2埃开始拉，必须用geom=nocrowd避免距离检测。此任务的执行路径如下  
#P nonstd <-----使用非标准路径  
 1/38=1,60=1/1,8;  
 2/12=1,17=6,18=5,29=3,40=1/2;  
 3/5=16,8=22,11=2,16=1,25=1,30=1,74=-5/1,2,3;  
 4//1;  
 5/5=2,38=5/2,55;  
 5//55;  <-----插入了l555  
 6/7=2,8=2,9=2,10=2,18=1,28=1/1;  
 1/60=1/8(1);  
 99/9=1/99;  
 2/12=1,29=3/2;  
 3/5=16,8=22,11=2,16=1,25=1,30=1,74=-5/1,2,3;  
 4/5=5,16=3/1;  
 5/5=2,38=5/2,55;  <-----插入了l555  
 1/60=1/8(-4);  
 99/9=1/99;  <-----由于每步都已经输出了波函数文件，就不需要末尾再次输出了，所以没有传入IOp(6)=100/200/300的信息。  
在这个scan任务中，从执行路径可以看到是先对初始结构做一次SCF，然后再把每个距离也都做SCF，每次遇到(-4)标签后回退开始新一轮循环，直到到达步数上限。这里用了两种插入link的写法，一种是直接写一行5//55;代表只调用l555且不传入任何IOp，第二种是在5/5=2,38=5/2;的分号前插入",55"，两种做法效果是一致的。尽管后者会把IOp(5)=2、IOp(38=2)这样的信息也传给l555，但是AllDun里并没利用到它们，等于没写。如果没有将l555.exe放进g09目录下而是别的地方，比如当前目录，为了让Gaussian能找到它，要在输入文件开头写上%subst l555 .（小点代表当前目录）。执行后就生成了H2_0000.wfn~H2_0021.wfn，其中H2_0000.wfn对应初始结构。  
  
还有一种插入l555的方法，虽然没有非标准路径方法那么灵活，但更为方便，免得列出冗长的执行路径，也就是在route section里写上ExtraLinks=l555，这样在每次调用完所有overlay 5的link后（此例仅为l502），就会调用l555。  
  
  

## 5 输出IRC任务每个点的波函数文件

上一节看似已经达到了我们的目的，但是对于IRC任务还需要考虑更多。附件里包含一个HCN的氢转移IRC任务，执行路径应当这样写：  
[略] （第一次的l502后面也插入l555）  
 2/9=110,29=1/2;  
 3/5=1,6=6,7=101,11=2,16=1,25=1,30=1,71=2,74=-5/1,2,3;  
 4/5=5,16=3/1;  
 5/5=2,38=5/2;  
 5//55; <----插入了l555  
 8/6=4,10=90,11=11/1;  
 11/6=1,8=1,9=11,15=111,16=1/1,2,10;  
 10/6=1,7=6,13=1/2;  
 7/10=1,18=20,25=1/1,2,3,16;  
 1/14=-1,18=20,39=30,44=3/23(-8);  <---- 更新坐标，开始一轮新循环  
[略]  
执行后会发现直接这样做行不通。因为IRC的每一步实际上执行的是限制性优化，这个限制性优化需要几步才能收敛。假设IRC包含20步，平均每步需要三次优化，那么l555将被调用约60次，即最后我们将得到约60个波函数文件！但是其中只有21个（其中1个是初始的TS结构）波函数文件是有用的。因此必须想办法只让每次限制性优化收敛的步才输出波函数文件，有两种实现办法：  
  
第一种方法是每次循环都输出波函数文件，而在最后根据输出文件信息将波函数文件中有用的分拣出来。使用shell脚本比较方便，内容如下：  
#!/bin/bash  
dir=HCN             # The directory where all wavefunction files were stored  
outname=HCN_IRC.out # Gaussian output filename  
i=0  
j=0  
res=(pass `grep -E "Delta-x Convergence NOT Met|Delta-x Convergence Met" $outname|awk '{print $3}'`)  
for filnam in `ls $dir/*.wfn`  
do  
echo ${res[$i]},$filnam  
if [ "${res[$i]}" == "NOT" ] && [ $i!=0 ]; then  
 rm -f $filnam  
else  
 mv -f $filnam $dir/`printf "%4.4i" $j`.wfn  
 j=$(($j+1))  
fi  
i=$(($i+1))  
done  
首先执行IRC任务，输出文件为当前目录下HCN_IRC.out，波函数文件都输出到HCN/目录下。执行这个脚本后（别忘了先切换回bash），HCN_IRC.out会被读取，每一步是否是收敛步会在屏幕上显示，"Not"代表这个波函数文件对应的是未收敛步，会被删掉；"Met"代表这个波函数文件是收敛步，将被保留，并且文件名将会被整理得连贯。过渡态，也就是第一步也这么处理，但显示为"Pass"。这样，最终剩下的文件名为0000.wfn~0020.wfn，0是过渡态，1~10和11~20对应两个方向。  
  
第二种办法这里只给出梗概，怎么具体实现就略过了。通过分析，会发现l123.F的PreDWI子程序与这个问题相关，当cordon变量为true时说明限制性优化已收敛。所以可以改写PreDWI，让收敛时传递一个信息给随后的l555。传递信息的方式多种多样，比如可以通过/Gen/里面的空余位置，也可以用call system("touch conv")命令，即仅当收敛的时候在当前目录建立conv空文件，WrtWfn中通过Inquire(file="conv",exist=ircconv)就能靠ircconv逻辑变量判断出是否已经收敛了，这就能使只有收敛的时候才输出波函数文件。注意还有一些细节问题要考虑，因为当WrtWfn得知限制性优化已收敛的时候，此时的波函数已经是下一步的了，需要靠一点trick来解决这个矛盾，请自行尝试。  
  
有了IRC过程每个点的波函数文件，我们就可以用它们做“这样或那样”的事情了。笔者在随后的文章中将介绍怎么绘制IRC过程中各种实空间函数变化的动画，这比起观看静态的图像更有趣，也能获得更丰富的信息。由于本文的l555里面删掉了一些信息，有可能导致特殊情况下所得波函数文件不正确，届时要以l9999输出的为准。
