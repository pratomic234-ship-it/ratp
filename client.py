from socket import *
from parser import parse
from asyncio import *
HOST="localhost"
PORT=8080

with socket(AF_INET,SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"hello world")#b encode la chaine en octets
    data=s.recv(1024)#lit avec caractères maximum
    print("received:",data.decode())
