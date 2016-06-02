from __future__ import print_function, division

import socket
from time import sleep
import struct
import argparse
import sys


def run_replay(filename, ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(s.connect((ip, int(port))))

    with open(filename, 'rb') as f:
        for data in iter(lambda: f.read(4), ''):
            print(data)
            print(struct.unpack('i', data))
            try:
                s.sendto(data, (ip, int(port)))
                sleep(.1)

            except:
                print(sys.exc_info()[1])
                s.close()
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starts a small test client sending packed integers to a UDP socket')
    parser.add_argument('ip', type=str, nargs=1,
                        help='ip connecting to')
    parser.add_argument('port', type=str, nargs=1,
                        help='port connecting to')

    args = parser.parse_args()

    run_client(args.ip[0], args.port[0])
