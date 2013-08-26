import sys

class BadEmployeeFormat(Exception):
    """Badly formatted employee name"""
    def __init__(self, reason, name):
        Exception.__init__(self, reason)
        self.name = name

def get_employee():
    """
    Retrieve User information.
    """
    employee = raw_input('Employee Name: ')
    role = raw_input("Employee's Role: ")
    employee, role = employee.strip(), role.strip()

    # Check for full name
    if not employee.count(' '):
        raise BadEmployeeFormat('Full Name Required for records database.', employee)
    return {'name': employee, 'role': role}

if __name__ == '__main__':
    employees = []
    failed_entries = []
    print 'Enter your employees, EOF to Exit...'
    while True:
        try:
            employees.append(get_employee())
        except EOFError:
            print
            print "Employee Dump"
            for number, employee in enumerate(employees):
                print 'Empy #%d: %s, %s' % (number+1, employee['name'], employee['role'].title())

            print 'The following entries failed: ' + ', '.join(failed_entries)
            print u'\N{Copyright Sign}2010, bleh'
            sys.exit(0)
        except BadEmployeeFormat, e:
            failed_entries.append(e.name)
            err_msg = 'Err: ' + str(e)
            print >>sys.stderr, err_msg.center(len(err_msg)+20, '*')
