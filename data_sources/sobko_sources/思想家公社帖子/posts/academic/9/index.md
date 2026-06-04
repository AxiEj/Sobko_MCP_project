---
post_id: 9
title: mpich2多节点并行运算的设置
url: http://sobereva.com/9
date: '2015-06-02T18:07:00+08:00'
source_categories:
- 其它
primary_topic: 其它软件
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章是MPICH2多节点并行设置，属于计算化学环境与软件配置经验。
topic_family: 软件
exclude_reason: ''
confidence: 0.82
image_count: 0
local_assets_dir: assets
---

**mpich2多节点并行运算的设置**Settings of mpich2 for multi-node parallel calculation  
  
文/Sobereva @[北京科音](http://www.keinsci.com)   写于约2008年

  
  
在单节点上使用mpich2，编译并行amber9并且并行运行的方法我前面已经介绍过了，下面介绍mpich2通用的多节点的设置方法，关于amber的并行设置，都在之前的帖子里。这里用root，fedora7。建立多节点并行运算，是计算化学工作者必备的能力，这里讲得详细些。  
  
  
这里假设有两台电脑，分别叫vmware1和vmware2，IP分别为192.168.0.2和192.168.0.3  
  
  
在两台电脑上都运行下列步骤：  
  
-------------------------------  
如果fortran编译器装了ifort，运行export FC=/opt/intel/fce/10.0.023/bin/ifort  
  
复制mpich2-1.0.6.tar.gz到/sob，解压到/sob/mpich2-1.0.6，进入此目录，运行：  
./configure  
make  
make install  
  
运行  
touch /etc/mpd.conf             
  
chmod 700 /etc/mpd.conf  
将下面加入mpd.conf:  
secretword=<secretword>            (比如secretword=ltwd)  
  
修改/etc/hosts，把里面的内容改为  
192.168.0.2 vmware1  
192.168.0.3 vmware2  
  
这样在linux中就可以用主机名称来代替IP了。  
  
  
  
修改/root/mpd.hosts，把里面的内容改为  
vmware1  
vmware2  
  
---------------------------------  
  
  
为了使MPICH2可以在两台电脑上相互传输数据，必须把ssh打通，也就是不用密码即可直接用ssh在电脑之间登陆，方法如下：  
  
  
在vmware1中：  
运行ssh-keygen -t rsa    全都按回车用默认，生成了RSA密钥  
cd /root/.ssh  
cp id_rsa.pub authorized_keys  
建立本身的信任连接：ssh vmware1   回答输入yes  
  
  
在vmware2中：  
运行ssh-keygen -t rsa    全都按回车用默认  
把vmware1中的/root/.ssh/*复制到vmware2中/root/.ssh/ 全部覆盖  
chmod 700 /root/.ssh/*        把.ssh内的文件设为root专用  
ssh vmware1              回答输入yes  
  
  
测试ssh:  
无论在vmware1还是vmware2，无论ssh vmware1还是ssh vmware2，现在都应当可以不输入任何东西直接登陆。  
可以用这个命令来验证是否无误，比如ssh vmware1 date，如果显示了日期，就没问题了。  
  
  
现在，在任意一台电脑中，输入mpdboot -n 2，就在两台电脑上都同时启动mpd了，-n 2代表启动2台上的mpd。要想并行运算，必须开启mpd才行。如果此时提示无法打开mpd.hosts，但确实已经在root下建立了mpd.hosts文件，则用mpd.hosts -n 2 -f /root/mpd.hosts来具体指定mpd.hosts的位置并启动mpd。  
  
然后运行mpdtrace，察看现在有哪些电脑可以并行运算了，应当显示：  
vmware1  
vmware2  
  
假设两台电脑都是双核，运行mpirun -np 4 sander.MPI xxxxxxxxxx就可以在两台电脑上同时运行sander了，自动调用总共4个core。注意用mpirun所运行的并行程序，必须存在于两台电脑相同位置上。  
  
如果退出mpd，输入mpdallexit。  
  
  
  
  
注意：两台电脑的mpich2安装位置最好一样，/etc/mpd.conf中的密码应当相同。  
  
验证是否可以多节点正常并行运算，可运行mpirun -np number /sob/mpich2-1.0.6/examples/cpi number为使用的core数。这是一个测试程序。  
  
  
  
  
以上方法适用于建立n台电脑并行运算。多个节点上，CPU不能100%满载是正常的，在一定程度上受限于网络连接方式，比如把100M网换到1000M网会有好处，若能用InfiniBand、Myrinet等专适于HPC的连接方式当然更好，只是没钱，只能用以太网了。如今中档芯片组大都集成1000M控制器，中档主板也带了1000M支持，便宜的realtek 1000M芯片的网卡诸如TP-LINK的，才35元。当然别忘了用超五类或者六类线。  
  
以上内容在vmware station 6，XP SP2，Q6600建立两台双核虚拟机测试通过。值得一提的是，vmware6中fedora下，网卡虚拟的是82545EM千兆网卡，双虚拟机互连速度是够了。这种方式可以解决目前vmware版本不支持4核的问题，经本测试，这种方式可以达到实际fedora中单节点4核速度的82%，实际运算速度等于单核的三倍，还是可以满意的。在测试过程中，虚拟机的网络用vmnet1也就是host-only方式，这样虚拟机之间以及主机之间可以互相访问，可以共享上网，比较方便。  
  
在双虚拟机中双节点并行跑amber在系统监视器中会看到数据吞吐量往往最高也才十几兆，当初我也怀疑是否实际上虚拟的是100M网。后来将监控的速度间隔调成0.25s，才发现峰值数据吞吐速度远高于100M网的限制，只是瞬间传一次数据后，持续几秒不传输数据，所以如果用了1s一次检测速度，会取平均值，误令人以为虚拟千兆网卡是假的。  
  
另外在vmware6中，可以将多个虚拟机建立一个team，在team中，虚拟机互相之间和外界是封闭的，并且可以在team里的虚拟机之间建立高速网络连接，没有数据传输速度上限，但经我测试，速度相对于vmnet1方式连接没有丝毫提升。而且team里面无论是开机关机都必须同时进行，不够灵活。team方式至少对跑amber9来说没有太大作用。但是我发现vmware6虚拟XP仍然是虚拟的100M AMD网卡，这种team内提供的专线虚拟机互联方式，对于XP虚拟机之间传输数据会有好处。
