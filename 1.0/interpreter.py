info = {}  # scripts
cmds = {}
loaded = ""
import os
import sys
#PLUGINS #T#O#D#O MOVE TO PLUGIN_LOADER.PY Not going to do
scripts=[]
if not os.path.isdir("./plugins/commands"):
    os.makedirs("./plugins/commands")
    print("Ceating Plugins Folder")
    sys.exit()
else:
    files=os.listdir("./plugins/commands")

    scripts=[]
    for file in files:
        if file.endswith(".py"):
            scripts.append(file)
for script in scripts:
    functions={}
    descriptions={}
    file=open("./plugins/commands/"+script, "r")
    data = file.read()
    file.close()
    exec(data)
    cmds.update(functions)
    info.update(descriptions)

#del description
description={}
#del functions
functions={}
#

def setvar(code, index):#used to be var, val
    global loaded
    try:
        var=code[index+1]
        val=code[index+2]
    except:
        loaded="names[$INSERTVALUEHERE] = $INSERTVALUEHERE[0]"
    else:

        if var == "name":
            loaded = "names[$INSERTVALUEHERE] = '" + val + "'"

descs={"set":"sets a VARIABLE",
       "help":"shows a list of commands",
       "?":"shows a list of commands"}
#descs="""\
#set : sets a VARIABLE\\
#help(?) : shows commands\\
#name : a VARIABLE to control the name shown when chatting
#"""
def hlp(*args):
    global loaded
    global descs
    loaded = """\
x={}
end=""
for i in x:
    end+=str(i) + ": " + str(x[i]) + "\\n"
clients[$INSERTVALUEHERE].sendall(bytes(end, 'utf-8'))""".format(descs)
    #loaded=str(descs)


keywords = {"set": setvar,
            "help": hlp,
            "?": hlp,}
keywords.update(cmds)
descs.update(info)



def interpret(code):
    data=""
    global loaded
    global keywords
    code = code.lower().replace("\r\n", "")
    code = code.split(" ")
    print(code)
    for i in code:
        if i in keywords:
            print("in KW")
            #try:
            #    keywords[i](code[code.index(i) + 1], code[code.index(i) + 2])
            #except:
            keywords[i](code, code.index(i))
            data=loaded
            loaded=""
    return data
