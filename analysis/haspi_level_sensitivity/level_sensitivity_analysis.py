import json 
import numpy as np
from matplotlib import pyplot as plt

with open('output.json') as f:
    data = json.load(f)
values = np.array([])
levels = np.array([])
listeners = np.array([])
for listener in data:
    print(listener)
    listener_data = data[listener]
    for k in listener_data:
        level = float(k[:(len(k)-2)])
        levels = np.append(levels, level)
        values = np.append(values, listener_data[k])
        listeners = np.append(listeners, listener)

f, a = plt.subplots(5,6)
for j, lis in enumerate(data):
    l1 = [l for i, l in enumerate(levels) if listeners[i]==lis]
    v1 = [l for i, l in enumerate(values) if listeners[i]==lis]
    a[j%5, int(np.floor(j/5))].scatter(l1, v1)
    a[j%5, int(np.floor(j/5))].set_ylim([0,1])
    a[j%5, int(np.floor(j/5))].set_title(lis)
    
plt.show()