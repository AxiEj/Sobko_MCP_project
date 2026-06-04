---
post_id: 143
title: 将Material Studio的xtd轨迹文件导出为xyz轨迹文件的方法
url: http://sobereva.com/143
date: '2015-06-07T23:56:00+08:00'
source_categories:
- 分子模拟
primary_topic: 结构与文件格式
secondary_topics:
- 分子动力学
- 其它软件
academic_relevant: true
classification_reason: 内容是把Material Studio的xtd轨迹导出为xyz轨迹，核心是轨迹文件转换。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**将Material Studio的xtd轨迹文件导出为xyz轨迹文件的方法**  
The way to export xtd trajectory file of Material $tudio to xyz trajectory file

文/Sobereva @[北京科音](http://www.keinsci.com/)  First release: 2012-May-23

Material Studio(MS)的xtd文件包含了原子或者粗粒化模拟中的bead的轨迹信息。这是MS的私有格式，为了能将轨迹放到其它程序，比如VMD中做更灵活细致的分析，需要转换为通用轨迹格式。xtd文件内含的实际轨迹信息实际上储存在同目录下的同名的.trj隐藏文件里（二进制文件），一种转换成通用格式的方法是利用MS自带的trj2ascii.exe程序将.trj文件内容转换成普通文本文件，然后再写个程序将其转换成其它轨迹格式。但这样步骤稍微麻烦些。

另一种做法是直接利用MS内部支持的Perl脚本，循环每一帧每一个原子或Bead，将其坐标属性写入到外部文本文件。比如按照常见的xyz坐标格式来写，就可以生成xyz轨迹了，可以被VMD等程序直接载入。

在<http://chembytes.wikidot.com/materials-studio>上有人提供了现成的这样的Perl脚本将原子轨迹转换成xyz轨迹。我进一步对其进行了修改使之用起来更方便些，另外加入了对周期性体系的支持。脚本如下所示

#!perl  
 #**********************************************************  
 #*                                                        *  
 #*     XTD2XYZ - Convert XTD files into XYZ ormat        *  
 #*                                                        *  
 #**********************************************************  
 # Version: 0.1  
 # Author: Andrea Minoia  
 # Date: 08/09/2010  
 #  
 # Convert MS trajectory xtd file into xYZ trajectory file.  
 # Backup of files that are about to be overwritten is managed  
 # by MS. The most recent file is that with higher index number (N)  
 # The script has to be in the same directory of the  
 # structure to modify and the user has to update the  
 # variable $doc (line 31) according to the name of the  
 # file containing the trajectory.  
 # The xmol trajectory is stored in trj.txt file and it is not  
 # possible to rename the file within MS, nor it is possible to  
 # automatically export it as xyz or car file. You should manage  
 # the new trajectory manually for further use (e.g. VMD)  
 #   
 # Modificator: Sobereva ([sobereva@sina.com](mailto:sobereva@sina.com))  
 # Date: 2012-May-23  
 # The range of the frames to be outputted can be altered by line 49 and 51

use strict;   
 use MaterialsScript qw(:all);

#open the multiframe trajectory structure file or die   
 my $doc = $Documents{"./benzene.xtd"};

if (!$doc) {die "no document";}

my $trajectory = $doc->Trajectory;

if ($trajectory->NumFrames>1) {

    print "Found ".$trajectory->NumFrames." frames in the trajectory\n";  
     # Open new xmol trajectory file  
     my $xmolFile=Documents->New("trj.txt");  
       
     #get atoms in the structure  
 #    my $atoms = $doc->Atoms;  
     my $atoms = $doc->DisplayRange->Atoms;  
     my [$Natoms=@$atoms](mailto:$Natoms=@$atoms);

    # loops over the frames  
     my $framebegin=1;  
     my $frameend=$trajectory->NumFrames;  
 #    my $frameend=10;  
     for (my $frame=$framebegin; $frame<=$frameend; ++$frame){  
         $trajectory->CurrentFrame = $frame;  
         #write header xyz  
         $xmolFile->Append(sprintf "%i \n", $Natoms);  
         $xmolFile->Append(sprintf "%s %i \n", "Frame",$frame);  
         foreach my $atom (@$atoms) {  
             # write atom symbol and x-y-z- coordinates  
             $xmolFile->Append(sprintf "%s %f  %f  %f \n",$atom->ElementSymbol, $atom->X, $atom->Y,

$atom->Z);   
         }      
     }   
     #close trajectory file  
     $xmolFile->Close;  
 }   
 else {   
     print "The " . $doc->Name . " is not a multiframe trajectory file \n";   
 }

使用时先将这些内容复制到一个文本文件里，后缀名改为.pl。然后在MS里将这个.pl加入到项目中。要转换哪个目录下的xtd文件就把这pl文件挪到哪个目录中，并且把my $doc = $Documents{"./benzene.xtd"}; 当中的文件名改成要转换的文件名。之后，保持此脚本文件窗口处于激活状态，选tools-scripting-debug（或者直接按F5，或者按工具栏的蓝色三角按钮）就开始对xtd文件进行转换，转换结束后在当前目录下会输出trj.txt文件。将其后缀改为.xyz之后就能被VMD等程序直接读取了。

debug模式对于大体系、帧数较多的轨迹转换起来颇慢，可以用tools-scripting-Run on server模式来运行，这样转换速度明显快得多，trj.txt将会生成到新的目录，当前目录下的其它文件也会被强行复制过去一份。

此脚本默认转换所有帧。如果想转换指定帧数范围，就把my $framebegin=1;和my $frameend=10;改成自定的起止帧号就行了，需要先将my $frameend=10;前面的注释去掉。

如果是周期性体系，那么在MS当中看起来轨迹是什么样转换过去就是什么样。比如，如果在display style-lattice中在某个方向上多显示一个周期，那么转换出的轨迹在相应方向上也会多出一倍原子。Default、In-Cell、Original的显示模式下转换出的原子坐标也会相应地可能有所不同。

上面的这个名为xtd2xyz脚本只能转换全原子模拟的轨迹，如Forcite的xtd轨迹，却不能转换粗粒化模拟的轨迹，如Mesocite的以bead描述粒子的xtd轨迹。我将之修改成下面的xtdbead2xyz脚本，专门用来转换粗粒化模拟的轨迹（但不能转换全原子的），用法同前。

#!perl  
# XTDbead2XYZ - Convert the XTD files containing beads into XYZ format  
# Creator: Sobereva ([sobereva@sina.com](mailto:sobereva@sina.com))  
# Date:    2012-May-23

use strict;   
use MaterialsScript qw(:all);

#open the multiframe trajectory structure file or die   
my $doc = $Documents{"./bilayer.xtd"};

if (!$doc) {die "no document";}

my $trajectory = $doc->Trajectory;

if ($trajectory->NumFrames>1) {

    print "Found ".$trajectory->NumFrames." frames in the trajectory\n";  
    # Open new xmol trajectory file  
    my $xmolFile=Documents->New("trj.txt");  
      
    #get atoms in the structure  
    my $Beads = $doc->DisplayRange->Beads;  
    my [$NBeads=@$Beads](mailto:$NBeads=@$Beads);

    # loops over the frames  
    my $framebegin=1;  
    my $frameend=$trajectory->NumFrames;  
#    my $frameend=10;  
    for (my $frame=$framebegin; $frame<=$frameend; ++$frame){  
        $trajectory->CurrentFrame = $frame;  
        #write header xyz  
        $xmolFile->Append(sprintf "%i \n", $NBeads);  
        $xmolFile->Append(sprintf "%s %i \n", "Frame",$frame);  
        foreach my $Bead (@$Beads) {  
            # write atom symbol and x-y-z- coordinates  
            $xmolFile->Append(sprintf "%s %f  %f  %f \n",$Bead->Name, $Bead->X, $Bead->Y, $Bead-

>Z);   
        }      
    }   
    #close trajectory file  
    $xmolFile->Close;  
}   
else {   
    print "The " . $doc->Name . " is not a multiframe trajectory file \n";   
}
