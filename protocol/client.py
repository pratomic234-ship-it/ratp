from socket import *#type:ignore
from asyncio import *#type:ignore
import time
HOST="localhost"
PORT=8080

with socket(AF_INET,SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"RATP/0.1 SELECT * ;")#b encode la chaine en octets
    time.sleep(1)
    s.sendall(b"FROM example.com")
    data=s.recv(1024)#lit avec caractères maximum
    print("received:",data.decode())
