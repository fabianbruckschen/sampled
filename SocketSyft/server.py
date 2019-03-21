#!/usr/bin/env python
# coding: utf-8

# # Checking Socket connection via pysyft module (Server)

# ## Preparations
# modules
import syft as sy
import torch;hook = sy.TorchHook(torch)  # hook into pytorch
import socket
import time
from syft.workers import WebsocketClientWorker
from syft.workers import WebsocketServerWorker
from multiprocessing import Process

# options
hostname = socket.gethostname()
port = 60387

# server starting function
def start_proc(participant, kwargs):  # pragma: no cover
    """ helper function for spinning up a websocket participant """
    def target():
        server = participant(**kwargs)
        server.start()
    p = Process(target=target)
    p.start()
    print('Server is listening')
    return p

# start server
kwargs = {'id': 'server', 'host': hostname, 'port': port, 
          'hook': hook, 'log_msgs': False, 'verbose': True,
          'data': torch.tensor([44,55,66,77])}

server = start_proc(WebsocketServerWorker, kwargs)

# time.sleep(0.1)  # give time for connection to be established
# socket_pipe = WebsocketClientWorker(**kwargs)
# time.sleep(30)
# socket_pipe._objects

# # define server
# server = WebsocketServerWorker(hook=hook,
#                                host=hostname,
#                                id='server',
#                                port=port,
#                                log_msgs=False,
#                                verbose=True)

# # and start it
# server.start()

