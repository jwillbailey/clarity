#!/bin/bash


python build_scenes.py path.root='/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data'
python render_scenes.py path.root='/media/williambailey/Elements/clarity_CEC2_core.v1_1/clarity_CEC2_data' 'render_starting_chunk=range(0, 100, 20)' --multirun