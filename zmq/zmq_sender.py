from __future__ import division
import zmq
import numpy as np
from time import sleep, time
import argparse
import h5py
import sys

T = 20
N = 1
#SIZES =  (50, 100, 200, 500, 1000, 1500, 2000, 2500)
SIZES = ()

def print_table(results):
    print "| array size | size MB | MB/s | Gbps |"
    for p, v in results.iteritems():
        speed = np.array(v[2], ) / np.array(v[0], )
        print "|", p, " | %.2f | %.1f +- %.1f | %.1f +- %.1f |" % (v[1][0], (speed).mean(), (speed).std(),  (8 * speed / 1000.).mean(), (8 * speed / 1000.).std())
    print ""


def send_array(socket, A, flags=0, copy=False, track=False):
    """send a numpy array with metadata"""
    md = dict(
        htype=["array-1.0", ],
        type=str(A.dtype),
        shape=A.shape,
    )
    #print md
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)


def recv_array(socket, flags=0, copy=False, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    #print md
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = buffer(msg)
    A = np.frombuffer(buf, dtype=md['type'])
    return A.reshape(md['shape'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starts a small test client receiving multipart JSON+data ZQM messages')
    parser.add_argument('ip', type=str, 
                        help='ip connecting to, including protocol and port, e.g.: tcp://127.0.0.1:8888')
    parser.add_argument('--type', type=str, choices=["PUB", "SUB", "PUSH", "PULL"], default="SUB",
                        help='ZMQ connection type, default: SUB')
    parser.add_argument('--mode', type=str, choices=["BIND", "CONNECT"], default="CONNECT",
                        help='ZMQ connection mode, default: CONNECT')
    parser.add_argument('--sizes', type=int, default=(1000,), nargs='+', )

    args = parser.parse_args()

    SIZES = []
    print args.sizes
        

    ctx = zmq.Context()
    
    skt_type = zmq.SUB
    if args.type != "SUB":
        if args.type == "PUB":
            skt_type = zmq.PUB
        elif args.type == "PUSH":
            skt_type = zmq.PUSH
        elif args.type == "PULL":
            skt_type = zmq.PULL
    skt = ctx.socket(skt_type)
    if args.type == "SUB":
        skt.setsockopt(zmq.SUBSCRIBE, "")

    if args.mode == "CONNECT":
        skt.connect(args.ip)
    else:
        skt.bind(args.ip)


    results = {}
    for n in range(N):
        t0 = time()
        for i in args.sizes:
            idx = 0
            t0 = time()
            data = np.ones((i, i), dtype=int)
            pshape = data.shape
            size = data.nbytes / (1000. * 1000)
            while True:
                try:
                    #print 
                    #data = np.ones((i, 1000))
                    send_array(skt, data)

                    #print data
                    idx += 1
                    if time() - t0 > T:
                        t = time() - t0
                        if pshape not in results.keys():
                            results[pshape] = [[], [], []]
                        results[pshape][0].append(t)
                        results[pshape][1].append(size)
                        results[pshape][2].append(float(idx * size))
                        print data.shape, "%.2f %f %.2f MB/s (%.2f MiB/s, %.2fGbps)" % (size, t, float(idx) * size / t, float(idx) * size*1000*1000/(1024*1024) / t, 8 * float(idx) * size / t/1000.)
                        print_table(results)
                        
                        break
                except KeyboardInterrupt:
                    print "CTRL-C pressed, exiting"
                    break


    skt.close()
    sys.exit()
