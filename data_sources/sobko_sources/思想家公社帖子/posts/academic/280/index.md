---
post_id: 280
title: 将双页扫描的pdf书籍转换为单页的方法
url: http://sobereva.com/280
date: '2015-06-08T00:17:00+08:00'
source_categories:
- 其它
primary_topic: 结构与文件格式
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章讲的是PDF扫描书双页转单页的文件处理方法。
topic_family: 软件
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**将双页扫描的pdf书籍转换为单页的方法**

文/Sobereva(1)   2015-Feb-11

很多网上的电子书都是扫描的，扫描的时候往往是两页连在一起，阅读的时候很不方便，得拉动页面看完左边再看右边。如果转换为每个页面只有一页内容的话在阅读时方便得多。虽然网上也有一些文章介绍通过一些特殊工具来实现，但是笔者感觉都不方便，最后摸索出本文的办法，非常好用，只要有Acrobat就行了（但不能是Acrobat reader），不需要任何第三方工具。笔者使用的是Acrobat 9 Pro，其它版本可能对话框有所不同，但过程是基本一致的。

## 1 切割页面

这一步我们把双页切割成左右两半分别存到两个pdf文件里。

这里我们先得到对应页面左半边的pdf文档。用acrobat打开双页pdf文档，选Document-Crop Pages，然后在Page Range里输入要切割的页面范围，比如From 2 to 281（假设第一页是单页的封面，所以略过）。窗口中有个缩略图，同时显示了当前页面的尺寸，比如11.760*8.547 in。我们在Margin Controls当中的Right框里面输入一个合适的值，比如11.760 .in的一半，即5.88 in，这就代表切掉页面右边5.88 in的部分。缩略图窗口就会出现一个分割线，如果差不多处在正中就行。然后点OK，当前文档就只剩左半边部分了。用File-Save As保存为left.pdf。

同理，我们获得对应于页面右半边的right.pdf。过程的区别仅在于5.88 in应当输入在Margin Controls当中的Left框里面。

## 2 分割页面成为独立的文件

我们建立一个文件夹叫Left，然后把left.pdf挪进去，改名为比如book.pdf。然后打开此文件，选Document-Split Document，把Number of pages设为1。点击Output Options，把Use label复选框去掉，然后点两次OK，此时这个文档里每个页面都切割为独立的了。文件名为比如book_1.pdf、book_2.pdf ... book_280.pdf。然后删掉book.pdf。

同样，我们把right.pdf这么分割成为一页一个pdf文件，保存在Right文件夹里。

## 3 重命名单页pdf文件

我们必须让Left文件夹和Right文件夹里的页面交错地合并，为做到这一点，我们需要先对文件名重命名，让左侧页面的文件名都带上a后缀，右侧的带上b后缀。做法是新建一个文本文件，内容只有一行：  
for /f  %%i in ('dir *.pdf /b') do (rename %%i %%~nia.pdf)  
然后把文件后缀名改为.bat，这就成了DOS批处理文件，会对当前目录下所有pdf文件的文件名末尾加上a。将此文件放到Left目录下，然后双击执行，马上文件名就成了book_1a.pdf、book_2a.pdf ... book_280a.pdf

然后把这个批处理文件里的%%~nia改为%%~nib，将之挪到Right文件夹里执行，文件名就都成了book_1b.pdf、book_2b.pdf ... book_280b.pdf。

## 4 合并页面

建立一个文件夹叫All，然后把Left和Right目录下的单页pdf文件都放到这里面。此时会看到编号是1a、1b、2a、2b、3a、3b...，即左右页面交错排列。先选择所有编号<10的，然后点右键选择Combine supported files in acrobat，点Combine file按钮，得到合并后的文档，将之保存为1.pdf。然后选择编号10~99的，合并为10.pdf。再选择100~999的，合并为100.pdf。

最后，把1.pdf、10.pdf、100.pdf再次合并，就OK了！

可能此时开头几页比如封面页会有重复的，在Acrobat里删掉即可。
