---
post_id: 302
title: 计算两个平面夹角的小程序
url: http://sobereva.com/302
date: '2015-08-20T22:29:00+08:00'
source_categories:
- 其它
primary_topic: 其它软件
secondary_topics:
- 可视化
- 结构与文件格式
academic_relevant: true
classification_reason: 核心是一个计算两个平面夹角的小工具。
topic_family: 软件
exclude_reason: ''
confidence: 0.96
image_count: 0
local_assets_dir: assets
---

2021-Mar-3补充：后来在Multiwfn里加入了对动力学轨迹计算指定的两个平面间夹角随帧号变化的功能，见《计算分子动力学轨迹中两个环平面间的距离和夹角》（<http://sobereva.com/590>）。

---

今天思想家公社QQ群有人问怎么计算两个平面的夹角。如果本身是二面角好办直接量就行了，但如果不属于这种情况就稍微麻烦，虽然有一些可视化程序如diamond可以量但终究为这点事安装一个也麻烦。这里提供个自写的不足挂齿的程序twoplane2angle来计算夹角。先输入定义第一个平面的三个点的坐标，再输入定义第二个平面的三个点的坐标，然后就会输出夹角。

下载地址：

[/usr/uploads/file/20150820/20150820222744_68251.rar](http://sobereva.com/usr/uploads/file/20150820/20150820222744_68251.rar)

源代码

program twoplane2angle  
implicit real*8 (a-h,o-z)  
write(*,*) "twoplane2angle: Get angle between two planes"  
write(*,*) "Programmed by Sobereva ([sobereva@sina.com](mailto:sobereva@sina.com)), 2015-Aug-20"  
write(*,"(a)") " Usage: Input three points for plane 1 and that for plane 2, then program outputs the angle between the two planes"  
write(*,*)  
do while(.true.)  
 write(*,*) "Input XYZ coordinates of point 1 for plane 1, e.g. 0.2,0.4,-3.6"  
 read(*,*) x1,y1,z1  
 write(*,*) "Input XYZ coordinates of point 2 for plane 1, e.g. 0.2,0.4,-3.6"  
 read(*,*) x2,y2,z2  
 write(*,*) "Input XYZ coordinates of point 3 for plane 1, e.g. 0.2,0.4,-3.6"  
 read(*,*) x3,y3,z3  
 call pointABCD(x1,y1,z1,x2,y2,z2,x3,y3,z3,A1,B1,C1,D1)  
 write(*,*) "Input XYZ coordinates of point 1 for plane 2, e.g. 0.2,0.4,-3.6"  
 read(*,*) x1,y1,z1  
 write(*,*) "Input XYZ coordinates of point 2 for plane 2, e.g. 0.2,0.4,-3.6"  
 read(*,*) x2,y2,z2  
 write(*,*) "Input XYZ coordinates of point 3 for plane 2, e.g. 0.2,0.4,-3.6"  
 read(*,*) x3,y3,z3  
 call pointABCD(x1,y1,z1,x2,y2,z2,x3,y3,z3,A2,B2,C2,D2)  
 pt1norm=dsqrt(A1**2+B1**2+C1**2)  
 pt2norm=dsqrt(A2**2+B2**2+C2**2)  
 vecprod=A1*A2+B1*B2+C1*C2  
 write(*,"(' Norm of normal vector 1:',f12.6)") pt1norm  
 write(*,"(' Norm of normal vector 2:',f12.6)") pt2norm  
 write(*,"(' Product of the two vectors:',f12.6)") vecprod  
 ang=acos(vecprod/pt1norm/pt2norm)  
 write(*,"(a,f12.4)") " The angle between the two planes is",ang/3.141592653589793238462D0*180  
 write(*,*)  
end do

end program

!!-------- Input three points, get ABCD of Ax+By+Cz+D=0  
subroutine pointABCD(x1,y1,z1,x2,y2,z2,x3,y3,z3,A,B,C,D)  
real*8 v1x,v1y,v1z,v2x,v2y,v2z,x1,y1,z1,x2,y2,z2,x3,y3,z3,A,B,C,D  
v1x=x2-x1  
v1y=y2-y1  
v1z=z2-z1  
v2x=x3-x1  
v2y=y3-y1  
v2z=z3-z1  
! Solve determinant(Vector multiply) to get the normal vector (A,B,C):  
!  i   j   k   //unit vector  
! v1x v1y v1z  
! v2x v2y v2z  
A=v1y*v2z-v1z*v2y  
B=-(v1x*v2z-v1z*v2x)  
C=v1x*v2y-v1y*v2x  
D=A*(-x1)+B*(-y1)+C*(-z1)  
end subroutine
