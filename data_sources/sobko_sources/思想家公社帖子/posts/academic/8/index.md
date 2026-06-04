---
post_id: 8
title: Fedora 8安装sybyl 8.0
url: http://sobereva.com/8
date: '2015-06-02T18:06:00+08:00'
source_categories:
- 分子模拟
primary_topic: 其它软件
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 内容是Sybyl 8.0的安装教程，软件不在指定列表内。
topic_family: 软件
exclude_reason: ''
confidence: 0.88
image_count: 0
local_assets_dir: assets
---

**Fedora 8安装sybyl 8.0**Installation of Sybyl 8.0 in Fedora 8  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)   写于约2008年

  
  
fedora8-64bit,root,之前无安装sybyl老版本  
  
1 下载：http://tanyenxao.blogspot.com/2008/06/tripos-sybyl-80-rapidshare-link.html（已失效），下载CD1和DVD1，crack在DVD1中，不需要单独下  
2 挂载：  
mkdir /mnt/iso  
mkdir /mnt/iso2  
mount -o loop /sob/SYBYL80DVD1.iso /mnt/iso  
mount -o loop /sob/SYBYL80_TBS.iso /mnt/iso2  
3 装ksh并进入ksh：yum install ksh，ksh  
4 安装：cd /mnt/iso，./install.sh，全选no，浏览器设置输入/usr/bin/firefox，安装目录设/sob/sybyl8.0，点install。中途需要换盘，输入/mnt/iso2，再次换盘输入/mnt/iso。全安装好后退出（不要循环安装）  
5 设置license：把/mnt/iso/crack/license.dat拷到/usr/local/flexlm/licenses目录下，也拷到/sob/AdminTools10.8/tables目录下，改名为license_file  
6 检查/etc/hosts，如果没有127.0.0.1 localhost这句话，添上。  
7 设置PATH环境变量：gedit /root/.bashrc，加上PATH=$PATH:/sob/trigo:/sob/AdminTools10.8/bin/linux。保存后，终端中输入bash使之生效。  
8 运行lmgrd triposlm  
9 运行sybyl8.0，即可进入sybyl程序图形界面  
  
  
安装DVD2（应确保硬盘有10G空间）  
mkdir /mnt/iso3  
mount -o loop /sob/SYBYL80DVD1.iso /mnt/iso3  
export TA_ROOT=/sob/sybyl8.0 (说明书说的是trigo -shell sybyl8.0)  
检查/sob/sybyl8.0/tables/linux/.tapedate的owner属性，是否为自己当前的用户，比如root。如果不是的话改成自己。chown root -R /sob/sybyl8.0  
cd /mnt/iso3  
source ./install.sh  
照提示安装即可，这里似乎不用ksh也能正常安装。安装时间极长，装好后有42.7万个文件。  
  
  
  
  
系统时间应注意不能太早也不宜太后，反正2008年8月14日没问题  
  
如果挂载到/mnt/cdrom，运行install.sh后可能会提示"You should not start the installer from the cdrom directory."，可以挂载到别的位置，或者拷到硬盘上安装。（原因见光盘中part2.sh）  
  
如果点install按钮后，终端中出现关于os.py的错误，安装终止，则应当用ksh。yum install ksh，进入ksh后重新安装即可解决。  
  
如果运行lmgrd triposlm，提示"Failed to open the TCP port number in the license"，看看/etc/hosts里面有没有127.0.0.1 localhost，没有的话加上即可。
