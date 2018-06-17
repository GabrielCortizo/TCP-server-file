import socket 
import os

HOST = ""
PORT = 5000

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))


login = raw_input("login $ ")
clientSocket.sendto(login.encode(),(HOST, PORT))

while True:
    comand = raw_input("Type your comand or (help to display avaibles ones) \n$ ")
    data = comand.split()
    if data[0] == 'help':

        print(''' 
                help - display avaible commands
                POST [filename] - To post filename into a sever.
                GET  [filename] - To download a filename from server.
                DEL  [filename] - To delete filename from server.
                LS              - To list the files into the server.
                exit            - Close the socket
                        ''')
        continue

    clientSocket.sendto(comand.encode(), (HOST, PORT))    
                   
    if data[0] == 'exit':
        break

    elif data[0] == 'GET':
        filesize = int(clientSocket.recv(1024).decode())
        clientSocket.sendto("ACK".encode(),(HOST, PORT))
        f = open(data[1],'wb')
        leftBytes = filesize
        while leftBytes!= 0:
            if leftBytes >= 1024:
                sz = 1024
            else:
                sz = leftBytes
            pckt = clientSocket.recv(sz)
            f.write(pckt)
            leftBytes -= int(len(pckt))

        f.close()
    elif data[1] == 'PUT':

        filesize = os.path.getsize(data[1])
        clientSocket.recv(1024)
        clientSocket.sendto(str(filesize).encode(),(HOST,PORT))
        rcvack = clientSocket.recv(1024)
        leftBytes = filesize
        f = open(data[1],'rb')
        while leftBytes != 0:
            if leftBytes >=1024:
                sz = 1024
            else :
                sz = leftBytes
            pckt = f.read(sz)
            clientSocket.sendall(pckt)
            leftBytes -= len(pckt)
        f.close()        


clientSocket.close()