# -*- coding: UTF-8 -*-
from random import choice
import string

def Passwd(length=8, chars=string.letters+string.digits):
    for x in xrange(10):
        yield ''.join([choice(chars) for i in range(length)])


def gen_passwd():
    line=[]
    for item in Passwd():
        print item
        line.append(item)
    print line

if __name__ == '__main__':
    gen_passwd()

