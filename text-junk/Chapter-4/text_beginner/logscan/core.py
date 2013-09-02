"""
This module contains all of our core log processing classes.
"""

import os
import string
import sys
import json
from collections import defaultdict
from ConfigParser import SafeConfigParser
from ConfigParser import ParsingError

class LogProcessor(object):
    """
    Process a combined log format.

    This processor handles log files in a combined format,
    objects that act on the results are passed in to
    the init method as a series of methods.
    """
    tmpl = string.Template(
        'line $line is malformed, raised $exc error: $error')

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
        Split a log file.

        Initially we just want size and requested file name, so
        we'll split on spaces and pull the data out.
        """
        parts = line.split()
        return {
            'size': 0 if parts[9] == '-' else int(parts[9]),
            'file_requested': parts[6],
            'status': parts[8]
        }

    def report(self):
        """
        Run report chain.
        """
        for c in self._call_chain:
            c.report()

    def parse(self, handle):
        """
        Parses the log file.

        Returns a dictionary composed of log entry values,
        for easy data summation.
        """
        line_count = 0
        for line in handle:
            line_count += 1
            try:
                fields = self.split(line)
            except Exception, e:
                print >>sys.stderr, self.tmpl.substitute(
                    line=line_count,
                    exc=e.__class__.__name__,
                    error=e)
                continue
            for handler in self._call_chain:
                getattr(handler, 'process')(fields)

        return line_count

class BaseHandler(object):
    """
    A Base class for all handlers.

    Not meant to be instanced directly,
    contains common methods and functions used
    within each handler.
    """
    def __init__(self, output, format):
        self.output = output
        self.format = format

    def do_text(self, results):
        """Render Text Data"""
        print >>self.output, results

    def render(self, results):
        """Dispatch the appropriate render routine"""
        getattr(self, 'do_%s' % self.format)(results)
        self.output.write('\n')

    def print_title(self):
        """
        Uniform title print method.
        """
        print >>self.output, "%s\n" % self.title, \
            "=" * len(self.title)

class ErrorCodeHandler(BaseHandler):
    """
    Collect Error Code Information.
    """
    title = 'Error Code Breakdown'

    def __init__(self, output=sys.stdout, format='text'):
        super(ErrorCodeHandler, self).__init__(output, format)
        self.error_codes = defaultdict(int)
        self.errors = 0
        self.lines = 0

    def process(self, fields):
        """
        Scan each line's data.

        Reading each line in, we'll save out the
        number of response codes we run into so we
        can get a picture of our success rate.
        """
        code = fields['status']
        self.error_codes[code] += 1

        # Assume anything > 400 is
        # an HTTP error
        self.lines += 1
        if int(code) >= 400:
            self.errors += 1

    def do_text(self, results):
        """
        Print out Status Summary.

        Create the status segment of the
        report.
        """
        self.print_title()
        longest_num = sorted(results.values())[-1]
        longest = len(str(longest_num))

        for k,v in results.items():
            print >>self.output, '{0}: {1:>{2}}'.format(k, v, longest)

        # Print summary information
        print >>self.output, 'Errors: {0}; Failure Rate: {1:%}; Codes: {2}'.format(
            self.errors, float(self.errors)/self.lines,
            len(results.keys()))

    def do_json(self, results):
        """
        Return as JSON a Status Summary.
        """
        results['title'] = self.title
        results['errors'] = self.errors
        results['failure_rate'] = float(self.errors)/self.lines
        results['codes'] = len(results.keys())

        print >>self.output, json.dumps(results, indent=4)

    def report(self):
        return self.render(self.error_codes)

class MaxSizeHandler(BaseHandler):
    """
    Check a file's size.
    """
    def __init__(self, size, output=sys.stdout, format='text'):
        super(MaxSizeHandler, self).__init__(output, format)
        self.size = size
        self.name_size = 0
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
            self.warning_files.add(
                (fields['file_requested'], fields['size']))

            # We want to keep track of the longest file
            # name, for formatting later.
            fs = len(fields['file_requested'])
            if fs > self.name_size:
                self.name_size = fs

    def do_text(self, result):
        """
        Format the Max Size Report.

        This method formats the report and prints
        it to the console.
        """
        self.print_title()
        for f,s in result.items():
            print >>self.output, '%-*s :%d' % (self.name_size, f, s)

    def do_json(self, result):
        """
        Format Max Size Report as JSON.
        output results to console.
        """

        # Add title attribute
        result['title'] = self.title
        print >>self.output, json.dumps(result, indent=4)

    def report(self):
        return self.render(
            dict(self.warning_files))

def load_config(config_file):
    """
    Load configuration.

    Reads the name of the configuration
    of of sys.argv and loads our config.
    from disk.
    """
    config_parser = SafeConfigParser(
        defaults={
            'input_source': '-',
            'dir': os.getcwd(),
            'threshold': '0',
            'show_footer': 'True',
            'output_format': 'text',
            'output_file': '-'
        }
    )

    if not config_parser.read(config_file):
        parser.error('Could not parse configuration')

    return config_parser

def get_stream(filename, default, mode):
    """
    Return a file stream.

    If a '-' was passed in, then we just
    return the default. In any other case,
    we return an open file with the specified
    mode.
    """
    if filename == '-':
        return default
    else:
        return(open(filename, mode))
