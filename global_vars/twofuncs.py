#global var_s #does nothing

def f1():
    # if no 'global' is present, will not implicitly
    # create a global variable, e.g. that f2() can use.
    global var_s
    var_s = "f1 var, first assignment"
    print var_s # non-func var
    var_s = "f1 var"
    print var_s # f1 var

def f2():
    global var_s # if ommited, will raise exception
    print var_s # f1 var
    var_s = "f2 var"
    print var_s # f2 var

#var_s = "non_func var"
f1()
f2()
print var_s #f2 var
