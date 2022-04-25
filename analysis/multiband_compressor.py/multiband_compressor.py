import os
import numpy as np
import json
from matplotlib import pyplot as plt
import scipy
from scipy.fftpack import fft
from scipy.fftpack import dct
from scipy.io import wavfile
from scipy.signal import butter
from scipy.signal import lfilter
import torch
from torchaudio.models import ConvTasNet as ctn

class Compressor:
    fs = 44100
    # size of RMS buffer
    time_constant = 0.01
    # rms buffer
    memory = np.zeros(int(np.floor(fs * time_constant)))
    idx = 0
    # attack interpolation coefficient - mut be set using method below
    attack = 0.001

    # release interpolation coefficient - mut be set using method below
    release = 0.001
    # initial rms value
    rms = 1
    # compression threshold
    threshold = 0.01
    # current compression (automatic) gain
    compression = 1
    # inverse of ratio attenuation factor
    attenuation = 0.1

    def set_attack(self, t_msec):
        t_sec = t_msec / 1000
        reciprocal_time = 1 / t_sec
        self.attack = reciprocal_time / self.fs

    def set_release(self, t_msec):
        t_sec = t_msec / 1000
        reciprocal_time = 1 / t_sec
        self.release = reciprocal_time / self.fs

    def process(self, x, return_type="audio", makeup_gain=1):
        self.memory[self.idx] = x
        self.idx += 1
        self.idx = self.wrap_idx(self.idx, self.memory.shape[0])
        self.rms = np.sqrt(np.mean(self.memory**2))
        if self.rms > self.threshold:
            temp_comp = (self.rms * self.attenuation) + ((1 - self.attenuation) * self.threshold)
            self.compression = (self.compression * (1 - self.attack)) + (
                temp_comp * self.attack
            )
        else:
            self.compression = (1 * self.release) + self.compression * (
                1 - self.release
            )
        if return_type == "audio":
            return self.compression * x * makeup_gain
        if return_type == "compression":
            return self.compression

    def __init__(self, attack=5, release=20, threshold=0.05, attenuation=0.1):
        # todo take init values
        self.set_attack(attack)
        self.set_release(release)
        self.threshold = threshold
        self.attenuation = attenuation
        pass

    @staticmethod
    def wrap_idx(i, lim):
        if i >= lim:
            return i - lim
        else:
            return i


def sigmoid(x):
    sig = 1 / (1 + np.exp(-x))
    return sig

def camfit_IG(hl, f):
    #from Use of a Loudness Model for Hearing Aid Fitting.
    #IV. Fitting Hearing Aids with Multi-Channel
    #Compression so as to Restore ‘Normal’ Loudness
    #for Speech at Different Levels - BCJ Moore
    ab = {
        250:[0.2, 0.0025],
        500:[0.2, 0.0025],
        1000:[0.37, -0.0003],
        2000:[0.31, 0.0016],
        3000:[0.31, 0.0016],
        4000:[0.3, 0.0019],
        6000:[0.3, 0.0019],
        8000:[0.3, 0.0019]
        }
    a = ab[f][0]
    b = ab[f][1]
    quad_side = b*(hl**2)
    db_gain = a*(hl + quad_side)
    return 10**(.05*db_gain)

