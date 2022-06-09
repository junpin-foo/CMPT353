import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from datetime import datetime 
from pykalman import KalmanFilter

filename1 = sys.argv[1]

def to_timestamp(data):
    
    ret = data.timestamp()
    return ret

#myDateFormat = lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
cpu_data = pd.read_csv(filename1, parse_dates = ['timestamp'])
#cpu_data['timestamp2'] = cpu_data['timestamp'].apply(to_timestamp)
print(cpu_data)

plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)


loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=0.02)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]

initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([0.13, 0.74, 0.7, 0.74]) ** 2 # TODO: shouldn't be zero
transition_covariance = np.diag([0.01, 0.01, 0.001, 0.01]) ** 2 # TODO: shouldn't be zero
transition = [[0.97,0.5,0.2,-0.001], [0.1,0.4,2.2,0], [0,0,0.95,0], [0,0,0,1]]

kf = KalmanFilter(
    initial_state_mean = initial_state, 
    initial_state_covariance = observation_covariance, 
    observation_covariance = observation_covariance, 
    transition_covariance = transition_covariance, 
    transition_matrices = transition)
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['Raw_data', 'loess', 'kalman'])
plt.show()
plt.savefig('cpu.svg')


