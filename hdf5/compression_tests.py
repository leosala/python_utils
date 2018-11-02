# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:18:47 2016

@author: sala
"""

import numpy as np
import tables
from contextlib import closing
from time import time, sleep
import random
import os
import h5py
import argparse
try:
    import jungfrau_utils as ju
except:
    print("Cannot import jungfrau_utils")
    print(sys.exc_info()[1])

import scipy.stats
import pickle
from pprint import pprint

#gain_file = "/sf/alvra/config/jungfrau/jungfrau_4p5_gaincorrections_v0.h5"
gain_file = "/sf/alvra/config/jungfrau/gainMaps/JF06T32V01/gains.h5"
#pede_file = "/sf/alvra/data/p17245/res/pedestal_20180703_1403_res.h5"
pede_file = "/sf/alvra/data/p17502/res/JF_pedestals/pedestal_20180813_0704.JF06T32V01.res.h5"

#label = "test"
#dataset = "data/JF4.5M/data"
n_tries = 1
data = None
#dest_dir = "/tmp/"
size = (400, 400)
#n_img = 100
tot_size = size[0] * size[1]
px_n = size[0] * size[1]
zeros_perc = 0

samples = ["orig", "zlib_5", "lzo", "blosc:lz4", "blosc:lz4_9", "blosc:lz4hc", 'blosc:snappy']

data = np.random.randint(0, 2**16, size=[100, 1024, 1024])
non_zeros = int((1 - zeros_perc) * tot_size)


def create_file(fname, data, complib, complevel, bitshuffle=False):
    FILTERS = None
    if complib != "orig":
        if complib.find("blosc") == -1:
            bitshuffle = False
            print("Bitshuffle only enabled for BLOSC")
        FILTERS = tables.Filters(complib=complib, complevel=complevel, bitshuffle=bitshuffle)
        with closing(tables.open_file(fname, mode='w', filters=FILTERS)) as hdf:
            hdf.create_carray('/', 'array', obj=data)
    else:
        with closing(tables.open_file(fname, mode='w', )) as hdf:
            hdf.create_carray('/', 'array', obj=data)
            

def read_file(fname, dset="/array", chunk=-1):
    f = tables.open_file(fname, "r")
    data = f.get_node(dset)
    times = []
    for i in range(data.shape[0]):
        start = time()
        d = data[i][:]
        times.append(time() - start)
    ntimes = np.array(times)
    f.close()
    return [ntimes.sum(), ntimes.mean(), ntimes.std()]


def write_file(fname, data, complib, complevel, bitshuffle=False, chunk=-1):
    
    FILTERS = None
    times = []

    if complib.find("_") != -1:
        print(complib.split("_"))
        complib, complevel = complib.split("_")
        complevel = int(complevel)
    if complib != "orig":
        if complib.find("blosc") == -1 and bitshuffle:
            bitshuffle = False
            print("Bitshuffle only enabled for BLOSC")
        FILTERS = tables.Filters(complib=complib, complevel=complevel, bitshuffle=bitshuffle)
        with closing(tables.open_file(fname, mode='w', filters=FILTERS)) as hdf:
            table = hdf.create_carray('/', 'array', tables.Atom.from_type(data.dtype.name), shape=data.shape)
            for i in range(data.shape[0]):
                start = time()
                table[i] = data[i][:]
                table.flush()
                times.append(time() - start)
                #print(time() - start)
        hdf.close()
    else:
        with closing(tables.open_file(fname, mode='w', )) as hdf:
            table = hdf.create_carray('/', 'array', tables.Atom.from_type(data.dtype.name), shape=data.shape)
            for i in range(data.shape[0]):
                start = time()
                table[i] = data[i][:]
                table.flush()
                times.append(time() - start)
        hdf.close()
    ntimes = np.array(times)
    print([ntimes.sum(), ntimes.mean(), ntimes.std()])
    return [ntimes.sum(), ntimes.mean(), ntimes.std()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do write / read performance test on HDF5 files and compression')
    parser.add_argument('files', type=str, nargs='+',
                        help='existing HDF5 files (if none, a random one will be created)')
    parser.add_argument('-n', type=int, default=100,
                        help='number of events to analyze (default=100)')
    parser.add_argument('--outdir', '-o', type=str, default="/tmp",
                        help='where to write temporary files')
    parser.add_argument('--convert', '-c', action="store_true",
                        help="create also the converted file")
    parser.add_argument('--zerosuppress', '-z', type=float, default=-99,
                        help="Put to zero values smaller than this. Onlu apply if convert is enabled")
    parser.add_argument('--label', '-l', type=str, default="test",
                        help='label for output file')
    parser.add_argument('--bitshuffle', '-b', action="store_true",
                        help="create also the converted file")
    parser.add_argument('--compression_level', type=int, help="compression level, when applicable", default=5)
    parser.add_argument('--dataset', '-d', type=str, help="Dataset name to be read", default="test")
    parser.add_argument('--keep', '-k', action="store_true", help="keep temporary files", default=False)

    args = parser.parse_args()
    label = args.label
    if args.convert:
        label += "-conv"
    if args.zerosuppress != -99:
        label += "-z{:.2f}".format(args.zerosuppress)
    if args.bitshuffle:
        label += "-bitshuffle"
        
    if args.files != []:
        n_tries = len(args.files)

    print(args)
    #corrections_file = ""
    if args.convert:
        gf = h5py.File(gain_file, "r")
        G = gf["gains"][:]
        cf = h5py.File(pede_file, "r")
        P = cf["gains"][:]
        
    sizes = {}
    ratios = {}
    times = {}
    reads = {}

    for s in samples:
        sizes[s] = np.zeros((n_tries, 3))
        ratios[s] = np.zeros((n_tries, 3))
        times[s] = np.zeros((n_tries, 3))
        reads[s] = np.zeros((n_tries, 3))

    for t in range(n_tries):
        if args.files == []:
            x = random.sample(list(range(size[0] * size[1])),
                              int((1 - zeros_perc) * size[0] * size[1]))
            data = np.zeros((args.n, size[0], size[1]), dtype="i2")
            create_jf_images(data, args.n, zeros_perc, size, mode=0)
            zeros_perc = 1 - np.count_nonzero(data[0]) / float(data[0].shape[0] * data[0].shape[1])
        else:
            print("Opening file", args.files[t])
            data = h5py.File(args.files[t], "r")[args.dataset][:args.n][:]
            if args.convert:
                data2 = np.ndarray(shape=data.shape, dtype=np.float32)
                for i, d in enumerate(data):
                    temp = ju.apply_gain_pede(d, G=G, P=P)
                    if args.zerosuppress != -99:
                        temp[temp < args.zerosuppress] = 0
			
                    data2[i][:] = temp[:]

        time_t = {}

        for s in samples:
            print(s, t)
            fname = os.path.join(args.outdir, "test_" + s + label +".h5").replace(":", "_")
            
            if args.convert:
                print("%d %f" % (data[0,0,0], data2[0,0,0]))
                times[s][t] = write_file(fname, data2, s, args.compression_level, args.bitshuffle)
            else:
                times[s][t] = write_file(fname, data, s, args.compression_level, args.bitshuffle)
            reads[s][t] = read_file(fname)
            sizes[s][t] = float(os.stat(fname).st_size) / (1000. * 1000.)
            print(fname, os.stat(fname).st_size)
            ratios[s][t] = sizes[s][t] / sizes["orig"][t]

            print("Removing ", fname)
            if not args.keep:
                os.remove(fname)
            #sleep(2)
        print(sizes)
    #print(times)
    h = "| Metric |"
    for s in samples:
        h += " %s |" % s

    print(h)

    line = "| SIZE |"
    plist = {}
    for s in samples:
        plist[s + "_m"] = sizes[s].mean()
        plist[s + "_s"] = sizes[s].std()
        line += " %.1f +- %.1f |" % (plist[s + "_m"], plist[s + "_s"])
    print(line)

    line = "| SIZE_RATIO |"
    plist = {}
    for s in samples:
        plist[s + "_m"] = ratios[s].mean()
        plist[s + "_s"] = ratios[s].std()
        line += " %.2f +- %.2f |" % (plist[s + "_m"], plist[s + "_s"])
    print(line)

#    line = "| WRITE_TIME (ms)|"
#    plist = {}
#    for s in samples:
#        line += " %.2f +- %.2f |" % (100 * times[s][0], 100 * times[s][1])
#    print(line)
#
#    line = "| READ_TIME (ms)|"
#    plist = {}
#    for s in samples:
#        line += " %.2f +- %.2f |" % (100 * reads[s][0], 100 * reads[s][1])
#    print(line)

    for s in samples:
        write_ratios = [x[0] / times['orig'][i][0] for i, x in enumerate(times[s])]

    outf = open(label + ".pkl", "wb")
    pickle.dump({"files":args.files, "sizes":sizes, "writes":times, "reads":reads}, outf)


    print(sizes)
    pprint(times)
