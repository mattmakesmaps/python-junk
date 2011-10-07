#!/usr/bin/python
from types import *

def doMaths(x, y, operation):
    assert type(operation) is StringType, "operation not a string, %s" %operation     
    if operation == '+':
        result = x + y
    elif operation == '-':
        result = x - y
    elif operation == '*':
        result = x * y
    elif operation == '/':
        result = x/y
    else:
        result = "Wrong Op Given"
        
    return result