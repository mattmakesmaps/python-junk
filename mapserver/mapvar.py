__author__ = 'matt'
__date__ = '8/11/13'
"""
This script is designed to process mapfiles with specially formatted variables.
As input, the user can pass a mapfile with a python dictionary header. Keys for this
dictionary can be inserted into the mapfile, prepended with a leading '@' symbol. The
script will replace the dictionary keys with their values, and export a revised mapfile.

The user can pass in a -v flag to specify an external variable file. Otherwise, the
variable dictionary is expected to be present in the input proto-mapfile.
"""
from ast import literal_eval
from optparse import OptionParser
import os

def returnFile(inFile, mode='r'):
    """
    Return a file like object
    """
    return open(os.path.join(os.path.dirname(__file__), inFile), mode)

def get_variables(inFile, var_file):
    """
    Given a seperate variable file, or a proto mapfile containing
    a variables dict, return a python dictionary of variables.
    """
    variables = ''
    # Seperate Variable File
    if var_file:
        raise NotImplementedError('ERROR: Variable File Not Yet Implemented.')
    # Variables listed directly in file
    else:
        varFlag = False
        for line in inFile:
            if '{' in line:
                varFlag = True
            if '}' in line:
                variables = variables+'}'
                varFlag = False
                break
            if varFlag:
                variables = variables+line
        return literal_eval(variables)

def convert_variables(inFile, outFile, var_dict):
    """
    Given a source document, a destination document, and a dictionary of variables
    Substitute dict keys in the input file for dict values in the output file.
    """
    for line in inFile:
        if '@' in line:
            for word in line.split():
                if word.startswith('@'):
                    try:
                        new_content = var_dict[word[1:]]
                        # Insert Content based on Type
                        if isinstance(new_content, str):
                            outFile.write(line.replace(word, "'" + var_dict[word[1:]] + "'"))
                        if isinstance(new_content, list):
                            new_content = ' '.join(str(x) for x in new_content)
                            outFile.write(line.replace(word, new_content))
                    except KeyError as e:
                        raise KeyError('Variable %s found in proto mapfile. No corresponding variable entry' % word)
        else:
            outFile.write(line)

if __name__ == '__main__':
    try:
        # Setup parser args
        usage = "usage: %prog [options] input_proto_mapfile"
        parser = OptionParser(usage)
        parser.add_option('-v','--var_file',action='store',type='string',dest='var_file',
                          help="File containing a python dictionary, 'variables' of key:value pairs.")
        parser.add_option('-o','--out_file',action='store',type='string',dest='out_file',
                          help="Location of output mapfile.")
        (options, args) = parser.parse_args()
        if len(args) != 1:
            parser.error("Incorrect Number of Arguments")

        # Open In and Out Files
        proto_mapfile = returnFile(args[0])
        if not options.out_file:
            output_mapfile = returnFile(args[0][:-4], 'w')
        else:
            output_mapfile = returnFile(options.outfile, 'w')

        # Extract dictionary of variables.
        var_dict = get_variables(proto_mapfile, options.var_file)
        # Convert keys to values in output mapfile.
        convert_variables(proto_mapfile, output_mapfile, var_dict)
    except Exception as e:
        print e
    finally:
        proto_mapfile.close()
        output_mapfile.close()

