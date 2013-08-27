import csv
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-f', '--file', help="CSV Data File")
opts, args = parser.parse_args()

if not opts.file:
    parser.error('File name is required')

csv.register_dialect('passwd', delimiter=':',
                     quoting=csv.QUOTE_NONE)

dict_keys = ('login', 'pwd', 'uid', 'gid',
             'comment', 'home', 'shell')

print >>sys.stdout, ','.join([i.title() for i in dict_keys])
writer = csv.DictWriter(sys.stdout, dict_keys)

# Create a dict reader from an open file
# handle and iterate through rows.
reader = csv.DictReader(
    open(opts.file, 'rU'),
    fieldnames=dict_keys,
    dialect='passwd'
)

writer.writerows(reader)
