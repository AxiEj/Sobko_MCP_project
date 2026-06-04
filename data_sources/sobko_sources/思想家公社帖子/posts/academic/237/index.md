---
post_id: 237
title: 将文件快速载入Multiwfn程序的几个技巧
url: http://sobereva.com/237
date: '2015-06-08T00:08:00+08:00'
source_categories:
- Multiwfn
primary_topic: Multiwfn
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 内容讲快速载入文件到Multiwfn的技巧，属于软件使用教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**将文件快速载入Multiwfn程序的几个技巧**

Several tips for quickly loading files into the Multiwfn program

文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2014-Jun-5   Last update: 2019-Sep-11

  
有一些量子化学初学者在使用波函数分析程序Multiwfn (<http://sobereva.com/multiwfn>)的时候，因为英语阅读理解能力极差，甚至都不知道第一步应该做什么。第一步要干的事如屏幕所示，显然是要填输入文件路径，但很多初学者竟连路径也反复输不对。输入路径是极为简单的事，比如Windows下，输入诸如D:\love_live\sunshine\yosoro.wfn，在Linux下，输入诸如/sob/love/nico.fch就完了。此文主要目的是介绍载入文件时候的一些技巧，以使用户们能够更高效地利用此程序。  
  
首先明确一下什么叫“当前目录”(current folder)，这在Multiwfn手册、程序的提示信息和博文里里频繁涉及到。对于Windows，比如可执行文件Multiwfn.exe放在了D:\CM\Multiwfn3.3目录下，如果你双击Multiwfn.exe图标来启动程序，那么当前目录就是D:\CM\Multiwfn_3.3。如果你是在Windows的cmd或powershell环境，或linux的命令行下调用的Multiwfn，比如目前处在E:\nico目录下，你输入D:\CM\Multiwfn_3.3\Multiwfn.exe来启动之，那么当前目录就是E:\nico。如果你在Windows里把输入文件的图标直接拖到Multiwfn图标上来载入之，或者Multiwfn启动后你按ENTER键通过图形窗口选择输入文件，那么输入文件所在目录就是当前目录。  
  
Multiwfn启动后会在当前目录下寻找settings.ini文件并从中读取设定，如果找不到但是你已经将某个目录设成了Multiwfnpath环境变量，则程序会到这个目录下继续找settings.ini，如果还找不到，就会使用程序里的默认设定（和未修改过的settings.ini里的设定一致）。  
  
  
载入文件的一些技巧如下  
  
1 如果不想以文本方式输入路径，启动Multiwfn后直接敲回车即可，此时会蹦出个图形界面用于选择输入文件。此时选择哪个文件，这个文件所在的目录就会成为当前目录。  
  
2 文件的路径既可以输入相对路径也可以输入绝对路径。绝对路径就是指类似这样的D:\CM\Multiwfn_3.3\examples\phenol.wfn，盘符和所有上级文件夹名称都得写进去。为了简便，也可以写相对路径，也就是要载入的文件相对于当前目录的路径。比如当前目录是D:\CM\Multiwfn_3.3，那么载入刚才那个文件只需要输入examples\phenol.wfn就可以了。如果有一些文件比较常用，不妨就拷到当前目录下，每次载入只需要写文件名就行了。  
  
3 每次程序成功载入文件后，会把载入的文件的路径写入到settings.ini的最后一行。下一次运行Multiwfn时，如果你还想再次分析上次载入的文件，只需要输入字母o就可以了，非常方便。Multiwfn会直接从settings.ini的最后一行中读入它的路径。  
  
4 如果你上次载入的文件是C:\lovelive\yuri\nicomaki.wfn，下次你想分析C:\lovelive\yuri\nozoeri.wfn，那么只需要输入?nozoeri.wfn就行了。问号代表上次载入的文件所处的路径。  
  
（注：显然，技巧3、4生效的前提是Multiwfn能够找到settings.ini文件）  
  
5 启动Multiwfn后，可以将要载入的文件图标直接拖入到命令行窗口里，文件的路径就会出现在窗口里，然后直接按回车就行了，非常便利。这个技巧对Windows和Linux都可以用。  
  
6 对于Windows系统，可以直接将要载入的文件拖到Multiwfn.exe图标上，Multiwfn就会立刻启动并将此文件载入。这样做有个缺点就是当前目录将是被载入的文件的所在目录。Multiwfn的很多功能输出的文件都是输出到当前目录下，因此如果用了这个技巧，那些文件就会被输出到被载入的文件所在的目录了。  
  
7 Windows和Linux的命令行界面都有补全文件名或目录名的功能，也就是输入文件名或目录名的前几个字母，然后按TAB键就可以把名字都补全。在Multiwfn程序里面没法用这种便利的补全功能，但是以命令行方式调用的话则可以利用这点。命令行模式下可以类似这样写：Multiwfn examples\N-phenylpyrrole，第一个参数是文件名，这使得在启动Multiwfn的同时就载入文件。因此，写这么一串实际上只需要依次这样按：m [TAB] [空格] e [TAB] \n- [TAB]，然后回车即可，很快捷。  
  
顺便介绍一个Windows技巧。如果你在某个目录里新建一个后缀为.bat的文本文件，比如叫ltwd.bat，用文本编辑器将其内容写为cmd，然后保存，那么只需要双击ltwd.bat这个图标就能立刻进DOS，而且所处的目录就是这个文件所在的目录！所以如果你嫌在DOS下经常要进入某个目录比较麻烦，不妨就把这个bat文件放到这个目录下，以后一双击就直接就进去了。另外，对于win7（XP不适用），还有更方便的方法，也就是按住shift然后在文件夹窗口里点击右键，会出现“在此处打开命令窗口”，选择后也会出现处在当前目录下的命令行窗口，就免得编辑.bat文件了。
