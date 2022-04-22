import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft
from scipy.fftpack import dct
from scipy.io import wavfile

data_path = 'E:\\clarity_CEC2_core.v1_0\\clarity_CEC2_data\\clarity_data\\dev\\scenes\\'

metadata_path = 'E:\\clarity_CEC2_core.v1_0\\clarity_CEC2_data\\clarity_data\\metadata\\'

mix_files = [l for l in os.listdir(data_path) if l.split('_')[1]=='mix']

interferer_files = [l for l in os.listdir(data_path) if l.split('_')[1]=='interferer']

target_files = [l for l in os.listdir(data_path) if l.split('_')[1]=='target' and l.split('_')[2]=='anechoic']

fs_mix, mix = wavfile.read(
                            os.path.join(data_path, f'{mix_files[0]}')
                        )

fs_target, target = wavfile.read(
                            os.path.join(data_path, f'{target_files[0]}')
                        )
mix = np.array(mix, dtype = 'float32') / (0.5*2**16)
target = np.array(target, dtype = 'float32') / (0.5*2**16)

def spectrogram(x):
    x_pad = np.append(x, np.zeros([256, 2]))
    output = np.zeros([256, x.shape[0]])
    for i, n in enumerate(x):
       output[:, i] = x[i:(i+256), 0]
    return output 