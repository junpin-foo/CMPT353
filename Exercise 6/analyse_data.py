
import sys
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt


filename1 = sys.argv[1]

data = pd.read_csv(filename1)
x_multi = [data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort']]
plt.hist(x_multi,50)
plt.show()

anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
print(anova)
print(anova.pvalue)

x_data = pd.DataFrame({'qs1':data['qs1'], 'qs2':data['qs2'], 'qs3':data['qs3'], 'qs4':data['qs4'], 'qs5':data['qs5'], 'merge1':data['merge1'], 'partition_sort':data['partition_sort']})
x_melt = pd.melt(x_data)
posthoc = pairwise_tukeyhsd(x_melt['value'], x_melt['variable'],alpha=0.05)

print(posthoc)
fig = posthoc.plot_simultaneous()
fig.savefig("result2")
