import sys
import numpy as np
import pandas as pd
import difflib

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

file = open(filename1, 'r')
list = file.readlines()

data = pd.DataFrame()
data['title'] = list

ratingsData = pd.read_csv(filename2)

def find(w): 
    return difflib.get_close_matches(w, data['title'], n=1, cutoff=0.6)

ratingsData['match'] = ratingsData['title'].apply(find)

ratingsData['match'] = ratingsData['match'].apply(lambda y: np.nan if len(y) == 0 else y)
ratingsData = ratingsData.dropna()

def clean(w):
    return w[0].strip('\n')

ratingsData['match'] = ratingsData['match'].apply(clean)

ratingsData = ratingsData.sort_values('match')
ratingsData = ratingsData.groupby(ratingsData['match'])
ratingsData = ratingsData.aggregate('mean')

ratingsData.rename(columns={'match': 'title'}, inplace=True)
ratingsData['rating'] = ratingsData['rating'].round(2)

ratingsData.to_csv(filename3)
