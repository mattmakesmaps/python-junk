#!/usr/bin/env python

# This version of parser-test.py uses a module, randGen
# to store the random number generator class.

from optparse import OptionParser
from random import randint
from randGen import randGen

# Original function to handle non-random math
def doMath(op,one,two):
    if op == "sum":
        x = one + two
        print "%(a)i + %(b)i = %(c)i" % {'a': one,'b': two,'c': x}
    elif op == "product":
        x = one * two
        print x
    else:
        print "sol"

def main():
    parser = OptionParser(version="%prog 0.0.2",
                  usage="usage: %prog [options] integer1 integer2")
    parser.add_option("-o", "--operation", action="store",
                  type="string", dest="op", metavar="OPERATION", default="sum",
                  help="The OPERATION type to be applied: "
                       "sum OR product [default: %default]")
    parser.add_option("-r", "--random", action="store_true",
                  dest="doRandom", default=False,
                  help="use a list of randomly generated values")
    parser.add_option("-l", "--length", action="store",
                  type="int", dest="listLength", metavar="LENGTH", default="10",
                  help="The LENGTH of list to create when using the -r flag "
                        "[default: %default]")

    # options are options
    # args are positional arguments
    (options, args) = parser.parse_args()

    print "random status: %s" %options.doRandom

    first=int(args[0])
    second=int(args[1])
    
    # check if random flag is throw if so, extract operation flag, and use
    # positional arguments as min/max ranges for values in list.
    # List length set with -l flag.
    if options.doRandom == False:
        doMath(options.op, first, second)
    elif options.doRandom == True:
        numInstance = randGen(options.listLength)
        newRandomList = numInstance.randNums(first, second)
        print newRandomList
        numInstance.doMathNums(newRandomList, options.op)

if __name__ == '__main__':
    main()
