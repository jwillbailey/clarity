"""Collate MBSTOI scores from multiple files"""

import argparse
import glob
import json
import logging
from pathlib import Path

from tqdm import tqdm

logging.basicConfig(level=logging.INFO, filename="logs/collate_MBSTOI_scores.log")


def parse_mbstoi_file(filename):
    system = str(Path(filename).parents[0]).split("/")[-1].split("_")[1]
    with open(filename, "r") as f:
        x_parts = f.readline().strip().split(" ")
    parts = (system, x_parts[1], x_parts[3], x_parts[5]) if len(x_parts) >= 6 else None
    if parts is None:
        logging.info(f"Missing MBSTOI value for: {filename}")
    return parts


def concatenate_transcription_files(input_files, output_file):
    files_to_process = glob.glob(input_files)
    mbstoi_data = [parse_mbstoi_file(filename) for filename in tqdm(files_to_process)]

    # Filter out None values
    mbstoi_data = [x for x in mbstoi_data if x is not None]

    # Restructure as a dictionary
    mbstoi_dict = [
        {"system": system, "scene": scene, "listener": listener, "mbstoi": mbstoi}
        for system, scene, listener, mbstoi in mbstoi_data
    ]

    with open(output_file, "w") as f:
        json.dump(mbstoi_dict, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", type=str)
    parser.add_argument("output_file", type=str)
    args = parser.parse_args()

    concatenate_transcription_files(args.input_files, args.output_file)


if __name__ == "__main__":
    main()

# python3 collate_MBSTOI_scores.py "data/transcriptions/*.json" output.json
