import pdb
import pickle
import os

def test(todos, abcd, ijkl):
    return "Command 'test' returned:\n" + \
            "abcd: " + abcd + "\nijkl: " + ijkl

def create_todo(todos, title, description, level):
    """Create a todo."""
    todo = {
            'title':title,
            'description':description,
            'level':level,
            }
    todos.append(todo)

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

def capitalize(todo):
    todo['level'] = todo['level'].upper()
    return todo

def show_todos(todos):
    """Given the todos object, display them"""
    output = ("Item|Title|Description|Level|\n")

    # List Comprehension
    important = [capitalize(todo) for todo in todos
            if todo['level'].lower() == 'important']
    unimportant = [todo for todo in todos
            if todo['level'].lower() == 'unimportant']
    medium = [todo for todo in todos
            if todo['level'].lower() != 'important' and
               todo['level'].lower() != 'unimportant']
    sorted_todos = (important + medium + unimportant) 

    for index, todo in enumerate(sorted_todos): #enumerate creates list w/ index
        """
        line = str(index+1).ljust(8)
        for key, length in [('title', 16),('description', 24),('level', 16)]:
            line += str(todo[key]).ljust(length)
        """
        line = str(index+1) + '|'
        for key in ['title','description','level']:
            line += str(todo[key]) + '|' 
            # equivalent to line = line + str(todo[key]) + '|'
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
        'show':[show_todos,[]],
        }

todos = []

def run_command(user_input, data=None):
    #pdb.set_trace()
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
