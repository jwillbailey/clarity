import numpy as np
import hydra
from omegaconf import DictConfig
import logging
import os
from tqdm import tqdm
from scipy.io import wavfile
from matplotlib import pyplot as plt
from tqdm import tqdm 

logger = logging.getLogger(__name__)

@hydra.main(config_path=".", config_name="config")
def zero_set_head_rotation(cfg: DictConfig) -> None:
    audio_path = cfg.path.audio_location
    output_path = cfg.path.output_location
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    files = [f for f in os.listdir(audio_path) if os.path.isfile(os.path.join(audio_path, f))]
    hr_files = [f for f in files if f.split("_")[-1]=="hr.wav"]
    wrapped = np.zeros(len(hr_files), dtype="bool")
    
    for i, file in tqdm(enumerate(hr_files), total=len(hr_files)):
        file_path = os.path.join(audio_path, file)
        fs, head_rotation = wavfile.read(file_path)
        wrapped[i] = np.sign(head_rotation[0])!=np.sign(head_rotation[-1])
        head_rotation -= head_rotation[0]
        output_file_path = os.path.join(output_path, file)
        wavfile.write(output_file_path, fs, head_rotation)    
    print(f"Evidence of wrapping? {np.all(wrapped)}")
if __name__=="__main__":
    zero_set_head_rotation()