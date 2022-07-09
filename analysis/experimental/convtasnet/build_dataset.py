import numpy as np
from pathlib import Path
import torch
from torch.utils.data import Dataset, DataLoader
from scipy.io import wavfile

class Clarity_Audio_Dataset(Dataset):
    """ Dataset for clarity data. """
    file_list = []
    input_file_list = []
    output_target_file_list = []
    output_interferer_file_list = []
    def __init__(self, audio_dir):
        path = Path(audio_dir)
        for p in path.iterdir():
            if p.is_file():
                self.file_list.append(p)
        self.input_file_list = [f for f in self.file_list if f.stem.split("_")[1]=="mix" and f.stem.split("_")[-1]=="CH1"]
        self.output_target_file_list = [f for f in self.file_list if (f.stem.split("_")[1]=="target" and f.stem.split("_")[2]!="anechoic") and f.stem.split("_")[-1]=="CH1"]
        self.output_interferer_file_list = [f for f in self.file_list if f.stem.split("_")[1]=="interferer" and f.stem.split("_")[-1]=="CH1"]    
        try:
            assert len(self.input_file_list) == len(self.output_target_file_list)
        except AssertionError as e:
            print(f'{e}\ninput file list not equal length of target outputs')
            print(f'{len(self.input_file_list)} / {len(self.output_target_file_list)}')
        try:
            assert len(self.output_interferer_file_list) == len(self.output_target_file_list)
        except AssertionError as e:
            print(f'{e}\ntarget file list not equal length of interferer outputs')
            print(f'{len(self.output_target_file_list)} / {len(self.output_interferer_file_list)}')
    
    def __len__(self):
        return len(self.input_file_list)
        

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        mix_file_path = self.input_file_list[idx]
        target_file_path = self.output_target_file_list[idx]
        interferer_file_path = self.output_interferer_file_list[idx]

        fs_mix, mix = wavfile.read(mix_file_path)
        mix = np.reshape(mix, [2,-1])
        mix = np.mean(mix, axis = 0)
        fs_target, target = wavfile.read(target_file_path)
        target = np.reshape(target, [2,-1])
        target = np.mean(target, axis = 0)
        fs_interferer, interferer = wavfile.read(interferer_file_path)
        interferer = np.reshape(interferer, [2,-1])
        interferer = np.sum(interferer, axis = 0)
        sample  = {'name' : self.input_file_list[idx].stem.split("_")[0],
                    'fs' : fs_mix,
                    'mix' : torch.tensor(mix, dtype=torch.float),
                    'target' : torch.tensor([target, interferer], dtype=torch.float) 
                    }
        return sample
data_path = "E:\\clarity_CEC2_data\\clarity_data\\dev\\scenes"
train_data = Clarity_Audio_Dataset(data_path)