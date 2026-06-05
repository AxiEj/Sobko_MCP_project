---
thread_id: 57134
source_id: forum_thread:57134
title: "利用Gaussian分解键长/键角/二面角对重组能的贡献"
url: http://bbs.keinsci.com/thread-57134-1-1.html
date: "2025-05-01T00:00:00+08:00"
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: wsl2_chrome_cdp_verified_session
source_crawled_at: "2026-06-05T11:56:17.315Z"
original_reply_count: 15
page_count: 1
views: 5792
software_tags:
- Gaussian
topic_tags:
- 综述/教程/投稿经验
- 量子化学
authority_level: B
confidence: 0.97
classification_reason: sobereva教程，讲解利用Gaussian分解结构参数对重组能贡献的方法。
---

# 利用Gaussian分解键长/键角/二面角对重组能的贡献

- 原帖 URL：<http://bbs.keinsci.com/thread-57134-1-1.html>
- 论坛板块：量子化学
- 作者：**sobereva**
- 浏览量：5792 | 回复数：15 | 共1页
- 完整性：**全部内容已完整抓取**。

## 楼层正文

### 1 楼（楼主）｜sobereva

本帖最后由 wal 于 2025-12-12 21:45 编辑 



工作原理

利用Gaussian的freq=intmode功能打印冗余内坐标对正则模式的贡献；

利用FCHT的print=huangrhys计算正则模式对重组能的贡献；

整合信息来计算冗余内坐标对重组能的贡献。

这边写不了latex，公式写在GitHub的readme部分了



计算部分

Gaussian计算输入：

%oldchk=opt_Azulene.chk

#p geom=allcheck freq(readfc,fcht,readfcht,intmode) IOp(7/75=-1)



initial=source=chk final=source=chk spectroscopy=onephotonemission print=(huangrhys,matrix=JK)



td_Azulene.chk

opt_Azulene.chk复制代码Huang-Rhys因子计算的输入参考了kalinite老师的帖子，内坐标贡献计算的输入参考了此贴sob老师和坛友Uus/pMeC6H4-/キ的回答。

Tips：

freq=intmode和IOp(7/75=-1)是打印冗余内坐标对正则模式的贡献，剩下的freq=FCHT这些是用来计算重组能的如果算发射过程就是spectroscopy=onephotonemission，算吸收过程是spectroscopy=onephotonabsorption，同时initial态与final态的chk位置需要对调





常见报错ERROR: Low progression after class xxx. Total convergence = xxx%.复制代码这个报错可无视，只要Huang-Rhys因子正常打印就能正常分解重组能

FileIo operation on non-existent file.复制代码这个报错九成概率是chk位置放反引起的，应首先检查initial态和final态chk文件的位置有没有放反。如果确信无误，检查chk文件是否损坏



分解重组能

运行完成后，用脚本处理log文件：

./intmode huang-rhys.log复制代码首先输出了所有冗余内坐标的贡献：

====================================================================================================

Internal Coordinate Contribution to Reorganization Energy

====================================================================================================



Detailed Contributions by Coordinate Type:

----------------------------------------------------------------------------------------------------



R (Bond Lengths/Angles/Dihedrals):

   Coord         Definition Contribution(%)

---------------------------------------------

     R12              R(6,7)         2.9900

      R6              R(3,5)         2.9900

     R11             R(5,13)         2.9407

....





A (Bond Lengths/Angles/Dihedrals):

   Coord         Definition Contribution(%)

---------------------------------------------

     A12           A(6,4,11)         3.3113

      A6            A(3,2,9)         3.3041

     A11           A(1,4,11)         3.2275

....





D (Bond Lengths/Angles/Dihedrals):

   Coord         Definition Contribution(%)

---------------------------------------------

     D19         D(11,4,6,7)         0.9518

     D11          D(9,2,3,5)         0.9518

      D8         D(8,1,4,11)         0.8774

....





复制代码随后求了总和，这个是饼图的数据：

====================================================================================================

Summary: Total Contribution by Coordinate Type

====================================================================================================



     Coordinate Type        Total %              Description

------------------------------------------------------------

    R (Bond Lengths)          33.62%

     A (Bond Angles)          58.93%

 D (Dihedral Angles)           7.24%

============================================================



Total (should be ~100%): 99.79%



Internal coordinate contributions saved to: intmode.dat

Reorganization energy data saved to: lambda.dat复制代码详细内容存在intmode.dat。另外顺便把分解重组能的结果整理了一下，在lambda.dat。



用输出的dat文件里的数据就能画出来论文里常见的这种图了：








QQ截图20251127220441.png (19.66 KB, 下载次数 Times of downloads: 159)

下载附件 Download



2025-11-27 22:13 上传 Uploaded













QQ截图20251127220134.png (25.88 KB, 下载次数 Times of downloads: 163)

下载附件 Download



2025-11-27 22:13 上传 Uploaded










下载

源码





intmode.cpp

(25.36 KB, 下载次数 Times of downloads: 39)



2025-12-3 17:16 上传 Uploaded
点击下载
Click to download








也可以去GitHub：bane-dysta/intmode

预编译版和例子





intmode.7z

(2.34 MB, 下载次数 Times of downloads: 91)



