from custom_socket import CustomSocket
import socket
import json
import numpy as np
import traceback
import select


def main():
    HOST = socket.gethostname()
    PORT = 10011

    server = CustomSocket(HOST, PORT)
    server.startServer()
    
    # server.sock.setblocking(0)


    while True:
        # Wait for connection from client :}
        try:
            conn, addr = server.sock.accept()
        except:
            continue
        
        print("Client connected from", addr)
        iter = 0
        # Process frame received from client
        while True:
            res = dict()
            print("iter:", iter)
            iter += 1
            try:
                data = server.recvMsg(conn)
                print(data.decode("utf-8"))

            except Exception as e:
                traceback.print_exc()
                print(e)
                print("Connection Closed")
                del res
                break

if __name__ == '__main__':
    main()