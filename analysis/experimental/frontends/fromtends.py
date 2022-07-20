import numpy as np
from scipy.fft import rfft 
from scipy.fft import irfft

class Cardioid:
    
    def __init__(self, fs=44100, distance=0.0076, c=344):
        self._fs = fs
        self._d = distance
        self._c = c
        self._set_time_delay()
    
    def _get_fs(self):
        return self._fs

    def _set_fs(self, value):
        self._fs = value
        self._set_time_delay()

    def _get_distance(self):
        return self._d

    def _set_distance(self, value):
        self._d = value
        self._set_time_delay()

    def _get_c(self):
        return self._c

    def _set_c(self, value):
        self._c = value
        self._set_time_delay()
    
    def _set_time_delay(self):
        self._t = self._d/self._c
        self._t_samples = np.round(self._t * self.fs)
    
    def _get_time_delay(self):
        return self._t
    
    def _get_time_delay_samples(self):
        return self._t_samples

    fs = property(
        fget=_get_fs,
        fset=_set_fs,
        doc="sample rate."
    )
    
    d = property(
        fget=_get_distance,
        fset=_set_distance,
        doc="distance between sensors."
    )

    c = property(
        fget=_get_c,
        fset=_set_c,
        doc="speed of sound."
    )

    fs = property(
        fget=_get_fs,
        fset=_set_fs,
        doc="sample rate."
    )

    time_delay = property(
        fget=_get_time_delay,
        doc="time delay between signals."
    )
    
    sample_delay = property(
        fget=_get_time_delay_samples,
        doc="number of samples between signals."
    )
    
    def process(self, front_audio, rear_audio, rear_gain):
        return front_audio - (np.roll(rear_audio, 2)*rear_gain)


class FFTBeamformer(Cardioid):
    
    def __init__(self, fs=44100, distance=0.076, c=344):
        self._fs = fs
        self._d = distance
        self._c = c
        self._set_time_delay()
    
    def _get_time_delay(self):
        return self._t_samples
        
    def _get_time_delay_samples(self):
        self._t = self._d/self._c
        self._t_samples = np.round(self._t)

    fs = property(
        fget=_get_time_delay_samples,
        doc="sample rate."
    )
    
    def process(self, x, theta ,d=0.076 ,c=344 ,fs=44100):
        L = x.shape[0]
        N = x.shape[1]
        reference_sensor = (N-1)/2
        u = np.cos(theta)
        omega = np.arange(0, 2*np.pi, (2*np.pi)/(L/2))
        k = omega/c
        n = np.arange(-reference_sensor, reference_sensor+1, 1)
        v = np.zeros([N, int(L/2)], dtype = "complex")
        for i, m in enumerate(n):
            jkmdu = np.array([complex(0,1) * kk * m * d * fs * L * u for kk in k])
            v[i, :] = np.e**(jkmdu)

        w = np.asmatrix(((1/N) * v))
        f_signal = np.array([rfft(_x) for _x in x.transpose()]).transpose()
        y = np.array([np.asarray(weight) * np.squeeze(sig[0:int(L/2)]) for weight, sig in zip(w.H.transpose(), f_signal.transpose())])
        y = np.squeeze(y)
        out_array = np.array([irfft(yy) for yy in y])
        sig_out = np.sum(out_array.transpose(), axis = 1)
        return sig_out