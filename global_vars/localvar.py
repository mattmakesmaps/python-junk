#global var_s #global variable here will still fail

def f1():
    global var_s
    #global var_s #global var here will pass
    print var_s
    var_s = "f1 var"
    print var_s

def f2():
    global var_s
    print var_s
    var_s = "f2 var"
    print var_s

global var_s
var_s = "non_func var"
f1()
f2()
print var_s
