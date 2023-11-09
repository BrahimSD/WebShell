import os
import sys


dataIN = os.read(1,100000)

#print(data , file=sys.stderr)
body = dataIN.decode("UTF-8")
#os.write(2,data.encode("utf-8"))
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
            #print('all param=',ALL_PARAM, file=sys.stderr)
            for x in ALL_PARAM:
                PARAMS.append(escaped_latin1_to_utf8(x.split("=")[1].replace('+', ' ')))
            #print('param=',PARAMS[0], file=sys.stderr)
        return PARAMS
    except ValueError:
        pass

#print('fils ON', file=sys.stderr)
PARAMS = get_param_from_url()

saisie = ""
if len(PARAMS) > 0:
    saisie = PARAMS[0]
    print('param=',saisie, file=sys.stderr)
body = dataIN.decode("utf-8").replace("\n","<br>")


payload = f"""
<!DOCTYPE html>
<head>
    <title>Hello, world!</title>
    <link rel="shortcut icon" href="data"/>
</head>
    <body>
    {body}
    {saisie}
        <form action="ajoute" method="get">
            <input type="text" name="saisie" value="Tapez quelque chose" />
            <input type="submit" name="send" value="&#9166;">
        </form>
    </body>
</html>
"""

data = f"""
HTTP/1.1 200 
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: """ + str(len(payload)) + "\n\n" + payload

os.write(1,data.encode("utf-8"))
