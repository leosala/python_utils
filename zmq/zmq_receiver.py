import zmq
import numpy as np
from time import sleep, time
import argparse
<<<<<<< HEAD
<<<<<<< HEAD
import h5py
import sys
=======
>>>>>>> 4c02664... wip
=======
import h5py
import sys
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07


def send_array(socket, A, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(
        htype=["array-1.0", ],
        type=str(A.dtype),
        shape=A.shape,
    )
    print md
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)


def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
<<<<<<< HEAD
<<<<<<< HEAD
    print md
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = buffer(msg)
    A = np.frombuffer(buf, dtype=md['type'])
=======
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = buffer(msg)
    A = np.frombuffer(buf, dtype=md['dtype'])
>>>>>>> 4c02664... wip
=======
    print md
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = buffer(msg)
    A = np.frombuffer(buf, dtype=md['type'])
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07
    return A.reshape(md['shape'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starts a small test client receiving multipart JSON+data ZQM messages')
    parser.add_argument('ip', type=str, 
                        help='ip connecting to, including protocol and port, e.g.: tcp://127.0.0.1:8888')
    parser.add_argument('--type', type=str, choices=["PUB", "SUB", "PUSH", "PULL"], default="SUB",
                        help='ZMQ connection type, default: SUB')
    parser.add_argument('--mode', type=str, choices=["BIND", "CONNECT"], default="CONNECT",
                        help='ZMQ connection mode, default: CONNECT')
<<<<<<< HEAD
<<<<<<< HEAD
    parser.add_argument('--output', type=str, default=None,
                        help='Output file (HDF5)')
=======
>>>>>>> 4c02664... wip
=======
    parser.add_argument('--output', type=str, default=None,
                        help='Output file (HDF5)')
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07

    args = parser.parse_args()

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

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07
    if args.output is not None:
        outf = h5py.File(args.output, "w")
        dst = None

    idx = 0
<<<<<<< HEAD
    while True:
        try:
            data = recv_array(skt)

            print data
            if args.output is None:
                continue
            if dst is None:
                dst = outf.create_dataset("/data", shape=(1000, ) + data.shape, dtype=data.dtype)
            dst[idx] = data
            idx += 1
        except KeyboardInterrupt:
            print "CTRL-C pressed, exiting"
            if dst is not None:
                outf.close()
            sys.exit()
=======
    while True:
        md = skt.recv_json()
        print md
        data = skt.recv()
>>>>>>> 4c02664... wip
=======
    while True:
        try:
            data = recv_array(skt)

            print data
            if args.output is None:
                continue
            if dst is None:
                dst = outf.create_dataset("/data", shape=(1000, ) + data.shape, dtype=data.dtype)
            dst[idx] = data
            idx += 1
        except KeyboardInterrupt:
            print "CTRL-C pressed, exiting"
            if dst is not None:
                outf.close()
            sys.exit()
>>>>>>> 93249f67847874c04104bd9cafb238e9a6d13b07
