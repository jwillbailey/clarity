import numpy as np

class Compressor:
    fs = 44100
    # size of RMS buffer
    rms_buffer_size = 0.25
    # rms buffer
    memory = np.zeros(int(np.floor(fs * rms_buffer_size)))
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
            #returns the gain reduction coefficient for debugging
            return self.compression

    def reset_rms_buffer(self, rms_buffer_size, fs):
        self.memory = np.zeros(int(np.floor(fs * rms_buffer_size)))
        self.idx=0

    def __init__(self, attack=5, release=20, threshold=0.05, attenuation=0.1, rms_buffer_size = .25):
        # todo take init values
    # rms buffer
        self.reset_rms_buffer(self.fs * rms_buffer_size)
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
