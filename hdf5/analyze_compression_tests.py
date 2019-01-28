import pickle
import numpy as np
import os
from math import sqrt
import matplotlib.pyplot as plt

labels = {"conv": "corrected", }


def create_label(fname, default="uncorrected"):
    if fname.find("-") == -1:
        return default
    label = '-'.join('.'.join(os.path.basename(fname).split(".")[:-1]).split("-")[1:])
    return label


def plot_histo(fname):
    data = np.load(fname)['arr_0']
    bins = data[0][1]
    values = data.sum(axis=0)[0]

    plt.figure()
    plt.bar(bins[:-1], values, width=bins[1] - bins[0], )
    plt.semilogy()
    plt.show()


def print_compr_report(fnames, labels=[], plot=False):
    if isinstance(fnames, str):
        fnames = [fnames, ]

    label = ""
    size_t = ""
    write_t = ""
    read_t = ""
    sizer_t = ""

    for i, fname in enumerate(sorted(fnames)):
        f = open(fname, "rb")
        d_unc = pickle.load(f)
        if labels != []:
            label = labels[i]
        else:
            label = create_label(fname)
        label = label.replace("_", " ")
        if i == 0:
            header = ' | ' + ' | '.join([compr for compr in d_unc["sizes"].keys()] ) + " |\n|----\n"
            size_t += '| size ' + header


        size_t += '| *' + label + '* |' + ' | '.join(["{:.0f} +- {:.0f}".format(np.mean(d_unc["sizes"][compr][:,0]), np.std(d_unc["sizes"][compr][:,0])) for compr in d_unc["sizes"].keys()]) + "|\n"
        #for compr in d_unc["sizes"].keys():
        #    print(compr, np.mean(d_unc["sizes"][compr][:,0] / d_unc["sizes"]["orig"][:,0]))

        if i == 0:
            write_t += '| write time ratio ' + header

        w = d_unc["writes"]
        write_t += '| *' + label + '* |' + ' | '.join(["{:.2f} +- {:.2f}".format(
            np.mean(d_unc["writes"][compr][:,0] / d_unc["writes"]["orig"][:,0]),
            sqrt(w[compr][:, 0].std() ** 2 / w[compr][:, 0].mean() ** 2 ))
                                                       for compr in d_unc["writes"].keys()
        ]) + "|\n"


        if i == 0:
            read_t += '| read time ratio ' + header
        read_t += '| *' + label + '* |' + ' | '.join(["{:.2f} +- {:.2f}".format(
            np.mean(d_unc["reads"][compr][:,0] / d_unc["reads"]["orig"][:,0]),
            sqrt(w[compr][:, 0].std() ** 2 / w[compr][:, 0].mean() ** 2 ))
                                                       for compr in d_unc["reads"].keys()
        ]) + "|\n"
            #np.mean(d_unc["reads"][compr][:,0] / d_unc["reads"]["orig"][:,0])) for compr in d_unc["reads"].keys()]) + "|\n"

        w = d_unc["sizes"]
        if i == 0:
            sizer_t += '| size ratio ' + header
        sizer_t += '| *' + label + '* |' + ' | '.join(["{:.2f} +- {:.2f}".format(np.mean(w[compr][:,0] / w["orig"][:,0]), np.std(w[compr][:,0] / w["orig"][:,0]) ) for compr in w.keys()]) + "|\n"

        f.close()

        if plot:
            plot_histo(fname.replace(".pkl", "-histo.npz"))

    print(size_t)
    print(sizer_t)
    print(write_t)
    print(read_t)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Basic analysis of compression tests')
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("files", type=str, nargs="+", help="Files containing the pickled compression performance metrics")

    args = parser.parse_args()

    print_compr_report(args.files, plot=args.plot)