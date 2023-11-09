import os,sys

data=os.read(1,100000)

a=data.split()[0] == b"GET"
b=data.split()[2] == b"HTTP/1.1"

if(a and b):
    os.write(2,data)
else:
    os.write(2,b"request not supported")
    sys.exit(1)