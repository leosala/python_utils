import socket
import sys
from time import sleep
import struct
import numpy as np

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print sock.fileno()


server_address = ("127.0.0.1", 50000)

data_size = 1000

i = 0
while True:
    try:
        data = np.random.randint(0, 65440, data_size)
        message = struct.pack('Q1000H', i, *data)
        sent = sock.sendto(message, server_address)
        print i, data[0], data[-1]
        i += 1
        sleep(1)
    except KeyboardInterrupt:
        sock.close()
        break
