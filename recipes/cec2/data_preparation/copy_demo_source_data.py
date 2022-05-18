import os
import json
import hydra
from pathlib import Path
import logging
from omegaconf import DictConfig
import shutil
logger = logging.getLogger(__name__)


@hydra.main(config_path=".", config_name="config")
def main(cfg):
    data_path = f"{cfg.path.data_dir}/scenes"
    metadata_path = f"{cfg.path.metadata_dir}/"
    demo_dataset_path = Path(f'{cfg.path.data_dir}/demo_dataset')
    if demo_dataset_path.exists() == False:
        print('making demo dataset directory')
        demo_dataset_path.mkdir(parents=True, exist_ok=True)
    with open(f'{metadata_path}scenes.demo.json') as f:
        demo_metadata = json.load(f)
    
    for scene in demo_metadata:
        target_path = Path(f'{cfg.path.data_dir}/demo_dataset/targets')
        if target_path.exists() == False:
            print('making target directory')
            target_path.mkdir(parents=True, exist_ok=True)

        interferer_path = Path(f'{cfg.path.data_dir}/demo_dataset/interferers')
        if interferer_path.exists() == False:
            print('making interferer directory')
            interferer_path.mkdir(parents=True, exist_ok=True)


        music_path = Path(f'{cfg.path.data_dir}/demo_dataset/interferers/music')
        if music_path.exists() == False:
            print('making interferer directory')
            music_path.mkdir(parents=True, exist_ok=True)
        for i in range(100):
            music_subpath = Path(f'{cfg.path.data_dir}/demo_dataset/interferers/music/{i:02}')
            if music_subpath.exists() == False:
                music_subpath.mkdir(parents=True, exist_ok=True)

        noise_path = Path(f'{cfg.path.data_dir}/demo_dataset/interferers/noise')
        if noise_path.exists() == False:
            print('making interferer directory')
            noise_path.mkdir(parents=True, exist_ok=True)

        speech_path = Path(f'{cfg.path.data_dir}/demo_dataset/interferers/speech')
        if speech_path.exists() == False:
            print('making interferer directory')
            speech_path.mkdir(parents=True, exist_ok=True)

        room_path = Path(f'{cfg.path.data_dir}/demo_dataset/rooms')
        if room_path.exists() == False:
            print('making room directory')
            room_path.mkdir(parents=True, exist_ok=True)

        ac_path = Path(f'{cfg.path.data_dir}/demo_dataset/rooms/ac')
        if ac_path.exists() == False:
            print('making ac directory')
            ac_path.mkdir(parents=True, exist_ok=True)

        rpf_path = Path(f'{cfg.path.data_dir}/demo_dataset/rooms/rpf')
        if rpf_path.exists() == False:
            print('making rpf directory')
            rpf_path.mkdir(parents=True, exist_ok=True)
            
        hoair_path = Path(f'{cfg.path.data_dir}/demo_dataset/rooms/HOA_IRs')
        if hoair_path.exists() == False:
            print('making hoair directory')
            hoair_path.mkdir(parents=True, exist_ok=True)

        target_src = (f"{cfg.path.data_dir}/targets/{scene['target']['name']}.wav")
        shutil.copy(target_src, target_path.as_posix())

        for i in scene['interferers']:
            interferer_src = f"{cfg.path.data_dir}/interferers/{i['type']}/{i['name']}"
            interferer_dest = f"{interferer_path.as_posix()}/{i['type']}/"
            shutil.copy(interferer_src, interferer_dest)

        ac_src = f"{cfg.path.data_dir}/rooms/ac/{scene['room']}.ac"
        rpf_src = f"{cfg.path.data_dir}/rooms/rpf/{scene['room']}"
        hoair_src = f"{cfg.path.data_dir}/rooms/HOA_IRs/HOA_{scene['room']}"

        shutil.copy(ac_src, ac_path.as_posix())
        
        for t in ['_t', '_i1', '_i2', '_i3']:
            shutil.copy(f'{rpf_src}{t}.rpf', rpf_path.as_posix())
            shutil.copy(f'{hoair_src}{t}.wav', hoair_path.as_posix())
        
if __name__=="__main__":
    main()    
