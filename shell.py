import basic

while True:
    text = input("basic > ")
    result,error = basic.run("mycode", text)
    if error: print(error.as_string())
    else: print(result)