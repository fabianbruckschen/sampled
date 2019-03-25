#!/usr/bin/env python3

import socket  # creating server client connections for efficient communication
import pickle  # efficient file saving & loading

p = 60387  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
server = socket.gethostname()  # Get local machine name
s.bind((server, p))  # Bind to the port
s.listen(2)  # Now wait for (max 2) client connections

print('Server '+server+' listening....')
known_conns = []  # ongoing list of received connections

while True:
    # connection
    conn, addr = s.accept()  # Establish connection with client.
    print("Got connection from", addr) 
    
    # receive data
    msg = conn.recv(pow(2,15))
    print("Server received", str(msg))
    
    # file
    i = '1'
    if addr[0] in known_conns:  # if we already received from this client
        i = '2'
        
    file = open('data/'+str(addr[0])+'-'+i+'.pickle', 'wb')
    # dump it here (serialisierung)
    pickle.dump(msg, file)
    known_conns.append(addr[0])

    # close
    file.close()
    print("Done receiving")
    conn.close()