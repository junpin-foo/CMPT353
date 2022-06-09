from matplotlib.pyplot import xlabel
import numpy as np
import pandas as pd
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AffinityPropagation
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

filename1 = sys.argv[1]
filename2 = sys.argv[2]

data_label = pd.read_csv(filename1)
data_unlabel = pd.read_csv(filename2)

# data_label_scale = data_label.loc[:, data_label.columns != 'city']
# data_label_scale2 = data_label_scale.loc[:,  data_label_scale.columns != 'year']
# city = data_label.loc[data_label['city']]
# year = data_label.loc[data_label['year']]
# print(data_label_scale2)
data_unlabel.pop('city')
data_unlabel.pop('year')

city = data_label.pop('city')
year = data_label.pop('year')

scaler = StandardScaler()
scaler.fit(data_label)
data_label_scaled = scaler.transform(data_label)
data_label_scaledDF = pd.DataFrame(data_label_scaled, columns= data_label.columns)

data_unlabel_scaled = scaler.transform(data_unlabel)
data_unlabel_scaledDF = pd.DataFrame(data_unlabel_scaled, columns= data_unlabel.columns)


X = data_label_scaledDF
y = city

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = RandomForestClassifier(n_estimators=200, max_depth = 7, min_samples_leaf=10)
model.fit(X_train, y_train)

print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

predictions = model.predict(data_unlabel_scaledDF)

pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)


