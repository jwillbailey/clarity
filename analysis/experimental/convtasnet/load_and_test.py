import numpy as np
import torch
from scipy.io import wavfile

model = torch.load('model.pickle')
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


model = model.to(torch.device("cpu"))
data_path = "F:\\clarity_CEC2_data\\clarity_data\\dev\\scenes"
import os
file = os.path.join(data_path, 'S06007_mix_CH0.wav')
from scipy.io import wavfile
from scipy.signal import resample_poly

fs, input = wavfile.read(file)
input = np.mean(input, axis=1)
input = resample_poly(input, 1, 3)
input = torch.tensor(np.reshape(input, [1,1,-1]), dtype=torch.float)
output = model(input).to('cpu').detach().numpy()
output = np.reshape(output, [2,-1])

from matplotlib import pyplot as plt
f, a = plt.subplots(2,1)
for i in range(2):
    a[i].plot(output[i])
plt.show()
wavfile.write('output.wav', int(fs/3), output.transpose())