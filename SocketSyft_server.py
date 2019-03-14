#!/usr/bin/env python
# coding: utf-8

# # Checking Socket connection via pysyft module (Server)

# ## Preparations

# modules
import syft as sy
import torch
import socket
from syft.workers import WebsocketClientWorker
from syft.workers import WebsocketServerWorker

# hook into pytorch
hook = sy.TorchHook(torch)

# define server
server = WebsocketServerWorker(hook=hook,
                               host=socket.gethostname(),
                               id='server',
                               port=60000,
                               log_msgs=True,
                               verbose=True)

# and start it
server.start()

