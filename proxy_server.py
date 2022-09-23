#!/usr/bin/env python3
import socket,sys
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():

    proxy_host = 'www.google.com'
    proxy_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    
        #QUESTION 3
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            #create a new socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(proxy_host)
                proxy_end.connect((remote_ip, proxy_port))
                p = Process(target=handle_echo, args=(proxy_end, addr, conn))
                p.daemon = True
                p.start()
                print("Started Process ",p)               
            
            conn.close()

def handle_echo(proxy_end, addr, conn):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)

if __name__ == "__main__":
    main()