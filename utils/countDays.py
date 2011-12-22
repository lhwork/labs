#!/usr/bin/python
# -*- coding: utf-8 -*-
#countDays.py
# version 0.10      edited by lingyue.wkl 20110819 11:00:00
# version 0.11      modified by lingyue.wkl 20110820 11:37:00   add functions for days list
#this script count days,between two date or one date and the days between them

#考虑下，很多方法可以抽象出来，进一步优化，先期先实现功能吧
#下一个版本  改进所有函数，优化之，抽象之


import time,getopt,sys,datetime

def date_to_str(in_date):
    return str(in_date)[:10]
#计算两个日期之间相隔天数
def get_count_between_two_date(begin_date,end_date):
  b_date = begin_date.split("-")
  b_date = [int(num) for num in b_date]
  b_date_time = datetime.datetime(b_date[0],b_date[1],b_date[2])

  e_date = end_date.split("-")
  e_date = [int(num) for num in e_date]
  e_date_time = datetime.datetime(e_date[0],e_date[1],e_date[2])

  return (e_date_time - b_date_time).days

#计算某个日期前n天是哪一天   默认日期是今天
def get_n_days_before_or_after_oneday(n_days,in_date=str(datetime.date.today())[:10]):
  begin_date = in_date.split("-")
  begin_date = [int(num) for num in begin_date]
  return str(datetime.datetime(begin_date[0],begin_date[1],begin_date[2]) + datetime.timedelta(days=n_days))[:10]


def get_year():
    return str(datetime.date.today())[:4]

def get_month():
    return str(datetime.date.today())[5:7]

def get_day():
    return str(datetime.date.today())[8:]

def get_now():
    return datetime.datetime.now()

def get_today():
    return datetime.date.today()

def get_yesterday():
  return get_n_days_before_or_after_oneday(-1,str(datetime.date.today())[:10])

def get_tomorrow():
  return get_n_days_before_or_after_oneday(1,str(datetime.date.today())[:10])

#两个日期之间  n天的日期列表

def get_n_daystimes_list_of_two_date(begin_date,end_date):
  b_date = begin_date.split("-")
  b_date = [int(num) for num in b_date]
  b_date_time = datetime.datetime(b_date[0],b_date[1],b_date[2])

  e_date = end_date.split("-")
  e_date = [int(num) for num in e_date]
  e_date_time = datetime.datetime(e_date[0],e_date[1],e_date[2])

  days = (e_date_time - b_date_time).days
  n_days_list = []
  for i in range(0,days+1):
    n_days_list.append(str(b_date_time + datetime.timedelta(days=i)))
  return n_days_list

def get_n_days_list_of_two_date(begin_date,end_date):
  return [str(day)[:10] for day in get_n_daystimes_list_of_two_date(begin_date,end_date)]

def get_n_dayswiththreetimes_list_of_two_date(begin_date,end_date):
  days =  get_n_days_list_of_two_date(begin_date,end_date)
  days_three_time_list = []
  for day in days:
    for i in range(0,3):
        if i == 0:
           days_three_time_list.append(day+" 00:00:00")
        elif i == 1:
           days_three_time_list.append(day+" 12:00:00")
        else:
           days_three_time_list.append(day+" 23:59:59")
  return days_three_time_list

#某个日期之前n天  所有日期列表

def get_n_daystimes_list_before_or_after_one_day(n_days,end_date=str(datetime.date.today())[:10]):
  begin_date = get_n_days_before_or_after_oneday(n_days,end_date)
  return get_n_daystimes_list_of_two_date(begin_date,end_date)

def get_n_days_list_before_or_after_one_day(n_days,end_date=str(datetime.date.today())[:10]):
  begin_date = get_n_days_before_or_after_oneday(n_days,end_date)
  return get_n_days_list_of_two_date(begin_date,end_date)

def get_n_dayswiththreetimes_list_before_or_after_one_day(n_days,end_date=str(datetime.date.today())[:10]):
  begin_date = get_n_days_before_or_after_oneday(n_days,end_date)
  return get_n_dayswiththreetimes_list_of_two_date(begin_date,end_date)

