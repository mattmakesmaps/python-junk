import pdb
import pickle
import os

def test(todos, abcd, ijkl):
    return "Command 'test' returned:\n" + \
            "abcd: " + abcd + "\nijkl: " + ijkl

def capitalize(todo):
    todo['level'] = todo['level'].upper()
    return todo

def sort_todos():
    global todos
    important = [capitalize(todo) for todo in todos
            if todo['level'].lower() == 'important']
    unimportant = [todo for todo in todos
            if todo['level'].lower() == 'unimportant']
    medium = [todo for todo in todos
            if todo['level'].lower() != 'important' and
            todo['level'].lower() != 'unimportant']
    todos = important + medium + unimportant

def create_todo(todos, title, description, level):
    """Create a todo."""
    todo = {
            'title':title,
            'description':description,
            'level':level,
            }
    todos.append(todo)
    sort_todos()
    return "Created '%s'." % title

def delete_todo(todos, which):
    if not which.isdigit(): # if FALSE, then
        return ("'" + which + "' needs to be the number of a todo!")
    which = int(which)
    if which < 1 or which > len(todos):
        return("'" + str(which) + "' needs to be the number of a todo!")
    del todos[which-1]
    return "Deleted todo #" + str(which)

def edit_todo(todos, which, title, description, level):
    if not which.isdigit():
        return("'" + which + "' needs to be the number of a todo!")
    which = int(which)
    if which < 1 or which > len(todos):
        return("'" + str(which) + "' needs to be the number of a todo!")

    todo = todos[which-1]
    if title != "":
        todo['title'] = title
    if description != "":
        todo['description'] = description
    if level != "":
        todo['level'] = level

    sort_todos()
    return "Edited todo #" + str(which)

def save_todo_list():
    """Save the todo list"""
    save_file = file("todos.pickle", "w")
    pickle.dump(todos, save_file)
    save_file.close()    

def load_todo_list():
    """Load the todo list is it exists"""
    global todos
    if os.access("todos.pickle", os.F_OK):
        save_file = file("todos.pickle")
        todos = pickle.load(save_file)

def show_todos(todos, which="All"):
    """Given the todos object, display them"""
    output = ("Item|Title|Description|Level|\n")
    
    if (which=="All" or which==""):
        for index, todo in enumerate(todos): #enumerate creates list w/ index
            line = str(index+1) + '|'
            for key in ['title','description','level']:
                line += str(todo[key]) + '|' 
            output += line + "\n"

    if (which!="All" and which!=""):        
        if not which.isdigit(): # if FALSE, then
            return ("'" + which + "' needs to be the number of a todo!")
        which = int(which)
        if which < 1 or which > len(todos):
            return("'" + str(which) + "' needs to be the number of a todo!")
        todo = todos[which-1]
        line = str(which) + '|'
        for key in['title','description','level']:
            line += str(todo[key]) + '|'
        output += line + "\n"

    return output

def get_input(fields):
    """Get user input"""
    user_input = {}
    for field in fields:
        user_input[field] = raw_input(field + "> ")
    return user_input

commands = {
        'new':[create_todo, ['title','description','level']],
        'test':[test,['abcd','ijkl']],
        'show':[show_todos,['which']],
        'delete':[delete_todo, ['which']],
        'edit':[edit_todo, ['which','title','description','level']],
        }

todos = []

def run_command(user_input, data=None):
    user_input = user_input.lower()
    if user_input not in commands:
        return user_input + "? Command not found."
    else:
        the_func = get_function(user_input)

    if data is None:
        the_fields = get_fields(user_input)
        data = get_input(the_fields)
    return the_func(todos, **data)

def get_function(command_name):
    """Given a command, return the associated function"""
    return commands[command_name][0]

def get_fields(command_name):
    """Given a command, return the associated fields"""
    return commands[command_name][1]

def main_loop():
    """Given some user input, execute it."""
    user_input = ""
    load_todo_list() #look for pre-existing save_file
    while 1:
        print run_command(user_input)
        user_input = raw_input("> ")
        if user_input.lower().startswith("quit"):
            print "Exiting..."
            break
    save_todo_list() #save after the break

if __name__ == '__main__':
    main_loop()
