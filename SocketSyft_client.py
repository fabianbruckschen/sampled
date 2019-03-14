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

# create client
socket_pipe = WebsocketClientWorker(hook=hook,
                                    host='ip-172-31-46-89',
                                    id='client1',
                                    port=60000,
                                    is_client_worker=True)

# send data
x = torch.tensor(6041)
x.send(socket_pipe)
