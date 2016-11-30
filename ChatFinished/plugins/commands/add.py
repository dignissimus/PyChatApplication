def add(code, index):
    try:
        global loaded
        a=code[index+1]
        b=code[index+2]
        value=str(int(a)+int(b))

    except:
        value="[ERROR]"
    finally:
        loaded = "clients[$INSERTVALUEHERE].sendall(bytes(str(" + value + ")+'\\n','utf-8'))"
description={"add":"adds two numbers"}
functions={"+": add,
           "add":add}