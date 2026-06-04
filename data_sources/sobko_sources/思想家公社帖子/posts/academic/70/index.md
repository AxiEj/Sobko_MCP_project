---
post_id: 70
title: 安装和使用molproView
url: http://sobereva.com/70
date: '2015-06-07T23:45:00+08:00'
source_categories:
- 量子化学
primary_topic: 其它软件
secondary_topics:
- 可视化
- 结构与文件格式
academic_relevant: true
classification_reason: 主要介绍 molproView 的安装与使用，属于软件教程。
topic_family: 软件
exclude_reason: ''
confidence: 0.97
image_count: 0
local_assets_dir: assets
---

注：如果你用molproView的目的就是看结构，看轨道什么的，远不如导出.molden文件用Multiwfn看，省事得多。详见《详谈Multiwfn支持的输入文件类型、产生方法以及相互转换》（<http://sobereva.com/379>）和《使用Multiwfn观看分子轨道》（<http://sobereva.com/269>）

**安装和使用molproView**Installation and use of molproView

文/Sobereva @[北京科音](http://www.keinsci.com/)  2010-Sep-20

molpro执行任务后会自动生成包含结果信息的.xml文件，molproView可以将之转化为网页文件，通过网页浏览器清晰地查看运行结果。molproView下载地址为<http://www.molpro.net/molproView>。  
  
此程序有两类执行模式：  
1 基于web服务器的模式。主机需要有PHP支持，通过网页浏览器访问解压目录下的molproView.php文件，然后输入.xml文件路径，就能看到结果页面。官方也提供了运行molproView的服务器http://www.molpro.net/molproView/molproView.php，但是没法直接输入本机文件路径，.xml文件需要先传到某web服务器上，略微麻烦。但若是molproView.php运行于本机，可以通过配置使之能够载入本地.xml文件。  
  
2 纯粹单机模式。这种模式下molproView只是作为一个基于命令行的文件转换器，不需要PHP运行环境，最适合单机使用，安装方式和使用方式见下文。以下步骤在FC6 32bit下执行成功，假设要安装到/sob/molproView下。  
  
将molproView压缩包解压到/sob下，然后去这里下载jmol压缩包（页面会经过自动跳转）：http://downloads.sourceforge.net/jmol/jmol-11.4.4-binary.tar.gz，然后放到/sob下。在/sob/molproView/Makefile里把JMOLURL变量设为file:/sob，也就是不自动从网上下载而是直接用已下载好的本地的jmol包（因为默认的下载路径不对），然后运行make，jmol会被解压到/sob/molproView/jmol下，此目录中自带的example.xml会被转换出example.html，用网页浏览器打开会看到计算结果、振动模式、等值面等信息，其中图表实际上是在线调用google在线作图程序，所以得联网。以后自行得到的新的.xml文件只要放在此目录下执行make就可得到转换后的网页文件，转换很快。  
  
网页浏览器需要有java支持才能显示分子结构和等值面，到SUN的网站下载Linux版Java运行环境包，目前的地址是http://java.com/en/download/linux_manual.jsp?locale=en&host=java.com，选其中的Linux RPM，下载后执行之，会自动解压并安装rpm包。然后给Firefox添加java插件，cd进入/usr/lib/firefox-1.5.0.7/plugins目录，执行ln -s /usr/java/jre1.6.0_21/plugin/i386/ns7/libjavaplugin_oji.so。  
重新启动Firefox，在地址栏输入about:plugins就可以看到是否的确已经安装好了插件。  
  
如果显示格点文件的地方显示access denied，则在/usr/java/jre1.6.0_21/lib/security里面的java.policy里面加入下面内容：  
grant codeBase "file:/sob/molproView/jmol/*" {  
 permission java.security.AllPermission;  
};  
这样就允许/sob/molproView/jmol/下的java程序文件访问本地文件了，错误就解决了。
