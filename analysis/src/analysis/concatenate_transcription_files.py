"""Concatenate transcription files

Takes a set of transcription files and concatenates them into one.

If the listener id is not present in the transcriptions, it is added from the filename.
"""

import argparse
import glob
import itertools
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, filename="logs/concatenate_transcription_files.log")


def concatenate_transcription_files(input_files, output_file):
    files_to_process = glob.glob(input_files)
    filenames = [Path(file).name for file in files_to_process]
    transcripts_to_process = [json.load(open(f, "r")) for f in files_to_process]

    # Add the listener field to the transcripts if it is not present
    for filename, transcript in zip(filenames, transcripts_to_process):
        listener = filename.split("_")[0]
        for response in transcript:
            if "listener" not in response:
                response["listener"] = listener

    all_transcripts = list(itertools.chain(*transcripts_to_process))

    with open(output_file, "w") as f:
        json.dump(all_transcripts, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", type=str)
    parser.add_argument("output_file", type=str)
    args = parser.parse_args()

    concatenate_transcription_files(args.input_files, args.output_file)


if __name__ == "__main__":
    main()

# python3 concatentate_transcription_files.py "data/transcriptions/*.json" output.json