2025-12-3 17:16 上传 Uploaded
点击下载
Click to download

### 2 楼

楼上好像有人需要，mingw编译了一个window版，测试是没问题的

### 3 楼

我将在下一届相关高级量子化学教程讲振动电子光谱的幻灯片里提及此程序

### 4 楼

sobereva 发表于 2025-11-28 10:52

我将在下一届相关高级量子化学教程讲振动电子光谱的幻灯片里提及此程序

哇，被高级班收录了，那我找时间修缮一下，这帖子昨天发的有点随手了

### 5 楼

wal 发表于 2025-11-28 19:28

哇，被高级班收录了，那我找时间修缮一下，这帖子昨天发的有点随手了

大佬，太强了。之前想做这个的时候，使用IOp(7/75=-1)内部选项没有效果，原来是要在Gaussian计算振动分辨电子光谱中设置呀。现在看看那个IOp的描述明明都提示了“正常模式位移”，属实被自己蠢到了。

### 6 楼

谢积环 发表于 2025-12-2 15:20

大佬，太强了。之前想做这个的时候，使用IOp(7/75=-1)内部选项没有效果，原来是要在Gaussian计算振动分辨 ...

啊其实不一定要在振动光谱里呀。这个IOp是配合freq=intmode用的，他俩单独搭配也会生效的

### 7 楼

wal 发表于 2025-12-2 16:24

啊其实不一定要在振动光谱里呀。这个IOp是配合freq=intmode用的，他俩单独搭配也会生效的

哦哦，那我再试试了

### 8 楼

老师好，我想请教一下关于Gaussian分解键长/键角/二面角对重组能的贡献，我的计算步骤如下：先将分子根据该关键词进行基态和激发态计算，#p opt freq b3lyp/6-311g(d) scrf=(solvent=toluene)、#p opt freq td=(nstates=5,root=1) cam-b3lyp/6-311g(d)

scrf=(solvent=toluene)

然后根据老师的输入进行Huang-Rhys因子计算，结果如附图1，结果显示出现错误，随后用老师写的脚本进行分解，结果显示重组能为零。如附图2，请问老师，整个过程哪里出现了问题？

### 9 楼

谢积环 发表于 2025-12-2 15:20

大佬，太强了。之前想做这个的时候，使用IOp(7/75=-1)内部选项没有效果，原来是要在Gaussian计算振动分辨 ...

这个一般翻译成“简正模式”而不是“正常模式”吧

### 10 楼

本帖最后由 wal 于 2025-12-3 11:39 编辑 

Bamind 发表于 2025-12-3 10:35

老师好，我想请教一下关于Gaussian分解键长/键角/二面角对重组能的贡献，我的计算步骤如下：先将分子根据该 ...

目前我电脑不在手边，不过根据我的经验，file io类报错大概率是td和opt的chk位置放反引起的，你可以检查一下有没有此类问题。如果确信无误，我晚上回去给你看下

### 11 楼

老师您例子中计算的S0与S1态结构的重组能包含了S0→S1和S1→S0两部分的弛豫能，那您的程序可以计算分解键长/键角/二面角对S1→S0弛豫能的贡献吗？

### 12 楼

wal 发表于 2025-12-3 11:37

目前我电脑不在手边，不过根据我的经验，file io类报错大概率是td和opt的chk位置放反引起的，你可以检查 ...

看了一下我的输入文件，确实放反了

### 13 楼

杲杲出日 发表于 2025-12-3 13:01

老师您例子中计算的S0与S1态结构的重组能包含了S0→S1和S1→S0两部分的弛豫能，那您的程序可以计算分解键长 ...

没有吧，spectroscopy=onephotonemission就是纯计算S1→S0啊，onephotonabsorption才是S0→S1

### 14 楼

wal 发表于 2025-12-3 16:32

没有吧，spectroscopy=onephotonemission就是纯计算S1→S0啊，onephotonabsorption才是S0→S1

我明白了，谢谢老师。那想分解anion和S0之间重组能，也是相同的操作吗

### 15 楼

wal 发表于 2025-12-3 11:37

目前我电脑不在手边，不过根据我的经验，file io类报错大概率是td和opt的chk位置放反引起的，你可以检查 ...

老师，更正chk文件的位置之后出现了新的问题，显示

ERROR: Low progression after class 2. Total convergence =  0.0%.

        The vibronic spectrum will likely be unreliable. Stopping.

随后查看了Kalinite老师的帖子 基于Gaussian FCHT计算分解重组能和计算Huang-Rhys因子的Python小脚本

http://bbs.keinsci.com/forum.php ... 8&fromuid=70892

(出处: 计算化学公社)

大家也有类似的问题，Kalinite老师回复说若只需要重组能和Huang-Rhys因子，无视该报错即可。想请问一下，如果继续用脚本处理分解键长/键角/二面角对重组能的贡献能进行下去吗？

### 16 楼

Bamind 发表于 2025-12-3 16:49

老师，更正chk文件的位置之后出现了新的问题，显示

ERROR: Low progression after class 2. Total conve ...

对的 这是振动分辨光谱的报错 无需在意 分解重组能只要Huang-Rhys正常打印即可

## 入库完整性评估

- 主帖全文收录
- 全部回复完整收录
