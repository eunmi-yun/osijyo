import matplotlib.pyplot as plt
import numpy as np

dataList = [10, 5, 1, 5, 9, 11, 30, 22, 50, 44, 32, 3]
monthList = []

for i in range(12):
    monthList.append(i + 1)

x = np.arange(12)

plt.bar(x, dataList)
plt.xticks(x, monthList)

plt.show()