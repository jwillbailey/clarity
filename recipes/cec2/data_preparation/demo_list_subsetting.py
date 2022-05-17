import json
import numpy as np

path = "/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data/clarity_data/metadata"

masker_noise_list = json.load(open(f"{path}/masker_nonspeech_list.json"))
masker_speech_list = json.load(open(f"{path}/masker_speech_list.json"))

short_noise_maskers = [m for m in masker_noise_list if m["duration"] < 10]

male_speakers = [m for m in masker_speech_list if m["speaker"][2] == "m"]
female_speakers = [m for m in masker_speech_list if m["speaker"][2] == "f"]


male_speaker_subset = [
    male_speakers[r] for r in np.random.permutation(len(male_speakers))[:4]
]

female_speaker_subset = [
    female_speakers[r]
    for r in np.random.permutation(female_speakers)[:4]
]
