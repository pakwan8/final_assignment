import numpy as np
import matplotlib.pyplot as plt
from main import Dataset

values = np.array([12.22, 12.63, 12.97, 12.88, 13.12, 13.03, 13.13, 13.26, 13.01, 12.85, 12.90, 12.43], dtype=np.float64)
values2 = np.array([10.41, 10.42, 10.34, 10.18, 10.35, 10.75, 10.99, 11.01, 10.66, 10.41, 10.35, 10.21], dtype=np.float64)
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
dataset = np.genfromtxt(r"./datasets/ave_retail_price.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
comparing = True
bar_colors_rgb = [[200, 0, 0], [200, 80, 10], [200, 200, 0], [80, 200, 0],
                  [0, 200, 0], [0, 200, 80], [0, 200, 200], [0, 80, 200],
                  [0, 0, 200], [80, 0, 200], [200, 0, 200], [200, 0, 80]]

temp_dataset = Dataset(dataset)
plt.figure(figsize=[8, 7], facecolor=[0, 0, 0])
plt.tight_layout(pad=5)
plt.title("bruh".title(), color=[1, 1, 1], fontsize=16)
plt.xlabel("Months", fontsize=14)
plt.ylabel(temp_dataset.units, fontsize=14)
plt.ylim(int(np.min(values)) - (int(np.min(values)) / 10), int(np.max(values)) + (int(np.max(values)) / 10))
plt.xticks([x for x in range(1, 13)], temp_dataset.months, rotation=35)
ax = plt.gca()
ax.spines['bottom'].set_color([1, 1, 1])
ax.spines['top'].set_color([0.35, 0.35, 0.35])
ax.spines['right'].set_color([0.35, 0.35, 0.35])
ax.spines['left'].set_color([1, 1, 1])
ax.xaxis.label.set_color([1, 1, 1])
ax.yaxis.label.set_color([1, 1, 1])
ax.set_facecolor([0, 0, 0])
ax.tick_params(axis='x', colors=[1, 1, 1])
ax.tick_params(axis='y', colors=[1, 1, 1])

if not comparing:
    plt.bar([x for x in range(1, 13)], values2, color=[[y / 255 for y in x] for x in bar_colors_rgb], edgecolor=[1, 1, 1], width=0.8)

else:
    print(values2)
    plt.bar([x + 0.2 for x in range(1, 13)], values, color=[1, 1, 1], edgecolor=[1, 1, 1], width=0.4)
    plt.bar([x - 0.2 for x in range(1, 13)], values2, color=[[y / 255 for y in x] for x in bar_colors_rgb], edgecolor=[1, 1, 1], width=0.4)


plt.show()
