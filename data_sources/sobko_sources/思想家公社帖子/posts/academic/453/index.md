---
post_id: 453
title: 使用CYLview绘制高质量分子结构图和制作化学反应演示动画（视频演示）
url: http://sobereva.com/453
date: '2018-12-26T08:26:00+08:00'
source_categories:
- 量子化学
primary_topic: 可视化
secondary_topics:
- 结构与文件格式
- 其它软件
academic_relevant: true
classification_reason: 文章围绕CYLview做分子结构绘制和反应动画，核心是可视化软件使用。
topic_family: 软件
exclude_reason: ''
confidence: 0.91
image_count: 0
local_assets_dir: assets
---

**使用CYLview绘制高质量分子结构图和制作化学反应演示动画**

Using CYLview to plot high-quality molecular structure maps and create chemical reaction demonstration animations

文/Sobereva@[北京科音](http://www.keinsci.com) 2018-Dec-26

CYLview的虽然功能不算多强大，但它在作图的很多特性方面没有其它程序能很好取代，所以笔者特意录制了长为11分钟的使用CYLview绘制分子结构图和制作各种类型动画的演示视频，见：[**https://www.bilibili.com/video/av39041185**](https://www.bilibili.com/video/av39041185)

本文内容是对视频内容进行一些补充说明。视频里并没有把CYLview所有特性一一展现，而是着重把新用户容易犯懵，不是显而易见，不容易自己试出来的操作进行了讲解，很容易理解的操作和选项视频里就没有去提，用户自己把玩几分钟就会得差不多了。

CYLview的下载地址是<http://www.cylview.org>。视频里用的版本是CYLview 1.0b Build 561。

如果机子里没装化学文件格式转换程序Openbabel的话，CYLview只能载入Gaussian输出文件，因此很不方便。所以强烈建议在机子里装上Openbabel，是个免费程序，在此文里有简单介绍：《基于OpenBabel批量产生特定基团以任意方式接到苯上的结构的方法》（<http://sobereva.com/440>）。

有些人发现目前的CYLview载入不了G16的输出文件，是因为没有按照视频里提及的方式去点击更新程序按钮，更新过之后就没问题了。

视频里使用了Houkmol的style，这是CYLview里内置的一种显示风格的组合，是搞有机体系计算知名的Houk文章里常见的显示风格。

视频里的renderall.bat是个DOS批处理文件，内容如下  
for /f %%i in ('dir *.pov /b') do (  
povray +W640 +H480 +A %%i  
)  
将这些内容复制到一个文本文件里，改名成renderall.bat即可使用。此脚本会调用当前目录下的povray.exe对当前目录下的所有povray渲染器文件（.pov）进行渲染，产生出同名图像文件。

视频中用的ffmpeg是业界非常知名的视频编码、解码、转换程序，免费，小巧，功能极强，支持格式众多，各个操作系统都有，可以在<https://ffmpeg.org>免费下载，Windows版解压即用无需安装。基本使用格式为ffmpeg [选项] [输入选项] -i [输入文件] [输出选项] [输出文件]。

制作mp4动画时用到了以下命令  
ffmpeg -r 15 -i FRAME%04d.png -crf 22 video.mp4  
其中%04d代表通配0001、0002、0003...。-r后面是每秒的帧数，视频实际长度就是图像数目除以r值，因此r越大动画播放越快，r越小播放越慢。-crf是ffmpeg调用的名为x264的编码器里的参数，数值越小动画越清晰，但是文件越大，一般-crf 22就比较合适。

制作gif动画时用到了以下命令  
ffmpeg -i FRAME0001.png -vf palettegen palette.png  
ffmpeg -r 15 -i FRAME%04d.png -i palette.png -lavfi paletteuse video.gif  
虽然ffmpeg也可以一步就产生gif动画，即把前述命令的mp4后缀改成gif，但是动画里的某些颜色比较诡异，远不如上面这样先根据实际图像文件生成调色板文件，再产生gif动画来得好。gif文件比mp4大得多，而且只能包含256色，但好处是可以直接嵌入到网页和ppt里。

视频里笔者写的用于合并带_txt后缀和不带这个后缀的.pov文件的CYL_mergeTXT.exe工具在这里下载：<http://sobereva.com/attach/453/CYL_mergeTXT.rar>。带_txt后缀的文件只包含标签内容，而不带这个后缀的包含的是分子结构信息。

视频里用的GauIRC2xyz在这里下载：《将Gaussian的IRC任务输出转换为.xyz轨迹文件的工具》（<http://sobereva.com/285>）。

笔者还写过其它与制作计算化学相关视频有关的文章，如下所示，里面用的imagemagick工具也都可以改用ffmpeg工具，速度更快而且还有Windows版。  
制作动画分析电子结构特征  
<http://sobereva.com/86>  
通过键级曲线和ELF/LOL/RDG等值面动画研究化学反应过程  
<http://sobereva.com/200>
