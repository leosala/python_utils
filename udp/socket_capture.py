from __future__ import print_function, division
import argparse
import socket
import sys


def run_server(ip, port, outfile):
    outf = open(outfile, 'wb')
    print("Opened output file %s" % outfile)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2000 * 1024 * 1024)

    print("Starting server on %s:%s" % (ip, port))
    print(s.bind((ip, int(port))))
    #s.listen(0)
    #clientsocket, address = s.accept()
    #print("connected to", address)

    while True:
        try:
            data, sender = s.recvfrom(2000 * 1024 * 1024)
            #print("Got data from %s, size %d" % (sender, len(data)))
            
            if len(data) == 0:
                print("No more data, closing")
                raise RuntimeError

            outf.write(data)
        except KeyboardInterrupt:
            s.close()
            outf.close()
            break
        except:
            print(sys.exc_info()[1])
            s.close()
            outf.close()
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Opens a small server listening to a socket and dumping data in a file')
    parser.add_argument('ip', type=str, nargs=1,
                        help='ip listening to')
    parser.add_argument('port', type=str, nargs=1,
                        help='port listening to')
    parser.add_argument('-o', '--outfile', action='store',
                        default=None,
                        required=False,
                        help='output file. Defaults to <ip>_<port>.dat')

    args = parser.parse_args()

    if args.outfile is None:
        args.outfile = args.ip[0] + "_" + args.port[0] + ".dat"

    run_server(args.ip[0], args.port[0], args.outfile)
