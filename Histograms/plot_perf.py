import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("histo_perf_meas_1M.txt", delimiter="\t")
#df2 = df.set_index("bins")
print df
del df["std"]

plt.figure()
plt.title("100M data points, uint16")
plt.xlabel("#bins")
plt.ylabel("seconds")
for i in ["std numpy", "dig / bincount", "cython"]:
    plt.plot(df[df["name"] == i]["bins"], df[df["name"] == i]["mean"], label=i, linewidth=2)
plt.legend(loc='best')
plt.show()
