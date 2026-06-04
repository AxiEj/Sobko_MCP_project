---
post_id: 258
title: 使用Gaussian时的几个实用脚本和命令
url: http://sobereva.com/258
date: '2015-06-08T00:11:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 结构与文件格式
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章是Gaussian常用脚本和命令汇总，核心是软件使用技巧。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**使用Gaussian时的几个实用脚本和命令**  
Several useful scripts and commands of using Gaussian

文/Sobereva @[北京科音](http://www.keinsci.com)

First release: 2014-Nov-5  Last update: 2022-Jun-6

本文提供几个平时Gaussian计算时常用的简单小脚本和命令，对于实际研究很有用处，也希望读者能举一反三。另外也非常建议读者看看《详谈Multiwfn的命令行方式运行和批量运行的方法》（<http://sobereva.com/612>），里面对脚本编写有深入浅出的介绍和不少例子，仔细看过后就能轻松理解下文介绍的各种脚本并随意改编。

## 1 依次执行多个指令

比如要依次执行g09 < 1.gjf > 1.out、g09 < 2.gjf > 2.out、g09 < 3.gjf > 3.out，可以只输入一条命令，每条命令间用分号隔开：  
g09 < 1.gjf > 1.out;g09 < 2.gjf > 2.out;g09 < 3.gjf > 3.out

也可以写一个文本文件比如t.sh，里面写上  
g09 < 1.gjf > 1.out  
g09 < 2.gjf > 2.out  
g09 < 3.gjf > 3.out

然后用chmod +x *给它加上可执行权限，再输入./t.sh运行即可（后同）。

如果不让指令依次执行，而是同时执行，把每行命令后面都加上&即可。

## 2 一次性执行当前目录下所有Gaussian输入文件

把以下内容存到比如runall.sh里，然后执行之即可。会把每个.gjf文件用g09执行，生成同文件名但后缀为.out的输出文件。脚本会提示正在运行哪个文件，运行完之后还会输出用时多少。  
#!/bin/bash  
icc=0  
nfile=`ls ./*.gjf|wc -l`  
for inf in *.gjf  
do  
((icc++))  
echo Running ${inf} ... \($icc of $nfile\)  
time g09 < ${inf} > ${inf//gjf/out}  
echo ${inf} has finished  
echo  
done

PS：如果是windows环境，需要写DOS批处理脚本，实现方式见《从高斯windows下的批量执行谈DOS批处理文件》（<http://sobereva.com/6>）。

## 3 一次性把当前目录下所有chk文件转换为fchk文件

把以下内容存到比如chk2fch.sh里，然后执行之即可。会依次调用formchk把当前目录下每个chk转换为同文件名的.fchk文件。  
#!/bin/bash  
for inf in *.chk  
do  
formchk ${inf}  
done

## 4 一次性执行当前文件夹下所有子目录里的Gaussian输入文件

此脚本会依次进入当前目录下的每个下一级目录，并把其中的.gjf都依次执行，产生的.out文件的文件名和所在位置都和输入文件相同。把以下内容存到比如folder_runall.sh里，然后执行它之即可。  
#!/bin/bash  
shopt -s nullglob  
for i in `ls -F |grep /`  
do  
cd $i  
for inf in *.gjf  
do  
echo Running ${inf} ...  
time g09 < ${inf} > ${inf//gjf/out}  
echo ${inf} has finished  
echo  
done  
cd ..  
done

上面的脚本只能进入下一级的目录，而再下一级的目录（或者更深的目录）里的.gjf文件，以及当前目录下的.gjf文件都不会执行。如果想把这些.gjf也都执行，应当把以下内容存到比如allfolder_runall.sh里，然后执行它。为清楚起见，每次进入新的目录时屏幕上都会提示。  
#!/bin/bash  
shopt -s nullglob  
for i in `ls -R |grep :|tr : " "`  
do  
echo  
cd $i  
echo "****** Entered" $i folder;echo  
for inf in *.gjf  
do  
echo Running ${inf} ...  
time g09 < ${inf} > ${inf//gjf/out}  
echo ${inf} has finished;echo  
done  
cd - > /dev/null  
done

## 5 字符替换

下面这个方法可以批量修改计算的级别和任务类型。

例如将当前目录下包括任意级子目录下的.gjf中的M062X替换为B3LYP，执行：sed -i "s/M062X/B3LYP/g" `grep M062X -rl *|grep .gjf`

如果要替换的字符有*、/这样的符号，需要前面加上\避免被sed转义。比如6-31G**需要写成6-31G\*\*，M062X/cc-pVTZ需要写成M062X\/cc-pVTZ。另外，如果有括号或空格出现，那么grep后面应该用双引号括住。  
例如把MP2/6-311+G(2d,p)都替换成M062X/6-31G*：sed -i "s/MP2\/6-311+G(2d,p)/M062X\/6-31G\*/g" `grep "MP2/6-311+G(2d,p)" -rl *|grep .gjf`  
例如把opt freq都替换成NMR关键词：sed -i "s/opt freq/NMR/g" `grep "opt freq" -rl *|grep .gjf`

如果只想替换当前目录下的.gjf，则把-rl改成-l即可。如果想处理所有文件而不仅限于.gjf，则把|grep .gjf部分删掉即可。

## 6 批量删除文件

用下面的命令可以删除当前目录和任意级子目录下的所有.out文件  
find ./ -name "*.out"|xargs rm -f

## 7 显示几何优化收敛情况

这个很简单。比如C4H8.out是几何优化输出文件，执行  
grep Converged C4H8.out -A4  
就会把当前的优化收敛情况输出出来。

如果执行  
grep Converged C4H8.out -c  
就会输出匹配的次数，也就是相当于显示优化到了第几步了。

也可以执行grep -E "out of|Converged" C4H8.out -A4，这样步数和收敛情况都会输出。

## 8 做Counterpoise任务时只用一半的BSSE校正能

笔者在《谈谈BSSE校正与Gaussian对它的处理》（<http://sobereva.com/46>）专门谈过BSSE校正问题。在J. Chem. Theory Comput., 10, 49 (2014)文中，作者建议对于<= aug-cc-pVTZ档次基组的计算时如果用Counterpoise方式考虑BSSE，应当只用一半BSSE校正能。但是直接用Gaussian的Counterpoise关键词只会产生不考虑和考虑完整的BSSE校正能的情况。如果把以下脚本放到当前目录，而且当前目录里有一批使用了Counterpoise关键词的.log输出文件，程序就会计算出只使用了一半BSSE校正能的结果。

for filename in `ls -v *.log`  
do  
echo $filename":"  
Edimer=`grep "Counterpoise corrected energy =" $filename | awk -F = '{print $2}'`  
EBSSE=`grep "BSSE energy =" $filename | awk -F = '{print $2}'`  
Esum=`grep "sum of fragments =" $filename | awk -F = '{print $2}'`  
echo "($Edimer-$EBSSE*0.5-$Esum)*627.51" |bc | awk '{printf "%6.2f", $0}'  
echo " kcal/mol"  
done

结果显示在屏幕上，如下所示  
1.log:  
 -3.03 kcal/mol  
2.log:  
-31.46 kcal/mol  
3.log:  
-20.91 kcal/mol  
...略

## 9 将当前目录下所有Gaussian输出文件(out)转换为输入文件(gjf)

参见下文，需要利用Multiwfn程序。  
一键把所有gjf文件转成xyz文件、把所有Gaussian输出文件转成gjf文件的脚本  
<http://sobereva.com/530>（<http://bbs.keinsci.com/thread-16161-1-1.html>）

### 10 显示当前目录下所有out文件最后一次SCF Done的能量

比如当前目录下有一大批分子做几何优化的输出信息，我们想把最后一次含有SCF Done的行连同输出文件名显示出来，由此得到每个体系最终结构下的电子能量，可以用以下脚本

#!/bin/bash  
for inf in *.out  
do  
tac $inf | grep -m 1 "SCF Done" | tr '\n' ' '  
echo $inf  
done

输出信息示例：  
SCF Done:  E(RB3LYP) =  -619.115825500     A.U. after    1 cycles C16H16.out   
SCF Done:  E(RB3LYP) =  -696.562886104     A.U. after    1 cycles C18H18.out   
SCF Done:  E(RB3LYP) =  -773.962700591     A.U. after    1 cycles C20H20.out   
...略
