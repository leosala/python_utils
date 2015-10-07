#cython:  nonecheck=False, cdivision=True
#cython: wraparound=False, boundscheck=False, nonecheck=False, cdivision=True
import numpy as np
cimport numpy as np
cimport cython
from cpython cimport bool

FLOAT = np.float64
ctypedef np.float64_t FLOAT_t
DOUBLE = np.double
ctypedef np.double_t DOUBLE_t

INT = np.int16
ctypedef np.int16_t INT_t
BOOL = bool
ctypedef bool BOOL_t

#def create_histogram_int(np.ndarray[INT_t, ndim=1] data_in, INT_t bins_in):
cpdef create_histogram_int(unsigned short[:] data, int bins):

    cdef int data_size = len(data)
    cdef double[:] histo = np.zeros(bins, dtype=DOUBLE)
    cdef float data_min
    cdef float data_max
#   cdef float[:] bins_array = np.zeros(bins, dtype=FLOAT)
    cdef int i
    cdef int bin
    cdef int[:] bins_range = np.arange(bins, dtype=np.int32)
    cdef float bin_step
    cdef int ibin

    data_max = data_min = data[0]

    for i in range(1, data_size):
        if data[i] > data_max:
            data_max = data[i]
        if data[i] < data_min:
            data_min = data[i]

    # FIXME
    if (data_min == data_max):
        return np.array([0]), np.array([0])

    cdef double[:] bins_array = np.arange(data_min, data_max, (data_max - data_min) / float(bins), dtype=DOUBLE)
    bin_step = bins_array[1] - bins_array[0]

    # workaround
    if len(bins_array) == bins + 1:
        bins_array = bins_array[:bins]

    for i in range(data_size):
        #if dp < bins_array[0]:
        #    print dp, bins_array[0]
        #    histo[0] += 1
        #    elif dp >= bins_array[bins - 1]:
        #        histo[bins - 1] += 1
        #    else:
        ibin = <int>((data[i] - data_min) / bin_step)

        if ibin < 0:
            ibin = 0
        elif ibin >= bins:
            ibin = bins - 1
        histo[ibin] += 1
            #for bin in range(bins):
            #    if data[i] >= bins_array[bin] and data[i] < bins_array[bin + 1]:
            #        histo[bin] += 1
            #        break

    return np.array(bins_array), np.array(histo)


cpdef create_histogram_double(double[:] data, int bins):

    cdef int data_size = len(data)
    cdef double[:] histo = np.zeros(bins, dtype=DOUBLE)
    cdef double data_min
    cdef double data_max
#   cdef float[:] bins_array = np.zeros(bins, dtype=FLOAT)
    cdef int i
    cdef int bin
    cdef int[:] bins_range = np.arange(bins, dtype=np.int32)
    cdef double bin_step
    cdef int ibin

    data_max = data_min = data[0]

    for i in range(1, data_size):
        if data[i] > data_max:
            data_max = data[i]
        if data[i] < data_min:
            data_min = data[i]

    # FIXME
    if (data_min == data_max):
        return np.array([0]), np.array([0])

    cdef double[:] bins_array = np.arange(data_min, data_max, (data_max - data_min) / float(bins), dtype=DOUBLE)
    bin_step = bins_array[1] - bins_array[0]

    # workaround
    if len(bins_array) == bins + 1:
        bins_array = bins_array[:bins]

    for i in range(data_size):
        #if dp < bins_array[0]:
        #    print dp, bins_array[0]
        #    histo[0] += 1
        #    elif dp >= bins_array[bins - 1]:
        #        histo[bins - 1] += 1
        #    else:
        ibin = <int>((data[i] - data_min) / bin_step)

        if ibin < 0:
            ibin = 0
        elif ibin >= bins:
            ibin = bins - 1
        histo[ibin] += 1
            #for bin in range(bins):
            #    if data[i] >= bins_array[bin] and data[i] < bins_array[bin + 1]:
            #        histo[bin] += 1
            #        break

    return np.array(bins_array), np.array(histo)



cpdef create_multipixel_histogram_int(unsigned short[:, :] data, int bins):
    #    t_data = data[:, i:i + chunk_size].astype(np.int32)
    cdef int j
    cdef float[:] histo = np.zeros(bins, dtype=FLOAT)
    cdef float[:] bins_array = np.zeros(bins, dtype=FLOAT)
    cdef float[:] t_histo = np.zeros(bins, dtype=FLOAT)
    cdef float[:] t_bins = np.zeros(bins, dtype=FLOAT)
    cdef float data_min
    cdef float data_max

    for j in range(data.shape[1]):
        t_bins, t_histo = create_histogram_int(data[:, j], 100)
        if j == 0:
            histo = t_histo
            bins_array = t_bins
        else:
            histo = t_histo #+ histo
            bins_array = t_bins #bins_array

    return np.array(bins_array), np.array(histo)
