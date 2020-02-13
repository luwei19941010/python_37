#-*-coding:utf-8-*-
# Author:Lu Wei

# from threading import Thread,current_thread
# from  concurrent.futures import ThreadPoolExecutor
# import os
#
# def func(l):
#     print(l)
#     # for i in l:
#     #     print(i)
#     #     # return i
#
# tp=ThreadPoolExecutor(10)
# count=0
# l=[]
# d=[]
# with open('test',mode='r',encoding='utf-8') as f:
#     for i in f:
#         if len(l)==100:
#             tp.submit(func,l)
#             l.clear()
#         l.append(i)




#====================================

#
# with open('test','w',encoding='utf-8')as f:
#     for i in range(20001):
#         f.write(str(i)+'\n')
import threading
from threading import RLock

#
# def print_line(lines):
#     print(lines)
#
# from concurrent.futures import ThreadPoolExecutor
#
# tp = ThreadPoolExecutor(20)
# with open('test', encoding='utf-8') as f:
#     lines = []
#     for line in f:
#         if len(lines) == 100:
#             tp.submit(print_line, lines)
#             lines.clear()
#         lines.append(line)
#     if lines:
#         tp.submit(print_line, lines)




#
def print_line(lines):
    print(lines,current_thread().ident)

def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            yield line

def submit_func(tp,line=None,end= False,lines = []):
    if line:
        lines.append(line)
    if len(lines) == 100 or end:
        # print(lines)
        tp.submit(print_line, lines)
        lines.clear()

from concurrent.futures import ThreadPoolExecutor
from threading import current_thread

tp = ThreadPoolExecutor(20)
for line in read_file('test'):
    submit_func(tp,line)
submit_func(tp,end=True)