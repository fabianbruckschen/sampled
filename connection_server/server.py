#!/usr/bin/env python3

import socket  # Import socket module

p = 60387  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
server = socket.gethostname()  # Get local machine name
s.bind((server, p))  # Bind to the port
s.listen(2)  # Now wait for client connection.


print(server)
print("Server listening....")

while True:
    conn, addr = s.accept()  # Establish connection with client.
    print("Got connection from", addr) 

    # open file
    filename='received_'+str(addr[0])+'.txt'
    f = open(filename, 'w')
    
    # receive data and write it to file
    data = conn.recv(1024)
    print("Server received", str(data))
    f.write(repr(data))
    f.close()

    # close server
    print("Done receiving")
    conn.close()
