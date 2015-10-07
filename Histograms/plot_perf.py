import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("histo_perf_meas_100M_uint16.txt", delimiter="\t")
#df2 = df.set_index("bins")
print df
#del df["std"]

plt.figure()
plt.title("100M data points, uint16")
plt.xlabel("#bins")
plt.ylabel("seconds")
for i in ["std numpy", "dig / bincount", "cython"]:
    t_df = df[df["name"] == i]
    plt.errorbar( t_df["bins"], t_df["mean"], yerr=t_df["std"], label=i, linewidth=2)
plt.legend(loc='best')
plt.show()
