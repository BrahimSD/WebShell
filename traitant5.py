import os
import sys

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
            # print('param=',ARGS, file=sys.stderr)
            ALL_PARAM = ARGS[1].split("&")
            for x in ALL_PARAM:
                PARAMS.append(escaped_latin1_to_utf8(x.split("=")[1].replace('+', ' ')))
        PID = ARGS[0].split("_")[-1] 
        return PARAMS,PID
    except ValueError:
        pass



PARAMS, PID = get_param_from_url()


saisie = ""
histdata = ""
if len(PARAMS) > 0:
    saisie = PARAMS[0]
HIST_FILE = f"/tmp/historique_session_{PID}.txt"
if len(PARAMS) > 0:
    
    fHist = os.open(HIST_FILE,os.O_CREAT | os.O_APPEND | os.O_WRONLY)
    fHistR = os.open(HIST_FILE,os.O_RDONLY)
    os.write(fHist,f"{saisie}\n".encode('utf-8'))
    histdata = os.read(fHistR,100000).decode("utf-8").rstrip().replace("\n" , "<br>")
else:
    PID = os.getpid()
    HIST_FILE = f"/tmp/historique_session_{PID}.txt"




payload = f"""
<!DOCTYPE html>
<head>
    <title>Hello, world!</title>
</head>
    <body>
        {histdata}
        <form action="ajouted_dans_session_{PID}" method="get">
            <input type="text" name="saisie" value="Tapez quelque chose" />
            <input type="submit" name="send" value="&#9166;">
        </form>
    </body>
</html>"""

data = f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: """ + str(len(payload)) + "\n\n" + payload

os.write(1,data.encode("utf-8"))

