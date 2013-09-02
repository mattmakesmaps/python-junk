"""
Command line entry points.
"""

import sys
import time
import optparse

# Our imports
from logscan.core import get_stream
from logscan.core import load_config
from logscan.core import ErrorCodeHandler, MaxSizeHandler
from logscan.core import LogProcessor

def main(arg_list=None):
    """
    Log Scanner Main.

    We still separate main off. This keeps it possible
    to use it from within yet another module, if we
    ever want to do that.
    """
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', dest='config',
                      help="Configuration File Path")

    opts, args = parser.parse_args(arg_list)
    if not opts.config:
        parser.error('Configuration File Required')

    # Now we can load the configuration file
    config = load_config(opts.config)

    # file_stream and output_stream simply expect to be file-like objects.
    file_stream = get_stream(
        config.get('main', 'input_source'), sys.stdin, 'r')

    output_stream = get_stream(
        config.get('main', 'output_file'), sys.stdout, 'w')

    output_format = config.get('display', 'output_format')

    call_chain = []

    # Size Check
    call_chain.append(
        MaxSizeHandler(
            int(config.get(
                'maxsize', 'threshold')
            ), output_stream, output_format)
    )

    # Error Code Checks
    call_chain.append(
        ErrorCodeHandler(
            output_stream, output_format)
    )

    # Build a processor object
    processor = LogProcessor(call_chain)

    initial = time.time()
    line_count = processor.parse(file_stream)
    duration = time.time() - initial

    # Ask the processor to display the
    # individual reports.
    processor.report()

    if config.getboolean('display', 'show_footer'):
        # Print our internal statistics, this always
        # goes to standard out.
        print
        print "Report Complete!"
        print "Elapsed Time: %#.8f seconds" % duration
        print "Lines Processed: %d" % line_count
        print "Avg. Duration per line: %#.16f seconds" % \
              (duration / line_count) if line_count else 0

if __name__ == '__main__':
    main(['/Users/matt/Documents/PyCharm/python-junk/text-junk/Chapter-4/text_beginner/logscan/cmd.py', '--config',
         '/Users/matt/Documents/PyCharm/python-junk/text-junk/Chapter-4/text_beginner/logscan.cfg'])