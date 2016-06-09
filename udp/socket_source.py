from __future__ import print_function, division

import socket
from time import sleep
import struct
import binascii
import argparse


def run_source(ip, port):
    """
    Runs a small UDP packets source, sending integers to a UDP socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(s.connect((ip, int(port))))

    i = 0
    while True:
        try:
            #data, sender = s.recv_from(1024)
            #p_data = binascii.hexlify(struct.pack('i', i))
            p_data = struct.pack('i', i)
            s.sendto(p_data, (ip, int(port)))
            i += 1
            sleep(.1)

        except:
            s.close()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starts a small test client sending packed integers to a UDP socket')
    parser.add_argument('ip', type=str, nargs=1,
                        help='ip connecting to')
    parser.add_argument('port', type=str, nargs=1,
                        help='port connecting to')

    args = parser.parse_args()

    run_source(args.ip[0], args.port[0])
