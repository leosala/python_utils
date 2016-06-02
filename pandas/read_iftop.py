import pandas as pd
import subprocess
import os

def normalize_file(fname):
    """
    Some basic and horrible data wrangling is needed before using pandas
    """

    # grep -v "#"  | grep -v "\---" | grep -v "rate" | grep -v "==" | grep -v "Cumulative" | grep -v '^$' | sed "s=^  ==g" | sed "s:^ ::g" | sed "s=  *=:=g"
    cmd = 'grep -v "#" %s |' % fname
    cmd += ' grep -v "\---" | grep -v "rate" | grep -v "==" | '
    cmd += ' grep -v "Cumulative" | grep -v "^$" | sed "s=^   ==g" |'
    cmd += ' sed "s=  *=:=g" > %s_norm.log' % fname
    print cmd
    retcode = subprocess.call(cmd, shell=True)
    if retcode != 0:
        print "[ERROR] Something went wrong in the IFTOP file normalization"
        return None
    return '%s_norm.log' % fname


def convert_units(x):
    """MB/s"""
    try:
        if x[-2:] == "MB":
            return float(x.replace("MB", "")) 
        elif x[-2:] == "KB":
            return float(x.replace("KB", "")) / 1000
        elif x[-2:] == "B":
            return float(x.replace("B", "")) / 1000000
    except:
        return -1


def read_iftop(fname):
    """
    loading normalized iftop output
    """
    #norm_fname = normalize_file(fname)
    norm_fname = fname
    if norm_fname is None:
        return -1

    # add case for extra columns (port)
    df = pd.read_csv(norm_fname, sep=':', skiprows=1,
                     names=["id", "host", "dir", "2s", "10s", "40s", "cum"],
                     converters={"2s": convert_units, "10s": convert_units, "40s": convert_units},
                     error_bad_lines=False)
    df.ix[1::2, "id"].values[:] = df[0::2]["id"].values[:]
    dest = df["host"].values[:].copy()
    dest[0::2] = dest[1::2]
    df['dest'] = pd.Series(dest, index=df.index)
    df["host"][1::2].values[:] = df["host"][0::2].values[:]
    cols = df.columns.tolist()
    cols = cols[:3] + [cols[-1], ] + cols[3:-2]
    df = df[cols]
    #os.unlink(norm_fname)
    return df
