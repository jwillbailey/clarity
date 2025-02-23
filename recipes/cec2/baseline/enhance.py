import os
import json
import logging
import numpy as np
from tqdm import tqdm
from scipy.io import wavfile

import hydra
from omegaconf import DictConfig

from clarity.enhancer.nalr import NALR
from clarity.enhancer.compressor import Compressor

logger = logging.getLogger(__name__)


@hydra.main(config_path=".", config_name="config")
def enhance(cfg: DictConfig) -> None:
    enhanced_folder = os.path.join(cfg.path.exp_folder, "enhanced_signals")
    os.makedirs(enhanced_folder, exist_ok=True)
    scenes_listeners = json.load(open(cfg.path.scenes_listeners_file))
    listener_audiograms = json.load(open(cfg.path.listeners_file))

    enhancer = NALR(**cfg.nalr)
    compressor = Compressor(**cfg.compressor)

    for scene in tqdm(scenes_listeners):
        for listener in scenes_listeners[scene]:
            # retrieve audiograms
            cfs = np.array(listener_audiograms[listener]["audiogram_cfs"])
            audiogram_left = np.array(
                listener_audiograms[listener]["audiogram_levels_l"]
            )
            audiogram_right = np.array(
                listener_audiograms[listener]["audiogram_levels_r"]
            )
            
            # scaling values by average audiogram level
            # to fit within dynamic range of digital system
            # assumes electronic amplification after digital processing 
            # to make up overall level
            # TODO: put parameter in config.yaml to switch this on and off
            scaling_left = 10**(.1 * -np.mean(audiogram_left))
            
            scaling_right = 10**(.1 * -np.mean(audiogram_right))
            
            fs, signal = wavfile.read(
                os.path.join(cfg.path.scenes_folder, f"{scene}_mix_CH1.wav")
            )
            signal = signal / 32768.0
            assert fs == cfg.nalr.fs
            nalr_fir, _ = enhancer.build(audiogram_left, cfs)
            out_l = enhancer.apply(nalr_fir, signal[:, 0]) * scaling_left

            nalr_fir, _ = enhancer.build(audiogram_right, cfs)
            out_r = enhancer.apply(nalr_fir, signal[:, 1]) * scaling_right

            out_l, _, _ = compressor.process(out_l)
            out_r, _, _ = compressor.process(out_r)
            enhanced = np.stack([out_l, out_r], axis=1)
            filename = f"{scene}_{listener}_HA-output.wav"

            n_clipped = np.sum(np.abs(enhanced) > 1.0)
            if n_clipped > 0:
                logger.warning(f"Writing {filename}: {n_clipped} samples clipped")
                if cfg.soft_clip:
                    enhanced = np.tanh(enhanced)
                np.clip(enhanced, -1.0, 1.0, out=enhanced)
            signal_16 = (32768.0 * enhanced).astype(np.int16)
            wavfile.write(
                os.path.join(enhanced_folder, filename), fs, signal_16,
            )


if __name__ == "__main__":
    enhance()