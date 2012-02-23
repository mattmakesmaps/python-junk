def f():
    global var_s
    print var_s
    var_s = "func value"
    print var_s

var_s = "non func value"
f()
print var_s
