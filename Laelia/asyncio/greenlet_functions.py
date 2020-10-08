
# -*- coding: utf-8 -*-
from greenlet import greenlet


def func1():
    print(1)       # Step 1: output 1
    gr2.switch()   # Step 2: skip to func2 function
    print(2)       # Step 5: output 2
    gr2.switch()   # Step 6: skip to func2 function


def func2():
    print(3)      # Step 3: output 3
    gr1.switch()  # Step 4: skip to func1 function
    print(4)      # Step 7: output 4


gr1 = greenlet(func1)
gr2 = greenlet(func2)

gr1.switch()   # Step 1: execute func1 function
