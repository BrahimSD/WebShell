#!/usr/bin/env python3
import os,time,sys

dataIN = os.read(1, 100000)
body = dataIN.decode("utf-8")

def escaped_latin1_to_utf8(s):
 res = '' ; i = 0
 while i < len(s):
     if s[i] == '%':
         res += chr(int(s[i+1:i+3], base=16))
         i += 3
     else :
         res += s[i]
         i += 1
 return res

def getDate():
    return f'<h3>{time.strftime("%Y-%m-%d %H:%M:%S")}$</h3>'

def generateReponseString(historique, PID):
    payload = f"""
<!DOCTYPE html>
<head>
    <title>Hello, world!</title>
</head>
    <body>
        {historique}
        <article class="cmd">
        {getDate()}
            <form action="ajoute_{PID}" method="get">
                <input type="text" name="saisie" value="Tapez quelque chose" />
                <input class="input" type="submit" name="send" value="&#9166;">
            </form>
        </article>
        <style>
            h3{{
                margin: 0;
                 color: green;
            }}
            body{{
                background-color : gray;
            }}
            .cmd {{
                display : flex;
            
            }}
            
        </style>
    </body>
</html>"""

    data = """
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: """ + str(len(payload)) + "\n\n" + payload

    return (data.encode('UTF-8'))

def send_reponse(traitantShell, shellTraitant, param, PID):
    HIST_FILE = f"/tmp/historique_{PID}.txt"
    w = os.open(traitantShell, os.O_WRONLY)
    r = os.open(shellTraitant, os.O_RDONLY)
    histData = ""

    if (firstExecFlag == 1):
        result = ""
    else:
        param = param[0] + "; echo MARKER \n"
        os.write(w, param.encode("utf-8"))

        result = ""
        while (not result.endswith('MARKER')): #lecture de chaque carctere jusqu'a trouver marker
            result += os.read(r, 1).decode("utf-8").replace("\n" , "<br>")

            if result == "<br>":
                result = ""
        
        fHist = os.open(HIST_FILE, os.O_CREAT | os.O_APPEND | os.O_WRONLY)
        fHistR = os.open(HIST_FILE, os.O_RDONLY)
        
        os.write(fHist, f"<div class ='cmd'>{getDate()}<b>{param.replace('; echo MARKER','')}</b></div>{result[:-6]}\n".encode('utf-8'))
        histData = os.read(fHistR, 100000).decode('utf-8')
        
    # print("histFile=",HIST_FILE, file=sys.stderr)
    # print("histData=",histData, file=sys.stderr)
    # print("firstExecFlag=", firstExecFlag ,"res=", result, file=sys.stderr)

    reponse = generateReponseString(histData, PID)
    os.write(1, reponse)

def get_param_from_url():
    try:
        PARAMS = []
        PATH = body.split("\n")[0].split()[1]
        ARGS = PATH.split("?")
        if (len(ARGS) > 1):
            ALL_PARAM = ARGS[1].split("&")
            for x in ALL_PARAM:
                PARAMS.append(escaped_latin1_to_utf8(x.split("=")[1].replace('+', ' ')))
        PID = ARGS[0].split("_")[-1] 
        return PARAMS,PID
    except ValueError:
        pass

param=''
result=""
firstExecFlag = 1
PID = os.getpid()


if ("ajoute" in dataIN.decode("utf-8").split('\r\n')[0]):
    #print("texte=",dataIN.decode("utf-8").split('\r\n')[0] , file=sys.stderr)
    firstExecFlag = 0
    param, PID = get_param_from_url()
   
shellTraitant = f"/tmp/shell_vers_traitant_{PID}" 
traitantShell = f"/tmp/traitant_vers_shell_{PID}" 

if (firstExecFlag == 0):
    send_reponse(traitantShell, shellTraitant, param, PID)
else:
    os.mkfifo(traitantShell)
    os.mkfifo(shellTraitant)

    pid = os.fork()
    if pid == 0:
        r = os.open(traitantShell, os.O_RDONLY)
        w = os.open(shellTraitant, os.O_WRONLY)
        
        os.dup2(r, 0)
        os.dup2(w, 1)
        os.dup2(w, 2)

        os.execvp('sh', ['sh'])
    else:
        send_reponse(traitantShell, shellTraitant, param, PID)
        os.wait()