import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

myFileName = sys.argv[0]
file1 = sys.argv[1]
file2 = sys.argv[2]

file1pd = pd.read_csv('pagecounts-20190509-120000.txt', sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])

file1PdSorted = file1pd.sort_values(by = 'views', ascending = False)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1) #Plot 1
plt.plot(file1PdSorted['views'].values)
plt.xlabel("Rank")
plt.ylabel("Views")
plt.title("Popularity Distribution")

file2pd = pd.read_csv('pagecounts-20190509-130000.txt', sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
file1PdSorted['views2'] = file2pd['views']
print(file1PdSorted)

plt.subplot(1, 2, 2) #Plot 2
plt.xscale('log')
plt.yscale('log')
plt.plot(file1PdSorted['views'], file1PdSorted['views2'], 'b.')
plt.title("Hourly Correlation")
plt.xlabel("Hour 1 views")
plt.ylabel("Hour 2 views")

plt.savefig('wikipedia.png')