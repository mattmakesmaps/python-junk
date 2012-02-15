import todo
import os
import pdb
import echo_server

def test_create_todo():
    todo.todos = []
    todo.create_todo(todo.todos,
        title="Make some stuff",
        description="Stuff needs to be programmed",
        level="Important")

    assert len(todo.todos) == 1, "Todo was not created!"
    assert todo.todos[0]['title'] == "Make some stuff"
    assert (todo.todos[0]['description'] == "Stuff needs to be programmed")
    assert todo.todos[0]['level'] == "IMPORTANT"

    print "ok -- create_todo"

test_create_todo()

def test_get_function():
    assert todo.get_function('new') == todo.create_todo
    print "ok -- get_function"

test_get_function()

def test_get_fields():
    assert (todo.get_fields('new') == ['title','description','level'])
    print "ok -- get_fields"

test_get_fields()

def test_run_command():
    result = todo.run_command(
            'test',
            {'abcd':'efgh','ijkl':'mnop'}
    )
    expected = """Command 'test' returned:
abcd: efgh
ijkl: mnop"""
    assert result==expected, \
            result + " != " + expected
    print "ok -- run_command"

test_run_command()

def test_show_todos():
    todo.todos = [
            {   
                'title':'test todo',
                'description':'this is a test',
                'level':'Important'
            }
        ]

    todo.sort_todos() #sort before you show!
    result = todo.show_todos(todo.todos)
    lines = result.split("\n")

    first_line = lines[0]
    assert "Item" in first_line
    assert "Title" in first_line
    assert "Description" in first_line
    assert "Level" in first_line

    second_line = lines[1]
    assert "1" in second_line
    assert "test todo" in second_line
    assert "this is a test" in second_line
    assert "IMPORTANT" in second_line

    print "ok -- show_todos"

test_show_todos()

def test_show_todos_subset():
    todo.todos = [
            { 'title': 'test unimportant todo',
                'description': 'An unimportant description',
                'level': 'Unimportant' 
            },
            { 'title': 'test medium todo',
                'description': 'A test',
                'level': 'Medium'
            },
            { 'title': 'test important todo',
                'description': 'An important test',
                'level': 'Important'
            }
        ]
    todo.sort_todos()
    result = todo.show_todos(todo.todos,"2")
    lines = result.split("\n")

    first_line = lines[0]
    assert "Item" in first_line
    assert "Title" in first_line
    assert "Description" in first_line
    assert "Level" in first_line

    second_line = lines[1]
    assert "2" in second_line
    assert "test medium todo" in second_line
    assert "A test" in second_line
    assert "Medium" in second_line

    print "ok -- show_todos_subset"

test_show_todos_subset()

def test_todo_sort_order():
    todo.todos = [
            { 'title': 'test unimportant todo',
                'description': 'An unimportant description',
                'level': 'Unimportant' 
            },
            { 'title': 'test medium todo',
                'description': 'A test',
                'level': 'Medium'
            },
            { 'title': 'test important todo',
                'description': 'An important test',
                'level': 'Important'
            }
        ]
    todo.sort_todos()
    result = todo.show_todos(todo.todos)
    lines = result.split("\n")
    assert "IMPORTANT" in lines[1]
    assert "Medium" in lines[2]
    assert "Unimportant" in lines[3]

    print "ok -- sort_order"

test_todo_sort_order()

def test_save_todo_list():
    todos_original = [
            { 'title':'test todo',
                'description':'This is a test',
                'level':'Important'
            }
        ]

    todo.todos = todos_original
    assert "todos.pickle" not in os.listdir('.')
    todo.save_todo_list()
    assert "todos.pickle" in os.listdir('.')
    todo.load_todo_list()
    #assert "todo.todos" == todos_original # order of dictionary items differ
    assert todo.todos[0]['level'] == todos_original[0]['level']
    assert todo.todos[0]['title'] == todos_original[0]['title']
    assert todo.todos[0]['description'] == todos_original[0]['description']
    os.unlink("todos.pickle")

    print "ok -- save_todo_list"

test_save_todo_list()

def test_todo_sort_after_creation():
    todo.todos = [
            { 'title':'test unimportant todo',
                'description':'This is an unimportant test',
                'level': 'Unimportant'
                },
            { 'title':'test medium todo',
                'description':'This is a test',
                'level':'Medium'
                },
            ]

    todo.create_todo(todo.todos,
            title="Make some stuff",
            description="Stuff needs to be programmed",
            level="Important")

    assert todo.todos[0]['level'] == "IMPORTANT"
    assert todo.todos[1]['level'] == "Medium"
    assert todo.todos[2]['level'] == "Unimportant"

    print "ok -- todo_sort_after_creation"

test_todo_sort_after_creation()

def test_delete_todo():
    todo.todos = [
            { 'title':'test important todo',
                'description':'this is an important test',
                'level':'IMPORTANT'
                },
            { 'title':'test medium todo',
                'description':'this is a test',
                'level':'Medium'
                },
            { 'title':'test unimportant todo',
                'description':'this is an unimportant test',
                'level':'Unimportant'
                },
            ]

    response = todo.delete_todo(todo.todos, which="2")

    assert response == "Deleted todo #2"
    assert len (todo.todos) == 2
    assert todo.todos[0]['level'] == 'IMPORTANT'
    assert todo.todos[1]['level'] == 'Unimportant'

    print "ok -- test_delete_todo"

test_delete_todo()

def test_delete_todo_failure():
    todo.todos = [
            { 'title':'test important todo',
                'description':'Thi is an important test',
                'level':'IMPORTANT'
                },
            ]

    for bad_input in ['','foo', '0', '42']:
        response = todo.delete_todo(
                todo.todos, which=bad_input)
        assert response == ("'" + bad_input + 
                "' needs to be the number of a todo!")
        assert len(todo.todos) == 1

    print "ok -- test_delete_todo_failures"

test_delete_todo_failure()

def test_edit_todo():
    todo.todos = [
            {'title':"Make some stuff",
                'description':'This is an important test',
                'level':'IMPORTANT'
                },
            ]

    response = todo.edit_todo(todo.todos,
            which="1",
            title="",
            description="Stuff needs to be programmed properly",
            level="")

    assert response == "Edited todo #1", response
    assert len(todo.todos) == 1
    assert todo.todos[0]['title']=="Make some stuff"
    assert (todo.todos[0]['description']==
             "Stuff needs to be programmed properly")
    assert todo.todos[0]['level']=="IMPORTANT"

    print "ok -- edit_todo"

test_edit_todo()

def test_edit_importance():
    todo.todos = [
            { 'title':'test medium todo',
                'description':'This is a medium todo',
                'level':'medium'
                },
            { 'title': 'test another medium todo',
                'description':'This is another medium todo',
                'level':'medium'
                },
            ]

    response = todo.edit_todo(todo.todos,
            which="2",
            title="",
            description="",
            level="Important")

    assert todo.todos[0]['level'] == "IMPORTANT"
    assert todo.todos[1]['level'] == "medium"

    print "ok -- edit_importance"

test_edit_importance()

def test_socket_get():
    echo_server.main_loop()
    todo.todos = [
            { 'title':'test medium todo',
                'description':'This is a medium todo',
                'level':'medium'
                },
            { 'title': 'test another medium todo',
                'description':'This is another medium todo',
                'level':'medium'
                },
            ]

    uri = '/1'
    method = 'GET'

    result = echo_server.handle_request(uri, method)
    print result

test_socket_get()

if __name__ == '__main__':
    echo_server.main_loop()
