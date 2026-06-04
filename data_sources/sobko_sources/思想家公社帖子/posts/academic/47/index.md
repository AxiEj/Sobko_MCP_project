---
post_id: 47
title: Gaussian03的Linda并行设置与VMware的虚拟集群
url: http://sobereva.com/47
date: '2015-06-05T01:28:00+08:00'
source_categories:
- 量子化学
primary_topic: Gaussian
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 主要讲 Gaussian 03 的 Linda 并行设置与 VMware 虚拟集群。
topic_family: 软件
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**Gaussian 03的Linda并行设置与VMware的虚拟集群**Linda parallel setup of Gaussian 03 and VMware virtual cluster  
文/Sobereva @[北京科音](http://www.keinsci.com/)  
First release: 2009-Sep-13    Last update: 2014-Sep-8

  
  
网上也有一些关于高斯linda并行设置的文章，也有讨论使用虚拟机模拟的集群跑高斯+linda的，但是说明都不甚具体，各种linux发行版本差异也不小，拿到手的高斯程序也有所不同，其设置方法往往不能直接套用。最近也有人问配置Linda的问题，故撰此文详细说明一下，只要使用与本文相同的软件环境，严格按照本文步骤，一定可以顺利地设置成功。另外对于vmware虚拟机虚拟集群跑g03+linda的效率也进行一些讨论。  
  
本文使用的是Gaussian03 C.02，压缩包自带用Linda程序7.1版，无需另行下载任何程序。在linda-exe子目录包含了已编译好的.exel后缀的专用于linda并行的高斯子程序。压缩包可以在这里下载<http://pan.baidu.com/s/1qWyKTmG>。  
  
由于条件窘迫没有实际的节点配置相仿佛的集群环境，只有四核单机，故用vmware 6.0.1做两个相同的双核虚拟机来组集群介绍Linda设置。两虚拟机内存皆500MB，主机操作系统WinXP SP2，虚拟机操作系统使用我认为最经典、最好用的Fedora7-64bit，都使用root账户（密码可以不一致），使用bash。主机CPU为Q6600(oc 3.0)。如果已有多个实际主机，则只看本文第二部分就行了。  
  
关于Gaussian的并行模式这里说一下。Gaussian的并行是通过openmp来实现的，但是openmp只适合共享内存架构。Gaussian的跨节点运算并不是通过科学计算软件常用的MPI实现，而是通过ACSI的Linda软件。Linda提供了一个虚拟的共享内存(VSM)环境，它将集群中的主机结合起来，获得一个全局的逻辑的共享内存，原始程序依靠这个环境实现跨节点并行运算只需要添加简单的指令来控制数据的交换即可。这样使用openmp并行方式的Gaussian就可以很容易地在集群环境中并行运行了。  
  
  

### 1 配置虚拟机集群环境

安装vmware，会自动给系统里增加一堆服务，都允许启动，并且会看到网络连接里多出VMnet1和VMnet8。之后启动vmware新建个虚拟机，configuration用custom，操作系统选Linux，version用Other Linux 2.6.x kernel 64bit，虚拟机名称设f71，Network connection设Use host-only networking，其它设置都随意，视情况而定。  
  
新建好虚拟机后找一个Fedora7-64bit安装盘或镜像文件。虚拟机名称点右键选setting，CD-ROM里面加载fedora7镜像文件，或者直接使用物理光驱读主机光驱里的fedora7光盘。之后照常安装系统，选择要安装的应用程序时将Software Development大类也选上，安装中提示的防火墙和selinux配置都关掉避免影响网络连接。装好后在虚拟机列表对应名称上点右键选Install VMware tools，之后Vmware tools的光盘应当被加载进了虚拟机的光驱里（/media/VMware Tools），进去将VMwareTools-6.0.1-55017.tar.gz解压到某处，进入其目录运行vmware-install.pl，只需要一直按回车就行了，最后设合适的分辨率。这样虚拟机就支持文件直接从主机拖放进去，可以在主机和虚拟机之间直接复制文本，也可以共享主机目录，方便使用。对系统根据自己使用习惯进行一些设置后关闭f71虚拟机。  
  
用vmware克隆功能将f71克隆（full clone方式）出一个名为f72的主机。建议此时将f71和f72都分别用take snapshot功能制作一个镜像，方便以后恢复到当前状态。  
  
察看vmware程序的Edit-Virtual Network Editor，Summary里面列表中会有个Host-only项，在我这里是VMnet1，相应的subnet显示的是192.168.153.0。这种情况下虚拟机IP地址应当设为192.168.153.x，但不能与实际主机的网络连接里VMnet1的IP地址一致（默认是通过DHCP分配的，我这里被分配为192.168.153.1）。  
  
现在以断网的方式启动f72，即启动f72后马上双击vmware右下角网卡图标后把connect对钩去掉，并且选择host-only。将f72的网络配置界面（图形界面的System-Administration-Network）中的所有网卡删掉，添加个新的网卡以避免MAC地址与f71的冲突，IP地址添192.168.153.4，子网掩码255.255.255.0，DNS标签页的Hostname填f72，其它留空。保存后重启，在刚刚出现vmware的logo时双击网卡图标把connect再钩上。  
  
f72启动后启动f71，网络配置界面里IP地址添192.168.153.3，子网掩码255.255.255.0，DNS标签页的Hostname填f71，其它留空，重启f71。  
  
此时，实际主机、f71虚拟机、f72虚拟机这三台计算机就组成了一个虚拟的内部的局域网，互相应该都能ping通了。这就是vmware的Host-only模式。  
  
  

### 2 设置G03+Linda并行运行环境

现在我们就可以看作有了两台实际的计算机，主机名分别为f71和f72，IP分别为192.168.153.3和192.168.153.4。（如果有两台真实主机，网络配置界面也应按上述虚拟机的进行设置，并关掉防火墙和selinux）  
  
f71和f72都作如下设置：  
  
修改/etc/hosts，添加IP地址与主机名的对应关系，删掉默认设的内容，都改为  
192.168.153.3    f71  
192.168.153.4    f72  
之后重启。  
  
把高斯压缩包解压到/sob/g03，并建立/sob/g03/scratch目录作为临时文件目录。跨节点计算必须每个节点上都有相同程序在相同位置，如果不想每个节点都存一份程序，可以用NFS方式共享，设置方法见附录。  
  
添加以下内容至/root/.bashrc  
export g03root=/sob  
source /sob/g03/bsd/g03.profile  
export GAUSS_SCRDIR=/sob/g03/scratch  
export GAUSS_LFLAGS='-vv -nodelist "f71 f72"'  
（这里-nodelist指定并行运算的节点，-vv代表very verbose输出，便于监控。我们也可以通过节点列表文件来指定使用哪些节点，比如创建一个/sob/a.txt文件，里面写两行，内容分别为f71和f72，然后export GAUSS_LFLAGS='-vv -nodefile /sob/a.txt'，效果是等价的。）  
  
之后在/sob/g03、/sob/g03/bsd、/sob/g03/linda-exe、/sob/g03/linda7.1/intel-linux2.4-rh8/bin文件夹下使用chmod 700 *来设定权限。  
改/sob/g03/ntsnet里面的/haydn/s0/scratch/frisch/g03/linda7.1/intel-linux2.4-rh8/为自己的路径/sob/g03/linda7.1/intel-linux2.4-rh8/  
（此文件里的TSNET_PATH环境变量路径我们不用理会，因为Gaussian03的Linda并行运行过程中不会用到它）  
改/sob/g03/linda7.1/intel-linux2.4-rh8/bin/LindaLauncher里面的/haydn/s0/scratch/frisch/g03/linda7.1/intel-linux2.4-rh8/为自己的路径/sob/g03/linda7.1/intel-linux2.4-rh8/  
  
Linda支持rsh（默认）和ssh方式连接不同节点，rsh和ssh实际速度经测试没有太大差异，而fedora7要想打开rsh步骤比较繁琐，所以这里用ssh。跨节点运行默认设置文件即global config file是/sob/g03/linda7.1/common/lib/tsnet.config。如果需要自定义参数，可以直接修改此文件，也可以创建并修改当前用户主目录下的.tsnet.config（这里即/root/.tsnet.config），里面的设置将会把默认配置文件的相应条目覆盖。我们这里直接修改默认参数文件/sob/g03/linda7.1/common/lib/tsnet.config，将里面的Tsnet.Node.lindarsharg后面的rsh改为ssh，其它不用改。（其它参数的意义可以下载http://www.lindaspaces.com/downloads/lindamanual.pdf查看第三章）  
  
接下来要使得f71与f72之间可以不需要密码直接通过ssh运行指令。  
在f71中：  
运行ssh-keygen -t rsa    全都按回车用默认，生成了RSA密钥  
cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys  
在f72中：  
运行ssh-keygen -t rsa    全都按回车用默认  
把f71中的/root/.ssh/下全部文件复制到f72中/root/.ssh/进行覆盖  
运行chmod 700 /root/.ssh/*        把.ssh内的文件设为root专用  
运行ssh f71           回答yes  
在f71中：运行ssh f72，回答yes  
  
为了测试ssh是否设好，在f71输入ssh f72 date，以及在f72输入ssh f71 date，如果都不需要密码并且显示了日期，就说明无密码ssh设置成功了。这样Linda就可调用ssh在远程节点上直接执行指令了。  
  
（如果有特殊原因必须用rsh，则不需要改tsnet.config文件，也不必进行上面ssh的设置。但需要节点间可以通过rsh和rlogin以无密码方式连接。在Fedora7下面设置rsh的方法见附录）  
  
此时准备工作已全部完成。Linda并行的Gaussian03输入文件中，%NprocLinda=n，%Nprocshared=m代表用n个节点，每个节点用m个核心运行，即总共n*m个核心运行。运行时单机的g03命令就换成g03l，如g03l < ltwd.gjf |tee a.out。现在在f71或f72上启动一个linda并行的计算任务，如果运行到支持linda并行的子程序时，其它节点上看到了高斯的并行子程序已启动并且有较高CPU占用率，说明已配置成功！如果想利用更多实际节点或虚拟更多节点，都使用类似上述配置f72的方法配置，GAUSS_LFLAGS环境变量中-nodelist后添加更多节点名就行了。  
  
G03中绝大部分支持单机SMP方式并行的功能也支持Linda方式并行，但值得注意的是FMM(Fast Multipole method)，这是一种加快电子积分的计算的方法，但加快并不多。FMM在体系原子数高于某个值后就自动开启，例如对没有对称性的体系原子数等于或大于60就开启。FMM支持SMP方式并行但是不支持Linda并行，开启了FMM后的任务即使使用Linda方式并行，在其它节点机上虽然也有L502子程序启动，但是不会有CPU占用率，运算更不会因此加速。可以用NoFMM关键字关闭它，使得Linda方式的并行运算在这部分计算中能切实发挥加速作用。在高斯09 B01版本及以后Linda方式并行也支持FMM了，就不再需要用NoFMM关闭它。  
  
  

### 3 VMware虚拟机下的并行效率

这里列出了vmware虚拟机用Linda和SMP方式并行及真实主机SMP方式并行在相同Fedora7操作系统下的运算效率，都是用C.02。用HF/Aug-cc-PV5Z算CH4单点，%mem=300MB，目的在于使计算集中在支持linda并行的L502。  
  
f71+f72 %NprocLinda=2，%Nprocshared=2  
181.486s  
f71+f72 %NprocLinda=2，%Nprocshared=1  
434.970s  
f71 %Nproc=2  
316.976s  
实际主机 %Nproc=2  //用时过长，估计和其它因素有关  
401.394s  
实际主机 %Nproc=4  
169.368s  
  
可以看到，用两台双核虚拟机Linda并行并不比在实际操作系统中用4核SMP方式并行慢多少(181s vs 169s)，比单虚拟机双核运行快了近一倍(181s vs 316s)，并行效率较高。而双核SMP并行甚至比实际操作系统中还快(316s vs 401s)，虽然这很怪，但至少可以说虚拟机里面运行绝不比实际运行慢多少，以我的经验，如果不跨节点，各种计算化学程序差不多都只慢10%。而跨节点的两颗核心运行显然比单节点双核慢得多(434s vs 316s)。但毕竟是虚拟机集群，其结果与物理以太网组的集群还是欠缺一些可比性的，而且单一测试任务结论并不具有普遍性。  
  
所以我鼓励充分利用虚拟机，在效能上不会有多少损失，vmware支持四核的虚拟机也是早晚的事（目前只能用双核双虚拟机模拟），届时就更方便了。尽管vmware虚拟机内存不是动态分配，会占不少内存，但对于当前内存行情来说这已不是什么问题。用vmware虚拟机的好处是可以随时中断计算；可以随时将虚拟机拷到别的机子上继续运行，那台机子只要装了vmware就可以而不需要装计算化学软件；可以随时很方便地恢复到原来机子的状态，可以大胆地进行各种操作不再担心系统崩溃；可以在windows平台下做linux下计算而不影响windows下程序运行，只需要将虚拟机CPU优先级调低即可，充分利用CPU资源；甚至可以在多台WinXP平台的机子上，每台机子弄个linux虚拟机，利用虚拟机的Bridged网络模式（每个虚拟机都等价于一个物理主机连到真实的交换机上），将这些windows机子组成linux集群。等等......我以后会专门做更详细的讨论。  
  
  
**附录1：用NFS共享高斯程序的设置方法**  
例如要把f71的/sob/g03目录挂到f72的相同位置，首先确认NFS服务和rpcbind服务（以前叫portmap）已经开启，可以在图形界面的System-Administration-Server settings-Services里面察看二者的状态是否为running，以及前面是否有对钩，即是否每次以当前level启动系统时都能自动开启。若为stopped或没有对钩就手动令其启动并加上对钩。然后在f71的/etc/exports里面加入：  
/sob/g03 192.168.153.4(rw,no_root_squash)  
之后重新启动NFS服务，这样就允许f72以可读写方式共享f71的/sob/g03目录，在f72上执行showmount -e f71察看f71的可共享目录时应该能显示出这个目录。在f72上建立/sob/g03文件夹，之后运行挂载命令mount f71:/sob/g03 /sob/g03即可，两台机子/sob/g03目录已经实时同步，此时f72机子上应该已能照常跑高斯程序。如果想每次开机自动挂载，可以把挂载命令加在f72的/etc/profile里。直接在每个节点上储存一份高斯程序与NFS方式共享高斯程序一般不会对计算速度有明显影响。  
  
**附录2：Fedora7开启无需密码的rsh、rcp、rlogin设置方法**  
假设/etc/hosts已经按正文进行了设置。  
下载xinetd-2.3.14-12.fc7.x86_64.rpm和rsh-server-0.17-44.fc8.x86_64.rpm  
在f71和f72上都进行下列操作：  
装xinetd-2.3.14-12.fc7.x86_64.rpm（图形界面直接双击即可）  
装rsh-server-0.17-44.fc8.x86_64.rpm（图形界面直接双击即可）  
运行setup命令，在其中的系统服务里打开rsh和rlogin和rexec  
在/etc/securetty后面加三行，内容分别是rsh、rlogin、rexec  
/root下面创建.rhosts，加上一行192.168.153.4 root和一行192.168.153.3 root  
运行service xinetd restart  
此时运行netstat -an |grep 514应该显示listen了  
  
此时rsh、rcp、rlogin都应该能用了。f71上运行rsh f72 ls或rlogin f72或使用rcp向另外节点复制文件应该都不需要密码了，这样就设置完毕了。（若rcp复制被拒，到/etc/pam.d/目录下，可以试试把rsh文件中的auth  required  /lib/security/pam_securetty.so一行用“#”封掉）。  
  
  
**针对Gaussian09的补充说明：**  
按照手册的说法，G09中不建议依靠GAUSS_LFLAGS来指定linda计算时的节点列表，也不建议用%NProcLinda来指定linda计算时的节点数。而应该直接用这种方式写明哪些名称的节点被用于linda计算：%LindaWorkers=f71,f72,f73...比如一共写进去了7个，那么这7个节点都会被用于linda计算。并且GAUSS_LFLAGS不用来定义节点列表了，但依然可以用来控制输出的冗余度，如export GAUSS_LFLAGS='-vv'
