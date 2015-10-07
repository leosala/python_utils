## Compilation

`python setup_histogram.py build_ext  --inplace`

## Performance tests

Setup:
* Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz
* 8 GB ram
* numpy 1.9.2
* cython 0.22.1
* python 2.7.10

Using the script `test_histo.py`:
![](https://github.com/leosala/python_utils/blob/master/Histograms/perf_100M_uint16.png)
![](https://github.com/leosala/python_utils/blob/master/Histograms/perf_100M_double.png)
