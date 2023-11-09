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
            ALL_PARAM = ARGS[1].split("&")
            for x in ALL_PARAM:
                PARAMS.append(escaped_latin1_to_utf8(x.split("=")[1].replace('+', ' ')))
        return PARAMS
    except ValueError:
        pass


PARAMS = get_param_from_url()
saisie = ""
histdata = ""
if len(PARAMS) > 0:
    saisie = PARAMS[0]
    print("params = ",saisie,file=sys.stderr)


    fHist = os.open("/tmp/historique.txt",os.O_CREAT | os.O_APPEND | os.O_WRONLY)
    fHistR = os.open("/tmp/historique.txt",os.O_RDONLY)
    os.write(fHist,f"{saisie}\n".encode('utf-8'))
    histdata = os.read(fHistR,100000).decode("utf-8").rstrip().replace("\n" , "<br>")
    


    
payload = f"""
<!DOCTYPE html>
<head>
    <title>Hello, world!</title>
</head>
    <body>
        {histdata}
        <form action="ajoute" method="get">
            <input type="text" name="saisie" value="Tapez quelque chose" />
            <input type="submit" name="send" value="&#9166;">
        </form>
    </body>
</html>"""

data = f"""
HTTP/1.1 200
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length:""" + str(len(payload)) + "\n\n" + payload

os.write(1,data.encode("utf-8"))

