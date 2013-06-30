__author__ = 'matt'
__date__ = '6/30/13'

"""
This example demonstrates the use of class inheritance (Points --> MultiPoints)
and compositions (Points --> Lines)
"""

class Point(object):
    """
    This class represents an X,Y point.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = [self.x,self.y]

    def __str__(self):
        return "Point Object: %s, %s" % (self.x, self.y)

class PositiveCheckPoint(Point):
    """
    A subclass of point with an additional method
    to determine if the coordinates are positive.
    """
    def is_Positive(self):
        for coord in self.coordinates:
            if coord < 0:
                return False
            else:
                return True


class Line(object):
    """
    This class represents a line, comprised of two point objects.
    """

    def __init__(self, startX, startY, endX, endY):
        self.start = Point(startX, startY)
        self.end = Point(endX, endY)

    def __str__(self):
        return "A line with start coordinates: %s and end coordinates %s" % (self.start.__str__(), self.end.__str__())

if __name__ == '__main__':
    p1 = Point(8,3)
    print p1

    p2 = Point(2,1)
    print p2

    l1 = Line(p1.x, p1.y, p2.x, p2.y)
    print l1

    posP1 = PositiveCheckPoint(9,2)
    print posP1
    print posP1.is_Positive()

    posP2 = PositiveCheckPoint(-9,1)
    print posP2
    print posP2.is_Positive()
