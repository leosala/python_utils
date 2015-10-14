# Pandas utilities and examples
## read_iftop

Just a simple utility to read logfiles as produced by `iftop` into a nicely formatted pandas DataFrame.

Usage:
```
from read_iftop import read_iftop

df = read_iftop(filename)
```