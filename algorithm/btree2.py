#!/usr/bin/env python
#coding = utf-8
'''
Author: Yang XU
E-mail: xuy1202@gmail.com
'''


class _Tree(object):
    def __init__(self, value, nodeClass):
        self.value = nodeClass(value)
        self.leftNode = None
        self.rightNode = None
    
    def setLeftNode(self, node):
        self.leftNode = node
        
    def setRightNode(self, node):
        self.rightNode = node
        
    def __str__(self):
        returnList = []
        returnList.append(self)
        index = 0
        while index<len(returnList) and returnList[index]:
            curNode = returnList[index]
            returnList.append(curNode.leftNode)
            returnList.append(curNode.rightNode)
            index += 1
        return str(returnList)
    
    def __repr__(self):
        return '<N:%s>'%self.value


def build(sequence, nodeClass=lambda *a: a):
    length = len(sequence)
    if length:
        middle_index = length / 2
        value = sequence[middle_index]
        _tree = _Tree(value, nodeClass)
        _leftnode = build(sequence[:middle_index], nodeClass)
        _rightnode = build(sequence[middle_index+1:], nodeClass)
        _tree.setLeftNode(_leftnode)
        _tree.setRightNode(_rightnode)
    else:
        _tree = None
    return _tree


if __name__ == '__main__':
    class d(object):
        def __init__(self, value):
            self.v = '$%s'%str(value)
            
        def __str__(self):
            return self.v
        __repr__ = __str__
    
    sequence = range(5)
    b = build(sequence)
    print b
    b = build(sequence, d)
    print b
    
