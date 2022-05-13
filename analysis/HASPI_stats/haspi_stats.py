import numpy as np
import pandas as pd
import json
import seaborn as sns
from scipy import stats
from scipy.fftpack import fft
from matplotlib import pyplot as plt


import binsreg

def binscatter(**kwargs):
    # Estimate binsreg
    est = binsreg.binsreg(**kwargs)
    
    # Retrieve estimates
    df_est = pd.concat([d.dots for d in est.data_plot])
    df_est = df_est.rename(columns={'x': kwargs.get("x"), 'fit': kwargs.get("y")})
    
    # Add confidence intervals
    if "ci" in kwargs:
        df_est = pd.merge(df_est, pd.concat([d.ci for d in est.data_plot]))
        df_est = df_est.drop(columns=['x'])
        df_est['ci'] = df_est['ci_r'] - df_est['ci_l']
    
    # Rename groups
    if "by" in kwargs:
        df_est['group'] = df_est['group'].astype(df[kwargs.get("by")].dtype)
        df_est = df_est.rename(columns={'group': kwargs.get("by")})

    return df_est

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
trend = np.polyfit(si_processed['SNR'], si_processed['haspi'], 4)
trendpoly = np.poly1d(trend) 
a[0].plot(si_processed['SNR'],trendpoly(si_processed['SNR']), color = 'red', alpha = .5)
a[1].set_title('unprocessed audio')
a[1].scatter(si_unprocessed['SNR'], si_unprocessed['haspi'], alpha = .2)
trend = np.polyfit(si_unprocessed['SNR'], si_unprocessed['haspi'], 4)
trendpoly = np.poly1d(trend) 
a[1].plot(si_processed['SNR'],trendpoly(si_unprocessed['SNR']), color = 'red', alpha = .5)
plt.show()

plt.scatter(si_processed['SNR'], si_processed['haspi']-si_unprocessed['haspi'])
plt.show()

f, a = plt.subplots(2,1)
binned_si_processed = binscatter(x='SNR', y = 'haspi', data = si_processed, ci = (1,1))
sns.scatterplot(ax = a[0], x = 'SNR', y = 'haspi', data = binned_si_processed)
a[0].errorbar('SNR', 'haspi', yerr='ci', data=binned_si_processed, ls='', lw=2, alpha=0.2)
a[0].set_ylim([0,1])
binned_si_unprocessed = binscatter(x='SNR', y = 'haspi', data = si_unprocessed, ci = (1,1))
sns.scatterplot(ax = a[1], x = 'SNR', y = 'haspi', data = binned_si_unprocessed)
a[1].errorbar('SNR', 'haspi', yerr='ci', data=binned_si_unprocessed, ls='', lw=2, alpha=0.2)
a[1].set_ylim([0,1])
plt.show()

plt.hist(si_processed['haspi']-si_unprocessed['haspi'], density = True)
plt.show()


f, a = plt.subplots(2,1)
a[0].hist(np.log(si_processed['haspi']), density = True)
a[0].set_ylim([0,1])
a[1].hist(np.log(si_unprocessed['haspi']), density = True)
a[1].set_ylim([0,1])
plt.show()