__author__ = 'matt'
__date__ = '8/14/13'

import sys
from optparse import OptionParser

class LogProcessor(object):
    """
    Process a combined log format.
    """

    def __init__(self, call_chain=None):
        """
        Setup parser.
        """
        if call_chain is None:
            call_chain = []
        self._call_chain = call_chain

    def split(self, line):
        """
        Split a logfile.
        """
        parts = line.split()
        return {
            'size': 0 if parts[9] == '-' else int(parts[9]),
            'file_requested': parts[6]
        }

    def parse(self, handle):
        """
        Parse the logfile.
        """
        for line in handle:
            fields = self.split(line)
            for func in self._call_chain:
                func(fields)

class ColumnLogProcessor(LogProcessor):
    def split(self, line):
        parts = line.split()
        return {
            'size': int(parts[1]),
            'file_requested': parts[0]
        }

class MaxSizeHandler(object):
    """
    Check a file's size.
    """

    def __init__(self, size):
        self.size = size

    def process(self, fields):
        """
        Look at each line individually.
        """
        if fields['size'] > self.size:
            print >>sys.stderr, 'Warning: %s exceeeds %d bytes (%d)!' % (fields['file_requested'],
                                                                         self.size, fields['size'])

class MinSizeHandler(MaxSizeHandler):
    """
    Return an error if the file size reported falls
    below a minimum specified threshold.
    """

    def process(self, fields):
        if fields['size'] < self.size:
            print >>sys.stderr, 'Warning: %s is below %d bytes (%d)!' % (fields['file_requested'],
                                                                         self.size, fields['size'])

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-m', '--max-size', dest='max_size',
                      help="Max File Size Allowed",
                      default=0, type="int")

    parser.add_option('-M', '--min-size', dest='min_size',
                      help="Min File Size Allowed",
                      default=0, type="int")

    opts,args = parser.parse_args()
    print opts, args
    call_chain = []

    if opts.max_size != 0:
        max_size_check = MaxSizeHandler(opts.max_size)
        call_chain.append(max_size_check.process)

    if opts.min_size != 0:
        min_size_check = MinSizeHandler(opts.min_size)
        call_chain.append(min_size_check.process)

    processor = ColumnLogProcessor(call_chain)
    processor.parse(sys.stdin)