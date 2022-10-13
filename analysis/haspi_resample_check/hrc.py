import numpy as np
from clarity.evaluator.haspi import haspi_v2_be
from scipy.signal import resample_poly
from scipy.signal import firwin
from scipy.signal import correlate
from matplotlib import pyplot as plt

fs_a = 44100
f = 100
t_a = np.arange(fs_a * 5)
signal_a = np.cos(2 * np.pi * (f / fs_a) * t_a)

gaps = int(0.25 * fs_a)
for i in np.arange(0, len(t_a), gaps):
    signal_a[i : (i + int(0.1 * fs_a))] = 0

fs_b = 32000
f = 100
t_b = np.arange(fs_b * 5)
signal_b = np.cos(2 * np.pi * (f / fs_b) * t_b)
gaps = int(0.25 * fs_b)
for i in np.arange(0, len(t_b), gaps):
    signal_b[i : (i + int(0.1 * fs_b))] = 0

np.random.seed(0)
corrupt_a = signal_a + np.random.normal(0, 0.1, len(t_a))
np.random.seed(0)
corrupt_b = signal_b + np.random.normal(0, 0.1, len(t_b))

sii_a = haspi_v2_be(
    signal_a,
    signal_a,
    corrupt_a,
    corrupt_a,
    fs_a,
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [250, 500, 1000, 2000, 4000, 6000],
)
print(sii_a)
sii_b = haspi_v2_be(
    signal_b,
    signal_b,
    corrupt_b,
    corrupt_b,
    fs_b,
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [250, 500, 1000, 2000, 4000, 6000],
)
print(sii_b)
sii_ab = haspi_v2_be(
    signal_a,
    signal_a,
    resample_poly(corrupt_b, fs_a, fs_b),
    resample_poly(corrupt_b, fs_a, fs_b),
    fs_a,
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [250, 500, 1000, 2000, 4000, 6000],
)
print(sii_ab)
sii_ba = haspi_v2_be(
    resample_poly(signal_a, fs_b, fs_a),
    resample_poly(signal_a, fs_b, fs_a),
    corrupt_b,
    corrupt_b,
    fs_a,
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [250, 500, 1000, 2000, 4000, 6000],
)
print(sii_ba)

x = np.zeros(100)
x[50] = 1

y = resample_poly(x, fs_a, fs_b)
plt.plot(x, color="red")
plt.stem(y)
plt.show()
