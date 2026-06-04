---
post_id: 55
title: 高斯fch文件与wfn波函数文件的介绍及转换方法
url: http://sobereva.com/55
date: '2015-06-07T23:43:00+08:00'
source_categories:
- 量子化学
primary_topic: 结构与文件格式
secondary_topics:
- Gaussian
- Multiwfn
- 波函数分析
academic_relevant: true
classification_reason: 主要讲 fch 与 wfn 波函数文件的格式及转换方法，重点是文件结构。
topic_family: 方法领域
exclude_reason: ''
confidence: 0.98
image_count: 0
local_assets_dir: assets
---

**高斯fch文件与wfn波函数文件的介绍及转换方法**Introduction and conversion method of Gaussian fch file and wfn wavefunction file  
  
文/Sobereva @[北京科音](http://www.keinsci.com/)  2010-Feb-1

  
  
了解高斯的格式化检查点文件fch和波函数文件wfn的格式和每项的意义对编写第三方量化辅助程序是很重要的，前者蕴含的信息丰富，后者更为简明而且通用。本文将解读wfn文件的格式和读、写代码，对fch中的一些要点进行介绍，介绍如何写出将fch转化为wfn文件的程序fch2wfn，以帮助大家认识这两种文件并利用fch和wfn写出相关程序。  
  

## 1. wfn(Wavefunction)文件的格式和意义

wfn文件最早作为Bader的AIMPAC程序的输入文件出现，AIMPAC是历史最久的AIM分析软件，后来其它的AIM分析软件如Multiwfn (<http://sobereva.com/multiwfn>)、AIM2000、AIMALL、Morphy、Xaim等等也都需要wfn文件。wfn文件包含的是所有高斯函数的信息和波函数向它们的展开系数，结构简洁，计算空间中波函数值、电子密度等属性很方便。Gaussian、GAMESS等许多主流量化程序都可以输出wfn文件，例如Gaussian中只需要在route section加上output=wfn，并在分子结构部分末尾空一行写上wfn文件输出路径即可，如c:\divokej_bill.wfn。  
  
这里以高斯中HF/3-21G计算的CH4分子输出的wfn文件为例对格式进行介绍  
  
第1行  
Title Card Required  
wfn中第一行没有任何意义，只是文件注释  
  
第2行  
GAUSSIAN              5 MOL ORBITALS     27 PRIMITIVES        5 NUCLEI  
开头的GAUSSIAN说明文件中记录的函数类型是高斯类型，一般wfn中都是高斯类型函数。  
5 MOL ORBITALS代表文件中的分子轨道数，wfn中只记录占据轨道，虚轨道不记录，因为AIM分析的对象是电子密度，而虚轨道对计算电子密度没有贡献。  
27 PRIMITIVES代表原始高斯函数的总数目，可独立变分的基函数是由它们收缩成的。  
5 NUCLEI是原子数  
  
第3-7行  
  C    1    (CENTRE  1)   0.00000000  0.00000000  0.00000000  CHARGE =  6.0  
  H    2    (CENTRE  2)   1.16740622  1.16740622  1.16740622  CHARGE =  1.0  
  H    3    (CENTRE  3)  -1.16740622 -1.16740622  1.16740622  CHARGE =  1.0  
  H    4    (CENTRE  4)  -1.16740622  1.16740622 -1.16740622  CHARGE =  1.0  
  H    5    (CENTRE  5)   1.16740622 -1.16740622 -1.16740622  CHARGE =  1.0  
这些是原子的信息。例如其中的第一行，C是原子符号，后面的1是原子序号。CENTRE后面的也是原子序号，与前面的序号是重复的，所以取其一即可。接下来是原子坐标，单位为波尔，最后是原子的核电荷数。使用赝势时核电荷数不等于原子序数，而等于被明确表达的价层电子数。  
  
第8、9行  
CENTRE ASSIGNMENTS    1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  2  2  2  3  3  
CENTRE ASSIGNMENTS    3  4  4  4  5  5  5  
每项代表每个高斯函数所在的原子序号。由于一共有27个高斯函数，这里也就有27项。  
  
第10、11行  
TYPE ASSIGNMENTS      1  1  1  1  1  2  2  3  3  4  4  1  2  3  4  1  1  1  1  1  
TYPE ASSIGNMENTS      1  1  1  1  1  1  1  
这是每个高斯函数的类型。wfn文件中一般都是用笛卡尔型高斯函数，这里的数字与类型的对应关系是  
1/2/3/4/5/6/7/8/9/10=S/X/Y/Z/XX/YY/ZZ/XY/XZ/YZ   
11/12/13/14/15/16/17/18/19/20=XXX/YYY/ZZZ/XXY/XXZ/YYZ/XYY/XZZ/YZZ/XYZ  
生成wfn文件时应注意应使用6d/10f型高斯函数而不要用球谐型。wfn文件对于g及更高角动量函数没有统一的序号定义，而且由于涉及这样的函数机会不多，所以多数AIM软件还不支持这些函数，如果体系中有这样的函数，高斯也无法输出wfn文件。  
  
第12-17行  
EXPONENTS  0.1722560D+03 0.2591090D+02 0.5533350D+01 0.3664980D+01 0.7705450D+00  
EXPONENTS  0.3664980D+01 0.7705450D+00 0.3664980D+01 0.7705450D+00 0.3664980D+01  
EXPONENTS  0.7705450D+00 0.1958570D+00 0.1958570D+00 0.1958570D+00 0.1958570D+00  
EXPONENTS  0.5447178D+01 0.8245472D+00 0.1831916D+00 0.5447178D+01 0.8245472D+00  
EXPONENTS  0.1831916D+00 0.5447178D+01 0.8245472D+00 0.1831916D+00 0.5447178D+01  
EXPONENTS  0.8245472D+00 0.1831916D+00  
这是每个高斯函数的指数，即N*x^ix*y^iy*z^iz*exp(-α*r^2)中的α。显然也是27项。  
  
第18-52行  
......  
MO    3     MO 0.0        OCC NO =    2.0000000  ORB. ENERGY =   -0.548298  
  0.00000000D+00  0.00000000D+00  0.00000000D+00  0.00000000D+00  0.00000000D+00  
  0.00000000D+00  0.00000000D+00  0.00000000D+00  0.00000000D+00  0.64363172D+00  
  0.33350218D+00  0.00000000D+00  0.00000000D+00  0.00000000D+00  0.57302486D-01  
  0.63659475D-01  0.89429130D-01  0.29385384D-01  0.63659475D-01  0.89429130D-01  
  0.29385384D-01 -0.63659475D-01 -0.89429130D-01 -0.29385384D-01 -0.63659475D-01  
 -0.89429130D-01 -0.29385384D-01  
......  
这部分是分子轨道信息，这里只列出第3条以说明。  
MO    3代表是第3条轨道，也就是它在高斯中的轨道序号。对于闭壳层，这个序号和此轨道在本文件中的序号一致。  
MO 0.0没有任何意义，只是个标签。  
NO =    2.0000000是占据数，这里就是代表有两个电子占据，若是非限制性波函数即为1。若是限制性开壳层计算，高斯会误把单占据轨道占据数写为2，需手动修改为1。  
ORB. ENERGY =   -0.548298是轨道能，单位为Hartree。  
接下来就是分子轨道向这27个高斯函数的展开系数，一定要注意，每个展开系数已经包含了高斯函数的归一化系数，也就是分子轨道向没有归一化的高斯函数（即x^ix*y^iy*z^iz*exp(-α*r^2)形式）展开的系数。  
  
这里的轨道并非一定是分子轨道，如果用后HF方法，并且加了density=current表明用后HF密度，则输出的每个轨道就是自然轨道，其占据数一般不是整数，输出的轨道数目与可独立变分的基函数一致。因为后HF密度的自然轨道没有是否占据之分，只有占据多少之分，每条轨道都对电子密度有贡献，所以所有的自然轨道都会列出。如果是开壳层计算，还应当加上pop=NOAB，这样就会记录自然自旋轨道。  
  
轨道记录顺序是能量由低往高。注意对于自旋轨道，wfn中先按这个次序记录完所有alpha轨道再记录beta轨道。由于第一个beta轨道的能量肯定比最后的alpha轨道的能量低，所以通过检验轨道能量与前一个轨道能量的关系就能判断beta轨道从哪里开始记录。如果是自然自旋轨道，则要判断它与前一个轨道的占据数关系。  
  
wfn中轨道的轨道序号，记录的前后顺序是随意的。高斯函数的顺序也是随意的，只要在类型、所在中心、指数、轨道展开系数段落中的位置对应就行，不会影响结果。  
  
第53行  
END DATA  
其中END DATA代表标准wfn文件要求的全部信息的说明已结束，在此之后允许附加一些信息。  
  
第54行及之后  
 THE  HF ENERGY =    -39.976405845082 THE VIRIAL(-V/T)=   2.00033480  
这些是附加信息，是随意的。一般量化程序输出的wfn都会按照这个格式输出能量和维里值。THE  HF ENERGY是体系HF或DFT总能量，如果是后HF方法，这里仍然是HF能量。有的程序还会附上其它一些信息。  
  
  

## 2.读、写wfn文件的fortran代码解析

首先根据wfn所拥有的数据，定义一些变量，以及两种自定义类型用于储存原子和高斯函数的数据。  
  
type atomtype  
character*2 name !元素名称  
real*8 x,y,z,charge !原子坐标和电荷  
end type  
  
type basistype  
integer center,functype !高斯函数所在原子序号，函数类型  
real*8 exp !指数  
end type  
  
character*8 mode !用来记录函数类型，一般wfn里都是高斯函数，所以可以不定义。  
integer nmo,nprims,ncenter !轨道、高斯函数、原子的数目  
real*8 totenergy,virialratio !总能量、维里值  
type(atomtype),allocatable :: a(:) !储存原子信息  
type(basistype),allocatable :: b(:) !储存基函数信息  
real*8,allocatable :: MOocc(:),MOene(:) !轨道占据数和能量  
real*8,allocatable :: CO(:,:) !系数矩阵，CO(i,j)代表第i个分子轨道向第j个高斯函数的展开系数，已包括归一化系数。  
  
还定义两个变量，并不是直接从wfn文件中读取，需要用代码来判断，在写一些相关程序时会用得到它们。  
integer,allocatable :: MOtype(:) !轨道类型，0代表双占据的空间轨道，1是alpha自旋轨道，2是beta自旋轨道  
integer wfntype !用来说明波函数类型，0/1/2代表R/U/ROHF波函数，3/4代表是闭壳层/开壳层后HF波函数，分别代表储存的是空间自然轨道和自旋自然轨道。  
  
下面是读取wfn文件的子程序，是作为主程序的内部函数使用的，能共享前面在主程序中定义的变量，主程序中已使用了隐式声明implicit real*8(a-h,o-z)。  
subroutine readwfn  
open(10,file=filename,access="sequential",status="old")  
read(10,*) !跳过wfn开头  
read(10,"(a8,i15,13x,i7,11x,i9)") mode,nmo,nprims,ncenter !读取函数类型、分子轨道数、高斯函数数、原子数  
allocate(a(ncenter)) !根据数目分配内存  
allocate(b(nprims))  
allocate(co(nmo,nprims))  
allocate(MOocc(nmo))  
allocate(MOene(nmo))  
allocate(MOtype(nmo))  
do i=1,ncenter !读原子信息  
    read(10,"(2x,a2,20x,3f12.8,10x,f5.1)") a(i)%name,a(i)%x,a(i)%y,a(i)%z,a(i)%charge  
end do  
read(10,"(20x,20i3)") (b(i)%center,i=1,nprims) !读高斯函数所在中心  
read(10,"(20x,20i3)") (b(i)%functype,i=1,nprims) !读高斯函数类型  
read(10,"(10x,5D14.7)") (b(i)%exp,i=1,nprims) !读高斯函数指数  
do i=1,nmo  
    read(10,"(35X,f12.7,15x,f12.6)") MOocc(i),MOene(i) !读轨道占据数和能量。轨道序数和轨道标签没意义，不读。  
    read(10,"(5D16.8)") (co(i,j),j=1,nprims) !读轨道展开系数  
end do  
read(10,*)  
read(10,"(18x,f19.12,20x,f12.8)") totenergy,virialratio !总能量和维里值  
close (10)  
write(*,"('There are',i6,' MOs,',i6,' atoms,',i7,' electrons,',i7,' Gaussian functions')") nmo,ncenter,int(sum(moocc)),nprims  
! 下面分析波函数的类型  
if (sum(MOocc)==2*nmo) then !总电子数是轨道数二倍（再次注意wfn只记录占据轨道），为HF闭壳层  
    wfntype=0  
    MOtype=0 !轨道类型都设双占据  
    write(*,"('This is restricted wavefunction')")  
else if (sum(MOocc)==nmo) then !总电子数等于轨道数，为HF开壳层  
    wfntype=1  
    MOtype=1 !先都设为alpha  
    do i=2,nmo  
        if (MOene(i)<=MOene(i-1)) exit !确定哪里是alpha轨道与beta轨道的分界处  
    end do  
    MOtype(i:nmo)=2 !将分界处后面的轨道都设成beta  
    write(*,"('This is unrestricted wavefunction,',i6,' alpha orbitals',i6,' beta orbitals')") i-1,nmo-i+1  
else if (MOocc(nmo)/=int(MOocc(nmo))) then !最后一个轨道占据数不为整数，为后HF波函数  
    wfntype=3 !先假设是闭壳层  
    MOtype=0  
    do i=2,nmo  
        if (MOocc(i)>MOocc(i-1)) then !寻找alpha与beta轨道分界位置，如果能找到，说明是开壳层  
            wfntype=4  
            MOtype(1:i-1)=1 !给自旋自然轨道赋予alpha/beta类型  
            MOtype(i:nmo)=2  
            exit  
        end if  
    end do  
    if (wfntype==3) write(*,"('This is restricted Post-HF wavefunction')")  
    if (wfntype==4) write(*,"('This is unrestricted Post-HF wavefunction')")  
    if (wfntype==4) write(*,"(i6,' alpha electrons',i6,' beta electrons')") int(sum(MOocc(1:i-1))),int(sum(MOocc(i:nmo)))  
else  
    wfntype=2 !以上情况都不是，就是限制性开壳层波函数  
    MOtype=0  
    j=0  
    do i=1,nmo  
        if (MOocc(i)==1) then  
            MOtype(i)=1 !单占据轨道都设成alpha类型  
            j=j+1  
        end if  
    end do  
    write(*,"('This is restricted open-shell wavefunction,',i6,' single occupied orbitals')") j  
end if  
write(*,"('Total energy:',f19.12,' hartree,   Virial ratio:',f12.8)") totenergy,virialratio  
write(*,*)  
end subroutine  
  
了解了wfn读入方法，输出wfn也就会了，以下是输出子程序。  
subroutine outwfn  
open(11,file=outfilename,status="replace")  
write(11,*) "Generated by fch2wfn"  
write(11,"('GAUSSIAN',i15,' MOL ORBITALS',i7,' PRIMITIVES',i9,' NUCLEI')") nmo,nprims,ncenter  
do i=1,ncenter  
    write(11,"(2x,a2,i4,4x,'(CENTRE',i3,')',1x,3f12.8,'  CHARGE =',f5.1)") a(i)%name,i,i,a(i)%x,a(i)%y,a(i)%z,a(i)%charge  
end do  
write(11,"('CENTRE ASSIGNMENTS  ',20i3)") b%center  
write(11,"('TYPE ASSIGNMENTS    ',20i3)") b%functype  
write(11,"('EXPONENTS ',5D14.7)") b%exp  
do i=1,nmo  
    write(11,"('MO',I5,'     MO 0.0        OCC NO = ',f12.7,'  ORB. ENERGY =', f12.6)") i,MOocc(i),MOene(i)  
    write(11,"(5D16.8)") (co(i,j),j=1,nprims)  
end do  
write(11,"('END DATA',/,' THE  HF ENERGY = ',f19.12,' THE VIRIAL(-V/T)= ',f12.8)") totenergy,virialratio  
close(11)  
end subroutine  
  
  

## 3. fch(Formatted check point)文件简介

任何平台下高斯执行任务生成的二进制的chk文件都可以用formchk生成fch/fchk文件，fch文件是ASCII文件，是人可读的。它独立于平台，可用于在不同平台上交换chk文件，也可方便地从中提取计算过程中有用的信息。fch文件在Gaussian03与09中内容大体不变，但是记录项目的顺序有所改变。  
  
fch中的信息远比wfn丰富，包含了获得wfn文件所需要的一切信息，里面也有不少冗余的信息。本文主要目的是介绍fch向wfn的转换方法，如何写fch2wfn程序，下面只谈一些相关要点，一些条目靠fch自带的解释就可以明白就不谈了。  
  
第一行是标题，是任意的，可以自行写一些附加信息在此告诉fch2wfn程序对它做哪些特殊处理。  
第二行是任务类型、方法、基组，格式是A10,A30,A30。看第11列是R、U还是RO就能判断波函数类型。  
  
每一类数组型数据前面都有一行标签，读取格式都是A40,3X,A1,5X,I12。比如  
Primitive exponents                        R   N=          18  
18代表下面有18个数据。R代表下面的是实数型数据。若是I、C、L则分别代表是整型、字符型、逻辑型数据。实数型数据读取格式是5(1PE16.8)，整型是6I12。  
  
fch中与wfn显著不同的一点是基函数的储存方法。wfn中是按高斯函数顺序储存的，而fch中是一层一层地储存的。Shell types代表了每个壳层的类型，0=s, 1=p, -1=sp, 2=6d, -2=5d, 3=10f, -3=7f, 4=15g, -4=9g。Number of primitives per shell代表的是每一壳层内的基函数的收缩度。  
  
fch中每个壳层里笛卡尔型基函数的类型是按如下顺序排列S,X,Y,Z, XX,YY,ZZ,XY,XZ,YZ, XXX,YYY,ZZZ,XYY,XXY,XXZ,XZZ,YZZ,YYZ,XYZ，对比wfn中的函数类型编号，会发现f轨道的顺序不一致，这在转换时需要特别注意。如前所述，wfn文件里不能记录g及更高角动量函数，但是在fch文件中可以，g函数的顺序为ZZZZ,YZZZ,YYZZ,YYYZ,YYYY,XZZZ,XYZZ,XYYZ,XYYY,XXZZ,XXYZ,XXYY,XXXZ,XXXY,XXXX。  
  
Coordinates of each shell其实是多余的，因为已经有Shell to atom map（壳层所属原子）和Current cartesian coordinates（每个原子xyz坐标），可以直接推出。  
  
Total SCF Density就是SCF密度矩阵，用了后HF方法并用density=current还会有后HF的密度矩阵被记录，如Total MP2 Density。由于是对称的，所以只记录了下三角部分（含对角元），顺序是(1,1)(2,1)(2,2)(3,1)(3,2)(3,3)(4,1)...，  
  
限制性方法计算的轨道能量和展开系数记录在Alpha Orbital Energies/Alpha MO coefficients里（尽管双占据称为Alpha轨道并不妥），如果是非限制性的计算还会多出Beta的。用density=current并不会使fch文件像wfn一样使记录的轨道成为自然轨道，它仍然是SCF的系数。如果想把自然轨道系数写入到Alpha MO coefficients当中，则先用后HF方法带着density=current关键字跑一次，然后再运行Guess=(Save,Only,NaturalOrbitals) ChkBasis即可。此时fch里轨道能量部分就不再是能量，而是占据数。  
  
加了pop=saveNBO使高斯调用NBO 3.1进行NBO分析后，会把NBO轨道保存到fch的分子轨道系数部分。如果用的SCF密度，则分子轨道能量部分保存的是NBO轨道能量，读入下文的fch2wfn程序前应把第一行改为saveNBOene；如果用的是后HF密度，这部分保存的则是NBO轨道占据数，读入fch2wfn前应把第一行改为saveNBOocc。fch中倒数的几个NBO轨道的能量或占据数误为1000，应根据NBO分析输出的结果手动修改。  
  
  
Primitive exponents、Contraction coefficients与P(S=P) Contraction coefficients的关系：  
这里举HF/STO-3G算CH4的fch的这部分作为例子，这三类只列出第一行来说明，最开头的就是C的S和SP壳层。  
Primitive exponents                        R   N=          18  
  7.16168373E+01  1.30450963E+01  3.53051216E+00  2.94124936E+00  6.83483096E-01  
...  
Contraction coefficients                   R   N=          18  
  1.54328967E-01  5.35328142E-01  4.44634542E-01 -9.99672292E-02  3.99512826E-01  
...  
P(S=P) Contraction coefficients            R   N=          18  
  0.00000000E+00  0.00000000E+00  0.00000000E+00  1.55916275E-01  6.07683719E-01  
...  
下面是一些linux版高斯自带的sto3g.gbs文件，  
-C  
S    3 1.00  
 0.7161683735D+02  0.1543289673D+00  
 0.1304509632D+02  0.5353281423D+00  
 0.3530512160D+01  0.4446345422D+00  
SP   3 1.00  
 0.2941249355D+01 -0.9996722919D-01  0.1559162750D+00  注：第一列是高斯函数指数，后两列分别是S和P型的收缩系数  
 0.6834830964D+00  0.3995128261D+00  0.6076837186D+00  
 0.2222899159D+00  0.7001154689D+00  0.3919573931D+00  
将fch的内容竖着看，而将sto3g.gbs的内容横着看，可见fch中与sto3g.gbs的内容是对应的。对于S壳层，P(S=P) Contraction coefficients对应的项都是0，到了SP壳层就不为0了，代表的就是P的收缩系数。如果用的是例如Dunning相关一致性基组，由于S和P壳层是独立的，没有SP壳层，则这部分就不会出现。  
  
  

## 4.读取fch文件的fortran代码

为了完成fch->wfn的转换，不需要读入所有fch的数据，只需要读入其中有用的数据并经过转换，把将前面outwfn子程序要用的变量全都填好就可以了。  
  
读取fch文件的代码中要用到在fch中定位标签的子程序，例如call loclabel(10,'Alpha MO coefficients')就会使当前读取位置处在Alpha MO coefficients这行开头，如果没找到要找的内容，则全局变量noentryinfch=1，否则为0。loclabel子程序代码如下：  
subroutine loclabel(fileid,label)  
integer fileid  
integer error  
character*80 :: c80=' '  
CHARACTER(LEN=*) label  
rewind(fileid) !每次都从头开始找，因为fch里内容的顺序与高斯版本有关，从头开始找比较保险。  
error=0  
noentryinfch=0  
do while(index(c80,trim(label))==0.and.error==0) !index函数的用处是在c80中找label代表的字符串所在位置，返回0说明没找到  
    read(fileid,"(a80)",iostat=error) c80 !每次读一整行  
    if (error/=0) noentryinfch=1  
end do  
backspace(fileid)  
end subroutine  
  
下面是读入fch文件的子程序readfch：  
subroutine readfch  
character*80 c80  
real*8 temp  
integer :: i,j,k,l,nbasis !nbasis是基函数数目  
integer :: type2norb(-3:3)=(/ 7,5,4,1,3,6,10 /) !将壳层类型转化为壳层所含轨道数，0=s->1,1=p->3,-1=sp->4,2=6d->6,-2=5d->5,3=10f->10,-3=7f->7  
integer,allocatable :: shelltype(:),shellcon(:),shell2atom(:) !壳层类型、收缩度、所属原子  
integer :: s2f(-3:3,30)=0 !s2f(i,j)就是第i类壳层中第j个基函数的类型编号  
real*8,allocatable :: primexp(:),concoeff(:),SPconcoeff(:) !每一壳层中高斯函数的指数、收缩系数和SP壳层的P型的收缩系数  
real*8,allocatable :: amocoeff(:,:),bmocoeff(:,:) !fch文件中alpha/beta分子轨道系数矩阵  
s2f(0,1)=1  
s2f(-1,1:4)=(/ 1,2,3,4 /)  
s2f(1,1:3)=(/ 2,3,4 /)  
s2f(2,1:6)=(/ 5,6,7,8,9,10 /)  
s2f(3,1:10)=(/ 11,12,13,17,14,15,18,19,16,20 /) !这是10f壳层，11~20不是按顺序排列，用来起到fch中f轨道顺序与wfn中顺序的转换。  
mode="GAUSSIAN" !Gaussian程序里用的都是高斯函数  
open(10,file=infilename,access="sequential",status="old")  
read(10,*) fchtitle !fch第一行  
!因为wfn只含占据轨道，故一般情况readfch只需读入占据轨道。如果fch第一行含有saveNO，说明存的是自然轨道。若第一行是saveNBOocc或saveNBOene，说明是NBO轨道。这三种情况所有轨道占据数皆不为0，都应输出到wfn，故应读入所有轨道。  
isaveNO=0   
isaveNBOocc=0  
isaveNBOene=0  
if (index(fchtitle,'saveNBOocc')/=0) isaveNBOocc=1  
if (index(fchtitle,'saveNBOene')/=0) isaveNBOene=1  
if (index(fchtitle,'saveNO')/=0) isaveNO=1  
if (isaveNBOocc==1.or.isaveNBOene==1) write(*,*) "The file contains NBO information"  
if (isaveNO==1) write(*,*) "The file contains natural orbitals information"  
read(10,"(a80)") c80  
if (c80(11:11)=="R") wfntype=0  
if (c80(11:11)=="U") wfntype=1  
if (c80(11:12)=="RO") wfntype=2  
call loclabel(10,'Number of electrons') !将读入位置移动到Number of electrons这行的开头  
read(10,"(49x,i12)") ntotelec !总电子数  
read(10,"(49x,i12)") nalphaelec !总alpha电子数  
read(10,"(49x,i12)") nbetaelec !总beta电子数  
read(10,"(49x,i12)") nbasis  
call loclabel(10,'Virial Ratio')  
read(10,"(49x,1PE22.15)") virialratio  
call loclabel(10,'Total Energy')  
totenergy=0.0D0  
if (noentryinfch==0) read(10,"(49x,1PE22.15)") totenergy !使用guess=(save,only,naturalorbitals)保存自然轨道的fch文件无Total Energy项，此时不读  
call loclabel(10,'Atomic numbers')  
read(10,"(49x,i12)") ncenter  
allocate(a(ncenter))  
read(10,"(6f12.0)") (a(i)%charge,i=1,ncenter)  
do i=1,ncenter  
    a(i)%name=name2ind(int(a(i)%charge)) !根据原子的质子数转换到元素名称  
end do  
call loclabel(10,'Current cartesian coordinates')  
read(10,*)  
read(10,"(5(1PE16.8))") (a(i)%x,a(i)%y,a(i)%z,i=1,ncenter) !读入每个原子的坐标，用隐式循环很方便  
call loclabel(10,'Shell types')  
read(10,"(49x,i12)") nshelltype  
allocate(shelltype(nshelltype))  
read(10,"(6i12)") (shelltype(i),i=1,nshelltype)  
call loclabel(10,'Number of primitives per shell')  
read(10,"(49x,i12)") nshellcon  
allocate(shellcon(nshellcon))  
read(10,"(6i12)") (shellcon(i),i=1,nshellcon)  
call loclabel(10,'Shell to atom map')  
read(10,"(49x,i12)") nshell2atom  
allocate(shell2atom(nshell2atom))  
read(10,"(6i12)") (shell2atom(i),i=1,nshell2atom)  
call loclabel(10,'Primitive exponents')  
read(10,"(49x,i12)") nprimexp  
allocate(primexp(nprimexp))  
read(10,"(5(1PE16.8))") (primexp(i),i=1,nprimexp)  
call loclabel(10,'Contraction coefficients')  
read(10,"(49x,i12)") nconcoeff  
allocate(concoeff(nconcoeff))  
read(10,"(5(1PE16.8))") (concoeff(i),i=1,nconcoeff)  
read(10,"(a80)") c80  
if (index(c80,"P(S=P) Contraction coefficients")/=0) then  
    backspace(10)  
    read(10,"(49x,i12)") nSPconcoeff  
    allocate(SPconcoeff(nSPconcoeff))  
    read(10,"(5(1PE16.8))") (SPconcoeff(i),i=1,nSPconcoeff)  
end if  
nprims=0  
!计算总高斯函数数目，用于分配内存给b(:)。每个壳层的基函数数目乘以壳层的收缩度就是每个壳层的高斯函数数目  
do i=1,nshelltype  
    nprims=nprims+type2norb(shelltype(i))*shellcon(i)  
end do  
allocate(b(nprims))  
call loclabel(10,'Alpha Orbital Energies') !定位到Alpha Orbital Energies处  
read(10,*)  
if (wfntype==0.or.wfntype==2) then !闭壳层或限制性开壳层，很多代码可以共用所以放到一起。  
    if (wfntype==0) nmo=ntotelec/2 !根据电子数和波函数类型判定占据轨道数  
    if (wfntype==2) nmo=nalphaelec !开壳层情况alpha电子>=beta电子数，故限制性开壳层取alpha电子数为占据轨道数  
    if (isaveNO==1.or.isaveNBOocc==1.or.isaveNBOene==1) nmo=nbasis !fch中为自然轨道或NBO轨道时读取所有轨道  
    allocate(MOene(nmo))  
    allocate(MOocc(nmo))  
    allocate(MOtype(nmo))  
    allocate(amocoeff(nmo,nbasis)) !给alpha系数矩阵分配内存  
    MOtype=0  
    MOocc=2.0D0  
    if (wfntype==2) then  
        MOtype(nbetaelec+1:nmo)=1 !限制性开壳层时设定单占据轨道  
        MOocc(nbetaelec+1:nmo)=1.0D0  
        write(*,"('This is restricted open-shell wavefunction,',i6,' single occupied orbitals')") nalphaelec-nbetaelec  
    else if (wfntype==0) then  
        write(*,"('This is restricted wavefunction')")  
    end if  
    read(10,"(5(1PE16.8))") (MOene(i),i=1,nmo)  
    call loclabel(10,'Alpha MO coefficients')  
    read(10,*)  
    read(10,"(5(1PE16.8))") ((amocoeff(imo,ibasis),ibasis=1,nbasis),imo=1,nmo) !双隐式循环读入轨道系数  
else if (wfntype==1) then !开壳层情况  
    nmo=ntotelec !占据轨道数等于总电子数  
    if (isaveNO==1.or.isaveNBOocc==1.or.isaveNBOene==1) then  
        nmo=2*nbasis  
        nalphaelec=nbasis !nalphaelec/nbetaelec控制着读取范围、如何设定轨道类型。含自然轨道/NBO信息时轨道全都读入，故将alpha轨道和beta轨道数目都设成基函数数。  
        nbetaelec=nbasis  
    end if  
    allocate(MOene(nmo))  
    allocate(MOocc(nmo))  
    allocate(MOtype(nmo))  
    allocate(amocoeff(nalphaelec,nbasis))  
    allocate(bmocoeff(nbetaelec,nbasis))  
    MOocc=1.0D0  
    MOtype(1:nalphaelec)=1 !设为alpha轨道  
    MOtype(nalphaelec+1:nmo)=2 !设为beta轨道  
    write(*,"('This is unrestricted wavefunction,',i6,' alpha orbitals',i6,' beta orbitals')") nalphaelec,nbetaelec  
    read(10,"(5(1PE16.8))") (MOene(i),i=1,nalphaelec) !读alpha轨道能量  
    call loclabel(10,'Beta Orbital Energies')  
    read(10,*)  
    read(10,"(5(1PE16.8))") (MOene(i),i=nalphaelec+1,nmo) !读beta轨道能量。alpha/beta轨道能量都一起存在MOene里。  
    call loclabel(10,'Alpha MO coefficients')  
    read(10,*)  
    read(10,"(5(1PE16.8))") ((amocoeff(imo,ibasis),ibasis=1,nbasis),imo=1,nalphaelec)  
    call loclabel(10,'Beta MO coefficients')  
    read(10,*)  
    read(10,"(5(1PE16.8))") ((bmocoeff(imo,ibasis),ibasis=1,nbasis),imo=1,nbetaelec)  
end if  
  
if (isaveNBOocc==1.or.isaveNO==1) MOocc=MOene !fch开头为saveNBOocc或saveNO时说明轨道能量部分其实是自然轨道/NBO的占据数，所以调换过来。  
if (isaveNBOocc==1.or.isaveNO==1) MOene=0.0D0  
if (isaveNBOene==1) MOocc=0.0D0 !fch开头为saveNBOene时fch里没有NBO占据数信息，故都设0。可以转换到wfn后手动补上占据数信息。  
where (MOocc==1000) !保存了NBO信息后，轨道能量/占据数最后几个数误为1000，都统一设为0。  
    MOocc=0.0D0  
end where  
where (MOene==1000)  
    MOene=0.0D0  
end where  
  
allocate(co(nmo,nprims))  
  
!!!!!!  
!现在就剩wfn的系数矩阵co(:,:)没有填好了，这部分用于生成它，代码及解释见下节  
!!!!!!  
  
write(*,"('There are',i6,' MOs,',i6,' atoms,',i7,' electrons,',i7,' Gaussian functions')") nmo,ncenter,int(dnint(sum(MOocc))),nprims  
write(*,"('Total energy:',f19.12,' hartree,   Virial ratio:',f12.8)") totenergy,virialratio  
write(*,*)  
close(10)  
end subroutine  
  
  

## 5.由fch的系数矩阵生成wfn的系数矩阵

后面的代码要用到计算高斯函数归一化系数的函数，如下所示。函数需要输入高斯函数类型代表的数字和指数。其中ft()代表阶乘函数。  
real*8 function normgau(type,exp)  
real*8 exp  
integer type,ix,iy,iz  
!类型顺序是S/X/Y/Z/ XX/YY/ZZ/XY/XZ/YZ/ XXX/YYY/ZZZ/XXY/XXZ/YYZ/XYY/XZZ/YZZ/XYZ，与wfn的类型顺序一致，与fch中的顺序不一致  
integer :: type2ix(20)=(/ 0,1,0,0, 2,0,0,1,1,0, 3,0,0,2,2,0,1,1,0,1 /)  
integer :: type2iy(20)=(/ 0,0,1,0, 0,2,0,1,0,1, 0,3,0,1,0,2,2,0,1,1 /)  
integer :: type2iz(20)=(/ 0,0,0,1, 0,0,2,0,1,1, 0,0,3,0,1,1,0,2,2,1 /)  
ix=type2ix(type)  
iy=type2iy(type)  
iz=type2iz(type)  
normgau=(2*exp/pi)**0.75*sqrt( (8*exp)**(ix+iy+iz)*ft(ix)*ft(iy)*ft(iz)/(ft(2*ix)*ft(2*iy)*ft(2*iz)) )  
end function  
  
从fch的系数矩阵amocoeff和bmocoeff转化到输出wfn文件要用的系数矩阵CO过程略微复杂，故单独说明。下面的图对3-21G计算的CH4的高斯函数循环过程进行了说明，每一排球是一个壳层，每个球是一个基函数，球中每条线是一个高斯函数，箭头指明了高斯函数循环次序。要把fch中通过层层循环描述的基函数的系数转换到wfn中的每个高斯函数的系数，就需要先把每个高斯函数都循环一遍，循环过程中赋予每个高斯函数系数、所在中心、指数和类型。  
  
下面的代码可以进行这个工作。最外层循环每一壳层（桔色箭头），在壳层中循环每个基函数（粉色箭头），在基函数中循环每个高斯函数（绿色箭头），在每个高斯函数中循环每个分子轨道。  
  
k=1 !初始化累加变量  
iexp=1  
ibasis=1  
do i=1,nshelltype !循环每一壳层  
    b(k:k+shellcon(i)*type2norb(shelltype(i))-1)%center=shell2atom(i) !同一壳层中高斯函数所属中心唯一，故把这一壳层中所有高斯函数所属中心都设好  
    do j=1,type2norb(shelltype(i)) !循环壳层中每个基函数，通过type2norb获得每个壳层所属的壳层类型含有基函数的数量  
        b(k:k+shellcon(i)-1)%functype=s2f(shelltype(i),j) !同一基函数中高斯函数所属类型唯一，故把这一基函数中所有高斯函数类型设好  
        do l=1,shellcon(i) !循环基函数中每个高斯函数，其数目由这一壳层收缩度shellcon(i)确定  
            b(k)%exp=primexp(iexp+l-1) !给高斯函数赋予指数  
            tnormgau=normgau(b(k)%functype,b(k)%exp) !获得高斯函数归一化系数  
            temp=concoeff(iexp+l-1) !确定高斯函数的收缩系数  
            if (shelltype(i)==-1.and.j/=1) temp=SPconcoeff(iexp+l-1) !如果是SP壳层且是壳层中第2、3、4个基函数（即P型），则改用P(S=P) Contraction coefficients里的收缩系数  
            do imo=1,nmo !循环每条分子轨道  
                if (wfntype==0.or.wfntype==2) then !闭壳层或限制性开壳层  
                    co(imo,k)=amocoeff(imo,ibasis)*temp*tnormgau !wfn文件中分子轨道向高斯函数的展开系数=分子轨道向基函数的展开系数*高斯函数在此基函数中的收缩系数*高斯函数的归一化系数  
                else if (wfntype==1) then !开壳层情况根据当前轨道序号判断所属自旋类型，使用fch中不同的系数矩阵生成co(imo,k)  
                    if (imo<=nalphaelec) co(imo,k)=amocoeff(imo,ibasis)*temp*tnormgau  
                    if (imo>nalphaelec) co(imo,k)=bmocoeff(imo-nalphaelec,ibasis)*temp*tnormgau !imo-nalphaelec就是当前轨道在beta轨道中的序号  
                end if  
            end do  
            k=k+1 !当前高斯函数在全部高斯函数中的序号  
        end do  
        ibasis=ibasis+1 !当前基函数在全部基函数中的序号，以确定取amocoeff中的哪个值  
    end do  
    iexp=iexp+shellcon(i) !当前壳层第一个收缩系数在收缩系数列表concoeff中的位置  
end do  
  
将上述内容组合在一起，就成为了fch2wfn程序，完整的代码及编译好的程序见[/usr/uploads/file/20150609/20150609184044_26809.rar](http://sobereva.com/usr/uploads/file/20150609/20150609184044_26809.rar)，在CVF6.5、ifort编译通过。可以运行后输入fch文件名和输出的wfn文件名，也可以直接用命令行模式，如fch2wfn c:\sob.fch ..\saint.wfn。再次提醒，含自然轨道的fch开头一行应改为saveNO。含NBO的fch若用了后HF密度要把开头改为saveNBOocc，若用了SCF密度要把开头改为saveNBOene，以便fch2wfn正确处理。  
  
转换的结果和直接用高斯输出的wfn文件几乎完全一致，一般只有末位由于数值精度问题相差1或2。但有时会发现含自然轨道信息的fch转化出来的wfn中有几条轨道系数和高斯输出的wfn不一致，但实际上都是正确的，只是自然轨道取向不同而已。  
  
AIMALL中的模块aimqb也能将fch向wfn的转换，但aimqb转换出的wfn虽然内容正确，与fch2wfn一致，但格式与标准格式不符，可能造成一些AIM程序无法读取。而且高斯函数的储存顺序与一般规则有异（当然这完全不影响结果），比如3-21G，一般SP壳层的高斯函数的类型储存顺序是X X Y Y Z Z | X Y Z，其中|代表分裂价基的分隔，而aimqb转换出来的顺序是X Y Z X Y Z X Y Z。fch2wfn的转换不仅结果正确，也完整保留了wfn文件的习俗。fch2wfn的功能也已经整合进了Multiwfn中，在Multiwfn中读入fch后选功能6，再选保存wfn文件即可。