def main():

    # hard paths for convenience in writing - change for your own data
    data_path = (
        "/media/williambailey/Elements/clarity_CEC2_core.v1_0/clarity_CEC2_data/clarity_data/dev/scenes/"
    )
    metadata_path = (
        "/media/williambailey/Elements/clarity_CEC2_core.v1_0/clarity_CEC2_data/clarity_data/metadata/"
    )
    with open(os.path.join(metadata_path, "scenes.dev.json")) as f:
        scenes = json.load(f)
    with open(os.path.join(metadata_path, "scenes_listeners.dev.json")) as f:
        scenes_listeners = json.load(f)
    with open(os.path.join(metadata_path, "listeners.json")) as f:
        listener_audiograms = json.load(f)
    # set for the scene you want - should be in loop controlled by config
    scene = scenes[200]
    fs_mix, mix = wavfile.read(os.path.join(data_path, f'{scene["scene"]}_mix_CH1.wav'))
    mix = np.array(mix, dtype="float32") / (0.5 * 2**16)
    mix*=20
    signal_l = torch.reshape(torch.tensor(mix[:, 0].transpose()), shape = [1,1,-1])
    signal_r = torch.reshape(torch.tensor(mix[:, 1].transpose()), shape = [1,1,-1])

    print('trying tasnet')
    #tasnet = ctn()
    print('trying left')
    #tas_out_l = tasnet.forward(signal_l).detach().numpy()

    #tasnet = ctn()
    print('trying right')
    #tas_out_r = tasnet.forward(signal_r).detach().numpy()
    
    tas_out_l = mix[:, 0]#tas_out_l[0,0,:].transpose()
    tas_out_r = mix[:, 1]#tas_out_r[0,0,:].transpose()

    print('tasnet worked!')
    fs = 44100
    cfs = np.array([250, 500, 1000, 2000, 3000, 4000, 6000, 8000])
    # octave band corner frequencies - may increase level when summing bands with fc closer than 1 octave
    # todo - find audiogram corner frequencies
    lfs = (cfs / np.sqrt(2)) / (0.5 * fs)
    ufs = (np.sqrt(2) * cfs) / (0.5 * fs)

    filter_coefs = [butter(2, [l, u], btype="bandpass") for l, u in zip(lfs, ufs)]

    filter_output_l = np.array([lfilter(f[0], f[1], tas_out_l) for f in filter_coefs])
    filter_output_r = np.array([lfilter(f[0], f[1], tas_out_r) for f in filter_coefs])
    
    gain = 1

    listeners = scenes_listeners[scene["scene"]]
    listener = listeners[0]
    audiogram = listener_audiograms[listener]

    left =  [camfit_IG(l, f) for l, f in zip(audiogram["audiogram_levels_l"], cfs)]
    right = [camfit_IG(l, f) for l, f in zip(audiogram["audiogram_levels_r"], cfs)]

    comp_l = [
        Compressor(attenuation=1 / 10.5),
        Compressor(attenuation=1 / 8.2),
        Compressor(attenuation=1 / 14.3),
        Compressor(attenuation=1 / 17.2),
        Compressor(attenuation=1 / 19),
        Compressor(attenuation=1 / 24.8),
        Compressor(attenuation=1 / 35.3),
        Compressor(attenuation=1 / 35.3),
    ]
    comp_r = [
        Compressor(attenuation=1 / 10.5),
        Compressor(attenuation=1 / 8.2),
        Compressor(attenuation=1 / 14.3),
        Compressor(attenuation=1 / 17.2),
        Compressor(attenuation=1 / 19),
        Compressor(attenuation=1 / 24.8),
        Compressor(attenuation=1 / 35.3),
        Compressor(attenuation=1 / 35.3),
    ]

    comp_filter_out_l = np.zeros(filter_output_l.shape)
    comp_filter_out_r = np.zeros(filter_output_r.shape)

    # the values used for tuning and debugging
    comp_out_l = np.zeros(filter_output_r.shape)
    comp_out_r = np.zeros(filter_output_r.shape)

    # using non-pythonic loop for samplewise processing
    for i in np.arange(filter_output_l.shape[0]):
        for j in np.arange(filter_output_r.shape[1]):
            comp_filter_out_l[i, j] = gain * comp_l[i].process(
                filter_output_l[i, j], makeup_gain=left[i]
            )
            comp_out_l[i, j] = comp_l[i].compression
            comp_filter_out_r[i, j] = gain * comp_r[i].process(
                filter_output_r[i, j], makeup_gain=right[i]
            )
            comp_out_l[i, j] = comp_r[i].compression

    #plotting for tuning and debugging
    print("plotting")
    f, a = plt.subplots(8,2)
    for aa, fl, fr, c in zip(a, comp_filter_out_l, filter_output_l, comp_out_l):
       aa[0].plot(fl[10000:10100])
       aa[0].plot(c[10000:10100])
       aa[0].set_ylim([np.min(fl[10000:10100]), np.max(fl[10000:10100])])
       aa[1].plot(fr)
       aa[1].plot(c)
    plt.show()

    l_out = np.sum(comp_filter_out_l, axis=0)
    r_out = np.sum(comp_filter_out_r, axis=0)
    output = np.array([l_out, r_out]).transpose()
    # nonlinearity to soft clamp output +/- 1
    output = np.tanh(output)
    wavfile.write(f'{scene["scene"]}_filtered_audio.wav', fs, output)
    wavfile.write(f'{scene["scene"]}_unfiltered_audio.wav', fs, mix)


if __name__ == "__main__":
    main()
