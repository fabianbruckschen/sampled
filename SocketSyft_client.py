#!/usr/bin/env python
# coding: utf-8

# # Checking Socket connection via pysyft module (Client)

# ## Preparations
# modules
import syft as sy
import torch;hook = sy.TorchHook(torch)  # hook into pytorch
import socket
from syft.workers import WebsocketClientWorker
from syft.workers import WebsocketServerWorker

# options
hostname = 'ip-172-31-46-89'  # DataNode3 (Fabi)
port = 60387

# create client
socket_pipe = WebsocketClientWorker(hook=hook,
                                    host=hostname,
                                    id='client2',
                                    port=port,
                                    is_client_worker=False)

# send data
socket_pipe.ws.connect(socket_pipe.uri)
x = torch.tensor([12, 77, 6041, 555])
ptr_x = x.send(socket_pipe)
# y = torch.ones(60)
# y.send(socket_pipe)
