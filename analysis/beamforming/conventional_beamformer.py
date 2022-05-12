import numpy as np
import json
import os
from scipy.fft import fft as fft
from scipy.fft import rfft as rfft
from scipy.fft import irfft
from scipy.io import wavfile
from matplotlib import pyplot as plt

data_path = (
    "/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data/clarity_data/dev/scenes/"
)
metadata_path = (
    "/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data/clarity_data/metadata/"
)


with open(os.path.join(metadata_path, "scenes.dev.json")) as f:
    scenes = json.load(f)
with open(os.path.join(metadata_path, "scenes_listeners.dev.json")) as f:
    scenes_listeners = json.load(f)
with open(os.path.join(metadata_path, "listeners.json")) as f:
    listener_audiograms = json.load(f)
# set for the scene you want - should be in loop controlled by config
scene = scenes[73]

N = 3
fs_fr, fr = wavfile.read(f'{data_path}{scene["scene"]}_mix_CH1.wav')
fs_mid, mid = wavfile.read(f'{data_path}{scene["scene"]}_mix_CH2.wav')
fs_rear, rear = wavfile.read(f'{data_path}{scene["scene"]}_mix_CH3.wav')

signal_l = np.array([fr[:,0],mid[:,0],rear[:,0]]).transpose() / ((2**16)*.5)
f_signal_l = np.array([rfft(_x) for _x in signal_l.transpose()]).transpose()
L = signal_l.shape[0]
signal_r = np.array([fr[:,1],mid[:,1],rear[:,1]]).transpose() / ((2**16)*.5)
f_signal_r = np.array([rfft(_x) for _x in signal_r.transpose()]).transpose()
L = signal_l.shape[0]

s = np.zeros(L)
s[200:5500] = np.sin(np.arange(-np.pi, np.pi, (2*np.pi)/5300) * 50)
noise = (np.random.rand(L)-.5) * .5

signal = np.array([np.roll(s, i*100) + noise for i in range(N)]).transpose() 

def beamform(x, w):
    f_signal = np.array([rfft(_x) for _x in x.transpose()]).transpose()
    y = np.array([np.asarray(weight) * np.squeeze(sig[0:int(L/2)]) for weight, sig in zip(w.H.transpose(), f_signal.transpose())])
    y = np.squeeze(y)
    out_array = np.array([irfft(yy) for yy in y])
    sig_out = np.sum(out_array.transpose(), axis = 1)
    return sig_out
    
reference_sensor = (N-1)/2
scan_response_l = np.zeros(50)
scan_response_r = np.zeros(50)

for j, theta in enumerate(np.arange(-np.pi, np.pi, (2*np.pi)/50)):
   
    u = np.cos(theta)
    d = 10
    c = 1
    fs = 10
    omega = np.arange(0, 2*np.pi, (2*np.pi)/(L/2))
    k = omega/c
    n = np.arange(-reference_sensor, reference_sensor+1, 1)
    v = np.zeros([N, int(L/2)], dtype = "complex")
    for i, m in enumerate(n):
        jkmdu = np.array([complex(0,1) * kk * m * d * u for kk in k])
        v[i, :] = np.e**(jkmdu)
    w = np.asmatrix(((1/N) * v))
    
    sig_out_l = beamform(signal_l, w)
    scan_response_l[j] = (np.sum(sig_out_l**2))
    print(scan_response_l)
    sig_out_r = beamform(signal_r, w)
    scan_response_r[j] = (np.sum(sig_out_r**2))

plt.plot(scan_response_r, alpha = 0.5)
#plt.ylim([-1,1])
plt.show()

u = np.cos(-.5 * np.pi)
d = 10
c = 1
fs = 10
omega = np.arange(0, 2*np.pi, (2*np.pi)/(L/2))
k = omega/c
n = np.arange(-reference_sensor, reference_sensor+1, 1)
v = np.zeros([N, int(L/2)], dtype = "complex")
for i, m in enumerate(n):
    jkmdu = np.array([complex(0,1) * kk * m * d * u for kk in k])
    v[i, :] = np.e**(jkmdu)
w = np.asmatrix(((1/N) * v))

sig_out_l = beamform(signal_l, w)
sig_out_r = beamform(signal_r, w)

f, a = plt.subplots(2,1)
a[0].plot(sig_out_l)
a[0].plot(sig_out_r)
a[1].plot(signal_l)
a[1].plot(signal_r)
a[0].set_ylim([-1,1])
a[1].set_ylim([-1,1])
plt.show()
sig_out = np.array([sig_out_l, sig_out_r]).transpose()
wavfile.write("beamformer_out.wav", fs_fr, sig_out)
wavfile.write("reference.wav", fs_fr, fr)