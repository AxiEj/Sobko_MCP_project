---
post_id: 6
title: 从高斯windows下的批量执行谈DOS批处理文件
url: http://sobereva.com/6
date: '2015-06-02T17:53:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 综述/教程/投稿经验
- 结构与文件格式
academic_relevant: true
classification_reason: 标题直接是Gaussian Windows下批量执行和DOS批处理，属于软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**从高斯windows下的批量执行谈DOS批处理文件**Batch execution of Gaussian under Windows and introduction to DOS batch files  
文/Sobereva @[北京科音](http://www.keinsci.com/)  写于约2008年

  
  
这是个老生常谈的问题，但通过DOS批处理文件，可以实现很多方便的功能，想在这里多说一下。  
  
先从最简单的解决方法说，网上老是有人问，我以前也回答过多次。windows下高斯批量执行有三种方法  
  
1 多个输入文件写入一个列表中，统一执行：创建.bcf文件，每一行都是C:\QCexperiment\exp3\b1.gjf , b1.out这样。没用的行开头写!注释掉。用gaussian打开此文件后，蹦出来的窗口先exit，然后点三角箭头开始运行。也可以用gaussian的Utilities-edit batch list来编辑批处理任务列表，可保存成.bcf。这个方法一个著名的问题是其中一个任务出错，整个批处理就会断掉。其实上可以在G03W界面的file-preference-Process里面设定来解决，将默认的"End Batch Run on Error"去掉，则运行中某任务出错将继续执行下面的任务。"Prompt Message"如果去掉的话，批量运行过程中将不再出现任何对话框，例如是否覆盖以前输出文件之类将不再提示，适合无人看管的情况下批量执行。  
  
2 多个工作写入一个文件中，统一执行：写一个输入文件，里面用例如--Link1--隔开。实际就是那个addition step方法创建的。这种方式适合多个任务有明显相关性的时候，将它们和在一起。  
  
3 用简单批处理文件完成多个任务  
首先在系统-高级-环境变量里，在系统变量的PATH里面把g03的路径添加到里面，再新增GAUSS_EXEDIR环境变量也设定为g03的所在路径。这样任何目录下都可以运行g03命令了  
比如在gaussian03W文件夹里面建立一个批处理文件k.bat  
如果要自动计算d:\study\2.gjf和d:\study\3.gjf两个文件，然后将结果生成到e:\下面，分别叫2p.out和3p.out，那么bat文件里就写：  
g03 d:\study\2 e:\2p  
g03 d:\study\3 e:\3p  
然后运行k.bat就可以自动计算了，只是看不到运行过程。注意别写后缀名，.gjf和.out不用写，自动默认读取.gjf和生成.out。如果不写输出文件的路径，就默认成生成和gjf同文件名的out文件在原gjf文件夹里（我现在用的E01里面写清楚输入和输出文件名的扩展名也可以运行，比如g03 1.gjf 1.out）。  
使用这种方法，若某个.gjf运行失败，将自动继续运行接下来的.gjf，不会因此出错停住。  
  
  
以上是最一般的方法，但是有时候需要运用类似linux的shell script来实现一些高级功能，比如执行当前文件夹所有.gjf。  
  
最简单的方法是编写一个批处理文件k.bat，内容是：  
for /f %%i in ('dir *.gjf /b') do g03 %%~ni %%~ni  
  
然后输入k来执行，当前目录下所有.gjf都被运行，输出的.out文件文件名与.gjf相同。  
for ... in ... do就是循环，/f指的是将%%i依次赋值为in后面()里面的内容，括号里面可以是一个文件，也可以是一条指令，如果是指令，需用'括起来。  
dir /b指的是只显示文件名（包括扩展名），不显示文件的其它信息  
%%i就是循环过程中的变量，在循环中被赋值为一个个.gjf文件。前面提到了g03后面输入输出文件不要加扩展名，%%~ni是将%%i的.gjf后缀去掉的结果。比如%%i是c60.gjf，%%~ni就是c60。  
  
  
运用batch script，还可以实现更高级的功能，比如想输出每个文件运行的结果，以及运行结束的时间，可以这么写批处理文件：  
  
@echo off  
setlocal enabledelayedexpansion  
for /f  %%i in ('dir *.gjf /b') do (  
g03 %%~ni %%~ni&if !errorlevel!==0 (  
echo Calculation of %%i finished at !date! !time!) else (  
echo Calculation of %%i failed at !date! !time!))  
  
echo off想必大家知道，可以用来屏蔽接下来运行的指令。@就是让echo off本身不显示。  
echo大家也都知道，就是显示文字，也可以显示变量。  
其中%%~ni&if里面的&用来将前面的语句和后面的语句连接，执行完&前面的语句再运行后面的语句。DOS批处理文件一个很不方便之处是do后面只能有一条语句，如果需要运行很多条指令，必须用&把它们连起来组成一条语句。如果为了看起来清楚需要换行，必须在括号的位置换行。  
errorlevel变量指的是程序返回代码，前面的指令运行成功就是0，错误就是非0。  
其中用到了分支语句if a==b (...) else (...)  
date和time环境变量是系统预置的，实时更新，内容分别是日/月/年和小时/分钟/秒/毫秒。  
  
  
批处理程序中的变量主要有4种，  
一种是%1 %2 %3这样的，比如运行k.bat 3 8 5，那么这三个变量分别等于3 8 5，%0是自身  
一种是%i%这样的，这是最普通的，可以用set设定，比如set i=5，调用时候就是%i%，比如echo %i%  
一种是%%i这样的，用在随循环而变化的变量，例子中的%%i就是典型。它不断根据in后面的内容被赋值。  
一种是用!括住的，比如!errorlevel!。为何要用!errorlevel!而不用%errorlevel%呢？  
  
这个问题是时间延迟问题，批处理文件中默认情况下，只有每运行完一条语句才更新一次变量的值，比如  
set i=5  
set i=3 & echo %i%  
显示出来的是5而不是3，因为set i=3 & echo %i%是一整条语句，设置i=3之后并没有立刻生效，所以显示的%i%还是上面那条语句设的5。  
这是批处理文件和其它语言的一个很显著差别。为了避免这种情况，需要加上setlocal enabledelayedexpansion。这样之后用!括住的变量数值都是使用即时的值。比如上面例子改成set i=3 & echo !i!，那么得到的就是3而不是5。  
  
之所以要用!errorlevel!，就是使这个errorlevel变量是真正的它的&前面那句g03 %%~ni %%~ni返回码而非以前的。同理!date!和!time!都是为了得到当前真正的日期和时间。如果不这么设，运行结果会判断错误，而且每一条输入文件完成日期和时间都是一样的。  
  
这样，把上面那条批处理脚本拷贝进all.bat，把它放进一个文件夹，文件夹里包含360.gjf，c60.gjf，vv60.gjf，xc0.gjf，其中360.gjf输入文件有误。运行all，得到：  
  
Calculation of 360.gjf failed at 01/11/2008  2:17:27.91  
Calculation of c60.gjf finished at 01/11/2008  2:17:35.97  
Calculation of vv60.gjf finished at 01/11/2008  2:17:44.07  
Calculation of xc0.gjf finished at 01/11/2008  2:17:52.10  
  
看，不错吧。运行结果和时间一目了然，很适合执行大批量任务。  
  
  
  
实际上很多人忽视了DOS的批处理文件的强大功能，令人心寒啊。由于windows的GUI做得太好了，DOS命令恐怕现在熟悉的人已经越来越少了，至少可以说，世界上所有人的大脑里，关于DOS的知识失去得比增加得快。windows平台搞计算模拟的人熟练使用DOS批处理文件的人很少，而在linux平台上搞计算模拟的人不得不使用文本控制台（光靠linux的GUI干不了什么大事，某些廉价计算机预装linux给菜鸟用，简直是笑话），以为shell script是甚至独一无二的法宝，加上linux内置的繁多的命令，认为是windows平台远不能及的。DOS批处理脚本，虽然在一定程度上比不上linux的shell script，但是足以实现绝大多数它的功能。甚至说到上面那个高斯windows下批处理运行的问题，有人以为这是windows下绝对做不成的事，说用什么bash for windows，真是舍近求远。DOS批处理文件在某些地方用得还是很广泛的，比如hei客，这是必会的。还有一些某些人认为方便的装机工具，比如番茄花园之流也用这些。以及一些别有用心的人，verycd上renchongyi是个典型，篡改别人辛辛苦苦破解的程序，通过批处理文件自动运行一堆病毒，号称是安装程序欺骗菜鸟，这是非常卑鄙的。  
  
总之，重拾DOS，重视起批处理文件吧！
