from socket import *#type:ignore
from asyncio import *#type:ignore
HOST="localhost"
PORT=8080
with socket(AF_INET,SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print("awaiting client")
    conn, addr= s.accept()
    with conn:
        print("client connected")
        data=b""
        while b";" not in data:
            chunk=conn.recv(1024)
            data+=chunk
            if not chunk:
                break
        conn.sendall(b"ACK")
        print("recu:",data.decode())

