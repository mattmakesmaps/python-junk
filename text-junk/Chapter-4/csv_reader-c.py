import csv
import sys
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--file', help="CSV Data File")
    opts, args = parser.parse_args()

    if not opts.file:
        parser.error('File name is required')

    csv.register_dialect('passwd', delimiter=':',quoting=csv.QUOTE_NONE)

    # required as passwd file doesn't contain headers.
    dict_keys = ('login', 'pwd', 'uid', 'gid', 'comment', 'home', 'shell')

    # Create a dict reader from an open file
    # handle and iterate through rows.
    reader = csv.DictReader(open(opts.file, 'rU'),
                            fieldnames=dict_keys,
                            dialect='passwd')  # 'U' indicates universal newlines.

    for user in reader:
        print '%s logs in with %s' % (user['login'], user['shell'])
