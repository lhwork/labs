# -*- coding:utf8 -*-
import os
import sys

#2进制 to 10进制
def binary2decimal(binary = "0001"):
    '''
    根据栈后进先出的特性，我们使用栈完成2 to 10 的 转换
    算法：
        公式： Xn,Xn-1,.....X1,X0 = X0 * 2 ** 0,X1 * 2**1,.......Xn-1 * 2 ** n-1.Xn *2 ** n
        1）将栈有大到小压入栈。
        2）逐个出栈，* 2 ** i ，这里i为出栈元素的个数，并将数据累加。
        3） 打印出结果。
    '''
    bs = binary
    #定义Stack
    stack = []
    sum = 0
    #初始化栈
    for i in xrange(len(bs)):
        stack.append(bs[i])
    #开始计算
    for i in xrange(len(stack)):
        value  = stack.pop()
        sum +=  int(value) * ( 2 ** i )
    
    print  "decimal is : %s"  % sum
    
#运行脚本
if __name__ =="__main__":
    binary2decimal("0111")
