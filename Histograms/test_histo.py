import numpy as np
import matplotlib.pyplot as plt
from time import time
from sys import argv
from histogram import create_histogram_int

#@profile
def histo_2(data, bins):
    binned_values = np.digitize(data.flatten(), bins[1:-1])
    values = np.bincount(binned_values)
    #bins = np.insert(bins, -1, 1)
    return bins, values


samples = 5
nbins = int(argv[1])
print "##### ", nbins

data = np.random.randint(0, 100, size=1000*1000*1).astype(np.uint16)

text_file = open("histo_perf_meas_1M.txt", "a+")

meas1 = np.zeros(samples)
meas2 = np.zeros(samples)
meas3 = np.zeros(samples)

for i in xrange(samples):
    sample = "std numpy"
    t0 = time()
    histo1, bins1 = np.histogram(data, nbins)
    meas1[i] = time() - t0

    sample = "dig / bincount"
    meas = np.zeros(samples)
    t0 = time()
    bins2 = np.arange(0, 100, 100. / (nbins))
    bins2 = np.insert(99, -1, bins2)
    bins2, histo2 = histo_2(data, bins2)
    meas2[i] = time() - t0

    sample = "cython"
    meas = np.zeros(samples)
    t0 = time()
    bins3, histo3 = create_histogram_int(data, nbins)
    meas3[i] = time() - t0

    print (histo1 - histo2 == 0).all()
    print (histo1 - histo3 == 0).all()


text_file.write("%s\t%s\t%s\t%s\n" % ("name", "bins", "mean", "std"))
sample = "std numpy"
print "%s: %.2f +- %.2f" %(sample, meas1.mean(), meas1.std())
text_file.write("%s\t%i\t%f\t%f\n" % (sample, nbins, meas1.mean(), meas1.std()))
sample = "dig / bincount"
print "%s: %.2f +- %.2f" %(sample, meas2.mean(), meas2.std())
text_file.write("%s\t%i\t%f\t%f\n" % (sample, nbins, meas2.mean(), meas2.std()))
sample = "cython"
print "%s: %.2f +- %.2f" %(sample, meas3.mean(), meas3.std())
text_file.write("%s\t%i\t%f\t%f\n" % (sample, nbins, meas3.mean(), meas3.std()))

text_file.close()

#plt.figure()
#plt.bar(bins[:], histo[:])
#plt.show()
