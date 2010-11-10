#!/usr/bin/env python

# optparse handles only options.
# not positional arguments
from optparse import OptionParser

def doMath(op,one,two):
    if op == "add":
	x = one + two
        print "%(a)s + %(b)s = %(c)s" % {'a': one,'b': two,'c': x}
    elif op == "subtract":
	x = one - two
        print x
    else:
        print "sol"

def main():
    parser = OptionParser(version="%prog 0.0.1")
    parser.add_option("-o", "--operation", action="store",
                  type="string", dest="op", metavar="OPERATION", default="add",
                  help="The OPERATION type to be applied: "
                       "add OR subtract [default: %default]")
    parser.add_option("-q", "--quiet", action="store_false",
                  dest="verbose", default=True,
                  help="don't print status messages to stdout")

    # options are options
    # args are positional arguments
    (options, args) = parser.parse_args()

    first=int(args[0])

    second=int(args[1])

    doMath(options.op, first, second)

if __name__ == '__main__':
    main()

