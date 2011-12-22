# -*- coding:utf8 -*-
import os
import sys

########################################################################
class BTree:
     """
     2叉树的建立与查找
     使用数字存储
     """
     nodes = []
     blank = "@"
     
     #初始化
     def __init__(self):
          """Constructor"""
          self.lnode = None
          self.rnode = None
          self.data = None
          
     @classmethod
     def createTree(klass,bt,message="root"):
          """
          这里使用先序遍历
          1）访问根节点，2）先序遍历左子树，2）先序遍历右子树
          """
          node = raw_input("please input " + message)
          if(node==""):
               bt.data = klass.blank
               return
          else:
               print node
               bt.data= node
               bt.lnode = BTree()
               klass.createTree(bt.lnode," %s left" % node) #创建左子树
               bt.rnode = BTree()
               klass.createTree(bt.rnode," %s right" % node) #创建右子树
     
     @classmethod
     def preOrderTraverse(klass,bt):
          """
          #先序遍历
          """
          if(bt):
               print bt.data,
               klass.preOrderTraverse(bt.lnode) #遍历左子树
               klass.preOrderTraverse(bt.rnode) #遍历右子树

#运行脚本
if __name__ =="__main__":
     bt = BTree()
     BTree.createTree(bt)
     BTree.preOrderTraverse(bt)
