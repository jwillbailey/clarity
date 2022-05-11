import numpy as np
import json
import os
from scipy.fft import fft as fft
from scipy.fft import rfft as rfft
from scipy.fft import irfft
from matplotlib import pyplot as plt

data_path = (
    "F:\\clarity_CEC2_core.v1_1\\clarity_CEC2_data\\clarity_data\\dev\\scenes\\"
)
metadata_path = (
    "F:\\clarity_CEC2_core.v1_1\\clarity_CEC2_data\\clarity_data\\metadata\\"
)
with open(os.path.join(metadata_path, "scenes.dev.json")) as f:
    scenes = json.load(f)
with open(os.path.join(metadata_path, "scenes_listeners.dev.json")) as f:
    scenes_listeners = json.load(f)
with open(os.path.join(metadata_path, "listeners.json")) as f:
    listener_audiograms = json.load(f)
# set for the scene you want - should be in loop controlled by config
scene = scenes[763]

N = 3
L = 1000
s = np.zeros(L)
s[200:500] = np.sin(np.arange(-np.pi, np.pi, (2*np.pi)/300) * 25)
s[200:500] = np.random.rand(300) - 0.5
theta_incident = np.pi*0
t = np.cos(theta_incident)
d = 100
c = 344
fs = 1
sensor_time = (d/c * fs) * t
signal = np.array([np.roll(s, i*int(sensor_time)) for i in range(N)]).transpose()

f_signal = np.array([rfft(_x) for _x in signal.transpose()]).transpose()


reference_sensor = (N-1)/2
resolution = 1000
scan_response = np.zeros(resolution)
for j, theta in enumerate(np.arange(-np.pi, np.pi, (2*np.pi)/resolution)):
    #theta = np.pi * 0
    u = np.cos(theta)

    omega = np.arange(0, 2*np.pi, (2*np.pi)/(L/2))
    k = omega/c
    n = np.arange(-reference_sensor, reference_sensor+1, 1)
    v = np.zeros([N, int(L/2)], dtype = "complex")
    for i, m in enumerate(n):
        jkmdu = np.array([complex(0,1) * kk * m * d * u for kk in k])
        v[i, :] = np.e**(jkmdu)
    w = np.asmatrix(((1/N) * v))


    y = np.array([np.asarray(weight) * np.squeeze(sig[0:int(L/2)]) for weight, sig in zip(w.H.transpose(), f_signal.transpose())])
    y = np.squeeze(y)
    out_array = np.array([irfft(yy) for yy in y]).transpose()
    #f, a = plt.subplots(3,1)
    #a[0].plot(np.sum(out_array, axis = 1))
    #a[1].plot(signal)
    #a[2].plot(out_array)
    #[aa.set_ylim([-1.1,1.1]) for aa in a]
    scan_response[j] = np.sum(np.sum(out_array, axis = 1)**2)
plt.plot(np.linspace(-np.pi, np.pi, resolution), scan_response)
plt.show()