# A module housing the randGen class
# created in parser-test.py

from optparse import OptionParser
from random import randint

# Class to handle generation of random numbers
# and performing basic math on them.

class randGen:
    # Each function must have 'self' as 1st arg.
    # initialize with length of list
    def __init__(self, numNums):
        self.numNums = numNums

    def showNums(self):
        print self.numNums

    def randNums(self, first, second):
        randList = []
        for idx in range(self.numNums):
            # first < second OR YOU FAIL
            randList.append(randint(first, second))
        return randList

    def doMathNums(self, randList, op):
        if op == "sum":
            sum = 0
            for i in randList:
                sum = sum + i
            print sum
        elif op == "product":
            product = 1
            for i in randList:
                product = product * i
            print product

