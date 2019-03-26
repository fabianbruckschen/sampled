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
    data = b''
    while True:
        packet = conn.recv(pow(2,12))
        if not packet: break
        data += packet
    print('Server received', len(data), ' bytes')
    
    # file
    if addr[0] in known_conns:  # if we already received from this client
        i = '2'  # this is the second interaction
        known_conns.remove(addr[0])  # remove the address for the next interaction
    else:  # if this is the (again) first interaction of this client
        i = '1'  # first interaction
        known_conns.append(addr[0])  # add to known conns
        
        
    file = open('data/'+str(addr[0])+'-'+i+'.pickle', 'wb')
    # dump it here (serialisierung)
    pickle.dump(data, file)
    file.close()
    

    # close
    print("Done receiving")
    conn.close()