---
post_id: 167
title: Multiwfn入门tips
url: http://sobereva.com/167
date: '2015-06-07T23:59:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 波函数分析
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章是 Multiwfn 的入门提示，典型软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**Multiwfn入门tips**Tips for getting started with Multiwfn

文/Sobereva @[北京科音](http://www.keinsci.com)  
First release: 2012-Nov-7   Last update: 2025-Nov-24

## 0 前言

Multiwfn（主页为<http://sobereva.com/multiwfn>）是由北京科音自然科学研究中心（[www.keinsci.com](http://www.keinsci.com)）的卢天从2009年11月起开发的非常强大的量子化学波函数分析程序，功能极为广泛、十分高效、非常易于使用，并且开源免费，用户已遍及全世界90多个国家，目前已被超过40000篇研究论文所使用，包括Science、Nature、Nature Chemistry/Materials/Energy/Photonics/Physics/Synthesis/Sustainability、JACS、Angew、PNAS等顶尖刊物。Multiwfn也被很多顶尖理论化学工作者如Truhlar、Grimme、Perdew、Morokuma、Shaik、Houk、Frank Neese等人的文章使用。在J. Comput. Chem.上的Multiwfn程序原文是迄今中国发表的所有论文（不限学科）中被引次数最高的10篇之一。Multiwfn在实际应用性量子化学的研究中价值巨大，很多情况都必不可少。

写本文的目的是帮助刚接触Multiwfn的人能够在短时间内了解Multiwfn的基本特点以及如何上手。但此文并不讲解程序操作过程和原理，因为这些内容已经在笔者的无数博文、程序手册里有详尽描述和示例。本文着重谈一下应该怎么上手和学习Multiwfn，读者将会明白Multiwfn虽然功能极其强大，但使用根本没有什么门槛，学习Multiwfn也超级容易！与此同时也提及一些计算化学基础薄弱的用户在使用Multiwfn时可能会忽略的要点或困惑的问题。

如果你不知道Multiwfn是干什么的话，非常建议仔细看《Multiwfn波函数分析程序的最新最全面的介绍文章已在JCP上发表！》（<http://sobereva.com/726>）里面提到的2024年发表的Multiwfn的介绍文章，这里面对Multiwfn的功能和用途进行了完整、系统的介绍（截止到2024年8月的Multiwfn版本）。并且强烈建议在看完此文后大致阅览一遍《Multiwfn FAQ》（<http://sobereva.com/452>），各方面常见问题在里面都做了汇总。

## 1 对使用者的要求

对于量化初学者，Multiwfn当成一个工具作为黑箱来用也可以，但是我还是建议使用者具备一些最基本的理论知识，这样才能避免犯低级错误，才能更透彻地理解程序原理和输出信息的物理意义。使用者只要参加过北京科音办的[初级量子化学培训班](http://www.keinsci.com/workshop/KEQC_content.html)，或具有相同级别的知识，就已经足够了，结合手册中对各个功能的理论的讲解，就完全能够理解Multiwfn涉及的全部功能的原理了。  

Multiwfn是基于量子化学程序输出的波函数信息来进行分析的程序。如果你是Gaussian程序的用户，那么可以使用Multiwfn的全部功能。但Multiwfn程序绝非是专为Gaussian而开发的，Multiwfn支持许多通用的记录波函数信息的格式，如.mwfn、.wfn、.wfx、molden文件，还支持GAMESS-US输出文件，还支持其它类型文件如.cub、.pdb、.xyz等。只要你用的量化程序能输出molden输入文件（如Molpro、ORCA、NWChem、deMon2k），或者能输出.fch文件（如PSI4、Q-Chem），或者你是GAMESS-US/Firefly的用户，那么就能用上Multiwfn的绝大部分功能。如果你只能得到.wfn/.wfx文件，也至少能利用Multiwfn的半数以上的功能，例如AIM分析、ELF等实空间函数的分析和绘图等等。如果你是第一性原理的研究者，只用VASP、CASTEP、CP2K之类的程序，那么Multiwfn中依赖于波函数的功能都暂时帮不上你（但是只需要提供几何结构的分析功能照样能做，如IGM分析）。笔者以后预计会开发专门面向第一性原理的程序的波函数分析程序。

关于Multiwfn支持的输入文件的具体说明以及产生的方法，在此文有详述《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）。

绝大部分Multiwfn的功能运算效率都很高，而且支持并行，在普通个人双核机子上运行就已经挺快了，除非研究的体系很大，或者用了很大的基组，或者跑那些个别特别耗时的分析任务，否则没必要非要弄到服务器上去执行。  
   

## 2 程序的下载、安装、执行

Multiwfn的可执行文件、源代码和手册在Multiwfn官网的Download栏目里可直接下载。文件名上带bin的是已编译好的含有可执行文件的包，src代表源代码文件包，manual是手册。

在主页的Update history栏目中可以看到最新版本更新了哪些内容。在每个正式版本发布之前，通常也把正在开发的临时版本，即后缀带(dev)的挂在这个栏目上。临时版本未经全面测试，手册也没写全，但是已经实现了更新历史上提到的最新功能和改进。如果想尝鲜可以试试。

Multiwfn更新很频繁。新版本中总会不断添加新的有用的功能、改善界面设计使之更好用、修正各种bug、提升运行效率。我强烈建议时常查看Multiwfn主页，更新到最新版本。老版本的一些bug可能造成结果是错的，但是没有经验的用户又察觉不出来，这种情况甚至有可能使文章的研究的结论有误，这将是很大问题。所以，即便新版本的新功能用不到，也应当勤快更新至最新版本。我强烈建议用户按照此帖的方式通过电子邮件自动接收Multiwfn的更新提醒：《推荐通过Visualping自动接收Multiwfn的更新提醒》（<http://bbs.keinsci.com/thread-12556-1-1.html>）。有四位Multiwfn用户还各自开发了方便的Multiwfn更新工具，如下所示，如果你懒得每次手动去Multiwfn官网下载新版本程序包的用户可以考虑使用：  
Multiwfn快乐更新小助手：<http://bbs.keinsci.com/thread-20052-1-1.html>  
mum: Multiwfn update manager：<http://bbs.keinsci.com/thread-20070-1-1.html>  
Updater for both Linux and Windows version of Multiwfn：<http://bbs.keinsci.com/thread-20109-1-1.html>  
A Python script for Multiwfn updates：<http://bbs.keinsci.com/thread-20115-1-1.html>

Windows版Multiwfn程序解压后双击Multiwfn.exe图标即可启动，Linux版应按照《Multiwfn在Linux下安装的中文说明》（<http://sobereva.com/688>）说的安装，MacOS版应当按照手册2.1.3节进行安装。解压后目录下的settings.ini里包含了各种运行参数，这些参数在Multiwfn启动时会被载入，这些参数平时使用时一般不需要修改。各个参数在文件中的//后面的注释中都有说明，大部分参数的用处在手册中会更详细地解释。这些参数中特别关键的一个是nthreads，当它设为n，则Multiwfn中并行化的代码部分运行时就会使用n个线程进行并行运算。如果你有较多的CPU核心，可以将它设大来加快计算（即便设得值超过了CPU核心数也没关系，此时实际有几个核心在并行时就会用几个核心）。

如果是第一次使用Multiwfn，强烈建议使用Windows版，有多个原因：1. Linux/MacOS版Multiwfn的极个别功能有限制，见手册开头的Linux and MacOS users must read部分的说明 2. Linux/MacOS版图形窗口显示效果没有Windows版好 3. Linux/MacOS版本使用时前需要对系统进行一些配置，而不像Windows版那样直接用就行。

Multiwfn是命令行与图形界面混合的程序，大部分操作在交互式的命令行界面下完成，而需要可视化结果的地方才会提供图形界面，这样的设计是最佳、使用效率最高的。不设计成全图形界面的原因在此帖有说明：《为什么我拒绝将Multiwfn做成全图形界面》（<http://sobereva.com/236>）。Multiwfn也可以通过命令行方式非常方便地使用，而且还可以嵌入到脚本中或者被第三方程序调用。用户还可以自己写shell脚本调用Multiwfn实现一键对大批量体系自动按照特定流程计算并自动提取和统计数据，从而彻底解放双手，极度方便。这些知识在这篇文章里有特别系统、详细、深入浅出的介绍，强烈建议一读：《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>）。

程序启动后，会看到一个文本界面，先输入要载入的文件的路径。如果你缺乏计算机基本常识，都不知道怎么输入文件路径的话，看《将文件快速载入Multiwfn程序的几个技巧》（<http://sobereva.com/237>）。然后根据屏幕上每个选项所表示的含义，选择相应选项，或输入相应内容即可。选项往往比较多，只要从选项的文字上觉得和自己的目的无关，就不必管它，这些暂时用不到的选项的用途日后你会渐渐明白。使用Multiwfn的过程中一定要注意阅读和领会屏幕上的各种信息和提示，Multiwfn会尽可能在不至于信息过于冗长的情况下，直接在屏幕上告诉用户接下来应该输入什么，免得用户老得查阅手册、记忆操作过程。但若是遇到想不明白的地方，则应去手册里查阅相应功能对应的章节，看看是否能找到说明，或者查看手册的教程部分，看看是否有示例。Multiwfn很多功能能够直接图形化显示结果，当出现图形界面时，想要关闭的话就点Return按钮，如果没有此按钮，在图上直接点右键即可返回。关闭程序直接点窗口右上角的X或者按Ctrl+C即可。如果程序运行中途突然关闭（对于Windows下直接双击程序图标来运行则表现为“闪退”），这是程序遇到错误导致的，通常是因为输入文件的类型不对、输入文件有毛病、输入的命令不合规范、使用方式不对、内存不足等原因造成的，请仔细看《Multiwfn FAQ》第3节的专门说明。

Multiwfn输出的电子密度、静电势等各种实空间函数的计算结果，以及几何坐标、键长等，如果输出信息中没写明单位，则一律是原子单位（a.u.），不懂的话去wiki看看atomic unit的页面。

## 3 程序的引用

Multiwfn的开发对用户分文不取，也不拿纳税人的一分钱，笔者对使用者的唯一要求是必须恰当进行引用，这不仅是最基本的学术道德，也是Multiwfn程序的使用条款里的内容。

如果Multiwfn程序在研究文章中被使用，必须**同时引用**这两篇Multiwfn的程序原文：**Tian Lu, Feiwu Chen, *J. Comput. Chem.*, 33, 580-592 (2012) 和 Tian Lu, *J. Chem. Phys.*, 161, 082503 (2024)**。**如果文章中用了Multiwfn，但是在文章中连这两篇必须引的文章都没引用的话，使用者将被加入Multiwfn黑名单，禁止以后再次使用Multiwfn发表文章**。不要把引用Multiwfn不当回事。有一些用户不当引用的行为已经被公开点名批评，例如：<http://bbs.keinsci.com/thread-26843-1-1.html>。

并且，请在文章正文里提及和引用Multiwfn，而不要只放到补充材料里，否则不仅读者难以注意到，而且也不会被纳入引用的统计。

Multiwfn可以用于给别人代算，但代算时必须明确告知对方要在文章里引用以上Multiwfn的原文。

支持Multiwfn程序开发的最好方式是恰当引用笔者的相关文章，使用Multiwfn的不同功能、做不同分析应当引用的文章不同，最恰当的引用Multiwfn的说明见Multiwfn可执行文件程序包里的How to cite Multiwfn.pdf文档。

## 4 程序手册

Multiwfn的各种功能涉及到的基本原理、选项的含义在程序手册里都有极其详尽描述。Multiwfn的可执行文件包里有一个Multiwfn quick start.pdf文档，如果你急于用Multiwfn计算某个常见的量、做某个常见的分析的话，通过这个文档可以立马查到应当看手册的哪一节，因此这个文档非常有用。

虽然Multiwfn的手册是英文版的，但写得特别简明易懂，对于中国的量子化学研究者来说在语言上绝对不会成为障碍。明白手册如何查阅对于使用程序是非常重要的，这样才便于在1100多页的手册中很快找到想要的信息。这里把手册的章节编排重点说明一下，读者可以通过点击文档的Bookmark的相应标题直接跳到相应章节。

手册第二页的内容是All users must read，这是一定要读的，所以把它放到手册最开头。第三页是Linux users must read，这是使用Linux版Multiwfn的用户一定要读的。

手册第一章是Multiwfn的特点、功能的整体概述。这一章务必要读。

手册第二章是关于Multiwfn程序自身的一些说明，包括Multiwfn的支持的文件格式、图像格式等等。这一章可以根据小节的标题有选择性地阅读。  
*如果是Linux用户，务必阅读2.1.2节，按照其中的方法配置系统。  
*Multiwfn在实空间函数的分析、绘制上是其强项之一，2.6节简明扼要地介绍了各种Multiwfn支持的实空间函数。如果要计算某实空间函数但是对它又不熟悉的话，应当阅读一下相应的介绍。另外，在实空间函数的计算上有一些可调设定会在相应位置说明，比如settings.ini文件里的laplfac参数，它控制电子密度拉普拉斯函数前面乘的系数，这个参数会在介绍拉普拉斯函数的地方说明。  
*2.5节建议尽量完整阅读一遍，其中介绍了Multiwfn支持的各种文件格式，特别注意其中的表格列出了每种文件格式包含了哪类信息。Multiwfn的不同功能所需要的信息不同，必须得在程序运行一开始将含有相应信息的输入文件载入才行。如果输入文件类型不对，则执行功能时可能出错退出。

手册第三章是Multiwfn的各个功能的基本原理和选项的含义。这一章可以有选择地看，用到哪个功能就去看哪一节。刚进入Multiwfn并载入文件后，会看到一个主菜单，这个列表里的每一项被称为“主功能”，主功能里面有的会有很多子功能，子功能里可能又会有很多选项。在手册第三章中，每一个二级标题对应于一个主功能，二级标题末尾的括号里的数字就是对应的主功能在Multiwfn主菜单里的编号。比如3.10 Orbital composition analysis (8)，这一节介绍的就是轨道成分分析功能，也就是Multiwfn的主功能8。这一节下面的各个三级标题对应了各种不同的轨道成份计算方法。Multiwfn的一些重要的、需要特别解释一下的选项会在手册相应章节里说明；而一些不重要的、从选项名字上一看就能明白的选项有的就不专门提及了。

特别注意第三章的每个章节末尾会看到类似这样的信息（以3.9节布居分析为例）  
Information needed: Basis functions (MPA, Lowdin, MMPA), GTFs (Hirshfeld, VDD, Becke, ADCH, CHELPG, MK), atom coordinates  
这就代表，如果要计算原子电荷，必须首先拥有原子坐标信息。若是计算MPA, Lowdin, MMPA这三种原子电荷，还需要基函数信息。若计算Hirshfeld, VDD, Becke, ADCH, CHELPG, MK这些电荷，则需要GTF（原始高斯函数）信息。从手册2.5节的表格可以看到，.wfn、.wfx、.fch、.molden等格式包含了原子坐标和GTF信息，因此计算Hirshfeld, VDD, Becke, ADCH, CHELPG, MK这些原子电荷时这几种文件都可以作为一开始的输入文件，只要产生它们的条件相同，则结果是一样的。从表格中也看到，由于只有.fch、.molden、.gms文件同时具备基函数和原子坐标信息，所以想计算MPA, Lowdin, MMPA原子电荷的话，就必须得用这几种格式作为输入文件。如果一开始载入的文件类型不含有某些功能所需要的信息，那么在Multiwfn的菜单中这些功能可能会消失不见，或者虽然能看见，但是选了之后就会出错终止。因此，使用Multiwfn的功能时如果不确定应该用什么类型输入文件，应当查看相应章节末尾的Information needed，看看这个功能需要什么信息，结合2.5节的表格来决定应该用什么输入文件。或者参考教程部分相应的例子也可以。关于如何正确选择输入文件，在此文有更详细的说明：《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）。

手册第四章的开头介绍了如何生成Multiwfn的各种输入文件（对于Gaussian用户，一般用fch/fchk文件即可），务必要看。之后是教程，包含了超过100个精心撰写例子，覆盖了Multiwfn的大部分重要的功能。自学Multiwfn的基本使用方法最好的方式就是看这些教程（以及后文提到的博文）！我十分建议用户将第四章的例子从头到尾做一遍，这些例子涉及到的文件基本上在程序压缩包里的examples目录下都提供了，做完这些例子后对Multiwfn的基本使用就比较熟练了，同时也会了解很多波函数分析的知识。但如果某些例子和自己的研究实在关系不大，有选择性地跳过一些也无妨。在做这些例子的时候，应当特别注意揣摩Multiwfn程序的设计思想，领会各个功能、每一步操作的含义，这样才能达到举一反三的效果，从而对于教程中没有涉及到的功能也能很快理解用法，实现教程中没有涉及到的应用。

注意第4.x节的例子对应于Multiwfn的主功能x，因此通过二级标题编号就能明白例子的内容是对应于程序的什么主功能的。由于Multiwfn的功能很多，灵活度极高，大量功能、细节和高级应用限于篇幅都没能在第四章涉及到。因此，对于感兴趣的功能，务必阅读第三章的相应章节了解功能的原理、详情，并且结合手册里的解释自行尝试教程中未曾提到过的功能选项（由于Multiwfn的功能选项都尽量设计得简明易用，所以不会遇到什么障碍）。另外，第四章末尾的4.A节包含一些高级教程，以及一些专题，比如如何用Multiwfn分析弱相互作用、如何分析芳香性。

手册第五章是一些使用技巧，比如介绍如何通过silent模式单纯靠命令行执行以及批量执行分析任务；或者介绍一些重要，但又和程序本身原理、功能关系不很紧密的内容，比如从屏幕上直接拷贝Multiwfn输出信息到剪切板中。有很多次有人问我Multiwfn输出的信息较长，把命令行窗口的滑条拉到顶头也看不全应该怎么办，实际上这在5.5节已经说明了，也就是加大窗口缓冲区尺寸。

手册最后是附录。其中说明了怎么设定Gaussian运行环境（Multiwfn的个别功能会调用Gaussian计算原子波函数文件，执行这类功能之前必须先设定Gaussian运行环境），介绍了Multiwfn源代码中各个实空间函数名（主要用于自己编写自定义函数时作为参考，这属于相对高级的应用），还有其它很多信息，若想对Multiwfn了解多一些很建议看看。

## 5 中文文章&学习资源

虽然Multiwfn的手册已经极其详细了，例子也极其丰富，但为了让国内的研究者们，尤其是量化初学者们能更容易地了解如何用Multiwfn解决一些实际问题，也算是对Multiwfn没有中文手册所作的弥补，我曾写了大量中文文章介绍Multiwfn的各个方面的应用或其它有关问题，超过100万字，其中不少内容和手册里的内容有交集。如果要抱怨Multiwfn没有中文的手册，那么请先把这些中文文章看了！很多帖子属于专题讨论，内容比手册里的明显更深、更广，因此与手册有高度的互补性。这些帖子最新版本都发在了笔者的blog中（<http://sobereva.com>），后来写的也同时发在了笔者创立的计算化学公社论坛上（<http://bbs.keinsci.com>）。这里将目前已经写过的这些帖子列在下面，还有一些其它的Multiwfn的相关资源也列在这里。

幻灯片《Multiwfn与波函数分析简介》（<http://sobereva.com/239>），不到400页，内容浅显，非常适合初学者入门波函数分析、了解Multiwfn！

《Multiwfn FAQ》（<http://sobereva.com/452>）必看！

• 笔者零散录的一些Multiwfn演示视频汇总，初学者很推荐看看：<https://space.bilibili.com/20718/#/channel/detail?cid=45163>。Multiwfn也有Youtube频道，内容和B站上的类似，但字幕都是英文：<https://www.youtube.com/playlist?list=PLGZRmytlfpyPMknda9_tdJh8HPHjSECsW>。

• 使用了Multiwfn发表的文章pdf合集（注意只是不完全统计，实际引用次数远多于此），可以作为例子库：  
第1~1010篇文章：<http://sobereva.com/322>  
第1011~2001篇文章：<http://sobereva.com/389>  
第2002~3000篇文章：<http://sobereva.com/438>  
第3001~4000篇文章：<http://sobereva.com/500>  
第4001~5000篇文章：<http://sobereva.com/546>  
第5001~6000篇文章：<http://sobereva.com/574>  
第6001~7000篇文章：<http://sobereva.com/592>   
第7001~8000篇文章：<http://sobereva.com/619>   
第8001~9000篇文章：<http://sobereva.com/636>   
第9001~10000篇文章：<http://sobereva.com/649>   
第10001~11000篇文章：<http://sobereva.com/654>   
第11001~12000篇文章：<http://sobereva.com/663>  
第12001~13000篇文章：<http://sobereva.com/677>  
第13001~14000篇文章：<http://sobereva.com/691>  
第14001~16000篇文章：<http://sobereva.com/713>  
第16001~19000篇文章：<http://sobereva.com/732>  
第19001~22000篇文章：<http://sobereva.com/747>

• 下面这几篇有综述性质，非常重要！

《Multiwfn支持的预测化学体系反应位点和反应活性方法一览》（<http://sobereva.com/767>）

《Multiwfn支持的电子激发分析方法一览》（<http://sobereva.com/437>）

《Multiwfn支持的分析化学键的方法一览》（<http://sobereva.com/471>）

《Multiwfn支持的弱相互作用的分析方法概览》（<http://sobereva.com/252>）

《衡量芳香性的方法以及在Multiwfn中的计算》（<http://sobereva.com/176>）

《Multiwfn可以计算的分子描述符一览》（<http://sobereva.com/601>）

《充分运用波函数分析的理论计算文章的模板》（<http://sobereva.com/764>）

《化学体系的静电势的计算和分析方法汇总》（<http://sobereva.com/769>）

• 下面这些是针对各个主题、问题进行讲解的文章

《使用Multiwfn快速产生超胞的格点数据》（<http://sobereva.com/770>）

《使用Multiwfn计算键双描述符考察不同化学键的反应性》（<http://sobereva.com/766>）

《使用amIGM方法图形化直观展现动态过程中的平均弱相互作用》（<http://sobereva.com/759>）

《Multiwfn结合ORCA的TDDFT计算做空穴-电子等分析的方法》（<http://sobereva.com/758>）

《通过格点屏蔽巨幅降低IGMH可视化分析片段间相互作用耗时的方法》（<http://sobereva.com/756>）

《使用mIGM方法基于几何结构快速图形化展现弱相互作用》（<http://sobereva.com/755>）

《利用Multiwfn令Dalton计算时使用其它程序产生的轨道作为初猜》（<http://sobereva.com/740>）

《计算IGMH等值面的面积和体积的方法》（<http://sobereva.com/738>）

《使用Multiwfn计算轨道的体积》（<http://sobereva.com/734>）

《使用Multiwfn计算FiPC-NICS芳香性指数》（<http://sobereva.com/724>）

《使用Multiwfn考察周期性体系的芳香性》（<http://sobereva.com/722>）

《使用Multiwfn对周期性体系做键级分析和NAdO分析考察成键特征》（<http://sobereva.com/719>）

《使用Multiwfn结合CP2K对周期性体系做电荷分解分析（CDA）》（<http://sobereva.com/716>）

《谈谈怎么考察、计算、分析化学体系的电子密度》（<http://sobereva.com/715>）

《使用Multiwfn对周期性体系计算Hirshfeld(-I)、CM5和MBIS原子电荷》（<http://sobereva.com/712>）

《使用Multiwfn结合CP2K计算晶体中原子的氧化态》（<http://sobereva.com/711>）

《使用Multiwfn计算原子的C6色散系数》（<http://sobereva.com/709>）

《使用Multiwfn计算双描述符势预测反应位点》（<http://sobereva.com/708>）

《使用Multiwfn图形化展现原子对色散能的贡献以及色散密度》（<http://sobereva.com/705>）

《使用Multiwfn观看轨道概率密度》（<http://sobereva.com/704>）

《使用Multiwfn做Hirshfeld surface分析直观展现分子晶体和复合物中的相互作用》（<http://sobereva.com/701>）

《使用Multiwfn基于Hirshfeld-I划分计算特定类型电子在各个原子上的分布量》（<http://sobereva.com/697>）

《使用Multiwfn极为方便地绘制(超)极化率密度和三维空间对(超)极化率的贡献》（<http://sobereva.com/683>）

《使用Multiwfn巨方便地绘制二维NICS平面图考察芳香性》（<http://sobereva.com/682>）

《使用Multiwfn绘制一维NICS曲线并通过积分衡量芳香性》（<http://sobereva.com/681>）

《使用Multiwfn通过局部电子附着能(LEAE)考察亲核反应位点、难易及弱相互作用》（<http://sobereva.com/676>）

《通过量子化学计算和Multiwfn程序预测化学物质的颜色》（<http://sobereva.com/662>）

《使用Multiwfn计算分子的球形度（sphericity）》（<http://sobereva.com/661>）

《使用Multiwfn展现过剩电子（excess electron）并计算它的回转半径》（<http://sobereva.com/658>）

《详谈使用CP2K产生给Multiwfn用的molden格式的波函数文件》（<http://sobereva.com/651>）

《使用Multiwfn计算特定方向的UV-Vis吸收光谱》（<http://sobereva.com/648>）

《使用Multiwfn对静电势和范德华势做拓扑分析精确得到极小点位置和数值》（<http://sobereva.com/645>）

《使用Multiwfn计算分子和晶体中孔洞的直径》（<http://sobereva.com/643>）

《谈谈怎么计算“原子的静电势”》（<http://sobereva.com/641>）

《基于原子电荷极快速绘制超大体系的分子表面静电势图》（<http://sobereva.com/639>）

《使用CP2K结合Multiwfn绘制密度差图、平面平均密度差曲线和电荷位移曲线》（<http://sobereva.com/638>）

《使用Multiwfn做IGMH分析非常清晰直观地展现化学体系中的相互作用》（<http://sobereva.com/621>）

《使用CP2K结合Multiwfn对周期性体系模拟UV-Vis光谱和考察电子激发态》（<http://sobereva.com/634>）

《使用Multiwfn绘制电荷转移光谱(CTS)直观分析电子光谱内在特征》（<http://sobereva.com/628>）

《谈谈第一超极化率(beta)的符号的物理意义》（<http://sobereva.com/622>）

《使用Multiwfn定量化和图形化考察分子的平面性（planarity）》（<http://sobereva.com/618>）

《使用Multiwfn计算晶体结构中自由区域的体积、图形化展现自由区域》（<http://sobereva.com/617>）

《电子空间范围<r^2>和电子径向分布函数的含义以及在Multiwfn中的计算》（<http://sobereva.com/616>）

《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>）

《Multiwfn中非常实用的几何操作和坐标变换功能介绍》（<http://sobereva.com/610>）

《使用Multiwfn计算odd electron density考察激发态单电子分布》（<http://sobereva.com/583>）

《使用Multiwfn通过ETS-NOCV方法深入分析片段间的轨道相互作用》（<http://sobereva.com/609>）

《通过电子定域化函数(ELF)、价层电子密度分析讨论亲核进攻的方向》（<http://sobereva.com/606>）

《使用Multiwfn计算分子中的原子极化率》（<http://sobereva.com/600>）

《使用IRI方法图形化考察化学体系中的化学键和弱相互作用》（<http://sobereva.com/598>）

《使用Multiwfn做aNCI分析图形化考察动态过程中的蛋白-配体间的相互作用》（<http://sobereva.com/591>）

《使用Multiwfn绘制分子和固体表面的距离投影图》（<http://sobereva.com/589>）

《使用Multiwfn结合CP2K通过NCI和IGM方法图形化考察固体和表面的弱相互作用》（<http://sobereva.com/588>）

《使用Multiwfn非常便利地创建CP2K程序的输入文件》（<http://sobereva.com/587>）

《用Multiwfn计算过渡金属的d-band center（d带中心）》（<http://sobereva.com/582>）

《使用Multiwfn计算分子片段的偶极矩和复合物中单体的偶极矩》（<http://sobereva.com/558>）

《谈谈范德华势以及在Multiwfn中的计算、分析和绘制》（<http://sobereva.com/551>）

《使用Multiwfn模拟扫描隧道显微镜(STM)图像》（<http://sobereva.com/549>）

《使用Multiwfn结合CP2K的波函数模拟周期性体系的隧道扫描显微镜（STM）图像》（<http://sobereva.com/671>）

《使用Multiwfn通过单位球面表示法图形化考察（超）极化率张量》（<http://sobereva.com/547>）

《使用Multiwfn图形化展示分子动力学模拟体系中的孔洞、自由区域》（<http://sobereva.com/539>）

《使用Multiwfn计算各种与信息论相关的量（information-theoretic quantities）》（<http://sobereva.com/537>）

《使用键级密度(BOD)和自然适应性轨道(NAdO)图形化研究化学键》（<http://sobereva.com/535>）

《通过轨道权重福井函数和轨道权重双描述符预测亲核和亲电反应位点》（<http://sobereva.com/533>）

《一键把所有gjf文件转成xyz文件、把所有Gaussian输出文件转成gjf文件的脚本》（<http://sobereva.com/530>）

《使用Multiwfn便利地查看所有激发态中的主要轨道跃迁贡献》（<http://sobereva.com/529>）

《通过轨道离域指数(ODI)衡量轨道的空间离域程度》（<http://sobereva.com/525>）

《将Multiwfn计算的键级直接标注在分子结构图上的方法》（<http://sobereva.com/523>）

《谈谈如何衡量分子的极性》（<http://sobereva.com/518>）

《使用Multiwfn和VMD绘制平均局部离子化能(ALIE)着色的分子表面图（含视频演示）》（<http://sobereva.com/514>）

《使用Multiwfn对第一超极化率做双能级和三能级模型分析》（<http://sobereva.com/512>）

《使用Multiwfn计算分子的动力学直径》（<http://sobereva.com/503>）

《使用Multiwfn考察分子轨道、NBO等轨道对密度差、福井函数的贡献》（<http://sobereva.com/502>）

《使用Multiwfn计算Bond length/order alternation (BLA/BOA)和考察键长、键级、键角、二面角随键序号的变化》（<http://sobereva.com/501>）

《使用Multiwfn计算与超瑞利散射(HRS)实验相关的量》（<http://sobereva.com/499>）

《绘制静电势全局极小点+等值面图展现孤对电子位置的方法》（<http://sobereva.com/493>）

《详谈Multiwfn产生ORCA量子化学程序的输入文件的功能》（<http://sobereva.com/490>）

《使用Multiwfn和VMD计算分子表面积和片段表面积》（<http://sobereva.com/487>）

《使用Multiwfn超级方便地计算出概念密度泛函理论中定义的各种量》（<http://sobereva.com/484>）

《使用Multiwfn绘制态密度(DOS)图考察电子结构》（<http://sobereva.com/482>）

《巨大体系的范德华表面静电势图的快速绘制方法》（<http://sobereva.com/481>）

《使用Multiwfn一键批量产生各类光谱图（含演示视频）》（<http://sobereva.com/479>）

《使用Multiwfn绘制光电子谱》（<http://sobereva.com/478>）

《使用Multiwfn计算CVB指数考察氢键强度》（<http://sobereva.com/461>）

《使用Multiwfn绘制跃迁密度矩阵和电荷转移矩阵考察电子激发特征》（<http://sobereva.com/436>）

《使用Multiwfn+VMD快速绘制高质量分子轨道等值面图（含视频）》（<http://sobereva.com/447>）

《使用Multiwfn+VMD快速地绘制高质量AIM拓扑分析图》（<http://sobereva.com/445>）

《使用Multiwfn+VMD快速地绘制静电势着色的分子范德华表面图和分子间穿透图》（<http://sobereva.com/443>）

《使用Multiwfn做基于分子力场的能量分解分析》（<http://sobereva.com/442>）

《RESP拟合静电势电荷的原理以及在Multiwfn中的计算》（<http://sobereva.com/441>）

《RESP2原子电荷的思想以及在Multiwfn中的计算》（<http://sobereva.com/531>）

《使用Multiwfn做空穴-电子分析全面考察电子激发特征》（<http://sobereva.com/434>）

《在Multiwfn中通过IFCT方法计算电子激发过程中任意片段间的电子转移量》（<http://sobereva.com/433>）

《在Multiwfn中单独考察pi电子结构特征》（<http://sobereva.com/432>）

《使用Multiwfn计算激发态之间的密度差》（<http://sobereva.com/429>）

《使用Multiwfn计算分子的长宽高》（<http://sobereva.com/426>）

《谈谈原子间是否成键的判断问题》（<http://sobereva.com/414>）

《利用布居分析判断基函数与原子轨道的对应关系》（<http://sobereva.com/418>）

《使用Multiwfn+VMD以原子着色方式表现原子电荷、自旋布居、电荷转移、简缩福井函数》（<http://sobereva.com/425>）

《使用Multiwfn可视化分子孔洞并计算孔洞体积》（<http://sobereva.com/408>）

《通过独立梯度模性(IGM)考察分子间弱相互作用》（<http://sobereva.com/407>）

《在Multiwfn中基于fch产生自然轨道的方法与激发态波函数、自旋自然轨道分析实例》（<http://sobereva.com/403>）

《基于Multiwfn产生的cube文件在VMD和GaussView中绘制填色等值面图的方法》（<http://sobereva.com/402>）

《电子激发过程中片段间电荷转移百分比的计算》（<http://sobereva.com/398>）

《使用Multiwfn+VMD绘制片段贡献的跃迁偶极矩矢量》（<http://sobereva.com/396>）

《在Multiwfn中分析比CCSD更高级别波函数的方法》（<http://sobereva.com/395>）

《使用Multiwfn绘制构象权重平均的光谱》（<http://sobereva.com/383>）

《Multiwfn的轨道定域化功能的使用以及与NBO、AdNDP分析的对比》（<http://sobereva.com/380>）

《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）

《使用Multiwfn做自然跃迁轨道(NTO)分析》（<http://sobereva.com/377>）

《使用Multiwfn考察轨道间重叠程度和质心距离》（<http://sobereva.com/371>）

《使用DORI函数同时考察共价和非共价相互作用》（<http://sobereva.com/367>）

《使用Multiwfn通过LOBA方法计算氧化态》（<http://sobereva.com/362>）

《谈谈自旋密度、自旋布居以及在Multiwfn中的绘制和计算》（<http://sobereva.com/353>）

《使用Multiwfn预测晶体密度、蒸发焓、沸点、溶解自由能等性质》（<http://sobereva.com/337>）

《使用Multiwfn观看分子轨道》（<http://sobereva.com/269>）

《利用Multiwfn计算倾斜、扭曲环的NICS_ZZ》（<http://sobereva.com/261>）

《将文件快速载入Multiwfn程序的几个技巧》（<http://sobereva.com/237>）

《使用Multiwfn基于完全态求和(SOS)方法计算极化率和超极化率》（<http://sobereva.com/232>）

《使用Multiwfn分析Gaussian的极化率、超极化率的输出》（<http://sobereva.com/231>）

《使用Multiwfn绘制红外、拉曼、UV-Vis、ECD、VCD和ROA光谱图》（<http://sobereva.com/224>）

《使用Multiwfn绘制NMR谱》（<http://sobereva.com/565>）

《使用Multiwfn计算激发态间的跃迁偶极矩和各个激发态的偶极矩》（<http://sobereva.com/227>）

《通过Multiwfn绘制等化学屏蔽表面(ICSS)研究芳香性》（<http://sobereva.com/216>）

《通过键级曲线和ELF/LOL/RDG等值面动画研究化学反应过程》（<http://sobereva.com/200>）

《谈谈分子半径的定义和计算方法》（<http://sobereva.com/190>）

《使用Multiwfn研究分子动力学中的弱相互作用》（<http://sobereva.com/186>）

《用Multiwfn+VMD做RDG分析时的一些要点和常见问题》（<http://sobereva.com/291>）

《制作动画分析电子结构特征》（<http://sobereva.com/86>）

《电子定域性的图形分析》（<http://sobereva.com/63>）

《使用Multiwfn图形化研究弱相互作用》（<http://sobereva.com/68>）

《使用Multiwfn做拓扑分析以及计算孤对电子角度》（<http://sobereva.com/108>）

《Multiwfn结合VMD绘制AIM拓扑分析图》（<http://sobereva.com/207>）

《使用Multiwfn作电子密度差图》（<http://sobereva.com/113>）

《使用Multiwfn绘制NBO及相关轨道》（<http://sobereva.com/134>）

《谈谈轨道成份的计算方法》（<http://sobereva.com/131>）

《使用AdNDP方法以及ELF/LOL、多中心键级研究多中心键》（<http://sobereva.com/138>）

《使用Multiwfn绘制原子轨道图形、研究原子壳层结构及相对论效应的影响》（<http://sobereva.com/152>）

《使用Multiwfn的定量分子表面分析功能预测反应位点、分析分子间相互作用》（<http://sobereva.com/159>）

幻灯片《Predicting reactive sites （反应位点的预测）》（<http://sobereva.com/234>）

《分子间轨道重叠的图形显示和计算》（<http://sobereva.com/163>）

《绘制跃迁密度矩阵平面图分析电子跃迁》（<http://sobereva.com/136>）

《使用Multiwfn做电荷分解分析(CDA)、绘制轨道相互作用图》（<http://sobereva.com/166>）

《使用Multiwfn做电子密度、ELF、静电势、密度差等函数的盆分析》（<http://sobereva.com/179>）

《使用Multiwfn结合VMD分析和绘制分子表面静电势分布》（<http://sobereva.com/196>）

《通过Multiwfn计算各个轨道的偶极矩》（<http://sobereva.com/251>）

《利用约化密度梯度考察AIM临界点的位置》（<http://sobereva.com/267>）

《将分子结构图和Multiwfn绘制的平面图准确合并的方法》（<http://sobereva.com/274>）

《使用Multiwfn计算超极化率密度》（<http://sobereva.com/305>）

《杂谈Multiwfn从1.0到3.0版的开发经历》（<http://sobereva.com/180>）

《回答一些关于Multiwfn的疑问以及未来Multiwfn的发展打算》（<http://sobereva.com/107>）

《Multiwfn程序名读法的统一说明》（<http://bbs.keinsci.com/thread-11011-1-1.html>）

笔者另有不少文章和Multiwfn有较大关系，如《使用Gaussian做镧系金属配合物的量子化学计算》（<http://sobereva.com/581>）、《在VMD里将cube文件瞬间绘制成效果极佳的等值面图的方法》（<http://sobereva.com/483>）、《谈谈分子体积的计算》（<http://sobereva.com/102>）、《AIM键临界点处电子密度拉普拉斯值符号判断相互作用类型失败原因的图形分析》（<http://sobereva.com/161>）、《绘制有填色效果的用于弱相互作用分析的RDG散点图的方法》（<http://sobereva.com/399>）、《计算RESP原子电荷的超级懒人脚本》（<http://sobereva.com/476>）、《谈谈18碳环的几何结构和电子结构》（<http://sobereva.com/515>）、《计算分子动力学轨迹中两个环平面间的距离和夹角》（<http://sobereva.com/590>）、《直观解释分子间相互作用如何影响不对称催化：Nature Chemistry上一个很好的IGMH分析范例》（<http://sobereva.com/700>）、《谈谈pi-pi相互作用》（<http://sobereva.com/737>）、《深度揭示互为等电子体的苯、无机苯和carborazine的芳香性的显著差异》（<http://sobereva.com/731>），都推荐看看。

很值得一提的是笔者关于18碳环（cyclo[18]carbon）的理论研究，这是非常新颖独特的体系。在2019年笔者在ChemRxiv上发表了一篇非常全面、系统的研究18碳环体系的理论文章，文章内容简述见《一篇最全面、系统的研究新颖独特的18碳环的理论文章》（<http://sobereva.com/524>）。此文综合运用了Multiwfn各种分析功能，对18碳环的各方面特征做了充分的探究，得到了一大批颇有价值的研究结果。此文可以作为一篇使用Multiwfn研究新奇特化学体系的范文，强烈建议阅读！大家也可以效仿里面的分析去考察各种新发现的有趣的化学体系。这篇文章的大部分内容后来经过大幅扩充后在碳化学领域权威的Carbon期刊上陆续发表，即Carbon, 165, 468 (2020)、Carbon, 165, 461 (2020)、Carbon, 171, 514 (2021)。这体现出在深刻理解波函数分析方法的意义、特点的前提下，充分、灵活运用Multiwfn研究新颖热门体系，即便是纯理论计算工作也是不难在高档次期刊上发文的。对于Carbon, 171, 514 (2021)这篇文章，我还专门写过一个深入浅出的介绍，并且写了大量相关评注，见《全面探究18碳环独特的分子间相互作用与pi-pi堆积特征》（<http://sobereva.com/572>）。如果你是研究弱相互作用的人，强烈建议仔细看看此文，估计会让你的思路开阔许多、认识到波函数分析在弱相互作用研究方面的价值有多么的大。在《8字形双环分子对18碳环的独特吸附行为的量子化学、波函数分析与分子动力学研究》（<http://sobereva.com/674>）介绍的我在PCCP上发表的研究文章、《全面揭示各种碳环与富勒烯之间独特的pi-pi相互作用！》（<http://sobereva.com/727>）介绍的我在Chem. Eur. J.上发表的文章中也充分利用Multiwfn对吸附作用做了分析，读者看了肯定会很有启发。

笔者还对18碳环在电场下的行为做了深入细致的研究，文章中也充分利用了Multiwfn的功能，深刻揭示了电场以及碱/碱土金属对18碳环几何结构、电子结构、电子光谱的显著影响及其本质，强烈建议阅读：《一篇文章深入揭示外电场对18碳环的超强调控作用》（<http://sobereva.com/570>）。此文是使用Multiwfn研究外电场对化学体系影响的很好的例子。《18个氮原子组成的环状分子长什么样？一篇文章全面揭示18氮环的特征！》（<http://sobereva.com/725>）介绍的笔者的研究18氮环的论文里用Multiwfn全面考察了其电荷分布、成键、电子离域，也是Multiwfn极好的应用实例。

笔者使用Multiwfn对18碳环及类似体系做的更多的研究以及各种相关博文见这里的汇总：<http://sobereva.com/carbon_ring.html>。

## 6 求助

使用Multiwfn中遇到问题时建议先查询手册、查看相关博文来试图解决。如果程序莫名其妙出错，应当先尝试使用最新版、反复检查输入文件和操作步骤看看能否解决。如果仍得不到答案，可以通过以下几种方式向开发者求助。求助时最好将完整的操作过程附上，如果输入文件不大的话最好也压缩后一起附上，以便于开发者检查是用户操作错误、输入文件有问题还是程序有bug。

(1) **（最推荐）**在笔者建立的计算化学公社论坛的Multiwfn讨论版咨询（<http://bbs.keinsci.com/wfn>），或者在Multiwfn的英文论坛咨询（<http://sobereva.com/wfnbbs>，提问时需要说英语），这都是官方指定的Multiwfn交流论坛，笔者基本每天都去看，看到后会立即详细回复。笔者不在其它任何论坛回复Multiwfn及计算化学相关问题。

(2) 在笔者建立的思想家公社QQ群里咨询，此群专门用于交流计算化学问题。群号码见<http://sobereva.com>上方的信息。如果在群里询问后一天内没有得到回复，可能笔者不在线，可以趁Sobereva在线时再次询问，或者把问题发到Multiwfn论坛里。因笔者十分忙碌，除非问题很私密，否则请不要发私窗。

(3) 通过电子邮件咨询。开发者的邮箱是Multiwfn主页上给出的邮箱（和手册第一页、Multiwfn程序刚启动时显示的信息里的邮箱一致）。除非问题非常私密，否则不建议用此方式提问。

笔者不在其它任何论坛和场所回答与计算化学相关（包括Multiwfn在内）的问题。

## 7 培训班

北京科音自然科学研究中心（<http://www.keinsci.com>）每年都举办“量子化学波函数分析与Multiwfn程序培训班”，培训的详细介绍和往届信息回顾请访问北京科音网站的“科研培训”栏目。本培训会由Multiwfn开发者卢天全面讲授波函数分析的理论知识并结合大量实例介绍Multiwfn的使用方法，详细讲授内容见<http://www.keinsci.com/workshop/WFN_content.html>。每年的此培训都会对内容有很多更新。未来的此培训班的举办时间在北京科音官网首页的"科研培训预告"一栏中会有体现。这是一次性完整地把各种波函数分析理论知识和Multiwfn、NBO等波函数分析程序的使用都彻底学透的极其难得的途径。本培训中的大部分内容都是在Multiwfn手册和相关博文里没有的，因此即便曾经通读过手册和全部博文的学员在参加过此培训后水平也会有显著提升！
