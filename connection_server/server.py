#!/usr/bin/env python3

import socket  # Import socket module

p = 60387  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
server = socket.gethostname()  # Get local machine name
s.bind((server, p))  # Bind to the port
s.listen(5)  # Now wait for client connection.


print(server)
print("Server listening....")

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print("Got connection from", addr) 
    data = conn.recv(1024)
    print("Server received", repr(data))

    filename='received.txt'
    f = open(filename, 'w')
    f.write(repr(data))
#     f = open(filename,'rb')
#     l = f.read(1024)
#     while (l):
#        conn.send(l)
#        print('Sent ',repr(l))
#        l = f.read(1024)
    f.close()

    print("Done receiving")
#     conn.send("Thank you for connecting")
    conn.close()
