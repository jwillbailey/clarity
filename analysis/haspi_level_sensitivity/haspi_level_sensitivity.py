from multiprocessing.connection import Listener
import os
import csv
import json
import logging
from scipy.io import wavfile
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

import hydra
from omegaconf import DictConfig
from clarity.evaluator.haspi import haspi_v2_be

def filter_snr(snr, scenes, scene_listeners, audiograms):
    scenes = [s for s in scenes if np.round(s['SNR'])==snr]
    scene_listeners = [s for j, s in zip(scene_listeners) if s['scene'] == ]
    return scenes, scene_listeners, audiograms
    

def main(cfg):
    data_path = f"{cfg.level_sensitivity.paths.clarity_data}dev\\scenes\\"

    metadata_path = f"{cfg.level_sensitivity.paths.clarity_data}\\metadata\\"

    with open(os.path.join(metadata_path, 'scenes.dev.json')) as f:
        scenes = json.load(f)

    with open(os.path.join(metadata_path, 'scenes_listeners.dev.json')) as f:
        scenes_listeners = json.load(f)

    with open(os.path.join(metadata_path, 'listeners.json')) as f:
        listener_audiograms = json.load(f)

    scenes, scenes_listeners, listener_audiograms = filter_snr(cfg.level_sensitivity.snr, scenes, scenes_listeners, listener_audiograms)

    mix_files = [l for l in os.listdir(data_path) if l.split('_')[1]=='mix']

    interferer_files = [l for l in os.listdir(data_path) if l.split('_')[1]=='interferer']

    target_files = [l for l in os.listdir(data_path) if l.split('_')[1]=='target' and l.split('_')[2]=='anechoic']

    output = {}
    start = cfg.level_sensitivity.starting_scene
    
    end = cfg.level_sensitivity.starting_scene + cfg.level_sensitivity.scenes_to_process

    for scene in tqdm(scenes[start:end]):
        for listener in scenes_listeners[scene['scene']]:
            output[f'{scene["scene"]}_{listener}'] = {}
            for ref_scale in tqdm(np.arange(-24,1,3)):
                fs_proc, proc = wavfile.read(
                            os.path.join(data_path, f'{scene["scene"]}_mix_CH1.wav')
                        )

                fs_ref, ref = wavfile.read(
                            os.path.join(data_path, f'{scene["scene"]}_target_anechoic_CH1.wav')
                        )
                assert fs_ref == fs_proc
                proc = np.array(proc, dtype='float32') / (0.5* 2**16)
                ref = np.array(ref, dtype = 'float32') / (0.5* 2**16)



                ref *= 10**(.05*ref_scale)

                cfs = np.array(listener_audiograms[listener]["audiogram_cfs"])
                audiogram_left = np.array(
                                listener_audiograms[listener]["audiogram_levels_l"]
                            )
                audiogram_right = np.array(
                                listener_audiograms[listener]["audiogram_levels_r"]
                            )

                sii = haspi_v2_be(
                    xl=ref[:, 0],
                    xr=ref[:, 1],
                    yl=proc[:, 0],
                    yr=proc[:, 1],
                    fs_signal=fs_ref,
                    audiogram_l=audiogram_left,
                    audiogram_r=audiogram_right,
                    audiogram_cfs=cfs,
                )
                
                try: 
                    output[f'{scene["scene"]}_{listener}'][f'{ref_scale}dB'] = sii
                except:
                    print('you are a failure')
    with open('output.json', 'w') as f:
        json.dump(output, f)
if __name__ == "__main__":
    main()