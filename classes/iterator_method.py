__author__ = 'matt'
__date__ = '5/25/13'

"""
Example 13.5 In Core Python Programming.
"""

class AnyIter(object):
    def __init__(self, data, safe=False):
        # Note how data is being passed as input, but not assigned as
        # an instance attribute. However, iter is created as an instance
        # attribute, while not being directly assigned in the calling signiture.
        self.safe = safe
        self.iter = iter(data)

    # You need to explicity declare this method to
    # Make this class iterable.
    def __iter__(self):
        return self

    def next(self, howmany=1):
        retval = []
        for eachItem in range(howmany):
            try:
                retval.append(self.iter.next())
            except StopIteration:
                if self.safe:
                    break
                else:
                    raise
        return retval

if __name__ == '__main__':
    a = AnyIter(range(10))
    i = iter(a)
    for j in range(1,5):
        print j, ':', i.next(j)

    print 'begin B.'
    b = AnyIter(range(10), safe=True)
    print b.next(4)
    print b.next(4)
    print b.next(4)
