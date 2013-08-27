import csv
import sys
from optparse import OptionParser

def calculate_profit(day):
    return float(day['Revenue']) - float(day['Cost'])

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--file', help="CSV Data File")
    opts, args = parser.parse_args()

    if not opts.file:
        parser.error('File name is required')

    # Create a dict reader from an open file
    # handle and iterate through rows.
    reader = csv.DictReader(open(opts.file, 'rU'))  # 'U' indicates universal newlines.
    for day in reader:
        print '%10s: %10.2f' % (day['Date'], calculate_profit(day))
