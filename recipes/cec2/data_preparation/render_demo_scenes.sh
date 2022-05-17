#!/bin/bash


python build_scenes.py path.root='/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data' interferer.speech_interferers='${path.metadata_dir}/masker_speech_list.demo.json' interferer.noise_interferers='${path.metadata_dir}/masker_nonspeech_list.demo.json'
python render_scenes.py path.root='/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data' 'render_starting_chunk=range(0, 100, 20)' --multirun