#!/usr/bin/env python3

import socket,sys,os,signal

HOST = "127.0.0.1" 
childList = []


if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "taritant port")
    sys.exit()

def controlPort():
    if (int(sys.argv[2]) <= 2000):
        print("entrer un port non resirve")
        sys.exit()
controlPort()


def handler(sig, ignore):
    
    for x in childList:
        os.kill(signal.SIGINT, x)
        os.wait()
    print("SIGINT reçu, fermeture des connections")
    sys.exit(0)

def handler2(sig,ignore):
    pid, status = os.wait()
    childList.remove(pid)

TRAITANT = sys.argv[1]
PORT = int(sys.argv[2])
print("ecoute sur le port",PORT)
args = ["python3","serveur.py"]
signal.signal(signal.SIGINT,handler)
signal.signal(signal.SIGCHLD,handler2)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((HOST,PORT)) 
    serversocket.listen(4) 
    while True:
        clientsocket,port = serversocket.accept()
        pid=os.fork()
        if pid==0:
            os.dup2(serversocket.fileno(),0)
            os.dup2(clientsocket.fileno(),1)
            os.execvp("python3", ["python3",sys.argv[1]])
        else:
            childList.append(pid)
        print(f"nouvelle connexion accepté (pid={pid}, port client={port[1]})")