import time
import sys
import pandas as pd
import numpy as np
from scipy import stats
from implementations import all_implementations

rows_list = []
for i in range(60):
    random_array = np.random.randint(10000, size=10000)
    dict1 = []
    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        dict1.append(en-st) 

    rows_list.append(dict1)
df = pd.DataFrame(rows_list , columns=('qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'))

df['qs1'] = np.sqrt(df['qs1'])
df['qs2'] = np.sqrt(df['qs2'])   
df['qs3'] = np.sqrt(df['qs3'])   
df['qs4'] = np.sqrt(df['qs4'])   
df['qs5'] = np.sqrt(df['qs5'])   
df['merge1'] = np.sqrt(df['merge1'])
df['partition_sort'] = np.sqrt(df['partition_sort'])         

df.to_csv('data.csv', index=False)