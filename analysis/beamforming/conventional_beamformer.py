import numpy as np
import json
import os
from scipy.fft import fft as fft
from scipy.fft import rfft as rfft
from scipy.fft import irfft
from matplotlib import pyplot as plt

data_path = (
    "F:\\clarity_CEC2_core.v1_0\\clarity_CEC2_data\\clarity_data\\dev\\scenes\\"
)
metadata_path = (
    "F:\\clarity_CEC2_core.v1_0\\clarity_CEC2_data\\clarity_data\\metadata\\"
)
with open(os.path.join(metadata_path, "scenes.dev.json")) as f:
    scenes = json.load(f)
with open(os.path.join(metadata_path, "scenes_listeners.dev.json")) as f:
    scenes_listeners = json.load(f)
with open(os.path.join(metadata_path, "listeners.json")) as f:
    listener_audiograms = json.load(f)
# set for the scene you want - should be in loop controlled by config
scene = scenes[763]

N = 21
L = 1000
s = np.zeros(L)
s[200:500] = np.sin(np.arange(-np.pi, np.pi, (2*np.pi)/300) * 5)

signal = np.array([np.roll(s, i*0) for i in range(N)]).transpose()

f_signal = np.array([rfft(_x) for _x in signal.transpose()]).transpose()


reference_sensor = (N-1)/2
theta = np.pi * .0
u = np.cos(theta)
d = 5
c = 344
omega = np.arange(0, 2*np.pi, (2*np.pi)/(L/2))
k = omega/c
n = np.arange(-reference_sensor, reference_sensor+1, 1)
v = np.zeros([N, int(L/2)], dtype = "complex")
for i, m in enumerate(n):
    jkmdu = (complex(0,1) * k) * m * d * u
    v[i, :] = np.e**(jkmdu)
w = np.asmatrix(((1/N) * v))


y = np.array([np.asarray(weight) * np.squeeze(sig[0:int(L/2)]) for weight, sig in zip(w.H.transpose(), f_signal.transpose())])
y = np.squeeze(y)
out_array = np.array([irfft(yy) for yy in y])
f, a = plt.subplots(2,1)
a[0].plot(np.sum(out_array.transpose(), axis = 1))
a[1].plot(signal)
a[0].set_ylim([-1,1])
plt.show()