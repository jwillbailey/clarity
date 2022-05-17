import json
from matplotlib.font_manager import json_dump
import numpy as np

path = "/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data/clarity_data/metadata"

masker_noise_list = json.load(open(f"{path}/masker_nonspeech_list.json"))
masker_speech_list = json.load(open(f"{path}/masker_speech_list.json"))

short_noise_maskers = [m for m in masker_noise_list if m["nsamples"] > 3 * 10**5 and m['duration']<20 and m['dataset']=='dev']

male_speakers = [m for m in masker_speech_list if m["speaker"][2] == "m" and m['dataset']=='dev']
female_speakers = [m for m in masker_speech_list if m["speaker"][2] == "f" and m['dataset']=='dev']


male_speaker_subset = [
    male_speakers[r] for r in np.random.permutation(len(male_speakers))[:4]
]

female_speaker_subset = [
    female_speakers[r]
    for r in np.random.permutation(len(female_speakers))[:4]
]

short_speech = male_speaker_subset +female_speaker_subset

with open(f'{path}/masker_nonspeech_list.demo.json', 'w') as f:
    json.dump(short_noise_maskers, f)


with open(f'{path}/masker_speech_list.demo.json', 'w') as f:
    json.dump(short_speech, f)