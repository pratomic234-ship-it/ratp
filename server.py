from parser import parse
from socket import *
from asyncio import *
HOST="localhost"
PORT=8080
with socket(AF_INET,SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print("awaiting client")
    conn, addr= s.accept()
    with conn:
        print("client connected")
        data=conn.rcv(1024)
        print("recu:",data.decode())
        conn.sendall(b"bien recu")