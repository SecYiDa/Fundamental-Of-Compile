## 简单函数绘图语言解释器

### 0x01

py实现的函数绘图语言解释器，经过词法、语法（递归下降分析）、语义分析等，实现绘图功能。



### 0x02

主要绘图语句：

origin is (xx,xx);  /设置原点

Rot     is  xxx;   /设置旋转角度

Scale  is  (xx,xx)  /设置坐标比

For T From xx to xx step xx draw  (xx,xx)   / 画图

### 0x03

给了四个测试输入，输出结果包含画图结果和词法分析记号流、表达式语法树、可能的错误点。

（其中，c.txt 是测试错误反馈的）

### 0x04

环境：py3 、matplotlib库



### 0x05

测试结果：

![](https://github.com/SecYiDa/Fundamental-Of-Compile/blob/master/TestResult/Figure_1.png)

![](https://github.com/SecYiDa/Fundamental-Of-Compile/blob/master/TestResult/Figure_2.png)