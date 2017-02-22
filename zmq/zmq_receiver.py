import zmq
import numpy as np
from time import sleep, time
import argparse
import h5py
import sys


def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    print md
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = buffer(msg)
    A = np.frombuffer(buf, dtype=md['type'])
    return md, A.reshape(md['shape'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starts a small test client receiving multipart JSON+data ZQM messages')
    parser.add_argument('ip', type=str, 
                        help='ip connecting to, including protocol and port, e.g.: tcp://127.0.0.1:8888')
    parser.add_argument('--type', type=str, choices=["PUB", "SUB", "PUSH", "PULL"], default="SUB",
                        help='ZMQ connection type, default: SUB')
    parser.add_argument('--mode', type=str, choices=["BIND", "CONNECT"], default="CONNECT",
                        help='ZMQ connection mode, default: CONNECT')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file (HDF5)')
    parser.add_argument('--other_fields', type=str, default="",
                        help="Additional datasets to be created from fields in the json header")
    parser.add_argument('--frames', type=int, required=True,
                        help="Number of frames to write")
    args = parser.parse_args()

    args.other_fields = args.other_fields.split(",")
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

    if args.output is not None:
        outf = h5py.File(args.output, "w")
        dst = None

    idx = 0
    dst_md = {}
    while idx < args.frames:
        try:
            md, data = recv_array(skt)
            
            if args.output is None:
                continue
            if dst is None:
                dst = outf.create_dataset("/data", shape=(args.frames, ) + data.shape, dtype=data.dtype)
                for f in args.other_fields:
                    dst_md[f] = outf.create_dataset(f, shape=(args.frames, ), dtype=md[f].__class__)
                        
            dst[idx] = data
            for f in args.other_fields:
                dst_md[f][idx] = md[f]
            idx += 1
        except KeyboardInterrupt:
            print "CTRL-C pressed, exiting"
            break
        
    if dst is not None:
        print "closing file"
        outf.close()
        print "closed"
        sys.exit()

    print("exit!")
