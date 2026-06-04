---
post_id: 282
title: 不同DFT泛函的HF成份一览
url: http://sobereva.com/282
date: '2015-06-08T00:17:00+08:00'
source_categories:
- 量子化学
primary_topic: 量子化学
secondary_topics:
- 激发态与光谱
academic_relevant: true
classification_reason: 文章汇总不同DFT泛函的HF交换比例，属于理论方法参考。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.95
image_count: 0
local_assets_dir: assets
---

**不同DFT泛函的HF成份一览**  
List of HF composition of different DFT functionals

文/Sobereva @[北京科音](http://www.keinsci.com/)

First release: 2015-Feb-23   Last update: 2022-May-7

这里把常见的杂化泛函的HF交换成份从低到高进行排序列出。一些类型的计算直接依赖于HF成份，因此有这么个列表是比较有用的。比如，众所周知激发能直接依赖于HF成份，GGA太红，HF太蓝，HF成分越高的杂化泛函激发能越高。因此，如果发现TDDFT计算和实验光谱有系统偏差，就可以挑HF比例合适的泛函来用（虽说有些人自己调HF成份使得和实验对得恰到好处，但这样做容易被审稿人质疑，给人感觉是故意去凑，有弄虚作假之嫌。而若取现成的泛函来用就没这个麻烦了）。其中粗体字标注的是值得主要关注的，把几个主要的档都覆盖了。

GGA、meta-GGA：0%  
TPSSh、r2SCANh：10%  
O3LYP：11.61%  
TPSS1KCIS：13%  
MPW1KCIS：15%  
杂化版B97：19.43%  
**B3LYP**、B3P86、B3PW91：20%  
B97-1、B97-2、HCTH93：21%  
MPW3LYP、X3LYP：21.8%  
PBE1KCIS：22%  
APFD：23%  
**PBE0**、TPSS0、SCAN0、r2SCAN0、B1B95、mPW1PW91：25%  
M06：27%  
PW6B95、M05：28%  
MPW1B95：31%  
PBE0-1/3：33.33%  
**PBE38**：37.5%  
BB1K、BMK：42%  
MPW1K：42.8%  
MPWB1K：44%  
**MN15**：44%  
PWB6K：46%  
BHandHLYP、PBE50、r2SCAN50：50%  
M08-HX：52.23%  
**M06-2X**：54%  
M05-2X：56%  
M08-SO：56.79%  
M06-HF：100%  
   
   
范围分离泛函（ω单位是Bohr^-1）  
**LC-ωPBE**：近程0%，远程100%，ω=0.4  
LC-PBE0：近程25%，远程100%，ω=0.3  
ωB97：近程0%，远程100%，ω=0.4  
**ωB97X**：近程15.77%，远程100%，ω=0.3  
**ωB97XD**：近程22.2%，远程100%，ω=0.2  
ωB97X-D3(0)：近程19.57%，远程100%，ω=0.25  
ωB97X-V：近程16.7%，远程100%，ω=0.3  
ωB97M-V：近程15%，远程100%，ω=0.3  
**CAM-B3LYP**：近程19%，远程65%，ω=0.33  
M11：近程42.8%，远程100%，ω=0.25  
HSE03（Gaussian里叫HSE2PBE）、HSE06（Gaussian里叫HSEh1PBE。交换部分叫ωPBEh）、MN12-SX、N12-SX：近程25%，远程0%
