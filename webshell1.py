#!/usr/bin/env python3
import os,time

dataIN = os.read(1, 100000)

body = dataIN.decode("UTF-8")
def escaped_latin1_to_utf8(s):
    res = ''
    i = 0
    while i < len(s):
        if s[i] == '%':
            res += chr(int(s[i+1:i+3], base=16))
            i += 3
        else:
            res += s[i]
            i += 1
    return res


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

def getDate():
    return f'<h3>{time.strftime("%Y-%m-%d %H:%M:%S")}$</h3>'

PARAMS , PID = get_param_from_url()
HIST_FILE = f"/tmp/historique_{PID}.txt"

histData = ""
if len(PARAMS) > 0:
    commande = PARAMS[0] + " ; echo MARKER" #creation MARKER
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.dup2(w, 1)
        os.dup2(w, 2) #verifier dans le shell les commandes taper
        os.execvp('sh', ['sh','-c', f"{commande}"])
    else:
        result = ''
        while (not result.endswith('MARKER')): #lecture de chauqe carctere jusque trouver marker
            result += os.read(r , 1).decode("utf-8").replace("\n" , "<br>")
    
    
        fHist = os.open(HIST_FILE, os.O_CREAT | os.O_APPEND | os.O_WRONLY)
        fHistR = os.open(HIST_FILE, os.O_RDONLY)
        os.write(fHist, f"<div class ='cmd'>{getDate()}<b>{commande.replace('; echo MARKER','')}</b></div>{result[:-6]}\n".encode('utf-8'))
        histData = os.read(fHistR, 10000000).decode('utf-8')
     
else:
    PID = os.getpid()
    HIST_FILE = f"/tmp/historique_{PID}.txt"


payload = f"""
<!DOCTYPE html>
<head>
    <title>Hello, world!</title>
</head>
    <body>
        {histData}
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

data = f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: """ + str(len(payload)) + "\n\n" + payload

os.write(1,data.encode("utf-8"))
