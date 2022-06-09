import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

def distance(cities, stations):
    R = 6371; # Radius of the earth in km
    dLat = np.radians(np.subtract(cities['latitude'], stations['latitude']))
    dLon = np.radians(np.subtract(cities['longitude'], stations['longitude']))
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(np.radians(stations['latitude'])) * np.cos(np.radians(cities['latitude'])) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)) 
    d = R * c * 1000
    return d

def best_tmax(city, stations):
    list = distance(city, stations)
    return stations.loc[list.idxmin()]['avg_tmax']

stations = pd.read_json(filename1, lines=True)
cities = pd.read_csv(filename2)
stations['avg_tmax'] = stations['avg_tmax'] / 10
cities = cities.dropna()
cities['area'] = cities['area'] / 1000 ** 2
cities.drop(cities.index[cities['area'] > 10000], inplace=True)
cities['density'] = cities['population'] / cities['area']
    
cities['max'] = cities.apply(best_tmax, stations=stations, axis=1)

plt.plot(cities['max'], cities['density'], 'b.', alpha=0.5)
plt.xlabel("Avg Max Temperature (\u00b0C)")
plt.ylabel('Population Density (people/km\u00b2)')
plt.title("Temperature vs Population Density")

plt.savefig(filename3)
