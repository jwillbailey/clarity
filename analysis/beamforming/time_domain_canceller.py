import numpy as np

import numpy as np
import json
import os
from scipy.fft import fft as fft
from scipy.fft import rfft as rfft
from scipy.fft import irfft
from scipy.io import wavfile
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
scene = scenes[1063]
 
N = 3
fs_hr, hr = wavfile.read(f'{data_path}{scene["scene"]}_HR.wav')
gyro_hr = np.concatenate([[0],np.diff(hr)])
plt.plot(np.linspace(0, (gyro_hr.shape[0]/44100), gyro_hr.shape[0]), gyro_hr)
fs_fr, fr = wavfile.read(f'{data_path}{scene["scene"]}_mix_CH1.wav')
fs_mid, mid = wavfile.read(f'{data_path}{scene["scene"]}_mix_CH2.wav')
fs_rear, rear = wavfile.read(f'{data_path}{scene["scene"]}_mix_CH3.wav')

out_1 = fr - np.roll(mid, 1)
out_2 = mid - np.roll(rear, 1)

out = out_1 - (np.roll(out_2, 2)*.5)

wavfile.write('delay_cancel.wav', fs_fr, out_1)
wavfile.write('delay_cancel_ref.wav', fs_fr, fr)