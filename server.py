import os
import sys
import socket
import thread


def serverFunc(conn, folder):
    while True:
        comand = conn.recv(1024).decode()
        data = comand.split()
        
        if data[0] == 'exit':
            break

        if data[0] == 'LS':
            doc= open(folder+'/files.txt','r')
            for line in doc:
                print(line[0:-1])

        elif data[0] == "DEL":
            os.remove(folder+'/'+data[1])
            doc = open(folder + '/files.txt','w')
            for f in os.listdir('.'):
                if os.path.isfile(f):
                    doc.writelines(f+'\n')
            doc.close()
            print("file deleted")

        elif data[0] == 'GET':
            print(data[1])
            filename = data[1]
            filesize = os.path.getsize(folder + '/' + filename)
            conn.sendto(str(filesize).encode(),(HOST, PORT))
            ack = conn.recv(1024)

            #print("\n")
            leftBytes = filesize
            f = open(folder + '/' + filename, 'rb')
            while leftBytes != 0 :
                if leftBytes >= 1024:
                    sz = 1024
                else:
                    sz = leftBytes

                pckt = f.read(sz)
                pcktSize = len(pckt)
                conn.sendall(pckt)
                leftBytes -= int(pcktSize)
            f.close()
            print("Sucessfull download")
            doc = open(folder + '/'+"files.txt",'w')
            for f in os.listdir('.'):
                if os.path.isfile(f):
                    doc.writelines(f+'\n')
            doc.close()

        elif data[0] == "PUT":
            print(data[1])
            conn.sendto(data[1].encode(),(HOST,PORT))
            filesize = int(conn.recv(1024).decode())
            conn.sendto("ACK".encode(),(HOST,PORT))
            leftBytes = filesize
            print(filesize)
            f = open(folder + '/' +data[1],'wb')
            while leftBytes != 0:
                if leftBytes >=1024:
                    sz = 1024
                else:
                    sz = leftBytes
                pckt = conn.recv(leftBytes)
                leftBytes -= len(pckt)
            f.close()


    conn.close()


if __name__ == '__main__':
    HOST = ''
    PORT = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind((HOST, PORT))
        s.listen(5)
    except:
        print("Bind error")
        sys.exit()

    while True:
            print(os.getcwd())
            conn, addr = s.accept()
            print("Conected to " + str(addr[0])+":"+str(addr[1]))
            folder = conn.recv(1024).decode()

            if(not os.path.isdir(folder)):
                os.mkdir(folder)
                os.mknod("./"+folder+"/files.txt")
            thread.start_new_thread(serverFunc,(conn, folder))

    s.close()


