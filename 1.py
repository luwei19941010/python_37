#-*-coding:utf-8-*-
# Author:Lu Wei
import threading
from threading import RLock,current_thread

#
def print_line(lines):
    print(lines,current_thread().ident)

from concurrent.futures import ThreadPoolExecutor

tp = ThreadPoolExecutor(20)
with open('test', encoding='utf-8') as f:
    lines = []
    for line in f:
        if len(lines) == 100:
            tp.submit(print_line, lines)
            lines.clear()
        lines.append(line)
    if lines:
        tp.submit(print_line, lines)
    # tp.shutdown()