#global var_s #does nothing

def f1():
    # if no 'global' is present, will not implicitly
    # create a global variable, e.g. that f2() can use.
    global var_s
    var_s = "f1 var, first assignment"
    print var_s # f1 var, first assignment 
    var_s = "f1 var"
    print var_s # f1 var
    return var_s

def f2(in_variable):
    #global in_variable # raises exception in_variable both global and local
    in_variable = var_s
    print in_variable # f1 var
    in_variable = "f2 var"
    print in_variable # f2 var

#var_s = "non_func var"
f1()
f2(var_s)
print var_s #f1 var
# print in_variable # see above, raises exception
