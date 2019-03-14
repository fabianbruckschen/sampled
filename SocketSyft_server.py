#!/usr/bin/env python
# coding: utf-8

# # Checking Socket connection via pysyft module (Server)

# ## Preparations
# modules
import syft as sy
import torch;hook = sy.TorchHook(torch)  # hook into pytorch
import socket
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
    return p

# start server
kwargs = {'id': 'server', 'host': hostname, 'port': port, 
          'hook': hook, 'log_msgs': True, 'verbose': True}
server = start_proc(WebsocketServerWorker, kwargs)

# # define server
# server = WebsocketServerWorker(hook=hook,
#                                host=hostname,
#                                id='server',
#                                port=port,
#                                log_msgs=True,
#                                verbose=True)

# # and start it
# server.start()

