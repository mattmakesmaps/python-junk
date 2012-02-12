import todo
import os
import pdb

def test_create_todo():
    todo.todos = []
    todo.create_todo(todo.todos,
        title="Make some stuff",
        description="Stuff needs to be programmed",
        level="Important")

    assert len(todo.todos) == 1, "Todo was not created!"
    assert todo.todos[0]['title'] == "Make some stuff"
    assert (todo.todos[0]['description'] == "Stuff needs to be programmed")
    assert todo.todos[0]['level'] == "Important"

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
    pdb.set_trace()
    assert "todos.pickle" not in os.listdir('.')
    todo.save_todo_list()
    assert "todos.pickle" in os.listdir('.')
    todo.load_todo_list()
    assert "todo.todos" == todos_original
    os.unlink("todos.pickle")

    print "ok -- save_todo_list"

test_save_todo_list()
