import pandas as pd
import subprocess
import os

def normalize_file(fname):
    """
    Some basic and horrible data wrangling is needed before using pandas
    """
    cmd = 'grep -v "#" %s |' % fname
    cmd += ' grep -v "\---" | grep -v "rate" | grep -v "==" | '
    cmd += ' grep -v "Cumulative" | grep -v "^$" | sed "s=^   ==g" |'
    cmd += ' sed "s=  *=:=g" > %s_norm.log' % fname
    retcode = subprocess.call(cmd, shell=True)
    print retcode
    return '%s_norm.log' % fname


def convert_units(x):
    try:
        return float(x.replace("MB", "000000").replace("KB", "000").replace("B", "")) / 1000000
    except:
        return -1


def read_iftop(fname):
    """
    loading normalized iftop output
    """
    norm_fname = normalize_file(fname)
    df = pd.read_csv(norm_fname, sep=':', skiprows=1, names=["id", "host", "dir", "2s", "10s", "40s", "cum"], converters={"2s": convert_units, "10s": convert_units, "40s": convert_units}, error_bad_lines=False)
    df.ix[1::2, "id"].values[:] = df[0::2]["id"].values[:]
    dest = df["host"].values[:].copy()
    dest[0::2] = dest[1::2]
    df['dest'] = pd.Series(dest, index=df.index)
    df["host"][1::2].values[:] = df["host"][0::2].values[:]
    cols = df.columns.tolist()
    cols = cols[:3] + [cols[-1], ] + cols[3:-2]
    df = df[cols]
    os.unlink(norm_fname)
    return df
