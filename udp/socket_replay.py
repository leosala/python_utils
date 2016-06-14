from __future__ import print_function, division

import socket
from time import sleep
import struct
import argparse
import sys
import numpy as np


def run_replay(filename, ip, port, sleep_time=0.01):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(s.connect((ip, int(port))))
    c = 0
    with open(filename, 'rb') as f:
        for data in iter(lambda: f.read(6080), ''):
        #for data in f.readlines():
            c += 1
            try:
                s.sendto(data, (ip, int(port)))
                print("sent", c) 
                sleep(sleep_time)
            except:
                print(sys.exc_info()[1])
                s.close()
                return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starts a small test client sending packed integers to a UDP socket')
    parser.add_argument('filename', type=str, nargs=1,
                        help='input filename')
    parser.add_argument('ip', type=str, nargs=1,
                        help='ip connecting to')
    parser.add_argument('port', type=str, nargs=1,
                        help='port connecting to')

    args = parser.parse_args()

    run_replay(args.filename[0], args.ip[0], args.port[0])
