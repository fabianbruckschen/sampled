#!/usr/bin/env python3

import socket  # Import socket module
import pickle  # Import Pickle module
import time    # Import time module


p = 60387  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
server = socket.gethostname()  # Get local machine name
s.bind((server, p))  # Bind to the port
s.listen(2)  # Now wait for (max 2) client connections

print('Server '+server+' listening....')

while True:
    #start timing
    start = time.time()
    #connection
    conn, addr = s.accept()  # Establish connection with client.
    print("Got connection from", addr) 
    
    # receive data
    msg = conn.recv(pow(2,15))
    print("Server received", str(msg))
    
    # file
    file = open('../data/'+str(addr[0])+'.pickle', 'wb')
    
    # dump it here (serialisierung)
    pickle.dump(msg, file)
    
    #NUR INFO: Daten deserialieren
    #pickle.loads(msg)
    
    # close
    file.close()
    print("Done receiving")
    
   # conn.close()
    conn.close()
    
   #end timing
    end = time.time()
    print (end - start)
    print("Got connection from", addr)