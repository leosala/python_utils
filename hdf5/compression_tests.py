# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:18:47 2016

@author: sala
"""

import numpy as np
import tables
from contextlib import closing
from time import time
import random
import os
import h5py
import argparse


label = "test"
dataset = "jungfrau/data"
n_tries = 1
data = None
dest_dir = "/tmp/"
size = (400, 400)
n_img = 100
tot_size = size[0] * size[1]
px_n = size[0] * size[1]
zeros_perc = 0

samples = ["orig", "zlib", "lzo", "blosc:lz4", 'blosc:snappy']
#samples = ["orig", "blosc:lz4"]

data = np.random.randint(0, 2**16, size=[100, 1024, 1024])
non_zeros = int((1-zeros_perc)*tot_size)


def create_file(fname, data, complib, complevel):
    FILTERS = None
    if complib != "orig":
        FILTERS = tables.Filters(complib=complib, complevel=complevel)
        with closing(tables.open_file(fname, mode='w', filters=FILTERS)) as hdf:
            hdf.create_carray('/', 'array', obj=data)
    else:
        with closing(tables.open_file(fname, mode='w', )) as hdf:
            hdf.create_carray('/', 'array', obj=data)
            
            
def create_jf_images(data, n_img, zeros_perc, size, mode=0):
    for i in range(0, n_img):
        if mode == 0:
            rand = np.random.random_integers(2000, 45000, size=int(len(x)))
        elif mode == 1:
            rand = np.random.random_integers(2000, 65000, size=int(len(x)))
        elif mode == 2:
            rand1 = np.random.random_integers(2000, 16000, size=int(14 * len(x) / 43))
            rand2 = np.random.random_integers(18000, 32000, size=int(14. * len(x) / 43))
            rand3 = np.random.random_integers(50000, 65000, size=int(15. * len(x) / 43))
            rand = np.random.choice(np.append(rand1, np.append(rand2, rand3)),
                                    int((1 - zeros_perc) * size[0] * size[1]))
        data[i].reshape(tot_size)[x] = rand


def read_file(fname, dset="/array", chunk=-1):
    f = tables.open_file(fname)
    data = f.get_node(dset)
    times = []
    for i in range(data.shape[0]):
        start = time()
        d = data[i][:]
        times.append(time() - start)
    ntimes = np.array(times)
    return [ntimes.mean(), ntimes.std()]


def write_file(fname, data, complib, complevel, chunk=-1):
    FILTERS = None
    times = []
    if complib != "orig":
        FILTERS = tables.Filters(complib=complib, complevel=complevel)
        with closing(tables.open_file(fname, mode='w', filters=FILTERS)) as hdf:
            table = hdf.create_carray('/', 'array', tables.Atom.from_type(data.dtype.name), shape=data.shape)
            for i in range(data.shape[0]):
                start = time()
                table[i] = data[i][:]
                table.flush()
                times.append(time() - start)
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
    return [ntimes.mean(), ntimes.std()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do write / read performance test on HDF5 files and compression')
    parser.add_argument('files', type=str, nargs='+',
                        help='existing HDF5 files (if none, a random one will be created)')
    parser.add_argument('-n', type=int, default=10,
                        help='number of events to analyze (default=10)')

    args = parser.parse_args()
    print(args.files)
    if args.files != []:
        n_tries = len(args.files)

    sizes = {}
    ratios = {}
    times = {}
    reads = {}
    for s in samples:
        sizes[s] = np.empty((n_tries))
        ratios[s] = np.empty((n_tries))
        times[s] = np.empty((n_tries))
        reads[s] = np.empty((2, ))

    for t in range(n_tries):
        if args.files == []:
            x = random.sample(list(range(size[0] * size[1])),
                              int((1 - zeros_perc) * size[0] * size[1]))
            data = np.zeros((args.n, size[0], size[1]), dtype="i2")
            create_jf_images(data, args.n, zeros_perc, size, mode=0)
            zeros_perc = 1 - np.count_nonzero(data[0]) / float(data[0].shape[0] * data[0].shape[1])
        else:
            data = h5py.File(args.files[t])[dataset][:args.n][:]

        time_t = {}

        for s in samples:
            fname = dest_dir + "test_" + s + ".h5"
            start = time()
            create_file(fname, data, s, 5)
            time_t[s] = time() - start

            
            sizes[s][t] = float(os.stat(fname).st_size) / (1000. * 1000.)
            ratios[s][t] = sizes["orig"][t] / sizes[s][t]
            times[s] = write_file(fname, data, s, 5)
            reads[s] = read_file(fname)
            #os.remove(fname)

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
        line += " %.1f +- %.1f |" % (plist[s + "_m"], plist[s + "_s"])
    print(line)

    line = "| WRITE_TIME (ms)|"
    plist = {}
    for s in samples:
        line += " %.2f +- %.2f |" % (100 * times[s][0], 100 * times[s][1])
    print(line)

    line = "| READ_TIME (ms)|"
    plist = {}
    for s in samples:
        line += " %.2f +- %.2f |" % (100 * reads[s][0], 100 * reads[s][1])
    print(line)

    np.savez(label, sizes, ratios, times)
