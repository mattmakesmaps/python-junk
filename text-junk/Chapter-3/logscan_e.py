#!/usr/bin/python

import time
import sys
from optparse import OptionParser

class LogProcessor(object):
    """
    Process a combined log format.

    This processor handles log files in a combined format, 
    objects that act on the results are passed in to 
    the init method as a series of methods.
    """
    def __init__(self, call_chain=None):
        """
        Setup parser.

        Save the call chain. Each time we process a log,
        we'll run the list of callbacks with the processed
        log results.
        """
        if call_chain is None:
            call_chain = []
        self._call_chain = call_chain

    def split(self, line):
        """
        Split a logfile line into a dict of specific
        attributes of interest.

        Initially we just want size and requested file name, so
        we'll split on spaces and pull the data out. 
        """
        parts = line.split()
        return {
            'size': 0 if parts[9] == '-' else int(parts[9]), 
            'file_requested': parts[6]
        }

    def report(self):
        """
        Run the report chain
        """
        for c in self._call_chain:
            print c.title
            print '=' * len(c.title)
            c.report()
            print

    def parse(self, handle):
        """
        Parses the log file.

        for each line of the log file, execute every
        class's process method added to the call_chain.

        Each class on the call_chain should expect a
        formatted dictionary of attribute values from the
        logfile. Each class on the call_chain should
        have an associated process method.
        """
        line_count = 0
        for line in handle:
            line_count += 1
            fields = self.split(line)
            for handler in self._call_chain:
                # execute the callback's expected 'process'
                # method, passing in fields dict.
                getattr(handler, 'process')(fields)

        return line_count

class MaxSizeHandler(object):
    """
    Check a file's size.
    """
    def __init__(self, size):
        self.size = size  # This is really the max allowable size.
        self.name_size = 0 # Name size is used to pprint report to console.
        self.warning_files = set()

    @property
    def title(self):
        return 'Files over %d bytes' % self.size

    def process(self, fields):
        """
        Looks at each line individually.

        Looks at each parsed log line individually and 
        performs a size calculation. If it's bigger than 
        our self.size, we just print a warning.
        """
        if fields['size'] > self.size:
            # Add files to the warning set
            self.warning_files.add(
                (fields['file_requested'], fields['size'])
            )

            # We want to keep track of the longest file
            # name, for formatting later.
            fs = len(fields['file_requested'])
            if fs > self.name_size:
                self.name_size = fs

    def report(self):
        """
        Format the Max Size Report

        This method formats the report and prints it
        to the console.
        """
        # for the file name 'f' and the size 's',
        # print formatted output.
        for f,s in self.warning_files:
            print '%-*s :%d' % (self.name_size, f, s)

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-s', '--size', dest="size",
        help="Maximum File Size Allowed",
        default=0, type="int")

    parser.add_option('-f', '--file', dest="file",
        help="Path to web log file", default="-")

    opts,args = parser.parse_args()
    call_chain=[]

    # If flag is not set (e.g. no file given,
    # default to standard input)
    if opts.file == '-':
        file_stream = sys.stdin
    else:
        try:
            file_stream = open(opts.file, 'r')
        except IOError, e:
            print >> sys.stderr, str(e)
            sys.exit(-1)

    size_check = MaxSizeHandler(opts.size)
    call_chain.append(size_check)
    processor = LogProcessor(call_chain)

    initial = time.time()
    line_count = processor.parse(file_stream)
    duration = time.time() - initial

    # Ask processor to display the individual repots.
    processor.report()

    # Print our internal statistics
    print "Report Complete!"
    print "Elapsed Time: %#.8f seconds" % duration
    print "Lines Processed: %d" % line_count
    print "Avg. Duration per line: %#.16f seconds" % (duration / line_count) if line_count else 0
