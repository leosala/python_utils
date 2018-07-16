
import zmq
import numpy as np
from time import sleep, time
import argparse
import h5py
import sys


def recv_array(socket, flags=0, copy=False, track=True):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    #print md
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = np.frombuffer(buf, dtype=md['type'])
    return md, A.reshape(md['shape'])


def print_table(results):
    print("")
    print("Throughput metrics:\n")
    print("| array size | size MB | MB/s | Gbps |")
    for p, v in results.items():
        speed = np.array(v[2], ) / np.array(v[0], )
        print("|", p, " | %.2f | %.1f +- %.1f | %.1f +- %.1f |" % (v[1][0], (speed).mean(), (speed).std(), (8 * speed / 1000.).mean(), (8 * speed / 1000.).std()))
    print("")


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
    parser.add_argument('--verbose', '-v', type=bool, default=False,
                        help='verbose mode')
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

    dst = None
    if args.output is not None:
        outf = h5py.File(args.output, "w")

    idx = 0
    size = None
    psize = None
    t0 = time()

    results = {}
    while True:
        try:
            md, data = recv_array(skt)
            if args.verbose:
                print(data.shape)
            idx += 1
            size = data.nbytes / (1000. * 1000.)
            if psize is None:
                psize = size
                pshape = data.shape

            if size != psize or len(data.shape) == 1:
                t = time() - t0
                if pshape not in list(results.keys()):
                    results[pshape] = [[], [], []]
                results[pshape][0].append(t)
                results[pshape][1].append(psize)
                results[pshape][2].append(float(idx * psize))

                idx = 0
                t0 = time()
                psize = size
                pshape = data.shape
                print_table(results)

            if args.output is None:
                continue
            if dst is None:
                dst = outf.create_dataset("/data", shape=(1000, ) + data.shape, dtype=data.dtype)
            #dst[idx] = data
            psize = size
        except KeyboardInterrupt:
            print("CTRL-C pressed, exiting")
            t = time() - t0
            if pshape not in list(results.keys()):
                results[pshape] = [[], [], []]
            results[pshape][0].append(t)
            results[pshape][1].append(psize)
            results[pshape][2].append(float(idx * psize))
            print_table(results)

            if dst is not None:
                outf.close()
            sys.exit()