def help_msg():
  print("功能：日期相关操作")
  print("选项:")
  print("\t 默认，无选项，输出当天日期，格式2011-08-20")
  print("\t -y   [可选，输出当前年份]")
  print("\t -m   [可选，输出当前月份]")
  print("\t -d   [可选，输出当前日]")
  print("\t -n +-数字  [可选，计算当前日期前后多少天的日期，数字为负表示往前]")
  print("\t -f 2011-10-22[可选,指定坐标日期，即以指定日期开始计算,若不指定，坐标日期为当天]")
  print("\t -t 2011-10-25  [可选，目标日期，可用于计算两个日期相隔天数]")
  print("\t -l [1|2|3]  [可选，是否列表，若选定，输出日期间的所有序列，1 2 3 代表三种不同格式]")
  sys.exit(0)

def print_list(l):
  for i in l:
    print(i)
#print(get_year())
#print(get_month())
#print(get_day())
#print(get_now())
#print(get_today())
#print(get_yesterday())
#print(get_tomorrow())
#print(get_n_days_before_or_after_oneday(2,"2011-08-20"))
#print(get_n_daystimes_list_of_two_date("2011-08-01","2011-08-05"))
#print(get_n_days_list_of_two_date("2011-08-01","2011-08-05"))
#print(get_n_dayswiththreetimes_list_of_two_date("2011-08-01","2011-08-05")) 
#print(get_n_daystimes_list_before_or_after_ond_day(-5,"2011-08-20"))
#print(get_n_days_list_before_or_after_ond_day(-5,"2011-08-20"))
#print(get_n_dayswiththreetimes_list_before_or_after_ond_day(-5,"2011-08-20"))

#程序入口，读入参数，执行
def main():
    is_list = False
    try:
        opts,args = getopt.getopt(sys.argv[1:],"n:f:t:o:ymdhrl:")
        
        if len(opts) == 0:
          print(get_today())
          sys.exit(0)

        for op,value in opts:
          if op in ("-h","-H","--help"):
            help_msg()
          if op == "-y":
            print(get_year())
            sys.exit(0)
          elif op == "-m":
            print(get_month())
            sys.exit(0)
          elif op == "-d":
            print(get_day())
            sys.exit(0)
          elif op == "-n":
            n_days = int(value)
          elif op == "-f":
            from_date = value
          elif op == "-t":
            to_date = value
          elif op == "-l":
            is_list = True
            list_type = value

    except getopt.GetoptError:
      print(sys.argv[0]+" : params are not defined well!")

    #if "n_days" not in dir() and "from_date" not in dir() and "to_date" not in dir():
    #     print(result_str)
   
    if "n_days" in dir() and "from_date" not in dir() and "to_date" not in dir():
      if not is_list:
         print(get_n_days_before_or_after_today(n_days))
      else:
         if list_type == "1":
           result_list = get_n_days_list_before_or_after_one_day(n_days)
         elif list_type == "2":
           result_list = get_n_daystimes_list_before_or_after_one_day(n_days)
         elif list_type == "3":
           result_list = get_n_dayswiththreetimes_list_before_or_after_one_day(n_days)
         print_list(result_list)
   
    if "n_days" in dir() and "from_date" in dir() and "to_date" not in dir():
      if not is_list:
         print(get_n_days_before_or_after_oneday(n_days,from_date))
      else:
         if list_type == "1":
           result_list = get_n_days_list_before_or_after_one_day(n_days,from_date)
         elif list_type == "2":
           result_list = get_n_daystimes_list_before_or_after_one_day(n_days,from_date)
         elif list_type == "3":
           result_list = get_n_dayswiththreetimes_list_before_or_after_one_day(n_days,from_date)
         print_list(result_list)


    if "n_days" not in dir() and "from_date" in dir() and "to_date" in dir():
      if not is_list:
         print(get_count_between_two_date(from_date,to_date))
      else:
         if list_type == "1":
           result_list = get_n_days_list_of_two_date(from_date,to_date)
         elif list_type == "2":
           result_list = get_n_daystimes_list_of_two_date(from_date,to_date)
         elif list_type == "3":
           result_list = get_n_dayswiththreetimes_list_of_two_date(from_date,to_date)
         print_list(result_list)
      
      

main()

