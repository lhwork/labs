#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataformat.py
#this script change data from your source to the dest data format

import os,getopt,sys

#read file ,return lines of the file
def read_file(path):
  f = open(path,"r")
  lines = f.readlines()
  f.close()
  return lines

#process one line
#now according to the order of to and the source file line order
#change to a more flexable way
def one_line_proc(parts,total,to,outsp):
    toindex = 0
    outline=""
    for i in range(1,total+1):
      if toindex!=len(to) and i==to[toindex]:
        outline+=parts[toindex]
        toindex+=1
      else:
        outline+="0"
      if i!=total:
        outline+=outsp
    return outline

#hand from inpath to the outpath
def process(inpath,total,to,outpath,insp="\t",outsp="\t"):
  lines = read_file(inpath)
  f = open(outpath,"w")
  result=[]
  for line in lines:
     parts = line.strip("\n").split(insp)
     if len(parts) == len(to):
       outline = one_line_proc(parts,total,to,outsp)
       result.append(outline+"\n")
  f.writelines(result)
  f.close()


def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"F:P:t:a:i:o:")
        if len(opts) < 3:
          print("the mount of params must great equal than 3")
          sys.exit(1)
        for op,value in opts:
          if op == "-i":
            inpath = value
          elif op == "-o":
            outpath = value
          elif op == "-t":
            total = int(value)
          elif op == "-a":
            to = value.split(",")
          elif op == "-F":
            insp = value.decode("string_escape")
          elif op == "-P":
            outsp = value.decode("string_escape")
        #print(opts)
        #print(args)
    except getopt.GetoptError:
        print("params are not defined well!")
    
    
    if 'outpath' not in dir():
      outpath = inpath+".dist"
    
    if 'inpath' not in dir():
      print("-i param is needed,input file path must define!")
      sys.exit(1)
    
    if 'total' not in dir(): 
      print("-t param is needed,the fields of result file must define!")
      sys.exit(1)

    if 'to' not in dir():
      print("-a param is needed,must assign the field to put !")
      sys.exit(1)

    if not os.path.exists(inpath):
      print("file : %s is not exists"%inpath)
      sys.exit(1)

    tmp=[]
    for st in to:
      tmp.append(int(st))
    to=tmp


    if 'insp' in dir() and 'outsp' in dir():
      #print("path a")
      process(inpath,total,to,outpath,insp,outsp)
    elif 'insp' in dir():
      #print("path b")
      process(inpath,total,to,outpath,insp)
    elif 'outsp' in dir():
      #print("path c")
      process(inpath,total,to,outpath,outsp=outsp)
    else:
      #print("path d")
      process(inpath,total,to,outpath)

#if __name__ =="__main__":
main()
