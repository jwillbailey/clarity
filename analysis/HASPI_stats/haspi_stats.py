import numpy as np
import pandas as pd
import json

from scipy import stats
from scipy.fftpack import fft
from matplotlib import pyplot as plt

metadata_path = 'F:\\clarity_CEC2_core.v1_1\\clarity_CEC2_data\\clarity_data\\metadata\\'
exp_path = "F:\\exp\\"

si_processed = pd.read_csv(f'{exp_path}si.csv')
si_unprocessed = pd.read_csv(f'{exp_path}si_unproc.csv')

with open(f'{metadata_path}scenes.dev.json') as f:
    scenes = json.load(f)


with open(f'{metadata_path}rooms.dev.json') as f:
    rooms = json.load(f)

snrs = pd.DataFrame([[s['scene'], s['SNR']] for s in scenes])
snrs = snrs.rename(columns={0:'scene', 1:'SNR'})

print(si_processed['scene'].equals(snrs['scene']))

si_processed['SNR'] = np.zeros(si_processed.shape[0])
si_unprocessed['SNR'] = np.zeros(si_processed.shape[0])

for i, s in enumerate(zip(snrs['scene'], snrs['SNR'])):
    si_processed['SNR'][si_processed['scene']==s[0]] = s[1]
    si_unprocessed['SNR'][si_processed['scene']==s[0]] = s[1]

f, a = plt.subplots(2,1)
a[0].set_title('processed audio')
a[0].scatter(si_processed['SNR'], si_processed['haspi'], alpha = .2)
trend = np.polyfit(si_processed['SNR'], si_processed['haspi'], 2)
trendpoly = np.poly1d(trend) 
a[0].plot(si_processed['SNR'],trendpoly(si_processed['SNR']), color = 'red', alpha = .5)
a[1].set_title('unprocessed audio')
a[1].scatter(si_unprocessed['SNR'], si_unprocessed['haspi'], alpha = .2)
trend = np.polyfit(si_unprocessed['SNR'], si_unprocessed['haspi'], 2)
trendpoly = np.poly1d(trend) 
a[1].plot(si_processed['SNR'],trendpoly(si_unprocessed['SNR']), color = 'red', alpha = .5)
plt.show()

plt.scatter(si_processed['SNR'], si_processed['haspi']-si_unprocessed['haspi'])
plt.show()

plt.hist(si_processed['haspi']-si_unprocessed['haspi'], density = True)
plt.show()


f, a = plt.subplots(2,1)
a[0].hist(np.log(si_processed['haspi']), density = True)
a[0].set_ylim([0,1])
a[1].hist(np.log(si_unprocessed['haspi']), density = True)
a[1].set_ylim([0,1])
plt.show()