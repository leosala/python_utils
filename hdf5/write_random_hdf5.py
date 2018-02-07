import numpy as np
import argparse
import h5py


def create_file(filename, size, datasetname, kind):
    f = h5py.File(filename, "w")
    dst = f.create_dataset(datasetname, shape=size, dtype=np.int64)

    for i in range(size[0]):
        if kind == "sequential":
            image = i * np.ones(size[1:], dtype=np.int64)
        else:
            image = np.random.randint(2 ** 32, size=size[1:])
        dst[i] = image
    f.close()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Writes test HDF5 files. Example:

    python write_random_hdf5.py test.h5 -s 20 100 100 -k random
""")
    parser.add_argument('filename', type=str, 
                        help='output file name, e.g. test.h5', )
    parser.add_argument('--kind', '-k', type=str, choices=["random", "sequential"], default="sequential",
                        help='type of data to be created. At the moment, only random and sequential (aka every image is a made up of a single integer, in a sequential way), default: sequential')
    parser.add_argument('--datasetname', '-n', type=str, default="data",
                        help='Dataset name, default: data')
    parser.add_argument('--size', '-s', type=int, nargs="+", default=[10, 100, 100],
                        help='Dataset size, where the first integer is to be understood as the number of items')

    args = parser.parse_args()

    create_file(args.filename, args.size, args.datasetname, args.kind)
