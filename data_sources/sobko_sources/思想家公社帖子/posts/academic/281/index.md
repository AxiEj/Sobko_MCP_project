---
post_id: 281
title: 简谈CPU峰值性能怎么计算
url: http://sobereva.com/281
date: '2015-06-08T00:17:00+08:00'
source_categories:
- 其它
primary_topic: 综述/教程/投稿经验
secondary_topics:
- 硬件工作流
academic_relevant: true
classification_reason: 内容是在解释CPU峰值性能的计算方式，属于硬件知识与计算工作流。
topic_family: 资源经验
exclude_reason: ''
confidence: 0.83
image_count: 0
local_assets_dir: assets
---

**简谈CPU峰值性能怎么计算**  
A brief discussion on how to calculate CPU peak performance

文/Sobereva @[北京科音](http://www.keinsci.com)  2015-Feb-13

CPU峰值性能就是CPU运算能力满打满算最最理想情况下的性能，这只有理论意义，实际性能要以软件实测为准。有人问寡人峰值性能怎么算，这里就很简单地说两句。搞计算化学的一般只关注浮点性能，所以这里只提峰值浮点性能。

峰值浮点性能=CPU核数*CPU频率*每周期执行的浮点操作数

时下普通的CPU的单精度(SP)浮点性能是双精度(DP)浮点性能的两倍。目前常见的几类CPU内核的每周期浮点操作数以及细节如下（引自网络，见<http://stackoverflow.com/questions/15655835/flops-per-cycle-for-sandy-bridge-and-haswell-sse2-avx-avx2>）

Intel Core 2 and Nehalem:  
4 DP FLOPs/cycle: 2-wide SSE2 addition + 2-wide SSE2 multiplication   
8 SP FLOPs/cycle: 4-wide SSE addition + 4-wide SSE multiplication

Intel Sandy Bridge/Ivy Bridge:  
8 DP FLOPs/cycle: 4-wide AVX addition + 4-wide AVX multiplication   
16 SP FLOPs/cycle: 8-wide AVX addition + 8-wide AVX multiplication

Intel Haswell:  
16 DP FLOPs/cycle: two 4-wide FMA (fused multiply-add) instructions   
32 SP FLOPs/cycle: two 8-wide FMA (fused multiply-add) instructions

AMD K10:  
4 DP FLOPs/cycle: 2-wide SSE2 addition + 2-wide SSE2 multiplication   
8 SP FLOPs/cycle: 4-wide SSE addition + 4-wide SSE multiplication

AMD Bulldozer/Piledriver/Steamroller, per module (two cores):  
8 DP FLOPs/cycle: 4-wide FMA   
16 SP FLOPs/cycle: 8-wide FMA

时下搞计算化学的人最常用的XEON E3/E5中，v3对应Haswell，v2对应Ivy Bridge，不带后缀的对应Sandy Bridge。更老的，比如XEON 5500系列对应Nehalem。如果不清楚，建议查阅笔者编纂的《硬件资料库》（<http://sobereva.com/datasheet.rar>）

根据这些资料，可以容易地计算峰值浮点性能，比如E5-2690 v2，基本频率为3.0GHz（这里不考虑Turbo boost动态升频），有10个核，每个核每周期可以做8次双精度浮点运算或16次单精度浮点运算，因此：  
单精度峰值浮点性能=3.0*10*16=480 GFLOPs  
双精度峰值浮点性能=3.0*10*8=240 GFLOPs

这里FLOPs (FLoating-point Operations Per Second)是衡量浮点性能的常用单位，即每秒做的浮点运算次数。1GFLOPs代表每秒十亿次浮点运算。目前世界顶尖的高性能计算机(HPC)的浮点性能都以PFLOPs来计，1P=1000T=1000000G。

从上面列的数据中看似XEON v3 (Haswell)比v2的浮点性能高一倍，这被一些商家用来忽悠消费者。实际上，同频同核下，v3比v2性能提升很小。如果v3价格只比v2贵一点，那么可以买v3，但如果贵得很多，切勿被表面上看多一倍的峰值性能所冲昏了头脑。适当了解下不同内核以及指令集的特点对理解这个问题是有益的。为了方便，这里我们只考虑双精度浮点。

第一代奔腾支持的MMX、奔3开始支持的SSE（最后发展到SSE4/4A），以及从Sandy Bridge开始支持的AVX等等都是SIMD（单指令多数据）指令集，它允许一个指令同时对多个数据进行处理以达到很大的吞吐量。Sandy Bridge/Ivy Bridge支持的AVX指令集可以一次处理256bit浮点指令，双精度浮点数长度为64bit，即通过AVX指令一次可以做四个双精度浮点运算。如前面给出的信息所示，Sandy Bridge/Ivy Bridge一个周期可以执行一次AVX浮点乘和一次AVX浮点加，也就是说一个周期可以做四个双精度浮点加和四个双精度浮点乘，故曰每周期可以做8个双精度浮点运算。这只是理论最大值，实际上水分很大，因为前提是必须所处理的完全是AVX 256bit指令，但实际中是做不到的，能利用上AVX指令集的只是实际计算程序中的某些部分而已（这需要编译器和操作系统的支持。如果写的时候专为AVX来调整代码编写方式可以更好地利用AVX来达到更好的性能）。另外，不可能总是恰好要算的是一条加法指令和一条乘法指令，比如传来的只有一串浮点加指令，那么乘法运算单元就空闲了，浮点性能也就浪费了一半。所以，虽然我们从前面列的数据中看到Sandy Bridge/Ivy Bridge得益于AVX而比Nehalem每周期能做的浮点运算次数高一倍，但这只是最理想的状况而已，而且这和实际表现出来的性能不是那么的密切。一般应用中前者比后者在同频同核数情况下性能高近一半，这主要还是因为CPU架构做了多方面改进带来的，具体说起来就比较复杂了，这里就不提了。可以说，如果所运行的程序对AVX优化较好，Sandy Bridge/Ivy Bridge表现的性能比Nehalem提升得会更多。

再来看XEON v3和v2的关系。Haswell相比Sandy Bridge/Ivy Bridge的一个主要改进是支持了AVX 2.0指令集，相比AVX有了一些改进，其中很关键的是支持了FMA3指令，这里FMA是Fused Multiply-Add（融合乘加）的缩写，FMA3是一种具体实现。原本，做result=a+(b*c)需要先做一次乘法再做一次加法，而利用FMA指令可以在一个周期内做完这个运算，所以可以认为做一次FMA运算等于做两次常规浮点运算。如前面列出的信息所示，Haswell的每个内核一个周期可以处理两个FMA指令，每条指令包含4个双精度浮点，一次FMA浮点运算又能当两次普通浮点运算来计，因此每个核每周期内满打满算可以做2*4*2=16次双精度浮点操作。由于支持了FMA，表面上看XEON v3比v2浮点性能高了一倍，但这种说法实际上水分巨大：哪可能要做的总是乘加运算？比如传来的就是一条AVX浮点乘指令，此时v3虽然支持FMA却也派不上用场，v3和v2都需要一个周期来完成，即表现出的性能相等。所以说，如果有人说v3比v2性能提升一倍那纯粹是天方夜谭，除非跑的是专门炫耀Haswell的程序，里面的运算全都是乘加。根据实际测试来看，Haswell跑现有的程序也就比Ivy Bridge性能高不到10%，但这很难说是支持FMA的功劳。以后的程序可能会有一些针对FMA专门进行优化，或在编译时使用相应的优化选项（如ifort里用-fma）而使v3有更好的性能，但不要抱太高期待。所以前面提到，买服务器时如果v3比v2贵一点可接受，但贵得太多就算了。

再来说说为什么如今AMD CPU的浮点性能为什么如此之烂。从推土机架构开始，即前面列的Bulldozer/Piledriver/Steamroller这一类，AMD就用了很糟糕的设计，两个核心作为一个模块，共用一个浮点单元，一个周期只能处理一次256bit FMA指令，而Haswell一个核就能同时处理两条256bit FMA指令，也就是说，论峰值浮点性能，现今AMD的U四个核才顶Haswell一个核。不过实际没这么夸张，抛开那些很虚的峰值性能数据，要达到如今XEON v2或v3的N个核的实际性能，同频情况下，如今的Opteron必须要用>2N个核。如果程序的并行效率很低，那么Opteron实际效能简直惨不忍睹，不管怎么算都远不如XEON划得来。所以说，如今做计算化学买AMD的U只有后悔的份。AMD的U的核数比较坑人，N个核才有N/2个浮点单元（想来，当年AMD还无耻地说Intel的Pentium D是胶水粘的，有点自己打脸的意味），但是整数性能还说得过去，整数单元和核数是相同的，但搞计算化学的人才不稀罕整数性能呢。

最后再说一下GPU。从峰值性能上看，GPU比起CPU弱点在于频率低，不支持SIMD，但它的浮点性能之所以胜于CPU在于流处理器数目多。以nVidia的高端的GTX Titan black为例，基础频率是0.889GHz，有2880个单精度浮点单元和960个双精度浮点单元，每个浮点单元每周期能做一次FMA指令，因此  
单精度峰值浮点性能：0.889*2880*2=5120GFLOPs  
双精度峰值浮点性能：0.889*960*2=1707GFLOPs

可见GTX Titan black峰值性能比前面举的E5-2690 v2的例子高了约一个数量级，但这水分太大，显然不能因为FMA就当成实际中有两倍处理能力，所以公平来说双精度浮点性能前者是后者4、5倍的样子。GPU的单精度浮点性能的确很好，性价比远胜于CPU，但一定要注意大多数消费级GPU的双精度性能其实不咋地。GTX Titan black价格比起同样流处理数目的GTX 780Ti贵出一倍，在我来看贵的主要道理不是因为它是烧包级，而是双精度性能能达到单精度的1/3，而这个比例对于GTX 780Ti仅为1/24！GTX 780Ti的基准频率为0.876GHz，单精度性能和GTX Titan black基本无异，但双精度峰值性能才区区210GFLOPs而已，要不把FMA满打满算记入峰值性能计算公式，那么还明显不如E5-2690 v2呢。

PS：这篇文章观点有点意思，大家不妨看看《GPU运算即将退潮 CPU浮点性能革命》（<http://www.cgan.net/cganself/founder/?p=2681>）
