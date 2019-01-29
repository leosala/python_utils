## Compression tests

These scripts contains a simple procedure to test compression algorithms performance. It is tuned for usage with SwissFEL Jungfrau 
data, but can be used with basic capabilities with any HDF5-based dataset.

### Examples

Running compression tests on few data files:

```
export a="/sf/alvra/data/p17296/raw/2018-08-04/lyzo/run14.JF06T32V01.h5 /sf/alvra/data/p17296/raw/2018-08-04/lyzo/run15.JF06T32V01.h5"
export dst=/data/JF06T32V01/data
export label=lyzo_run14to25

export gainfile="/sf/alvra/config/jungfrau/gainMaps/JF06T32V01/gains.h5"
export pedefile="/sf/alvra/data/p17502/res/JF_pedestals/pedestal_20180813_0704.JF06T32V01.res.h5"
export n=100

# with data correction
python compression_tests.py -n $n -l ${label}_${n}frames  -d ${dst} -o /sf/alvra/data/p17502/res/test \
    --bitshuffle --convert --gainfile=$gainfile --pedefile=$pedefile $a

# without data correction
python compression_tests.py -n $n -l ${label}_${n}frames  -d ${dst} -o /sf/alvra/data/p17502/res/test \
    --bitshuffle $a

```