import socket
import struct
import os
import ctypes

_mod = ctypes.cdll.LoadLibrary(os.getcwd() + "/libudpreceiver.so")
gm = _mod.get_message
gm.argtypes = (ctypes.c_int, )
gm.restype = ctypes.c_int


UDP_IP = "127.0.0.1"
UDP_PORT = 50000


sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

print sock.fileno()
i = 0 
while True:
    try:
        r = gm(sock.fileno())
        if r != -1:
            print r
        #data, addr = sock.recvfrom(4096)  # buffer size is 1024 bytes
        #i = struct.unpack('L', data[:8])
        #data_c = struct.unpack('1000i', data[8:])
        #print "received message:", i, data_c[0], data_c[-1]
        i+=1
    except KeyboardInterrupt:
        sock.close()
        break
