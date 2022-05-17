#!/bin/bash

python copy_demo_source_data.py path.root='/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data'  interferer.speech_interferers='${path.metadata_dir}/masker_speech_list.demo.json' interferer.noise_interferers='${path.metadata_dir}/masker_nonspeech_list.demo.json'
tar -cvzf ../../demo/rooms.tgz interferers
tar -cvzf ../../demo/targets.tgz targets
tar -cvzf ../../demo/rooms.tgz rooms
tar -cvzf ../../demo/metadata.tgz ../../demo/metadata
tar -cvzf ../../demo/scenes.tgz ../../demo/scenes
