import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from pykalman import KalmanFilter
from sklearn import datasets


def get_data(name):
    tree = ET.parse(name)
    root = tree.getroot()
    lat = []
    lon = []

    for child in root.iter('{http://www.topografix.com/GPX/1/0}trkpt'):
        data = pd.DataFrame
        lat.append(float(child.attrib['lat']))
        lon.append(float(child.attrib['lon']))

    data = pd.DataFrame()
    data['lat'] = lat
    data['lon'] = lon
    return data

# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
# from user: user1921
def distance(data): 
    shifted = data.shift(periods=1)
    data.dropna(inplace=True)
    R = 6371; # Radius of the earth in km
    dLat = np.radians(np.subtract(shifted['lat'], data['lat']))
    dLon = np.radians(np.subtract(shifted['lon'], data['lon']))
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(np.radians(data['lat'])) * np.cos(np.radians(shifted['lat'])) * np.sin(dLon/2) * np.sin(dLon/2)
        
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)) 
    d = R * c
    d = d.sum() * 1000

    return d

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def smooth(data):

    initial_state = data.iloc[0]
    observation_covariance = np.diag([0.00015,0.0002]) ** 2 
    transition_covariance = np.diag([0.0001, 0.0001]) ** 2 
    transition = [[1,0],[0,1]]

    kf = KalmanFilter(
        initial_state_mean = initial_state, 
        initial_state_covariance = observation_covariance, 
        observation_covariance = observation_covariance, 
        transition_covariance = transition_covariance, 
        transition_matrices = transition)

    kalman_smoothed, _ = kf.smooth(data)
    ret = pd.DataFrame(kalman_smoothed, columns=['lat','lon'])
    return ret
   

def main():
    points = get_data(sys.argv[1]) 
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    
    main()

