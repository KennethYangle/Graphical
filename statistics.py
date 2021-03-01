import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fontsize = 16
data = [[95, 90, 90, 92, 90, 87, 96, 92, 98, 100],
        [90, 87, 90, 88, 85, 87, 96, 92, 98, 92],
        [90, 83, 85, 88, 85, 87, 96, 92, 98, 92],
        [80, 87, 90, 82, 85, 87, 96, 92, 94, 92],
        [80, 87, 80, 82, 85, 82, 96, 92, 94, 92]]
labels = [10, 20, 30, 40, 50]
ax2x = [1, 2, 3, 4, 5]
ratios = [90, 85, 92, 93, 95]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.boxplot(data, labels=labels, showmeans=True, patch_artist=True)
ax.grid(linestyle="--", alpha=0.3)
ax.set_xlabel("The number of WLs", size=fontsize)
ax.set_ylabel("Coverage rate (%)", size=fontsize)
ax.set_ylim(78, 102)
ax.tick_params(axis='both', which='major', labelsize=fontsize)

ax2 = ax.twinx()
ax2.plot(ax2x, ratios, color="c")
ax2.set_ylabel("Average return ratio (%)", size=fontsize)
ax2.set_ylim(78, 102)
ax2.tick_params(axis='both', which='major', labelsize=fontsize)
# ax2.axes.yaxis.set_visible(False)       # hide y axis, open when plot average

plt.savefig("31.png", dpi=1200)
plt.show()
