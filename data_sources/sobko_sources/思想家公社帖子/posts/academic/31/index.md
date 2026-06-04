---
post_id: 31
title: 量子化学半经验方法的缩写和全称对照
url: http://sobereva.com/31
date: '2015-06-05T00:22:00+08:00'
source_categories:
- 量子化学
primary_topic: 量子化学
secondary_topics:
- 综述/教程/投稿经验
academic_relevant: true
classification_reason: 文章整理半经验量子化学方法的缩写和全称，属于量子化学知识整理。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.87
image_count: 0
local_assets_dir: assets
---

**量子化学半经验方法的缩写和全称对照**Correspondence between abbreviations and full names of semi-empirical methods in quantum chemistry  
文/Sobereva @[北京科音](http://www.keinsci.com/)   2008-Dec-28

  

ZDO=Zero Differential Overlap（非方法名，为半经验方法常用的近似）

FE MO=Free-electron Molecular Orbital Method  
HMO=Huckel Molecular Orbital Method  
EHMO=Extended Huckel Molecular Orbital Method(or Extended Huckel Theory)  
EHMO-ASED=Extended Hückel Molecular Orbital and Atom Superposition and Electron Delocalization  
PPP=Pariser-Parr-Pople method  
CNDO(include CNDO/1,CNDO/2)=Complete Neglect of Differential Overlap (Version 1/2)  
CNDO/S=CNDO parametrized for spectra (including correlation)  
INDO=Intermediate Neglect of Differential Overlap  
SINDO(new version=SINDO/1)=Symmetric Orthogonalised INDO  
SPINDO=Spectroscopic Potentials adjusted INDO  
MINDO(/1,/2,/3)=Modified Intermediate Neglect of Differential Overlap (Version 1(=MINDO),2,3)  
ZINDO=Zerner's Intermediate Neglect of Differential Overlap  
注：ZINDO=INDO/S，由Zerner等人开发的，因为INDO/S用在出名的ZINDO程序中，所以被称为ZINDO，准确来讲叫ZINDO/S，专做激发态，ZINDO-1是做基态的  
NDDO=Neglect of Diatomic Differential Overlap  
MNDO=MNDDO=Modified Neglect of Differential Overlap  
MNDO/d=based on MNDO, adds d functions  
MNDOC=MNDO including correlation  
PNDO=PNDDO=Partial Neglect of Diatomic Differential Overlap  
PRDDO(and /M,/M/FCP,/M/NQ)=Partial Retention of Diatomic Differential Overlap  
LNDO/S=Local Neglect of Differential Overlap (including correlation)  
IRDO=Intermediate Retention of Differential Overlap  
AM1=Austin Model 1  
SAM1=SemiChem Austin Model 1 (or Semi-Ab-initio Model 1), Andy Holder's extension of AM1 in Ampac by the addition of d-orbitals in the Hamiltonian(SAM1d)  
PM3/4/5/6=Parameterized Model number 3/4/5/6  (PM4/5未公开)  
PM3(TM)=PM3 for transition-metal  
PDDG-PM3 & PDDG-MNDO=Pairwise Distance Directed Gaussian PM3/MNDO  
RM1=Recife Model 1 http://www.rm1.sparkle.pro.br  
OM1/2/3=Orthogonalization Models 1/2/3  
OMx-D=Orthogonalization Models x with an empirical dispersion term  
TNDO=Typed Neglect of Differential Overlap  
注：TNDO是在hyperchem中引入的，特点是适合计算与磁相关的属性，比如磁场屏蔽效果。第1版和第2版分别叫做TNDO/1，TNDO/2。一般的半经验法都是把原子按照元素来区分，一个原子只有一种类型。在TNDO中，不同环境下的原子除了元素属性外，还有化学环境的属性，比如sp2与sp3的就不同，脂肪链中的C与芳香环中的不同。TNDO/1基于CNDO，TNDO/2基于INDO。详见Hyperchem 7手册p227
