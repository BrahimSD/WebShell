import os

dataIN = os.read(1,100000)

body = dataIN.decode("utf-8").replace("\n","<br>")

payload = f"""
<!DOCTYPE html>
<head>
    <title>Hello, world!</title>
</head>
<body>
    {body}
</body>
</html>
"""

data = f"""
HTTP/1.1 200 
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: """ + str(len(payload)) + "\n\n" + payload

os.write(1,data.encode('utf-8'))