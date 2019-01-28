"""
Basic compression tests on HDF5 using a mixture of h5py and pytables

Heavily focused on SwissFEL data format, but should be easily modifiab;e
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


### Gain / pede files - needed if want to test calibrated data
# TODO pass this as arguments
gain_file = "/sf/alvra/config/jungfrau/gainMaps/JF02T09V01/gains.h5"
#gain_file = "/sf/alvra/config/jungfrau/gainMaps/JF06T32V01/gains.h5"
pede_file = "/sf/alvra/data/p17245/res/pedestal_20180703_1403_res.h5"
#pede_file = "/sf/alvra/data/p17502/res/JF_pedestals/pedestal_20180813_0704.JF06T32V01.res.h5"

### Parameters for fake data production
n_tries = 1
data = None
size = (400, 400)
tot_size = size[0] * size[1]
px_n = size[0] * size[1]
zeros_perc = 0

### Compression algos to be tested: [library:]algo_compressionfactor
#samples = ["orig", "zlib_5", "lzo", "blosc:lz4", "blosc:lz4_9", "blosc:lz4hc", 'blosc:snappy']
samples = ["orig", "zlib_5", "blosc:lz4", 'blosc:snappy']

data = np.random.randint(0, 2**16, size=[100, 1024, 1024])
non_zeros = int((1 - zeros_perc) * tot_size)


def round_half_up(n, decimals=0):
    """Rounds a number using the half-up method. Taken
    from: https://realpython.com/python-rounding/#applications-and-best-practices

    
    Parameters
    ----------
    n : float
        number to be rounded up
    decimals : int, optional
        number of decimals to keep, with negative values going into the
        powers of 10 (the default is 0, which means round to integer)
    
    Returns
    -------
    float
        the rounded up number
    """

    multiplier = 10 ** decimals
    # Replace math.floor with np.floor
    return np.floor(n * multiplier + 0.5) / multiplier


def create_file(fname, data, complib, complevel, bitshuffle=False):
    """[summary]
    
    Parameters
    ----------
    fname : str
        name of the file to be created
    data : NDarray
        Numpy array containing the data to be written
    complib : str
        compression lib to be used, in the form [library:]algo. If None, do not compress
        E.g. blosc:lz4, gzip
    complevel : int
        Compression level
    bitshuffle : bool, optional
        Enable bitshuffle for the compression (the default is False, which means disable)
    
    """

    FILTERS = None

    if complib is not None:
        if complib.find("blosc") == -1:
            bitshuffle = False
            print("Bitshuffle only enabled for BLOSC")
        FILTERS = tables.Filters(complib=complib, complevel=complevel, bitshuffle=bitshuffle)
        with closing(tables.open_file(fname, mode='w', filters=FILTERS)) as hdf:
            hdf.create_carray('/', 'array', obj=data)
    else:
        with closing(tables.open_file(fname, mode='w', )) as hdf:
            hdf.create_carray('/', 'array', obj=data)
            

def read_file(fname, dset="/array"):
    """Read data file, and return read time statistics
    
    Parameters
    ----------
    fname : str
        File name
    dset : str, optional
        Name of the dataset to be written (the default is "/array")
    
    Returns
    -------
    list
        List containing the sum of all reads, the mean and the standard deviation
    """

    f = tables.open_file(fname, "r")
    data = f.get_node(dset)
    times = []
    for i in range(data.shape[0]):
        start = time()
        _ = data[i][:]
        times.append(time() - start)
    ntimes = np.array(times)
    f.close()
    return [ntimes.sum(), ntimes.mean(), ntimes.std()]


def write_file(fname, data, complib, complevel, bitshuffle=False):
    """Write an HDF5 file using pytables
    
    Parameters
    ----------
    fname : str
        name of the file to be created
    data : NDarray
        Numpy array containing the data to be written
    complib : str
        compression lib to be used, in the form [library:]algo. If "orig", do not compress
        E.g. blosc:lz4, gzip
    complevel : int
        Compression level
    bitshuffle : bool, optional
        Enable bitshuffle for the compression (the default is False, which means disable)
        
    Returns
    -------
    list
        List containing the sum of all reads, the mean and the standard deviation
    """

    FILTERS = None
    times = []

    if complib.find("_") != -1:
        complib, complevel = complib.split("_")
        complevel = int(complevel)
    
    if complib != "orig":
        if complib.find("blosc") == -1 and bitshuffle:
            bitshuffle = False
            print("Bitshuffle only enabled for BLOSC")
        FILTERS = tables.Filters(complib=complib, complevel=complevel, bitshuffle=bitshuffle)
    
        with closing(tables.open_file(fname, mode='w', filters=FILTERS)) as f:
            table = f.create_carray('/', 'array', tables.Atom.from_type(data.dtype.name), shape=data.shape)
    
            for i in range(data.shape[0]):
                start = time()
                table[i] = data[i][:]
                table.flush()
                times.append(time() - start)
        
    else:
        with closing(tables.open_file(fname, mode='w', )) as f:
            table = f.create_carray('/', 'array', tables.Atom.from_type(data.dtype.name), shape=data.shape)
            for i in range(data.shape[0]):
                start = time()
                table[i] = data[i][:]
                table.flush()
                times.append(time() - start)

    ntimes = np.array(times)
    print([ntimes.sum(), ntimes.mean(), ntimes.std()])
    return [ntimes.sum(), ntimes.mean(), ntimes.std()]


def create_jf_images(data, n_img, zeros_perc, size, mode=0):	
    """Create a randomly generate image.
    
    Parameters
    ----------
    data : NDarray
        output array
    n_img : int
        Number of images to be created
    zeros_perc : float
        Percentage of zeros in the image, range 0-1
    size : list
        shape of the array
    mode : int, optional
        Generation mode. 0 means in the [2000, 45000] range, 1 in [2000, 65000],
        2 in the [2000, 16000] + [18000, 32000] + [50000, 65000], equally probable ranges
        (the default is 0)
    
    """

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


if __name__ == "__main__":
    # CLI arguments
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
    parser.add_argument('--round', '-r', type=int, help="Round half-up", default=-1)
    parser.add_argument('--toint', '-i', action="store_true", help="Store converted data to in32",)
    parser.add_argument('--modulo', '-m', type=int, help="Store data as data - (data % [modulo])", default="1")
    parser.add_argument('--remove_lsb', action="store_true", help="set the LSB to 0")
    
    args = parser.parse_args()

    # Creation of output file names based on options
    label = args.label
    if args.convert:
        label += "-conv"
    if args.zerosuppress != -99:
        label += "-z{:.2f}".format(args.zerosuppress)
    if args.bitshuffle:
        label += "-bitshuffle"
    if args.round != -1:
        label += "-round_{}".format(args.round)
    if args.modulo != 1:
        label += "-mod_{}".format(args.modulo)
    if args.remove_lsb:
        label += "-remove_lsb"

    histos = []


    # Get the number of loops from file list, if available        
    if args.files != []:
        n_tries = len(args.files)

    # Set up necessary conversion data, if required
    if args.convert:
        gf = h5py.File(gain_file, "r")
        G = gf["gains"][:]
        cf = h5py.File(pede_file, "r")
        P = cf["gains"][:]

    # Initialize counters. Each counter contains 3 values: sum, mean, std
    sizes = {}
    ratios = {}
    times = {}
    reads = {}


    for s in samples:
        sizes[s] = np.zeros((n_tries, 3))
        ratios[s] = np.zeros((n_tries, 3))
        times[s] = np.zeros((n_tries, 3))
        reads[s] = np.zeros((n_tries, 3))

    # Start loop over files, or tries when random data is generated
    for t in range(n_tries):
        data2 = None

        # Create random data file, if no input files are available NOT TESTED
        if args.files == []:
            x = random.sample(list(range(size[0] * size[1])),
                              int((1 - zeros_perc) * size[0] * size[1]))
            data = np.zeros((args.n, size[0], size[1]), dtype=np.uint16)
            create_jf_images(data, args.n, zeros_perc, size, mode=0)
            zeros_perc = 1 - np.count_nonzero(data[0]) / float(data[0].shape[0] * data[0].shape[1])
        else:
            print("Opening file", args.files[t])
            data = h5py.File(args.files[t], "r")[args.dataset][:args.n][:]
            
            if args.remove_lsb:
                data = np.bitwise_and(data, ~1).astype(np.uint16)  # if operate conversion

            if args.convert:
                if args.toint:
                    data2 = np.ndarray(shape=data.shape, dtype=np.int32)
                else:
                    data2 = np.ndarray(shape=data.shape, dtype=np.float32)

                for i, d in enumerate(data):
                    temp = ju.apply_gain_pede(d, G=G, P=P)

                    if args.zerosuppress != -99:
                        temp[temp < args.zerosuppress] = 0
                    
                    if args.round != -1:
                        data2[i][:] = round_half_up(temp[:], args.round)
                    elif args.toint:
                        temp[:] *= 1000
                        if args.modulo != 0:
                            data2[i][:] = temp[:] - (temp[:] % args.modulo)
                        else:
                            data2[i][:] = temp[:]
                    else:
                        data2[i][:] = temp[:] 
            elif args.round != -1:
                print("Rounding")
                data = round_half_up(data, args.round)
                
        # from -10 kEv to 1000 keV
        bins = np.arange(-1e4, 1e6, 10)
        if data2 is not None:
            histos.append(np.histogram(np.clip(data2, bins[0], bins[-1]), bins=bins))
        else:
            histos.append(np.histogram(data, bins=np.arange(data.min(), data.max(), 10)))
            
        time_t = {}


        # execute test for each sample / compression
        for s in samples:
            fname = os.path.join(args.outdir, "test_" + s + label +".h5").replace(":", "_")
            
            if args.convert:
                times[s][t] = write_file(fname, data2, s, args.compression_level, args.bitshuffle)
            else:
                times[s][t] = write_file(fname, data, s, args.compression_level, args.bitshuffle)

            reads[s][t] = read_file(fname)
            sizes[s][t] = float(os.stat(fname).st_size) / (1000. * 1000.)
            ratios[s][t] = sizes[s][t] / sizes["orig"][t]

            if not args.keep:
                print("Removing ", fname)
                os.remove(fname)

        print("Sizes {}: {}".format(s, sizes))

    print("Saving histograms as {}".format(label + "-histo.npz"))
    np.savez_compressed(label + "-histo.npz", histos)


    # Metrics printing
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

    for s in samples:
        write_ratios = [x[0] / times['orig'][i][0] for i, x in enumerate(times[s])]

    outf = open(label + ".pkl", "wb")
    pickle.dump({"files":args.files, "sizes":sizes, "writes":times, "reads":reads}, outf)

    print(sizes)
    pprint(times)
